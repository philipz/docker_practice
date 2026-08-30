## 容器網路進階特性

本節聚焦 Docker 自身可見的進階網路能力：Overlay 網路、服務發現和 DNS 解析。更偏 Kubernetes 編排網路的概念，如 CNI 和 NetworkPolicy，不在本章展開。

### Overlay 網路原理與設定

Overlay 網路在現有網路基礎上建立虛擬網路，允許容器跨宿主機通訊。它是 Swarm 場景下的核心網路驅動之一。

#### Overlay 網路工作原理

Overlay 網路透過隧道封裝技術（通常是 VXLAN）將容器網路流量封裝在宿主機物理網路的 UDP 資料包中傳輸。Docker overlay 網路預設使用 `4789/udp` 作為資料通道埠號，同時 Swarm 控制面與節點通訊還需要相應開放 `2377/tcp`、`7946/tcp` 和 `7946/udp`。

```text
容器 A (192.168.0.2)
    ↓
veth 對
    ↓
br-net (橋接器)
    ↓
Docker 引擎 (VXLAN 封裝)
    ↓
物理網路 (172.16.0.0/24)
    ↓
Docker 引擎 (VXLAN 解封裝)
    ↓
br-net (橋接器)
    ↓
veth 對
    ↓
容器 B (192.168.0.3，不同宿主機)
```

#### 建立和使用 Overlay 網路

Overlay 網路依賴 Swarm。若要讓獨立容器加入 overlay 網路，需要把網路建立為 `attachable`。

```bash
# 初始化 Swarm
docker swarm init

# 建立 attachable overlay 網路
docker network create --driver overlay \
  --attachable \
  --subnet 192.168.0.0/24 \
  --opt com.docker.network.driver.mtu=1450 \
  my-overlay-net

# 驗證網路建立
docker network ls
docker network inspect my-overlay-net

# 在 Swarm 服務中使用 overlay 網路
docker service create --name web \
  --network my-overlay-net \
  --replicas 3 \
  nginx  # 確保與環境相容的 Nginx 版本

# 單機環境下也可以讓普通容器加入 attachable overlay 網路
docker run -d --name container1 --network my-overlay-net busybox sleep 1d
docker run -d --name container2 --network my-overlay-net busybox sleep 1d

# 測試跨容器通訊
docker exec container1 ping -c 1 container2
```

#### Overlay 網路效能最佳化

```bash
# 調整 MTU（Maximum Transmission Unit）避免分片
# VXLAN 開銷 50 位元組，物理 MTU 1500 時建議設定為 1450
docker network create --driver overlay \
  --attachable \
  --opt com.docker.network.driver.mtu=1450 \
  optimized-overlay

# 啟用 IP 位址管理（IPAM）自訂
docker network create --driver overlay \
  --attachable \
  --subnet 10.0.9.0/24 \
  --aux-address "my-router=10.0.9.2" \
  my-custom-overlay
```

### 容器 DNS 解析機制

Docker 內建 DNS 伺服器，但 DNS 解析涉及多個層面的設定。

#### DNS 解析流程

```text
容器應用 (dig www.example.com)
    ↓
容器內 /etc/resolv.conf (127.0.0.11:53)
    ↓
Docker 內嵌 DNS 伺服器 (127.0.0.11)
    ↓
使用者自訂 DNS 或宿主機 /etc/resolv.conf
    ↓
外部 DNS 伺服器 (8.8.8.8 等)
    ↓
DNS 回應 → 容器快取 → 應用
```

#### 設定容器 DNS

**在執行時指定 DNS：**

```bash
# 單個容器
docker run -d \
  --dns 8.8.8.8 \
  --dns 1.1.1.1 \
  --dns-search example.com \
  nginx  # 確保與環境相容的 Nginx 版本

# DNS 選項
docker run -d \
  --dns-option ndots:2 \
  --dns-option timeout:1 \
  --dns-option attempts:3 \
  nginx  # 確保與環境相容的 Nginx 版本

# 查看容器 DNS 設定
docker exec <container_id> cat /etc/resolv.conf
```

**Docker Compose DNS 設定：**

```yaml
services:
  web:
    image: nginx
    dns:
      - 8.8.8.8
      - 1.1.1.1
    dns_search:
      - example.com
      - local

  db:
    image: postgres
    networks:
      - backend
    hostname: postgres-db

networks:
  backend:
    driver: bridge

# 容器內 /etc/resolv.conf 將被自動設定
# search example.com local
# nameserver 8.8.8.8
# nameserver 1.1.1.1
```

**Docker 守護程式級別設定：**

```json
{
  "dns": ["8.8.8.8", "1.1.1.1"],
  "dns-search": ["example.com"]
}
```

#### 自訂服務發現

**使用 Docker 內建 DNS 的服務發現：**

```bash
# 建立自訂網路
docker network create mynet

# 執行服務
docker run -d --name web --network mynet nginx  # 確保與環境相容的 Nginx 版本
docker run -d --name db --network mynet postgres  # 確保與環境相容的 PostgreSQL 版本

# 在其他容器中透過服務名存取
docker run -it --network mynet busybox sh

# ping web  # 自動解析到 web 容器 IP
# ping db   # 自動解析到 db 容器 IP
```

**Compose 服務名自動發現：**

```yaml
services:
  frontend:
    image: nginx
    depends_on:
      - backend
    environment:
      BACKEND_URL: http://backend:8080

  backend:
    image: myapp
    depends_on:
      - database

  database:
    image: postgres
    environment:
      POSTGRES_DB: mydb

# frontend 容器可以直接存取 http://backend:8080
# backend 容器可以直接存取 postgres://database:5432
```

### 本章邊界

Docker 的網路章節重點討論 bridge、host、none、overlay 和 DNS 等能力。CNI、NetworkPolicy、Calico、Cilium 這類概念屬於 Kubernetes 編排網路的範疇，後續在 Kubernetes 章節中再展開會更清晰。

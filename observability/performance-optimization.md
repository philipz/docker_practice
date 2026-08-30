## 19.3 容器效能最佳化與故障診斷

容器的輕量級特性不代表效能問題會自動消失。在實際維運中，效能瓶頸可能來自 CPU 限制、記憶體溢位、磁碟 I/O、網路擁塞等多個層面。本節深入討論容器效能監控、診斷方法和最佳化策略。

### 19.3.1 容器效能監控指標

#### 核心效能指標體系

容器效能監控涉及 Docker CLI、Prometheus/cAdvisor 指標和底層 cgroup 檔案。現代 Linux 與 Kubernetes 新版本通常使用 cgroup v2；舊系統或相容環境仍可能看到 cgroup v1 名稱。

| 類型 | Docker / Prometheus 常見指標 | cgroup v2 檔案 | cgroup v1 相容名 |
|------|------------------------------|----------------|------------------|
| CPU 使用 | `CPU %`、`container_cpu_usage_seconds_total` | `cpu.stat` 中的 `usage_usec` | `cpuacct.usage` |
| CPU 限流 | `container_cpu_cfs_throttled_periods_total` | `cpu.stat` 中的 `nr_throttled`、`throttled_usec` | `cpu.stat.nr_throttled`、`cpu.stat.throttled_time` |
| 記憶體使用 | `MEM USAGE`、`container_memory_working_set_bytes` | `memory.current` | `memory.usage_in_bytes` |
| 記憶體限制 | `MEM USAGE / LIMIT` | `memory.max` | `memory.limit_in_bytes` |
| OOM 次數 | `container_oom_events_total` 或執行時期事件 | `memory.events` 中的 `oom` / `oom_kill` | `memory.failcnt` |
| 網路收發 | `NET I/O`、`container_network_receive_bytes_total` / `transmit_bytes_total` | 網路命名空間介面計數 | `rx_bytes` / `tx_bytes` |
| 塊 I/O | `BLOCK I/O`、`container_fs_*` / `container_blkio_*` | `io.stat` | `blkio.throttle.io_service_bytes` |
| 檔案系統 | `container_fs_usage_bytes` / `container_fs_limit_bytes` | 執行時期或檔案系統採集 | `fs_usage_bytes` / `fs_limit_bytes` |

### 19.3.2 使用 docker stats 即時監控

`docker stats` 是最基礎但強大的監控工具，提供即時的容器資源使用情況。

**基本使用：**

```bash
# 即時監控所有運行中的容器
docker stats

# 輸出示例：
# CONTAINER ID   NAME      CPU %   MEM USAGE / LIMIT     MEM %     NET I/O       BLOCK I/O
# abc123def456   nginx     0.45%   24.3 MiB / 256 MiB    9.49%     1.2kB / 3.4kB 0 B / 0 B
# def789ghi012   redis     0.23%   12.5 MiB / 512 MiB    2.44%     2.1kB / 1.5kB 0 B / 0 B

# 只監控特定容器
docker stats nginx redis

# 一次性輸出不進入互動模式
docker stats --no-stream

# 每 2 秒採樣一次（docker stats 沒有 --interval 選項）
while true; do
  docker stats --no-stream
  sleep 2
done

# 格式化輸出（使用 Go 模板）
docker stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}" --no-stream

# 匯出為 JSON 格式用於日誌記錄
docker stats --format json --no-stream > stats.json
```
**在腳本中使用：**

```bash
#!/bin/bash

# 持續監控並記錄到檔案
while true; do
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    docker stats --no-stream --format "{{.Container}},{{.CPUPerc}},{{.MemUsage}}" | \
        awk -v ts="$timestamp" '{print ts","$0}' >> container_stats.log
    sleep 10
done
```
**效能指標解讀：**

```bash
# CPU % 超過 80%：需要增加 CPU 限制或最佳化應用
# MEM % 接近 100%：容器即將 OOM，需要增加記憶體或排查記憶體洩漏
# NET I/O 只顯示收發位元組；丟包要看 ip -s link、cAdvisor/Prometheus 或主機網卡計數器
```

### 19.3.3 cAdvisor 容器監控系統

cAdvisor 是 Google 開發的容器監控工具，提供比 `docker stats` 更詳細的效能資料。

> **⚠️ 安全權衡提示**：下面的示例為簡化部署使用了 `privileged: true`，與 [第 18 章](../security/README.md) 中“最小權限 / `cap_drop=all`”的原則相衝突。生產環境建議改為按需授予能力（如 `cap_add: [SYS_ADMIN]` 加 `device_cgroup_rules` 與精確的 `devices`、`volumes` 掛載），並將 cAdvisor 部署在獨立的監控網路中。如何選擇請參考 [18.4 節](../security/kernel_capability.md) 關於核心能力（capabilities）的細化授權。

**Docker Compose 部署 cAdvisor：**

```yaml
services:
  cadvisor:
    image: ghcr.io/google/cadvisor:v0.56.2
    container_name: cadvisor
    ports:
      - "8080:8080"
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
      - /dev/disk/:/dev/disk:ro
    privileged: true
    devices:
      - /dev/kmsg
    networks:
      - monitoring

networks:
  monitoring:
    driver: bridge
```
啟動後存取 `http://localhost:8080` 查看：

- 容器效能統計
- 系統資源使用情況
- 歷史效能資料

**從 cAdvisor 提取指標：**

```bash
# 取得所有容器的 JSON 格式效能資料
curl http://localhost:8080/api/v1.3/machine | jq .

# 取得特定容器資訊
curl http://localhost:8080/api/v1.3/docker | jq '.docker | keys' | head -5

# 取得容器統計資訊
curl http://localhost:8080/api/v1.3/docker/abc123/ | jq '.stats[-1]'
```
**與 Prometheus 整合：**

```yaml
# prometheus.yml 設定
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'cadvisor'
    static_configs:
      - targets: ['localhost:8080']
    metrics_path: '/metrics'
```

### 19.3.4 Prometheus 容器監控設定

使用 Prometheus 和 node-exporter 進行長期的容器效能監控。

**完整監控堆疊部署：**

> [!TIP]
> 以下示例中的映像檔標籤（如 `prom/prometheus:v3.11.2`、`prom/node-exporter:v1.11.1`、`ghcr.io/google/cadvisor:v0.56.2`、`grafana/grafana:13.0.1`）僅為參考。在生產環境部署前，請存取各專案的官方發佈頁或文件取得最新版本號。

> [!WARNING]
> 該完整堆疊示例包含宿主機根目錄、`/proc`、`/sys`、Docker 資料目錄掛載以及 `privileged: true`。Docker Compose 官方信任模型把這些欄位列為高風險宿主機控制面；只應在受控監控節點使用，並優先改為 rootless、唯讀、最小掛載和獨立監控網路。

```yaml
services:
  prometheus:
    image: prom/prometheus:v3.11.2
    container_name: prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--storage.tsdb.retention.time=30d'
    extra_hosts:
      - "host.docker.internal:host-gateway"
    networks:
      - monitoring

  node-exporter:
    image: prom/node-exporter:v1.11.1
    container_name: node-exporter
    ports:
      - "9100:9100"
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro
    command:
      - '--path.procfs=/host/proc'
      - '--path.sysfs=/host/sys'
      - '--collector.filesystem.mount-points-exclude=^/(sys|proc|dev|host|etc)($$|/)'
    networks:
      - monitoring

  cadvisor:
    image: ghcr.io/google/cadvisor:v0.56.2
    container_name: cadvisor
    ports:
      - "8080:8080"
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
    privileged: true
    networks:
      - monitoring

  grafana:
    image: grafana/grafana:13.0.1
    container_name: grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_ADMIN_PASSWORD:?set GRAFANA_ADMIN_PASSWORD}
      - GF_INSTALL_PLUGINS=grafana-piechart-panel
    volumes:
      - grafana_data:/var/lib/grafana
    networks:
      - monitoring

volumes:
  prometheus_data:
  grafana_data:

networks:
  monitoring:
    driver: bridge
```
**Prometheus 設定檔案（prometheus.yml）：**

如果需要採集 Docker daemon 自身指標，需要先在 Docker daemon 設定中開啟 metrics：

```json
{
  "metrics-addr": "127.0.0.1:9323"
}
```

Prometheus 運行在容器裡並使用 `host.docker.internal:9323` 抓取時，daemon 必須監聽容器可達的主機位址；若改為 `0.0.0.0:9323`，會把指標埠號暴露給更大網路，必須配合防火牆和可信網路邊界。

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']

  - job_name: 'cadvisor'
    static_configs:
      - targets: ['cadvisor:8080']

  - job_name: 'docker'
    static_configs:
      - targets: ['host.docker.internal:9323']
```
**常用的 Prometheus 查詢（PromQL）：**

```text
# 容器 CPU 使用百分比
rate(container_cpu_usage_seconds_total[5m]) * 100

# 容器記憶體使用百分比
(container_memory_usage_bytes / container_spec_memory_limit_bytes) * 100

# 容器網路入站流量（MB/s）
rate(container_network_receive_bytes_total[5m]) / 1024 / 1024

# 容器網路出站流量（MB/s）
rate(container_network_transmit_bytes_total[5m]) / 1024 / 1024

# 容器磁碟讀取速率（MB/s）
rate(container_fs_reads_bytes_total[5m]) / 1024 / 1024

# CPU 限流情況
rate(container_cpu_cfs_throttled_seconds_total[5m])

# 記憶體快取佔比
container_memory_cache_bytes / container_memory_usage_bytes

# 按映像檔統計容器數
count(container_memory_usage_bytes) by (image)
```

### 19.3.5 容器 OOM 排查與記憶體限制調校

#### OOM 問題診斷

```bash
# 檢查容器是否因 OOM 被殺死
docker inspect <container_id> | grep OOMKilled

# 查看容器退出碼：137 表示被 OOM 殺死
docker ps -a --format "{{.ID}}\t{{.Status}}" | grep "137"

# 查看容器日誌中的 OOM 資訊
docker logs <container_id> 2>&1 | grep -i "out of memory\|oom"

# 從宿主機日誌查看 OOM 事件
dmesg | grep -i "oom\|kill"
journalctl -u docker -n 100 | grep -i "oom"
```

#### 記憶體洩漏檢測

使用專項工具分析應用記憶體使用：

**Python 應用記憶體洩漏檢測：**

```python
# Dockerfile
FROM python:3.14-slim
WORKDIR /app
COPY requirements.txt .
# tracemalloc 是 Python 標準庫模組（自 3.4 起內建），無需安裝
RUN pip install -r requirements.txt memory_profiler

COPY app.py .
CMD ["python", "-m", "memory_profiler", "app.py"]
```
```python
# app.py - 記憶體洩漏示例
from memory_profiler import profile
import tracemalloc

@profile
def memory_leak():
    # 不斷建立未釋放的列表
    data = []
    while True:
        data.append([0] * 1000000)
        print(f"List size: {len(data)}")

# 使用 tracemalloc 追蹤記憶體分配
tracemalloc.start()

# 執行可能洩漏的程式碼
# ...

current, peak = tracemalloc.get_traced_memory()
print(f"Current: {current / 1024 / 1024:.2f} MB")
print(f"Peak: {peak / 1024 / 1024:.2f} MB")
```
**Java 應用記憶體分析：**

```bash
# 在容器中啟用 JVM 遠端偵錯
docker run -e JAVA_OPTS="-Xmx512m -Xms256m -XX:+UseG1GC" \
  -p 5005:5005 \
  myapp:latest

# 使用 jstat 檢查垃圾回收情況
jstat -gc <pid> 1000  # 每秒採樣一次

# 輸出示例：
#  S0C    S1C    S0U    S1U      EC       EU        OC         OU       MC       MU    CCSC   CCSU
# 6144   6144      0   6144   39424    12288   149504     84320     50552   47689  6464   5989
```

#### 記憶體限制最佳實務

```bash
# 為容器設定記憶體限制
docker run -m 512m --memory-swap 1g myapp:latest

# 參數說明：
# -m / --memory：記憶體限制（這裡是 512MB）
# --memory-swap：記憶體+SWAP 總額（這裡是 1GB，意味著 SWAP 為 512MB）
# 如果設定 --memory 但不設定 --memory-swap，有主機 swap 時容器總量可達記憶體限制的 2 倍；
# 要禁用 swap，應把 --memory-swap 設定為與 --memory 相同

# Docker Compose 設定
services:
  app:
    image: myapp:latest
    deploy:
      resources:
        limits:
          memory: 512M
        reservations:
          memory: 256M
```
**記憶體超額提交（Memory Overcommit）：**

```bash
# 在 Docker Compose 中區分限制和預留
# limits：絕不能超過的最大值
# reservations：Compose 排期時的參考值

services:
  web:
    memory: 512M  # 限制
    memswap_limit: 1G  # SWAP 限制

  db:
    memory: 2G
    memory_reservation: 1G  # 預留 1GB，允許突發到 2GB
```

### 19.3.6 映像檔體積最佳化與多階段建立

#### 映像檔體積分析工具

**使用 dive 分析映像檔層：**

```bash
# 安裝 dive
wget https://github.com/wagoodman/dive/releases/download/v0.13.1/dive_0.13.1_linux_amd64.deb
sudo apt install ./dive_0.13.1_linux_amd64.deb

# 分析映像檔
dive myapp:latest

# 輸出詳細的分層資訊，顯示每一層的大小和內容
```
**使用 Dockerfile 分析工具：**

```bash
# 安裝 hadolint
curl https://github.com/hadolint/hadolint/releases/download/v2.14.0/hadolint-Linux-x86_64 -L -o hadolint
chmod +x hadolint

# 檢查 Dockerfile 最佳實務
./hadolint Dockerfile
```

#### 多階段建立最佳實務

**Go 應用的最小化映像檔建立：**

```dockerfile
# Stage 1: 建立階段
FROM golang:1.26-alpine AS builder

WORKDIR /build

# 安裝依賴
RUN apk add --no-cache git ca-certificates tzdata

COPY go.mod go.sum ./
RUN go mod download

COPY . .

# 建立靜態二進位（支持 scratch 基礎映像檔）
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build \
    -a -installsuffix cgo \
    -ldflags="-w -s" \
    -o app .

# Stage 2: 運行階段
FROM scratch

# 從 builder 複製必要的檔案
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /usr/share/zoneinfo /usr/share/zoneinfo
COPY --from=builder /build/app /app

EXPOSE 8080
ENTRYPOINT ["/app"]

# 最終映像檔大小通常 < 15MB（相比 golang:1.26 基礎映像檔的 ~900MB）
```
**Node.js 應用的多階段建立：**

```dockerfile
# Stage 1: 依賴安裝
FROM node:24-alpine AS dependencies

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production && \
    npm cache clean --force

# Stage 2: 建立階段
FROM node:24-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# Stage 3: 運行階段
FROM node:24-alpine

WORKDIR /app

# 從依賴階段複製 node_modules
COPY --from=dependencies /app/node_modules ./node_modules

# 從建立階段複製建立產物
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package*.json ./

# 刪除開發依賴和不必要的檔案
RUN rm -rf src tests *.config.js

USER node
EXPOSE 3000

CMD ["node", "dist/index.js"]

# 映像檔大小對比：
# 不最佳化：~500MB
# 多階段建立後：~120MB（減少 76%）
```
**Python 應用的多階段建立：**

```dockerfile
# Stage 1: 建立階段
FROM python:3.14-slim AS builder

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: 運行階段
FROM python:3.14-slim

WORKDIR /app

# 從 builder 複製虛擬環境
COPY --from=builder /root/.local /root/.local

# 設定 PATH
ENV PATH=/root/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

COPY . .

USER nobody
EXPOSE 5000

CMD ["python", "app.py"]
```

#### 映像檔體積最佳化檢查清單

```bash
# 檢查清單
□ 使用精簡基礎映像檔（Alpine、Distroless）
□ 清理套件管理器快取（apt-get clean、rm -rf /var/cache/*）
□ 在同一 RUN 指令中安裝和清理依賴
□ 使用 .dockerignore 排除不必要的檔案
□ 多階段建立避免建立依賴污染最終映像檔
□ 去除偵錯符號：-ldflags="-w -s"（Go）、strip 命令（C/C++）
□ 壓縮靜態資源和應用檔案
□ 使用 BuildKit 快取最佳化加速建立

# 最佳化示例：
FROM ubuntu:24.04

# ❌ 不推薦
RUN apt-get update
RUN apt-get install -y curl wget git
RUN apt-get clean

# ✓ 推薦
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    wget \
    git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

### 19.3.7 常見效能問題及解決方案

**問題 1: 容器頻繁被 OOM 殺死**

症狀：容器程式被無故殺死，exit code 137
解決方案：
```bash
# 增加記憶體限制
docker update -m 1g <container_id>

# 排查記憶體洩漏
docker exec <container_id> ps aux | grep -E "VSZ|RSS"

# 使用 docker stats 即時監控
docker stats <container_id>

# 啟用記憶體交換（作為最後手段）
docker run -m 512m --memory-swap 1g myapp:latest
```
**問題 2: CPU 被限流（CPU Throttling）**

症狀：應用效能突然下降，但 CPU 使用率不高
診斷：
```bash
# 查看 CPU 限流統計；現代發行版多為 cgroup v2，具體路徑需先定位容器 cgroup
docker inspect --format '{{.State.Pid}}' <container_id>
grep cgroup /proc/<pid>/mountinfo
docker exec <container_id> cat /sys/fs/cgroup/cpu.stat

# cgroup v1 主機可能仍使用：
# docker exec <container_id> cat /sys/fs/cgroup/cpu/cpu.stat

# 如果 nr_throttled / throttled_usec > 0，說明發生了 CPU 限流
# 解決方案：增加 CPU 限制
docker update --cpus 2 <container_id>
```
**問題 3: 網路丟包或延遲高**

診斷：
```bash
# 進入容器檢查網路狀態
docker exec <container_id> ip -s link show

# 檢查路由和 DNS
docker exec <container_id> cat /etc/resolv.conf

# 測試網路延遲
docker exec <container_id> ping 8.8.8.8

# 檢查容器網路驅動
docker inspect <container_id> | grep -A 10 NetworkSettings

# 解決方案：更換網路驅動或調整 MTU
# host 網路可降低網路堆疊開銷，但會放棄容器網路隔離；僅在明確接受安全邊界變化時使用
docker run --net=host myapp:latest
```

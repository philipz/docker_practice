## 16.3 阿里雲

如圖 16-3 所示，阿里雲是國內主流雲服務平台之一。

![阿里雲](./_images/aliyun-logo.png)

圖 16-3：阿里雲標識

[阿里雲](https://www.aliyun.com/)創立於 2009 年，是中國較早的雲端運算平台。阿里雲致力於提供安全、可靠的計算和資料處理能力。

[阿里雲](https://www.aliyun.com/)的客戶群體中，活躍著微博、虎牙、魅族、優酷等一大批明星網際網路公司。在天貓雙 11 全球狂歡節等極富挑戰的應用場景中，阿里雲保持著良好的運行紀錄。

[阿里雲容器服務 Kubernetes 版 ACK](https://cn.aliyun.com/product/ack) 提供了高效能、可伸縮的容器應用管理服務，支持在一群雲伺服器上通過 Docker 容器來進行應用生命週期管理。容器服務極大簡化了使用者對容器管理集群的搭建工作，無縫整合了阿里雲虛擬化、儲存、網路和安全能力。容器服務提供了多種應用發佈方式和流水線般的持續交付能力，原生支持微服務架構，助力使用者無縫上雲和跨雲管理。

<!-- 注意：原阿里雲容器服務截圖連結已失效，請參考阿里雲官方文件取得最新介面截圖 -->
<!-- 原連結: https://img.alicdn.com/tps/TB10yjtPpXXXXacXXXXXXXXXXXX-1531-1140.png -->

圖 16-4：阿里雲容器服務示意圖（請存取 [阿里雲容器服務 ACK 官方文件](https://help.aliyun.com/zh/ack/) 查看最新介面）

### 阿里雲容器服務 ACK 簡介

阿里雲容器服務 Kubernetes 版 (ACK, Container Service for Kubernetes) 是一款託管式 Kubernetes 服務，基於開源 Kubernetes 建立，提供企業級的容器編排和管理能力。ACK 整合了阿里雲儲存、網路和安全能力，支持多種應用部署模式和持續交付流程。

### 基本使用步驟

#### 1. 建立集群

登入阿里雲控制台，進入容器服務 > Kubernetes 集群：

- 點擊 “建立集群”，選擇集群設定
- 設定集群名稱、地域、可用區和節點類型
- 選擇節點規格和數量（支持彈性伸縮）
- 設定網路參數和安全設定
- 完成建立，下載 kubeconfig 檔案

```bash
# 設定本地 kubectl
export KUBECONFIG=/path/to/kubeconfig.yaml
kubectl get nodes
```

#### 2. 部署容器應用

通過 Deployment 部署應用示例：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-server
spec:
  replicas: 2
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: web
        image: registry.cn-hangzhou.aliyuncs.com/myapp/web:v1
        ports:
        - containerPort: 8080
        resources:
          limits:
            memory: "512Mi"
            cpu: "500m"
```
部署應用：

```bash
kubectl apply -f deployment.yaml
kubectl get pods -o wide
kubectl logs <pod-name>
```

#### 3. 暴露服務

建立 Service 暴露應用：

```yaml
apiVersion: v1
kind: Service
metadata:
  name: web-service
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 8080
  selector:
    app: web
```
應用：

```bash
kubectl apply -f service.yaml
kubectl get svc web-service
```

### 阿里雲 Docker 映像檔加速器設定

為了加快從阿里雲映像檔源拉取官方映像檔的速度，可以設定映像檔加速器。阿里雲為容器服務 ACK 使用者提供了免費的映像檔加速服務。

#### 取得加速器位址

登入阿里雲容器映像檔服務控制台，在 “映像檔工具” > “映像檔加速器” 中可取得個人的加速器位址（類似於 `https://xxxxxx.mirror.aliyuncs.com`）。

#### Linux 系統設定

編輯或建立 `/etc/docker/daemon.json` 檔案：

```bash
sudo mkdir -p /etc/docker
sudo nano /etc/docker/daemon.json
```
加入或修改以下內容（替換為你的加速器位址）：

```json
{
  "registry-mirrors": [
    "https://xxxxxx.mirror.aliyuncs.com"
  ]
}
```
重新載入並重新啟動 Docker：

```bash
sudo systemctl daemon-reload
sudo systemctl restart docker
```
驗證設定生效：

```bash
docker info | grep -A 5 "Registry Mirrors"
```

#### Windows/Mac 設定

在 Docker Desktop 的 Settings 中：

1. 進入 “Docker Engine” 標籤
2. 編輯 JSON 設定，加入 `registry-mirrors` 欄位
3. 點擊 “Apply & Restart”

#### 測試加速效果

```bash
# 從加速器拉取映像檔（速度應該明顯提升）
docker pull nginx:latest
time docker pull alpine:latest
```

### 阿里雲容器映像檔服務：ACR

阿里雲容器映像檔服務 (ACR, Container Registry) 是企業級的容器映像檔儲存和分發平台：

- **私有映像檔倉庫**：支持多個命名空間，細粒度權限控制
- **映像檔建立**：雲端編譯和建立，支持自動化 CI/CD
- **映像檔掃描**：自動檢測映像檔中的漏洞和惡意程式碼
- **跨地域複製**：支持映像檔在多個地域的同步和加速
- **整合 ACK**：與 ACK 無縫整合，自動身分認證
- **映像檔版本管理**：標籤管理、映像檔過期清理、保留策略

#### 完整推送/拉取示例

```bash
# 登入阿里雲映像檔倉庫（使用 Docker 登入）
# 使用阿里雲帳戶 ID 和 RAM 存取金鑰或密碼
docker login registry.cn-hangzhou.aliyuncs.com \
  --username=<阿里雲帳戶ID>

# 拉取阿里雲公開映像檔
docker pull registry.cn-hangzhou.aliyuncs.com/library/nginx:latest

# 建立本地映像檔
docker build -t my-app:v1.0 .

# 標記映像檔為阿里雲倉庫位址
docker tag my-app:v1.0 \
  registry.cn-hangzhou.aliyuncs.com/myapp/my-app:v1.0

# 推送映像檔到阿里雲 ACR
docker push registry.cn-hangzhou.aliyuncs.com/myapp/my-app:v1.0

# 在 Dockerfile 中使用 ACR 映像檔
FROM registry.cn-hangzhou.aliyuncs.com/myapp/my-app:v1.0
COPY . /app
RUN echo "已成功使用阿里雲映像檔"
```

#### ACK 集群中使用 ACR 映像檔

在 ACK 集群中，需要先設定映像檔拉取憑證（Secret），然後在 Deployment 中引用：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-server
  namespace: default
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      # 如果是私有映像檔，需設定映像檔拉取憑證
      imagePullSecrets:
      - name: acr-secret
      containers:
      - name: web
        image: registry.cn-hangzhou.aliyuncs.com/myapp/web:v2.0
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "500m"
      affinity:
        # 設定 Pod 反親和性，分散到不同節點
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - web
              topologyKey: kubernetes.io/hostname
```

#### 建立映像檔拉取憑證

在 ACK 集群中建立 Secret，用於拉取私有映像檔：

```bash
# 避免把真實口令寫入命令歷史。使用臨時 Docker config 並通過標準輸入登入。
export DOCKER_CONFIG="$(mktemp -d)"
read -rsp "ACR token: " ACR_TOKEN; echo
printf "%s" "$ACR_TOKEN" | docker login registry.cn-hangzhou.aliyuncs.com \
  --username "<阿里雲帳戶ID>" \
  --password-stdin

kubectl create secret generic acr-secret \
  --from-file=.dockerconfigjson="$DOCKER_CONFIG/config.json" \
  --type=kubernetes.io/dockerconfigjson

rm -rf "$DOCKER_CONFIG"
unset ACR_TOKEN DOCKER_CONFIG

# 查看建立的 Secret
kubectl get secret acr-secret
kubectl describe secret acr-secret
```

#### ACR 優勢

- 在 ACK 集群中與映像檔倉庫無縫整合，簡化身分認證
- 支持 Helm Chart 儲存和版本管理，方便應用交付
- 提供完整的圖形化映像檔倉庫管理介面
- 完整的稽核日誌和操作追蹤功能
- 支持映像檔自動掃描和漏洞報告

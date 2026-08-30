## HEALTHCHECK 健康檢查

### 基本語法

```docker
HEALTHCHECK [選項] CMD <命令>
HEALTHCHECK NONE
```
`HEALTHCHECK` 指令告訴 Docker 如何判斷容器狀態是否正常。這是保障服務高可用的重要機制。

---

### 為什麼需要 HEALTHCHECK

在沒有 HEALTHCHECK 之前，Docker 只能透過 **程式退出碼** 來判斷容器狀態。**問題場景**：

- Web 服務死鎖，無法回應請求，但程式仍在執行
- 資料庫正在啟動中，尚未準備好接受連線
- 應用陷入無窮迴圈，CPU 爆滿但程式存活

**引入 HEALTHCHECK 後**：
Docker 定期執行指定的檢查命令，根據回傳值判斷容器是否「健康」。

```bash
容器狀態轉換：
Starting ──成功──> Healthy ──失敗N次──> Unhealthy
                    ▲                │
                    └──────成功──────┘
```
---

### 基本用法

#### Web 服務檢查

```docker
# 註：nginx 映像檔推薦使用具體的版本標籤（如 nginx:1.28-alpine）
FROM nginx
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD curl -fs http://localhost/ || exit 1
```

#### 命令回傳值

- `0`：成功 (healthy)
- `1`：失敗 (unhealthy)
- `2`：保留值（不使用）

#### 常用選項

| 選項 | 說明 | 預設值 |
|------|------|--------|
| `--interval` | 兩次檢查的間隔 | 30s |
| `--timeout` | 檢查命令的超時時間 | 30s |
| `--start-period` | 啟動緩衝期（期間失敗不計入次數）| 0s |
| `--retries` | 連續失敗多少次標記為 unhealthy | 3 |

---

### 遮蔽健康檢查

如果基礎映像檔定義了 HEALTHCHECK，但你不想使用它：

```docker
FROM my-base-image
HEALTHCHECK NONE
```
---

### 常見檢查腳本

#### HTTP 服務

使用 `curl` 或 `wget`：

```docker
## 使用 curl

HEALTHCHECK CMD curl -f http://localhost/ || exit 1

## 使用 wget（Alpine 預設包含）

HEALTHCHECK CMD wget -q --spider http://localhost/ || exit 1
```

#### 資料庫

```docker
## MySQL

HEALTHCHECK CMD mysqladmin ping -h localhost || exit 1

## Redis

HEALTHCHECK CMD redis-cli ping || exit 1
```

#### 自訂腳本

```docker
COPY healthcheck.sh /usr/local/bin/
HEALTHCHECK CMD ["healthcheck.sh"]
```
---

### 在 Compose 中使用

可以在 `compose.yaml`（或 `docker-compose.yml`）中覆蓋或定義健康檢查：

```yaml
services:
  web:
    image: nginx
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost"]
      interval: 1m30s
      timeout: 10s
      retries: 3
      start_period: 40s
```
帶健康檢查的依賴啟動：

```yaml
services:
  web:
    depends_on:
      db:
        condition: service_healthy  # 等待 db 變健康才啟動 web
  db:
    image: mysql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
```
---

### 查看健康狀態

```bash
## 查看容器狀態（包含健康資訊）

$ docker ps
CONTAINER ID   STATUS
abc123         Up 1 minute (healthy)
def456         Up 2 minutes (unhealthy)

## 查看詳細健康日誌

$ docker inspect --format '{{json .State.Health}}' mycontainer | jq
{
  "Status": "healthy",
  "FailingStreak": 0,
  "Log": [
    {
      "Start": "...",
      "End": "...",
      "ExitCode": 0,
      "Output": "..."
    }
  ]
}
```
---

### 最佳實踐

#### 1. 避免副作用

健康檢查會被頻繁執行，不要在檢查腳本中進行寫操作或消耗大量資源的操作。

#### 2. 使用輕量級工具

優先使用映像檔中已有的工具（如 `wget`），避免為了健康檢查安裝龐大的依賴（如 `curl`）。

#### 3. 設定合理的 Start Period

應用啟動可能需要時間（如 Java 應用）。設定 `--start-period` 可以防止在啟動階段因檢查失敗而誤判。

```docker
## 給應用 1 分鐘啟動時間

HEALTHCHECK --start-period=60s CMD curl -f http://localhost/ || exit 1
```

#### 4. 只檢查核心依賴

健康檢查應主要關注 **目前服務** 是否可用，而不是檢查其下游依賴（資料庫等）。下游依賴的檢查應由應用邏輯處理。

#### 5. 與容器編排平台的關係

不同平台對 HEALTHCHECK 的支援有所不同：

- **Docker Compose**：直接使用 Dockerfile 中定義的 HEALTHCHECK，也可在 `compose.yaml` 中覆蓋
- **Docker Swarm**：使用 HEALTHCHECK 進行服務健康判斷和滾動更新決策
- **Kubernetes**：**忽略** Dockerfile 中的 HEALTHCHECK，使用自己的 `livenessProbe` 和 `readinessProbe` 機制

如果應用同時部署在 Docker Compose 和 Kubernetes 環境中，建議在 Dockerfile 中保留 HEALTHCHECK（供 Compose 使用），同時在 Kubernetes 的 Pod 設定中定義對應的探針。

---

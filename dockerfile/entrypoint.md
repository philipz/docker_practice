## ENTRYPOINT 入口點

### 何時使用 ENTRYPOINT：從「容器」到「命令」

如果說 CMD 是「容器中的預設程式」，那麼 ENTRYPOINT 就是「把容器變成一個命令」。這個思維轉變決定了你何時使用 ENTRYPOINT。

**使用 ENTRYPOINT 的典型場景**：

1. **命令列工具**：你想讓映像檔像 `curl` 或 `wget` 一樣使用
   ```dockerfile
   ENTRYPOINT ["curl"]
   # docker run myimage http://example.com → curl http://example.com
   ```

2. **應用啟動腳本**：你有一個初始化腳本，需要接收命令列參數
   ```dockerfile
   ENTRYPOINT ["/app/entrypoint.sh"]
   # docker run myimage --debug → /app/entrypoint.sh --debug
   ```

3. **與 CMD 結合**：ENTRYPOINT 定義入口，CMD 定義預設參數
   ```dockerfile
   ENTRYPOINT ["python", "app.py"]
   CMD ["--port", "8000"]
   # docker run myimage → python app.py --port 8000
   # docker run myimage --port 9000 → python app.py --port 9000
   ```

**對比 CMD**：如果沒有這些「把容器當命令用」的需求，通常使用 CMD 就足夠了。

### 什麼是 ENTRYPOINT

`ENTRYPOINT` 指定容器啟動時執行的入口程式。與 CMD 不同，ENTRYPOINT 定義的命令不會被 `docker run` 的參數覆蓋，而是 **接收這些參數**。

> **核心作用**：讓映像檔像一個可執行程式一樣使用，`docker run` 的參數作為這個程式的參數。

---

### 語法格式

| 格式 | 語法 | 推薦程度 |
|------|------|---------|
| **exec 格式**| `ENTRYPOINT ["可執行檔案", "參數1"]` | ✅**推薦** |
| **shell 格式** | `ENTRYPOINT 命令 參數` | ⚠️ 不推薦 |

```docker
## exec 格式（推薦）

ENTRYPOINT ["nginx", "-g", "daemon off;"]

## shell 格式（不推薦）

ENTRYPOINT nginx -g "daemon off;"
```
---

### ENTRYPOINT vs CMD

#### 核心區別

| 特性 | ENTRYPOINT | CMD |
|------|------------|-----|
| **定位** | 固定的入口程式 | 預設參數 |
| **docker run 參數** | 追加為參數 | 完全覆蓋 |
| **覆蓋方式** | `--entrypoint` | 直接指定命令 |
| **適用場景** | 把映像檔當命令用 | 提供預設行為 |

#### 行為對比

```docker
## 只用 CMD

CMD ["curl", "-s", "http://example.com"]
```
```bash
$ docker run myimage              # curl -s http://example.com
$ docker run myimage -v           # 執行 -v（錯誤！）
$ docker run myimage curl -v ...  # curl -v ...（完全替換）
```
```docker
## 只用 ENTRYPOINT

ENTRYPOINT ["curl", "-s"]
```
```bash
$ docker run myimage                      # curl -s（缺參數）
$ docker run myimage http://example.com   # curl -s http://example.com ✓
```
```docker
## ENTRYPOINT + CMD 組合（推薦）

ENTRYPOINT ["curl", "-s"]
CMD ["http://example.com"]
```
```bash
$ docker run myimage                      # curl -s http://example.com（預設）
$ docker run myimage http://other.com     # curl -s http://other.com ✓
$ docker run myimage -v http://other.com  # curl -s -v http://other.com ✓
```
---

### 場景一：讓映像檔像命令一樣使用

#### 需求：啟動前準備

建立一個查詢公網 IP 的「命令」映像檔。

#### 使用 CMD 的問題

```docker
FROM ubuntu:24.04
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
CMD ["curl", "-s", "http://myip.ipip.net"]
```
```bash
$ docker run myip           # ✓ 正常工作
當前 IP：61.148.226.66

$ docker run myip -i        # ✗ 錯誤！
exec: "-i": executable file not found

## -i 替換了整個 CMD，被當作可執行檔案

...
```

#### 使用 ENTRYPOINT 解決

```docker
FROM ubuntu:24.04
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
ENTRYPOINT ["curl", "-s", "http://myip.ipip.net"]
```
```bash
$ docker run myip           # ✓ 正常工作
當前 IP：61.148.226.66

$ docker run myip -i        # ✓ 新增 -i 參數
HTTP/1.1 200 OK
...
當前 IP：61.148.226.66
```

#### 互動圖示

```bash
ENTRYPOINT ["curl", "-s", "http://myip.ipip.net"]
            │
docker run myip -i
            │
            ▼
curl -s http://myip.ipip.net -i
└─────────────────────────────┘
     ENTRYPOINT + docker run 參數
```
---

### 場景二：啟動前的準備工作

#### 需求

在啟動主服務前執行初始化腳本（如資料庫遷移、權限設定）。

#### 實作方式

```docker
# 建議使用 redis:7 等具體版本標籤，避免 latest，具體版本號根據生產需求選擇
FROM redis:7-alpine
COPY docker-entrypoint.sh /usr/local/bin/
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["redis-server"]
```
**docker-entrypoint.sh**：

```bash
#!/bin/sh
set -e

## 準備工作

echo "Initializing..."

## 如果第一個參數是 redis-server，以 redis 使用者執行

if [ "$1" = 'redis-server' ]; then
    chown -R redis:redis /data
    exec gosu redis "$@"
fi

## 其他命令直接執行

exec "$@"
```

#### 工作流程

```bash
docker run redis                    docker run redis bash
        │                                    │
        ▼                                    ▼
docker-entrypoint.sh redis-server   docker-entrypoint.sh bash
        │                                    │
        ├─ 初始化                            ├─ 初始化
        ├─ chown -R redis:redis /data        │
        └─ exec gosu redis redis-server      └─ exec bash
           (以 redis 使用者執行)               (以 root 使用者執行)
```

#### 關鍵點

1. **exec "$@"**：用傳入的參數替換當前程式，確保訊號正確傳遞
2. **條件判斷**：根據 CMD 不同執行不同邏輯
3. **使用者切換**：使用 `gosu` 切換使用者（比 `su` 更適合容器）

---

### 場景三：帶參數的應用

```docker
# 建議使用 python:3.12 或 python:3，具體版本號根據應用相容性需求選擇
FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "app.py"]
CMD ["--host", "0.0.0.0", "--port", "8080"]
```
```bash
## 使用預設參數

$ docker run myapp

## 執行: python app.py --host 0.0.0.0 --port 8080

## 覆蓋參數

$ docker run myapp --host 0.0.0.0 --port 9000

## 執行: python app.py --host 0.0.0.0 --port 9000

## 完全不同的參數

$ docker run myapp --help

## 執行: python app.py --help

...
```
---

### 覆蓋 ENTRYPOINT

使用 `--entrypoint` 參數覆蓋：

```bash
## 正常執行

$ docker run myimage

## 覆蓋 ENTRYPOINT 進入 shell 除錯

$ docker run --entrypoint /bin/sh myimage

## 覆蓋 ENTRYPOINT 並傳入參數

$ docker run --entrypoint /bin/cat myimage /etc/os-release
```
---

### ENTRYPOINT 與 CMD 組合表

| ENTRYPOINT | CMD | 最終執行命令 |
|------------|-----|-------------|
| 無 | 無 | 無（容器無法啟動）|
| 無 | `["cmd", "p1"]` | `cmd p1` |
| `["ep", "p1"]` | 無 | `ep p1` |
| `["ep", "p1"]` | `["cmd", "p2"]` | `ep p1 cmd p2` |
| `ep p1` (shell)| `["cmd", "p2"]` | `/bin/sh -c "ep p1"`（CMD 被忽略）|

> ⚠️ **注意**：shell 格式的 ENTRYPOINT 會忽略 CMD！

---

### 最佳實務

#### 1. 使用 exec 格式

```docker
## ✅ 推薦

ENTRYPOINT ["python", "app.py"]

## ❌ 避免 shell 格式

ENTRYPOINT python app.py
```

#### 2. 提供有意義的預設參數

```docker
ENTRYPOINT ["nginx"]
CMD ["-g", "daemon off;"]
```

#### 3. 入口腳本使用 exec

```bash
#!/bin/sh

## 準備工作...

## 使用 exec 替換當前程式

exec "$@"
```

#### 4. 處理訊號

確保 ENTRYPOINT 腳本能正確傳遞訊號：

```bash
#!/bin/bash
trap 'kill -TERM $PID' TERM INT

## 啟動應用

app "$@" &
PID=$!

## 等待應用退出

wait $PID
```
---

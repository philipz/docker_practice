## WORKDIR 指定工作目錄

### 基本語法

```docker
WORKDIR <工作目錄路徑>
```
`WORKDIR` 指定後續指令的工作目錄。如果目錄不存在，Docker 會自動建立。

---

### 基本用法

```docker
WORKDIR /app

RUN pwd          # 輸出 /app
RUN echo "hello" > world.txt    # 建立 /app/world.txt
COPY . .         # 複製到 /app/
```
---

### 為什麼需要 WORKDIR

#### 常見錯誤

```docker
## ❌ 錯誤：cd 在下一個 RUN 中無效

RUN cd /app
RUN echo "hello" > world.txt    # 檔案在根目錄！
```

#### 原因分析

```dockerfile
RUN cd /app
    ↓
啟動容器 → cd /app（僅記憶體變化）→ 提交映像檔層 → 容器銷毀
                                   │
                                   ↓ 工作目錄未改變！
RUN echo "hello" > world.txt
    ↓
啟動新容器（工作目錄在 /）→ 建立 /world.txt
```
每個 RUN 都在新容器中執行，**前一個 RUN 的記憶體狀態（包括工作目錄）不會保留**。

#### 正確做法

```docker
## ✅ 正確：使用 WORKDIR

WORKDIR /app
RUN echo "hello" > world.txt    # 建立 /app/world.txt
```
---

### 相對路徑

WORKDIR 支援相對路徑，基於上一個 WORKDIR：

```docker
WORKDIR /a
WORKDIR b
WORKDIR c

RUN pwd    # 輸出 /a/b/c
```
---

### 使用環境變數

```docker
ENV APP_HOME=/app
WORKDIR $APP_HOME

RUN pwd    # 輸出 /app
```
---

### 多階段建立中的 WORKDIR

```docker
## 建立階段
## 建議使用 node:22 或 node: 等具體版本標籤，避免使用 latest

FROM node:22 AS builder
WORKDIR /build
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

## 生產階段
## 建議使用 nginx:alpine 或其他具體版本

FROM nginx:alpine
WORKDIR /usr/share/nginx/html
COPY --from=builder /build/dist .
```
---

### 最佳實踐

#### 1. 盡早設定 WORKDIR

```docker
# 建議使用 node:22 等主/次版本號標籤
FROM node:22
WORKDIR /app    # 盡早設定

COPY package*.json ./
RUN npm install
COPY . .
CMD ["node", "server.js"]
```

#### 2. 使用絕對路徑

```docker
## ✅ 建議：絕對路徑，意圖明確

WORKDIR /app

## ⚠️ 避免：相對路徑可能造成混淆

WORKDIR app
```

#### 3. 不要用 RUN cd

```docker
## ❌ 避免

RUN cd /app && echo "hello" > world.txt

## ✅ 建議

WORKDIR /app
RUN echo "hello" > world.txt
```

#### 4. 適時重置 WORKDIR

```docker
WORKDIR /app

## ... 應用程式相關操作 ...

WORKDIR /data

## ... 資料相關操作 ...

...
```
---

### 與其他指令的關係

| 指令 | WORKDIR 的影響 |
|------|---------------|
| `RUN` | 在 WORKDIR 中執行命令 |
| `CMD` | 在 WORKDIR 中啟動 |
| `ENTRYPOINT` | 在 WORKDIR 中啟動 |
| `COPY` | 相對目標路徑基於 WORKDIR |
| `ADD` | 相對目標路徑基於 WORKDIR |

```docker
WORKDIR /app

RUN pwd                    # /app
COPY . .                   # 複製到 /app
CMD ["./start.sh"]         # /app/start.sh
```
---

### 執行期覆寫

使用 `-w` 參數覆寫工作目錄：

```bash
$ docker run -w /tmp myimage pwd
/tmp
```
---

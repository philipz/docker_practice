## ARG 建立參數

### 基本語法

```docker
ARG <參數名>[=<預設值>]
```
`ARG` 指令定義建立時的變數，可以在 `docker build` 時透過 `--build-arg` 傳入。

---

### ARG vs ENV

| 特性 | ARG | ENV |
|------|-----|-----|
| **生效時間** | 僅建立時 | 建立時 + 執行期 |
| **持久性** | 建立後消失 | 寫入映像檔 |
| **覆寫方式** | `docker build --build-arg` | `docker run -e` |
| **適用場景** | 建立參數（版本號等）| 應用程式設定 |
| **可見性** | `docker history` 可見 | `docker inspect` 可見 |

```dockerfile
建立時                         執行期
├─ ARG VERSION=1.0             │ （ARG 已消失）
├─ ENV APP_ENV=prod            │ APP_ENV=prod（仍存在）
└─ RUN echo $VERSION           │
```
> ⚠️ **安全提示**：不要用 ARG 傳遞密碼等敏感資訊，`docker history` 可以查看所有 ARG 值。

---

### 基本用法

#### 定義和使用

```docker
## 定義有預設值的 ARG
## 建議使用主版本號，如 20 而非 20.10.0，這樣可以自動取得最新的修補版本

ARG NODE_VERSION=20

## 使用 ARG

FROM node:${NODE_VERSION}-alpine
RUN echo "Using Node.js $NODE_VERSION"
```

#### 建立時覆寫

```bash
## 使用預設值

$ docker build -t myapp .

## 覆寫預設值

$ docker build --build-arg NODE_VERSION=18 -t myapp .
```
---

### ARG 的作用域

#### FROM 之前的 ARG

```docker
## FROM 之前的 ARG 只能用於 FROM 指令

ARG REGISTRY=docker.io
ARG IMAGE_NAME=node

FROM ${REGISTRY}/${IMAGE_NAME}:20

## ❌ 這裡無法使用上面的 ARG

RUN echo $REGISTRY  # 輸出空
```

#### FROM 之後重新宣告

```docker
ARG NODE_VERSION=20

FROM node:${NODE_VERSION}-alpine

## 需要再次宣告才能使用

ARG NODE_VERSION
RUN echo "Node version: $NODE_VERSION"
```

#### 多階段建立中的 ARG

```docker
ARG BASE_VERSION=alpine

FROM node:22-${BASE_VERSION} AS builder

## 需要重新宣告

ARG NODE_VERSION=20
RUN echo "Building with Node $NODE_VERSION"

FROM node:22-${BASE_VERSION}

## 每個階段都需要重新宣告

ARG NODE_VERSION=20
RUN echo "Running with Node $NODE_VERSION"
```
---

### 常見使用場景

#### 1. 控制基礎映像檔版本

```docker
# 建議使用主版本號（如 3），或指定次版本號（如 3.19），避免指定完整修補版本
ARG ALPINE_VERSION=3
FROM alpine:${ALPINE_VERSION}
```
```bash
$ docker build --build-arg ALPINE_VERSION=3.19 .
```

#### 2. 設定軟體版本

```docker
# 使用次版本號 (1.30) 而非完整版本號 (1.30.0)，以便自動更新到最新修補版本
ARG NGINX_VERSION=1.30

RUN curl -fsSL https://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz | tar -xz
```

#### 3. 設定建立環境

```docker
ARG BUILD_ENV=production
ARG ENABLE_DEBUG=false

RUN if [ "$ENABLE_DEBUG" = "true" ]; then \
        npm install --include=dev; \
    else \
        npm install --production; \
    fi
```

#### 4. 設定私有倉庫

不要用 `ARG` 或 `ENV` 傳遞倉庫 token。Docker 官方建立檢查會把這類寫法視為不安全，因為建立參數和環境變數可能進入映像檔中繼資料或歷史記錄。使用 BuildKit secret mount 只在單條 `RUN` 指令期間暴露憑據：

```docker
RUN --mount=type=secret,id=npm_token \
    NPM_TOKEN="$(cat /run/secrets/npm_token)" && \
    printf "//registry.npmjs.org/:_authToken=%s\n" "$NPM_TOKEN" > ~/.npmrc && \
    npm install && \
    rm ~/.npmrc
```
```bash
## 建立時傳入 token

$ docker build --secret id=npm_token,env=NPM_TOKEN .
```
---

### 將 ARG 傳遞給 ENV

如果需要在執行期使用 ARG 的值：

```docker
ARG VERSION=1.0.0

## 將 ARG 傳遞給 ENV

ENV APP_VERSION=$VERSION

## 執行期可用

CMD echo "App version: $APP_VERSION"
```
---

### 預定義 ARG

Docker 提供了一些預定義的 ARG，無需宣告即可使用：

| ARG | 說明 |
|-----|------|
| `HTTP_PROXY` | HTTP 代理 |
| `HTTPS_PROXY` | HTTPS 代理 |
| `NO_PROXY` | 不使用代理的位址 |
| `FTP_PROXY` | FTP 代理 |

```bash
## 建立時使用代理

$ docker build --build-arg HTTP_PROXY=http://proxy:8080 .
```
---

### 最佳實踐

#### 1. 為 ARG 提供合理預設值

```docker
## ✅ 好：有預設值，建議使用主或次版本號而非完整版本號

ARG NODE_VERSION=20

## ⚠️ 需要每次傳入

ARG NODE_VERSION
```

#### 2. 不要用 ARG 儲存敏感資訊

```docker
## ❌ 錯誤：密碼會被記錄在映像檔歷史中

ARG DB_PASSWORD
RUN echo "password=$DB_PASSWORD" > /app/.env

## ✅ 正確：使用 secrets 或執行期環境變數

...
```

#### 3. 使用 ARG 提高建立靈活性

```docker
# 建議使用次版本號標籤，允許 Docker 自動拉取最新的修補版本
ARG BASE_IMAGE=python:3.12-slim
FROM ${BASE_IMAGE}

## 可以建立不同基礎映像檔的版本

## docker build --build-arg BASE_IMAGE=python:3-slim .

...
```
---

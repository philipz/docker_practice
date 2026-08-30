## BuildKit

**BuildKit** 是下一代的映像檔構建元件，在 [moby/buildkit](https://github.com/moby/buildkit) 開源。

> **重要**：自 Docker 23 起，BuildKit 已成為 **預設穩定構建器**，無需手動啟用。Docker Engine 29 在新安裝情境中進一步將 containerd image store 設為預設，提升多平台映像檔、SBOM/Provenance 等 OCI 中繼資料能力。

目前，Docker Hub 自動構建已經支援 BuildKit，具體請參考 [docker-practice/docker-hub-buildx](https://github.com/docker-practice/docker-hub-buildx)。

### `Dockerfile` 新增指令詳解

BuildKit 引入了多項新指令，旨在最佳化構建快取和安全性。以下將詳細介紹這些指令的用法。

使用 BuildKit 後，我們可以使用下面幾個新的 `Dockerfile` 指令來加快映像檔構建。

要使用最新的 Dockerfile 語法特性，建議在 Dockerfile 開頭加入語法指令：

```docker
# syntax=docker/dockerfile:1

```
這將使用最新的穩定版語法解析器，確保你可以使用所有最新特性。

#### `RUN --mount=type=cache`

目前，幾乎所有的程式都會使用依賴管理工具，例如 `Go` 中的 `go mod`、`Node.js` 中的 `npm` 等等，當我們構建一個映像檔時，往往會重複的從網際網路中取得依賴套件，難以快取，大大降低了映像檔的構建效率。

例如一個前端工程需要用到 `npm`：

```docker
FROM node:alpine as builder

WORKDIR /app

COPY package.json /app/

RUN npm i --registry=https://registry.npmmirror.com \
        && rm -rf ~/.npm

COPY src /app/src

RUN npm run build

FROM nginx:alpine

COPY --from=builder /app/dist /app/dist
```
使用多階段構建，構建的映像檔中只包含了目標資料夾 `dist`，但仍然存在一些問題，當 `package.json` 檔案變動時，`RUN npm i && rm -rf ~/.npm` 這一層會重新執行，變更多次後，產生了大量的中間層映像檔。

為解決這個問題，可以把套件管理器的下載快取掛載到構建步驟中，例如 npm 的 `/root/.npm`。注意：`type=cache` 只能作為效能最佳化，不能成為構建正確性的前提。快取目錄可能被並行構建改寫，也可能被 GC 清理，所以不要把 `node_modules`、編譯產物等必須存在的內容只放在 cache mount 裡。

`BuildKit` 提供了 `RUN --mount=type=cache` 指令，可以實作上邊的設想。

```docker
# syntax=docker/dockerfile:1

FROM node:alpine as builder

WORKDIR /app

COPY package.json /app/

RUN --mount=type=cache,target=/root/.npm,id=npm_cache \
        npm install --registry=https://registry.npmmirror.com

COPY src /app/src

RUN npm run build

FROM nginx:alpine

COPY --from=builder /app/dist /app/dist
```

第一個 `RUN` 指令執行後，`id` 為 `npm_cache` 的快取資料夾掛載到了 `/root/.npm`，後續構建可複用下載快取。

第二個 `RUN` 指令執行時，`node_modules` 已經作為上一層真實寫入到 builder 階段的檔案系統中，構建不依賴快取目錄內容。

最後使用 `COPY --from=builder` 將上一階段產生的檔案複製到最終映像檔。跨階段複製構建產物應使用 `COPY --from`；如果只是臨時讀取上一階段檔案，可使用 `RUN --mount=type=bind,from=builder,source=/app/dist,target=/tmp/dist,ro`。

上面的 `Dockerfile` 中 `--mount=type=cache,...` 中指令作用如下：

|Option               |Description|
|---------------------|-----------|
|`id`                 | `id` 設定一個標誌，以便區分快取。|
|`target`（必填項）    | 快取的掛載目標資料夾。|
|`ro`,`readonly`      | 唯讀，快取資料夾不能被寫入。 |
|`sharing`            | 有 `shared` `private` `locked` 值可供選擇。`sharing` 設定當一個快取被多次使用時的表現，由於 `BuildKit` 支援並行構建，當多個步驟使用同一快取時（同一 `id`）會發生衝突。`shared` 表示多個步驟可以同時讀寫，`private` 表示當多個步驟使用同一快取時，每個步驟使用不同的快取，`locked` 表示當一個步驟完成釋放快取後，後一個步驟才能繼續使用該快取。|
|`from`               | 快取來源（構建階段），不填寫時為空資料夾。|
|`source`             | 來源的資料夾路徑。|

#### `RUN --mount=type=bind`

該指令可以將一個映像檔（或上一構建階段）的檔案掛載到指定位置。

```docker
# syntax=docker/dockerfile:1

RUN --mount=type=bind,from=php:alpine,source=/usr/local/bin/docker-php-entrypoint,target=/docker-php-entrypoint \
        cat /docker-php-entrypoint
```

#### `RUN --mount=type=tmpfs`

該指令可以將一個 `tmpfs` 檔案系統掛載到指定位置。

```docker
# syntax=docker/dockerfile:1

RUN --mount=type=tmpfs,target=/temp \
        mount | grep /temp
```

#### `RUN --mount=type=secret`

該指令可以將一個檔案（例如金鑰）掛載到指定位置。

```docker
# syntax=docker/dockerfile:1

RUN --mount=type=secret,id=aws,target=/root/.aws/credentials \
        test -s /root/.aws/credentials && echo "credentials mounted"
```
```bash
$ docker build -t test --secret id=aws,src=$HOME/.aws/credentials .
```

#### `RUN --mount=type=ssh`

該指令可以掛載 `ssh` 金鑰。

```docker
# syntax=docker/dockerfile:1

FROM alpine
RUN apk add --no-cache openssh-client
RUN mkdir -p -m 0700 ~/.ssh && ssh-keyscan gitlab.com >> ~/.ssh/known_hosts
RUN --mount=type=ssh ssh git@gitlab.com | tee /hello
```
```bash
$ eval $(ssh-agent)
$ ssh-add ~/.ssh/id_rsa
(Input your passphrase here)
$ docker build -t test --ssh default=$SSH_AUTH_SOCK .
```

### 使用 `docker compose build` 與 BuildKit

Docker Compose 同樣支援 BuildKit，這使得多服務應用的構建更加高效。

自 Docker 23 起，BuildKit 已預設啟用，無需額外設定。如果使用舊版本，可設定 `DOCKER_BUILDKIT=1` 環境變數啟用。

### 官方文件

* https://docs.docker.com/reference/dockerfile/

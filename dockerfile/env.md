## ENV 設定環境變數

### 基本語法

```docker
## 格式一：單個變數

ENV <key>=<value>

## 格式二：多個變數

ENV <key1>=<value1> <key2>=<value2> ...
```
> ⚠️ 用空格分隔的舊寫法 `ENV <key> <value>`（`ARG` 同理）雖然仍能建立，但已被官方棄用。BuildKit 的
> [LegacyKeyValueFormat](https://docs.docker.com/reference/build-checks/legacy-key-value-format/) 建立檢查會報
> `"ENV key=value" should be used instead of legacy "ENV key value" format`，`docker buildx build --check`（見 [10.2](../buildx/buildx.md)）會直接把它標出來。一律用等號。

---

### 基本用法

#### 設定單個變數

```docker
ENV NODE_VERSION=20
ENV APP_ENV=production
```

#### 設定多個變數

```docker
ENV NODE_VERSION=20 \
    APP_ENV=production \
    APP_NAME="My Application"
```
> 💡 包含空格的值用雙引號括起來。

---

### 環境變數的作用

#### 1. 後續指令中使用

```docker
ENV NODE_VERSION=20.10.0

## 在 RUN 中使用

RUN curl -fsSL https://nodejs.org/dist/v${NODE_VERSION}/node-v${NODE_VERSION}-linux-x64.tar.xz \
    | tar -xJ -C /usr/local --strip-components=1

## 在 WORKDIR 中使用

ENV APP_HOME=/app
WORKDIR $APP_HOME

## 在 COPY 中使用

COPY . $APP_HOME
```

#### 2. 容器執行期使用

```docker
ENV DATABASE_URL=postgres://localhost/mydb
```
應用程式碼中可以讀取：

```python
import os
db_url = os.environ.get('DATABASE_URL')
```
```javascript
const dbUrl = process.env.DATABASE_URL;
```
---

### 支援環境變數的指令

以下指令可以使用 `$變數名` 或 `${變數名}` 格式：

| 指令 | 範例 |
|------|------|
| `RUN` | `RUN echo $VERSION` |
| `CMD` | `CMD ["sh", "-c", "echo $HOME"]` |
| `ENTRYPOINT` | 同上 |
| `COPY` | `COPY . $APP_HOME` |
| `ADD` | `ADD app.tar.gz $APP_HOME` |
| `WORKDIR` | `WORKDIR $APP_HOME` |
| `EXPOSE` | `EXPOSE $PORT` |
| `VOLUME` | `VOLUME $DATA_DIR` |
| `USER` | `USER $USERNAME` |
| `LABEL` | `LABEL version=$VERSION` |
| `FROM` | `FROM node:$NODE_VERSION` |

> **注意**：`FROM` 是上表中的特例——它只能引用在第一條 `FROM` 之前用 `ARG` 宣告的變數，**無法**使用 `ENV` 定義的環境變數（`ENV` 要進入建立階段後才生效）。其餘指令才能引用 `ENV` 環境變數。

---

### 執行期覆寫

使用 `-e` 或 `--env` 覆寫 Dockerfile 中定義的環境變數：

```bash
## 覆寫單個變數

$ docker run -e APP_ENV=development myimage

## 覆寫多個變數

$ docker run -e APP_ENV=development -e DEBUG=true myimage

## 從環境變數檔案讀取

$ docker run --env-file .env myimage
```

#### .env 檔案格式

```bash
## .env

APP_ENV=development
DEBUG=true
DATABASE_URL=postgres://localhost/mydb
```
---

### ENV vs ARG

| 特性 | ENV | ARG |
|------|-----|-----|
| **生效時間** | 建立時 + 執行期 | 僅建立時 |
| **持久性** | 寫入映像檔，執行期可用 | 建立後消失 |
| **覆寫方式** | `docker run -e` | `docker build --build-arg` |
| **適用場景** | 應用程式設定 | 建立參數（如版本號）|

#### 組合使用

```docker
## ARG 接收建立時參數

ARG NODE_VERSION=20

## ENV 保存到執行期

ENV NODE_VERSION=$NODE_VERSION

## 後續指令使用

RUN curl -fsSL https://nodejs.org/dist/v${NODE_VERSION}/...
```
```bash
## 建立時指定版本

$ docker build --build-arg NODE_VERSION=18 -t myapp .
```
---

### 最佳實踐

#### 1. 統一管理版本號

```docker
## ✅ 好：版本集中管理

ENV NGINX_VERSION=1.30 \
    NODE_VERSION=22 \
    PYTHON_VERSION=3.12

RUN apt-get install nginx=${NGINX_VERSION}

## ❌ 差：版本分散在各處

RUN apt-get install nginx=1.30
```

#### 2. 不要儲存敏感資訊

```docker
## ❌ 錯誤：密碼寫入映像檔

ENV DB_PASSWORD=secret123

## ✅ 正確：執行期傳入

## docker run -e DB_PASSWORD=xxx myimage

...
```

#### 3. 為應用程式提供合理預設值

```docker
ENV APP_ENV=production \
    APP_PORT=8080 \
    LOG_LEVEL=info
```

#### 4. 使用有意義的變數名

```docker
## ✅ 好：清晰的命名

ENV REDIS_HOST=localhost \
    REDIS_PORT=6379

## ❌ 差：模糊的命名

ENV HOST=localhost \
    PORT=6379
```
---

### 常見問題

#### Q：環境變數在 CMD 中不展開

exec 格式不會自動執行 shell 展開，因此命令參數裡的 `$PORT` 會按字面值傳給程式；但環境變數本身仍會注入程式環境，應用程式可以透過語言執行期讀取。

```docker
## ❌ 不會展開 $PORT

CMD ["python", "app.py", "--port", "$PORT"]

## ✅ 使用 shell 格式或明確呼叫 sh

CMD ["sh", "-c", "python app.py --port $PORT"]
```

#### Q：如何查看容器的環境變數

```bash
$ docker inspect mycontainer --format '{{json .Config.Env}}'
$ docker exec mycontainer env
```

#### Q：多行 ENV 還是多個 ENV

```docker
## ✅ 建議：減少層數

ENV VAR1=value1 \
    VAR2=value2 \
    VAR3=value3

## ⚠️ 多個 ENV 會建立多層

ENV VAR1=value1
ENV VAR2=value2
ENV VAR3=value3
```
---

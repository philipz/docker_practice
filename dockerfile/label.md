## LABEL 為映像檔加入元資料

### 基本語法

```docker
LABEL <key>=<value> <key>=<value> ...
```
`LABEL` 指令以鍵值對的形式給映像檔加入元資料。這些資料不會影響映像檔的功能，但可以幫助使用者理解映像檔，或被自動化工具使用。

---

### 為什麼需要 LABEL

1. **版本管理**：記錄版本號、建立時間、Git Commit ID
2. **聯絡資訊**：維護者信箱、文件位址、支援管道
3. **自動化工具**：CI/CD 工具可以讀取標籤觸發操作
4. **許可證資訊**：聲明開源協定

---

### 基本用法

#### 定義單個標籤

```docker
LABEL version="1.0"
LABEL description="這是一個 Web 應用伺服器"
```

#### 定義多個標籤：推薦

```docker
LABEL maintainer="user@example.com" \
      version="1.2.0" \
      description="My App Description" \
      org.opencontainers.image.authors="Yeasy"
```
> 💡 包含空格的值需要用引號括起來。

---

### 常用標籤規範

為了標準和互操作性，推薦使用 [OCI Image Format Specification](https://github.com/opencontainers/image-spec/blob/main/annotations.md#pre-defined-annotation-keys) 定義的標準標籤：

| 標籤 Key | 說明 | 示例 |
|----------|------|------|
| `org.opencontainers.image.created` | 建立時間(RFC 3339) | `2024-01-01T00:00:00Z` |
| `org.opencontainers.image.authors` | 作者/維護者 | `support@example.com` |
| `org.opencontainers.image.url` | 專案主頁 | `https://example.com` |
| `org.opencontainers.image.documentation`| 文件位址 | `https://example.com/docs` |
| `org.opencontainers.image.source` | 源碼倉庫 | `https://github.com/user/repo` |
| `org.opencontainers.image.version` | 版本號 | `1.0.0` |
| `org.opencontainers.image.licenses` | 許可證 | `MIT` |
| `org.opencontainers.image.title` | 映像檔標題 | `My App` |
| `org.opencontainers.image.description` | 描述 | `Production ready web server` |

#### 示例

```docker
LABEL org.opencontainers.image.authors="yeasy" \
      org.opencontainers.image.documentation="https://yeasy.gitbook.io/docker_practice/" \
      org.opencontainers.image.source="https://github.com/yeasy/docker_practice" \
      org.opencontainers.image.licenses="MIT"
```
---

### MAINTAINER 指令：已廢棄

舊版本的 Dockerfile 中常看到 `MAINTAINER` 指令：

```docker
## ❌ 已棄用

MAINTAINER user@example.com
```
現在推薦使用 `LABEL`：

```docker
## ✅ 推薦

LABEL maintainer="user@example.com"

## 或

LABEL org.opencontainers.image.authors="user@example.com"
```
---

### 動態標籤

 配合 `ARG` 使用，可以在建立時動態注入標籤：

```docker
ARG BUILD_DATE
ARG VCS_REF

LABEL org.opencontainers.image.created=$BUILD_DATE \
      org.opencontainers.image.revision=$VCS_REF
```
建立命令：

```bash
$ docker build \
  --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') \
  --build-arg VCS_REF=$(git rev-parse --short HEAD) \
  .
```
---

### 查看標籤

#### docker inspect

查看映像檔的標籤資訊：

```bash
$ docker inspect nginx --format '{{json .Config.Labels}}' | jq
{
  "maintainer": "NGINX Docker Maintainers <docker-maint@nginx.com>"
}
```

#### 過濾器

可以使用標籤過濾映像檔：

```bash
## 列出作者是 yeasy 的所有映像檔

$ docker images --filter "label=org.opencontainers.image.authors=yeasy"

## 刪除所有帶有特定標籤的映像檔

$ docker rmi $(docker images -q --filter "label=stage=builder")
```
---

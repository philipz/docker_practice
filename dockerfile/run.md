## RUN 執行命令

### 何時使用 RUN

`RUN` 是 Dockerfile 中最常用的指令，主要用於在映像檔建立階段執行命令來修改映像檔。具體來說：

- **安裝相依**：`RUN apt-get install nginx`
- **編譯程式**：`RUN gcc -o app main.c`
- **下載檔案**：`RUN curl -O https://example.com/file.tar.gz`
- **設定系統**：`RUN mkdir -p /app/data`

理解 RUN 的核心是理解**映像檔分層**：每一個 RUN 都會在當前層之上建立新的一層，這會影響映像檔大小。因此，合理使用 RUN（特別是合併多個 RUN）是建立輕量級映像檔的關鍵。

### 基本語法

```docker
RUN <command>
RUN ["executable", "param1", "param2"]
```
`RUN` 指令是 Dockerfile 中最常用的指令之一。它在 **當前映像檔層** 之上建立一個新層，執行指定的命令，並提交結果。

---

### 兩種格式對比

#### 1. Shell 格式

```docker
RUN apt-get update
```

- **特點**：預設透過 `/bin/sh -c` 執行。
- **優勢**：可以使用環境變數、管線、重定向等 Shell 特性。
- **範例**：
  ```docker
  RUN echo "Hello" > /test.txt
  ```

#### 2. Exec 格式

```docker
RUN ["apt-get", "update"]
```

- **特點**：直接呼叫可執行檔案，不經過 Shell。
- **優勢**：避免 Shell 字串解析問題，適用於參數中包含特殊字元的情況。
- **注意**：無法使用 `$VAR` 環境變數替換（除非顯式呼叫 shell）。

---

### 常見最佳實務

#### 1. 組合命令：減少層數

每一個 `RUN` 指令都會新建一層映像檔。為了減少映像檔體積和層數，應使用 `&&` 連接命令。

**❌ 糟糕的寫法**（建立 3 層）：

```docker
RUN apt-get update
RUN apt-get install -y nginx
RUN rm -rf /var/lib/apt/lists/*
```
**✅ 推薦寫法**（建立 1 層）：

```docker
RUN apt-get update && \
    apt-get install -y nginx && \
    rm -rf /var/lib/apt/lists/*
```

#### 2. 清理快取

在安裝完軟體後，立即清除快取，可以顯著減小映像檔體積。

- **Debian/Ubuntu**:
  ```docker
  RUN apt-get update && apt-get install -y package-bar \
      && rm -rf /var/lib/apt/lists/*
  ```

- **Alpine**:
  ```docker
  RUN apk add --no-cache package-bar
  ```

#### 3. 使用 `set -e` 和 `pipefail`

預設情況下，管線命令 `cmd1 | cmd2` 的回傳值由最後一個命令 (`cmd2`) 決定，即使前面的命令失敗了，整個 `RUN` 仍可能視為成功。

**❌ 隱蔽的錯誤**：

```docker
## 如果下載失敗，gzip 可能會報錯，但如果不影響後續，建立可能繼續

RUN wget http://error-url | gzip -d > file
```
**✅ 推薦寫法**：

```docker
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN wget http://url | gzip -d > file
```
---

### 常見問題

#### Q：為什麼 `RUN cd /app` 不生效？

```docker
RUN cd /app
RUN touch hello.txt
```
**結果**：`hello.txt` 會出現在根目錄 `/`，而不是 `/app`。**原因**：每個 `RUN` 都在一個新的 Shell/容器環境中執行。`cd` 只影響當前 `RUN` 的環境。**解決**：使用 `WORKDIR` 指令。

```docker
WORKDIR /app
RUN touch hello.txt
```

#### Q：環境變數不生效？

```docker
RUN export MY_VAR=hello
RUN echo $MY_VAR
```
**結果**：輸出為空。**原因**：同上，環境變數只在當前 `RUN` 有效。**解決**：使用 `ENV` 指令，或在同一行 `RUN` 中匯出。

```docker
ENV MY_VAR=hello
RUN echo $MY_VAR
```
---

### 進階技巧

#### 1. 使用 BuildKit 的掛載快取

BuildKit 支援在 `RUN` 指令中使用 `--mount` 掛載快取，加速建立。

```docker
## 快取 apt 套件

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y gcc
```
```docker
## 快取 Go 模組

RUN --mount=type=cache,target=/go/pkg/mod \
    go build -o app
```

#### 2. 掛載金鑰

安全地使用 SSH 金鑰或 Token，而不將其記錄在映像檔中。

```docker
RUN --mount=type=secret,id=mysecret \
    my-private-tool --token-file /run/secrets/mysecret
```

不要在建立命令中 `cat`、`echo` 或列印金鑰內容；應把 `/run/secrets/<id>` 路徑交給真正消費金鑰的工具。

#### 3. Heredoc 語法

BuildKit 支援使用 heredoc 語法編寫多行腳本，無需行末反斜線 `\` 連接：

```docker
RUN <<EOF
apt-get update
apt-get install -y \
  build-essential \
  curl \
  git
rm -rf /var/lib/apt/lists/*
EOF
```

優勢：

- 可讀性更強，不需要在每行末尾新增 `\`
- 避免在腳本中轉義引號
- 支援多個 heredoc 區塊，可指定不同的 Shell

```docker
RUN <<EOF
echo "使用預設 /bin/sh"
EOF

RUN <<'EOF'
#!/bin/bash
set -euo pipefail
echo "使用 bash"
wget http://example.com/file.tar.gz
EOF
```

> 使用 heredoc 需要在 Dockerfile 首行宣告 BuildKit 語法版本：`# syntax=docker/dockerfile:1`

---

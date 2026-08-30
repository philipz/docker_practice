## 快速上手

> **版本說明**：本節範例基於 Docker v29.x 編寫。範例中使用的 `nginx:alpine` 映像檔標籤為演示用途，請查閱 [Docker Hub - nginx](https://hub.docker.com/_/nginx) 確認最新可用版本。

開始前請先完成 [第 3 章安裝 Docker](../install/README.md)，並確認 `docker version` 與 `docker run hello-world` 可以正常執行。若你只是先瀏覽流程，可以讀完本節後再回到安裝章實踐。

本節將透過一個簡單的 Web 應用範例，帶你快速體驗 Docker 的核心流程：建立映像檔、執行容器。

### 為什麼選擇 Nginx + HTML 作為入門範例？

在學習 Docker 之前，我們先來理解為什麼這個範例適合初學者。Docker 的核心價值在於**一致性交付**：在相同映像檔、CPU 架構、核心能力、設定和外部相依都滿足的前提下，應用行為可以保持高度一致。這個 Nginx + 靜態 HTML 的範例之所以被廣泛採用，是因為它展現了 Docker 工作流的三個核心階段：

1. **映像檔定義（Image Layer）**：透過 Dockerfile 描述如何把應用打包成一個自包含的單元
2. **映像檔建立（Build）**：執行 `docker build`，Docker 根據 Dockerfile 逐層建立映像檔
3. **容器執行（Runtime）**：透過 `docker run` 啟動容器實例，應用真正開始提供服務

Nginx 是一個輕量級、使用廣泛的 Web 伺服器，學習完這個範例後，你可以輕鬆擴展到部署 Node.js、Python、Go 等任何語言的應用。

### 準備程式碼

建立一個名為 `hello-docker` 的資料夾，並在其中建立一個 `index.html` 檔案：

```html
<h1>Hello, Docker!</h1>
```

### 編寫 Dockerfile

在同級目錄下建立一個名為 `Dockerfile`（無副檔名）的檔案：

```dockerfile
FROM nginx:alpine
COPY index.html /usr/share/nginx/html/index.html
```

### 建立映像檔

開啟終端機，進入該目錄，執行建立命令：

```bash
$ docker build -t my-hello-world .
```

* `docker build`：建立命令
* `-t my-hello-world`：給映像檔起個名字（標籤）
* `.`：指定上下文路徑為目前目錄

### 執行容器

使用剛才建立的映像檔啟動一個容器：

```bash
$ docker run -d -p 8080:80 my-hello-world
```

* `docker run`：執行命令
* `-d`：背景執行
* `-p 8080:80`：將宿主機的 8080 埠號映射到容器的 80 埠號

### 存取測試

開啟瀏覽器存取 [http://localhost:8080](http://localhost:8080)，你應該能看到「Hello, Docker!」。

### 清理

停止並刪除容器：

```bash
# 查看正在執行的容器 ID

$ docker ps

# 停止容器

$ docker stop <CONTAINER_ID>

# 刪除容器

$ docker rm <CONTAINER_ID>
```
恭喜！你已經完成了第一次 Docker 實戰。接下來請閱讀 [Docker 基本概念](../basic_concept/README.md)做深入了解。

## 參考文件

### 官方文件

* `Dockerfile` 官方參考手冊：https://docs.docker.com/reference/dockerfile/

* `Dockerfile` 最佳實踐指南：https://docs.docker.com/build/building/best-practices/

* `Docker` 官方映像檔 `Dockerfile` 庫：https://github.com/docker-library/docs

### 常用指令總結

Dockerfile 中的常用指令包括：

- **FROM**: 指定基礎映像檔，必須是第一條建立指令（只有全域 `ARG`、註解和 parser 指令可以在它之前）
- **RUN**: 在映像檔中執行命令，用於安裝軟體套件等
- **COPY**: 複製檔案到映像檔中
- **ADD**: 更進階的複製檔案（支援 URL 和自動解壓縮）
- **CMD**: 容器預設執行的命令
- **ENTRYPOINT**: 容器啟動時的進入點
- **ENV**: 設定環境變數
- **ARG**: 建立時的參數變數
- **VOLUME**: 定義匿名卷掛載點
- **EXPOSE**: 宣告容器監聽的埠號
- **WORKDIR**: 設定工作目錄
- **USER**: 指定執行容器時的使用者
- **HEALTHCHECK**: 設定容器健康檢查
- **ONBUILD**: 設定觸發器指令，在子映像檔建立時執行
- **LABEL**: 為映像檔新增中繼資料標籤
- **SHELL**: 指定 RUN 等指令使用的 shell

### 最佳實踐建議

1. 使用具體的基礎映像檔版本標籤而非 latest
2. 最小化映像檔層數，合併 RUN 指令
3. 使用 .dockerignore 檔案排除不必要的檔案
4. 安裝必要的軟體套件後清理快取
5. 使用多階段建立減小最終映像檔體積
6. 避免以 root 身分執行容器應用

### 相關資源

- Docker 官方映像檔庫：https://hub.docker.com/
- Docker 映像檔建立最佳實踐：https://docs.docker.com/build/building/best-practices/

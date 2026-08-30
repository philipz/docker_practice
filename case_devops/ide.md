## 在 IDE 中使用 Docker

使用 IDE 進行開發，往往要求本地安裝好工具鏈。一些 IDE 支援 Docker 容器中的工具鏈，這樣充分利用了 Docker 的優點，而無需在本地安裝。

本節關注一個核心目標：**把「開發依賴」放進容器，把「原始碼編輯體驗」留在本地 IDE**。

### 適用場景

* 團隊希望統一開發環境（Go/Node/Python 版本、系統依賴、編譯鏈）。
* 本地系統不方便安裝依賴（例如 Windows、公司管控環境）。
* 專案依賴較重（例如需要 `gcc`、資料庫客戶端、特定系統庫）。

不太適合的場景：強依賴本機 GPU/USB 設備、或需要非常低延遲檔案 IO 的工程（此時可能需要額外調優掛載/同步策略）。

### 最小可用模式：docker compose + 開發容器

下面用一個「長期執行的開發容器」作為例子（以 Go 為例，你可以替換為 Node/Python）。

1. 在專案中建立 `compose.yaml`（或複用你已有的 compose 檔案）：

   ```yaml
   services:
     dev:
       image: golang:1.26
       working_dir: /work
       volumes:
         - ./:/work
       command: sleep infinity
   ```

1. 啟動開發容器：

   ```bash
   docker compose up -d
   ```

1. 進入容器安裝依賴/執行命令：

   ```bash
   docker compose exec dev bash
   go version
   go test ./...
   ```

這個模式的優點是「簡單直接、IDE 無關」，缺點是 IDE 需要額外設定
（例如設定遠端直譯器/語言服務，或使用 VS Code Dev Containers）。

### 目錄掛載與權限建議

* Linux 下如果遇到容器內寫檔案權限問題，優先確保容器內使用者與宿主機 UID/GID 對齊。
  VS Code Dev Containers 支援自動處理；手寫 Dockerfile/compose 時也可以明確設定使用者。

* 如果遇到檔案變更監聽不生效（常見於 macOS/Windows 的虛擬化檔案系統），
  優先使用語言/工具支援的輪詢模式或提高 watcher 限制。

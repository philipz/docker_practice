## Drone Demo

### Demo 專案說明

這是一個基於 Go 語言編寫的簡單 Web 應用示例，用於演示 Drone CI 的持續整合流程。

### 目錄結構

* `drone_demo.app.go`：簡單的 Go Web 伺服器程式碼。
* `drone_demo.drone.yml`：Drone CI 的設定檔案，定義了建立和測試流程。

### 如何使用

1. 確保本地已安裝 Docker 環境。
2. 將示例檔案重新命名為 Drone 期望的檔案名稱：

   ```bash
   cp drone_demo.app.go app.go
   cp drone_demo.drone.yml .drone.yml
   ```

3. 將 `app.go` 與 `.drone.yml` 推送到你的 `drone-demo` 倉庫，即可在 Drone 中看到建立結果。

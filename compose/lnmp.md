## 實戰 LNMP

### 什麼是 LNMP

LNMP 是一個經典的 Web 應用棧，由以下四個開源軟體組合而成：

- **L**：Linux（作業系統）
- **N**：Nginx（Web 伺服器）
- **M**：MySQL（資料庫伺服器）
- **P**：PHP（腳本語言）

這個組合被廣泛用於建立高效能的 Web 應用。

### 使用 Docker Compose 部署 LNMP

本專案的維護者 [khs1994](https://github.com/khs1994) 的開源專案 [khs1994-docker/lnmp](https://github.com/khs1994-docker/lnmp) 使用 Docker Compose 搭建了一套完整的 LNMP 環境。

### 參考專案

該專案中包含的服務：

- **Nginx**：Web 伺服器，用於處理 HTTP 請求
- **MySQL/MariaDB**：關聯式資料庫服務
- **PHP-FPM**：PHP 處理器，與 Nginx 透過 Fast CGI 協定通訊
- **Redis**：可選的記憶體快取服務（用於會話或快取）

### 學習資源

各位開發者可以參考該專案在以下場景中執行 LNMP：

- Docker 容器化部署
- Kubernetes 集群編排
- 開發環境快速搭建
- 生產環境設定參考

專案位址：[khs1994-docker/lnmp](https://github.com/khs1994-docker/lnmp)

透過該專案，你可以學習到如何使用 Docker Compose 定義多個相互關聯的服務，以及如何在容器化環境中管理應用的生命週期。

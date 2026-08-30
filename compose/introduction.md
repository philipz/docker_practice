## 簡介

`Compose` 專案是 Docker 官方的開源專案，負責實作對 Docker 容器的快速編排。從功能上看，跟 `OpenStack` 中的 `Heat` 十分類似。

其程式碼目前在 [docker/compose 倉庫](https://github.com/docker/compose) 上開源。

`Compose` 定位是 「定義和執行多個 Docker 容器的應用 (Defining and running multi-container Docker applications)」，其前身是開源專案 Fig。

透過第一部分中的介紹，我們知道使用一個 `Dockerfile` 模板檔案，可以讓使用者很方便的定義一個單獨的應用容器。然而，在日常工作中，經常會碰到需要多個容器相互配合來完成某項任務的情況。例如要實作一個 Web 專案，除了 Web 服務容器本身，往往還需要再加上後端的資料庫服務容器，甚至還包括負載均衡容器等。

`Compose` 恰好滿足了這樣的需求。它允許使用者透過一個單獨的 `compose.yaml`（歷史預設名也常見為 `docker-compose.yml`）模板檔案（YAML 格式）來定義一組相關聯的應用容器為一個專案 (project)。

### 概述

Docker Compose 讓使用者能夠以宣告式方式定義和管理多容器應用。它的核心價值在於：用一個 YAML 檔案取代一連串手動的 `docker run` 命令，使得複雜應用的啟動、停止和重建變得一鍵可達。

對於開發團隊而言，Compose 解決了三個關鍵問題：環境一致性（「在我機器上能跑」的問題）、服務依賴管理（確保資料庫在應用之前啟動）、以及開發-測試-生產的設定差異管理（透過 `compose.override.yaml` 實作多環境適配）。

### 模板檔案規範

Compose 模板檔案採用 YAML 格式，擴展名為 `.yml` 或 `.yaml`。

> **注意**：Compose Specification 的頂層 `version` 欄位僅用於向後相容，目前已被標記為 obsolete。新檔案建議直接省略該欄位。

Docker Compose 預設使用 `compose.yaml`，也相容 `compose.yml`、`docker-compose.yaml`、`docker-compose.yml` 等檔案名。

`Compose` 中有兩個重要的概念：

* 服務 (`service`)：一個應用的容器，實際上可以包括若干執行相同映像檔的容器實例。

* 專案 (`project`)：由一組相關聯的應用容器組成的一個完整業務單元，在 Compose 檔案中定義。

`Compose` 的預設管理物件是專案，透過子命令對專案中的一組容器進行便捷地生命週期管理。

`Compose` 專案早期由 Python 編寫，稱為 Docker Compose V1。

現在的 Docker Compose V2 是一個 Go 語言編寫的 Docker CLI 外掛（目前版本號已演進至 v5.x 系列，以避免與舊 Compose 檔案格式版本混淆）。Docker Desktop 預設包含它；在 Linux 上，也可以將它作為獨立的 CLI 外掛安裝後直接透過 `docker compose` 命令使用。它提供了更快的效能和更好的整合體驗。

只要所操作的平台支援 Docker API，就可以在其上利用 `Compose` 來進行編排管理。

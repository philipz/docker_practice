# 第十一章 Docker Compose

`Docker Compose` 是 Docker 官方編排 (Orchestration) 專案之一，負責快速定義和啟動本地或單機多容器應用。跨主機集群編排應交給 Swarm、Kubernetes 或雲廠商託管服務。

> ⚠️ **重要提示：Compose V1 已停止支援**
>
> 早期基於 Python 編寫的 Compose V1（命令為 `docker-compose`）已於 2023 年中正式停止支援。現已全面升級為基於 Go 編寫的 Compose V2，作為 Docker CLI 的官方外掛提供（命令為 `docker compose`，中間為空格）。本書強烈推薦且後續章節均以 V2 為核心標準進行講解。

## Docker Compose 解決什麼問題？

在學習 Compose 之前，筆者想強調它的真正價值。假設你正在開發一個微服務應用——前端、後端、資料庫三個服務。如果你用 Docker 容器分別執行它們，你會遇到這些問題：

1. **啟動順序**：需要先啟動資料庫，再啟動後端，最後啟動前端
2. **網路連線**：三個容器需要能彼此通訊
3. **卷掛載**：本地程式碼需要映射到容器內
4. **環境變數**：每個服務的設定需要逐個設定

使用 `docker run` 逐個啟動的話，需要記住 3 條複雜的命令。而 **Docker Compose 的核心價值就是用一個 YAML 檔案來定義整個應用**，然後一條命令 `docker compose up` 啟動所有服務。這是 Compose 被廣泛採用的原因——它極大地簡化了本地開發和測試的複雜性。

**誰應該學 Compose？** 任何使用 Docker 進行本地開發的人，以及需要快速部署多容器應用的團隊。

## 本章內容

本章將介紹 `Compose` 專案情況以及安裝和使用。

* [簡介](introduction.md)
* [安裝與移除](install.md)
* [使用](usage.md)
* [命令說明](commands.md)
* [Compose 模板檔案](compose_file.md)
* [實戰 Django](django.md)
* [實戰 Rails](rails.md)
* [實戰 WordPress](wordpress.md)
* [實戰 LNMP](lnmp.md)

## 本章小結

Docker Compose 是管理多容器應用的利器，透過 YAML 檔案宣告式地定義服務、網路和資料卷。

| 概念 | 要點 |
|------|------|
| **核心概念** | 服務 (service) 和專案 (project) |
| **設定檔案** | `compose.yaml`（推薦）或 `docker-compose.yml` |
| **版本** | Compose V2 為 Go 編寫的 CLI 外掛，透過 `docker compose` 使用 |
| **啟動** | `docker compose up -d` 啟動所有服務 |
| **停止** | `docker compose down` 停止並移除容器 |
| **查看狀態** | `docker compose ps` 查看服務狀態 |
| **查看日誌** | `docker compose logs` 查看服務日誌 |
| **模板檔案** | 支援 `services`、`networks`、`volumes` 等頂層設定 |

### 延伸閱讀

- [Compose 模板檔案](compose_file.md)：詳細模板語法參考
- [Compose 命令說明](commands.md)：完整命令列表
- [網路設定](../network/README.md)：Docker 網路基礎
- [資料管理](../data_management/README.md)：資料卷管理

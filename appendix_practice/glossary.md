# 術語表

本附錄整理了本書中常見的一些專業術語及其解釋。

## A

* **Alpine**：一個輕量級的 Linux 發行版，常作為基礎映像檔用於建立體積較小的 Docker 映像檔。
* **API (Application Programming Interface)**：應用程式程式設計介面，Docker Daemon 提供 RESTful API 供客戶端或外部程式與之互動。

## B

* **Base Image（基礎映像檔）**：沒有父映像檔的映像檔，通常是作業系統的最小安裝集合（如 `ubuntu` 或 `alpine`）。
* **BuildKit**：Docker 下一代的建立引擎，提供了更高的建立效能、更好的快取處理和並發建立支援。
* **Buildx**：Docker CLI 的一個外掛程式，擴充了建立功能，支援 BuildKit 的所有高級特性，例如多系統架構映像檔建立。

## C

* **Cgroups (Control Groups)**：控制組，Linux 核心特性，用於限制、記錄、隔離程式群組使用的物理資源（如 CPU、記憶體、磁碟 I/O 等）。
* **Cluster（集群）**：一組協同工作的節點（如主機、虛擬機器等），在容器領域常指 Kubernetes 集群。
* **Compose (Docker Compose)**：用於定義和執行多容器 Docker 應用程式的工具，透過 YAML 檔案設定應用服務。
* **Container（容器）**：映像檔的執行實例，帶有額外的可寫檔案層，具有獨立性。
* **Containerd**：行業標準的容器執行時期，核心功能是管理宿主機上容器的生命週期（建立、啟動、停止、銷毀）。

## D

* **Daemon（守護程式）**：Docker 的背景守護程式，負責接收和處理 Docker API 請求，並管理映像檔、容器、網路和資料卷等物件。
* **Docker**：開源的應用容器引擎，讓開發者可以打包應用程式及其相依套件到一個可移植的容器中，然後發布到任何流行的 Linux 或 Windows 機器上。
* **Docker Desktop**：包含 Docker Engine、Docker CLI 客戶端、Docker Compose 和 Kubernetes 等的桌面應用程式，適用於 macOS 和 Windows。
* **Docker Hub**：Docker 官方的公共映像檔倉庫服務，提供容器映像檔的儲存和分發。
* **Dockerfile**：包含用於組合映像檔的命令的文字檔案，Docker 透過讀取 `Dockerfile` 中的指令即可自動完成映像檔建立。

## E

* **Etcd**：一個高可用、強一致性的分散式鍵值儲存系統，常用於容器集群（如 Kubernetes）的服務發現和狀態設定管理。

## I

* **Image（映像檔）**：Docker 映像檔是一個唯讀模板，帶有建立 Docker 容器的說明。

## K

* **Kubernetes (K8s)**：開源的容器編排引擎，用於自動化容器化應用程式的部署、擴充和管理。

## L

* **Layer（映像檔層）**：Docker 映像檔由多個唯讀層疊合而成，每一層通常代表 Dockerfile 中的一條指令的操作結果，透過聯合檔案系統（UFS）疊加在一起形成完整的檔案系統。

## M

* **Multistage Build（多階段建立）**：Dockerfile 中的特性，允許在同一個 Dockerfile 中使用多個 `FROM` 敘述，從一個階段複製所需的建立產物到另一個階段，從而大幅減小最終映像檔的體積。

## N

* **Namespace（命名空間）**：Linux 核心特性，用於隔離各種系統資源，如程式、網路、掛載點等，使容器看起來就像是一個獨立的作業系統。
* **Node（節點）**：容器集群（如 Kubernetes）中的一台工作機器，可以是物理機或虛擬機器。

## O

* **OCI (Open Container Initiative)**：開放容器規範，由多家行業領頭企業共同制定的容器執行時期和映像檔格式的行業標準。
* **Orchestration（編排）**：自動化部署、管理、擴充和網路設定容器的系統和技術（如 Kubernetes）。

## P

* **Pod**：Kubernetes 中最小的、可部署的計算單元，包含一個或多個緊密相關的容器，共享相同的網路命名空間和儲存。
* **Prometheus**：開源的系統監控和告警工具包，廣泛應用於雲原生的監控體系中。

## R

* **Registry（註冊伺服器）**：提供 Docker 映像檔下載和上傳等儲存分發服務的伺服器。
* **Repository（倉庫）**：集中存放某個應用的所有映像檔的地方，通常由映像檔名定義。一個 Registry 中可以包含多個 Repository。

## S

* **Swarm (Docker Swarm)**：Docker 原生的集群和編排管理工具，可將多個 Docker 主機組合成一個統一的虛擬 Docker 主機池。維護節點時通常將節點可用性設為 `Drain`，這隻影響 Swarm service 排程，不會停止該節點上獨立執行的容器。

## U

* **UFS (Union File System)**：聯合檔案系統，一種分層、輕量級並且高效的檔案系統，它支援對檔案系統的修改一層層疊加。

## V

* **Volume（資料卷）**：專為繞過聯合檔案系統而設計的特殊目錄，用於實現容器資料的持久化，或在多個容器之間提供檔案共享。

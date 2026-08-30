## 17.6 containerd - 核心容器執行時期

> **版本說明**：containerd 和 nerdctl 保持活躍的發佈週期。建議查閱 [containerd 官方文件](https://containerd.io/) 和 [nerdctl GitHub Releases](https://github.com/containerd/nerdctl/releases) 取得最新版本資訊。

本節介紹 containerd，它是現代容器技術棧中最為核心的基礎元件之一。了解 containerd 有助於更深入地理解 Docker 和 Kubernetes 的底層運行機制。

### 17.6.1 containerd 簡介

[containerd](https://containerd.io/) 是一個行業標準的容器執行時期，它最初是由 Docker 引擎中剝離出來的一個核心元件，後來 Docker 將其捐贈給了雲原生計算基金會（CNCF），目前已經是一個 CNCF 畢業（Graduated）專案。

它的主要職責是管理單個宿主機上完整的容器生命週期，包括：

- 映像檔的傳輸和儲存
- 容器執行和管理
- 儲存和網路介面的管理

簡單來說，當你在使用 Docker 或者 Kubernetes 時，真正去底層呼叫作業系統介面（如 Linux 的 Namespace 和 Cgroups）來啟動和管理容器程式的，往往是 containerd（及它所呼叫的 runc 元件）。

### 17.6.2 與 Docker 和 Kubernetes 的關係

> **版本說明**：本章節涉及 containerd、Docker 和 Kubernetes 的多個版本。建議查閱官方文件了解最新的相容性資訊。

理解 containerd，首先要釐清它與使用者日常操作的 Docker 以及 Kubernetes 的關係。

#### Docker 的架構

在早期，Docker 引擎是一個包含了所有功能的單體架構。隨著技術的發展和標準化要求，Docker 將底層關於容器執行時期的部分解耦出來，形成了 `containerd` 和 `runc`。

當你執行一個 `docker run` 命令時，呼叫鏈路大致如下：

1. Docker Client 發送請求給 Docker Daemon（`dockerd`）。
2. `dockerd` 將請求轉發給 `containerd`。
3. `containerd` 準備好映像檔和容器的必要環境，然後呼叫 `runc`。
4. `runc` 負責按照 OCI（Open Container Initiative）標準，拉起並運行真正的容器程式。

因此，Docker 現在實際上是建立在 containerd 之上的一個包含更多開發者友好特性（如建立映像檔、Compose 管理等）的增強平台。

#### Kubernetes 與 CRI

Kubernetes 作為一個容器編排系統，為了遮蔽底層不同容器執行時期的實現差異，引入了 CRI（Container Runtime Interface）標準。

- 早期版本中，Kubernetes 預設使用 docker 作為執行時期，通過一個名為 `dockershim` 的橋接元件對接 Docker，Docker 再對接 containerd。
- 隨著 containerd 原生支持了 CRI 外掛程式，Kubernetes 開始直接與 containerd 通訊，去掉了 `dockershim` 和 `dockerd` 的中間層。這就是為什麼從 Kubernetes 1.24+ 開始“棄用 Docker”引發了廣泛關注，實際上 Kubernetes 只是棄用 `dockershim`，底層可以使用 containerd、CRI-O 等符合 CRI 的執行時期。參見 [Kubernetes 官方文件](https://kubernetes.io/docs/setup/production-environment/container-runtimes/)。
- containerd 2.0+ 移除了已棄用的 CRI v1alpha2 介面，僅保留 CRI v1（Kubernetes 1.26+ 僅支持 CRI v1）。如果集群中仍有依賴 CRI v1alpha2 的元件，升級 containerd 2.x 前需先完成遷移。containerd 2.x 系列中 2.0 和 2.3 均為 LTS 版本，其中 2.3 支持從 1.7 LTS 直接升級，生產環境推薦使用。詳見 [containerd 發佈說明](https://github.com/containerd/containerd/releases)。

### 17.6.3 為什麼直接使用 containerd？

對普通應用開發者來說，Docker 依然是本地開發和測試的首選。但對於建立雲平台、自動化流水線或深度管理 Kubernetes 集群的系統工程師來說，直接使用 containerd 可以帶來：

- **更高的效能與更少的開銷**：去掉了 Docker Daemon 等附加元件的資源佔用，鏈路更短。
- **更強的穩定性**：作為專注於執行時期的底層元件，它的核心功能極為穩定且更新受控。
- **直接符合 Kubernetes CRI 標準**：在生產級 Kubernetes 集群中作為標準設定。

### 17.6.4 基礎用法與工具介紹

不同於 `docker` 命令列工具，containerd 提供了不同的客戶端來滿足不同的使用場景：

- **ctr**：containerd 自帶的偵錯用客戶端。它功能比較基礎，主要用於開發者在開發 containerd 時進行快速偵錯，一般不作為最終使用者的日常管理工具。
- **crictl**：Kubernetes 提供的 CRI 命令列工具。它用於排查 Kubernetes 節點上的容器和沙箱（Pod）問題。
- **nerdctl**：這是一個由 containerd 專案維護者開發的，完全相容 Docker CLI 體驗的 containerd 命令列客戶端。對於習慣了 `docker run/ps/build` 命令的使用者來說，`nerdctl` 可以作為直接操作 containerd 的理想替代品，並且它還支持直接建立映像檔（依賴 BuildKit）。

#### nerdctl 使用示例

安裝完 containerd 和 nerdctl 後，你可以體驗到幾乎與 Docker 完全一致的命令列：

```bash
# 啟動一個 nginx 容器
$ nerdctl run -d -p 8080:80 --name my-nginx nginx:alpine

# 查看運行中的容器
$ nerdctl ps

# 查看本地映像檔
$ nerdctl images
```
對於那些希望在生產伺服器上剝離 Docker 龐大體積，但又想要保留類似 Docker 方便的命令列體驗的使用者，`containerd` + `nerdctl` 是一個極佳的組合。

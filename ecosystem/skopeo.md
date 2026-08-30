## 17.5 Skopeo - 容器映像檔管理工具

> **版本說明**：Skopeo 與 Podman、Buildah 同屬 `podman-container-tools` 專案生態。建議存取 [Skopeo 官方倉庫](https://github.com/podman-container-tools/skopeo) 和 [GitHub Releases](https://github.com/podman-container-tools/skopeo/releases) 取得最新版本資訊。

本節介紹 Skopeo，包括其基礎概念、應用場景以及基本指令。

### 17.5.1 Skopeo 簡介

Skopeo 是一個由 Red Hat 贊助開源的命令列工具，它可以在不需要運行容器常駐程式（如 Docker Daemon）的前提下，對容器映像檔進行極其高效的操作和管理，包括：檢查、複製、刪除和簽章等操作。

Skopeo 最大的特點是其可以在“不將映像檔拉取到本地”的情況下，直接在遠端 Registry（映像檔倉庫）之間完成檢查和搬運，從而大幅度節省頻寬和磁碟空間。這也是它在容器維運和分發領域非常受歡迎的原因。

### 17.5.2 核心特性

- **遠端巡檢**：通過 `skopeo inspect` 可以查看遠端倉庫中映像檔的中繼資料（例如包含哪些層、環境變數資訊、入口命令等），而完全無需拉取該映像檔。
- **映像檔複製與同步**：支持各種格式之間的相互傳輸，如在不同的容器倉庫之間、或者從倉庫拉取到本地的目錄、或者儲存為 OCI 佈局結構等。
- **映像檔刪除**：可以遠端刪除倉庫中的映像檔（需要擁有權限）。
- **簽章驗證**：支持在分發映像檔前進行數位簽章以保障安全性。

### 17.5.3 安裝 Skopeo

類似於 Buildah，Skopeo 也直接包含在大部分主流的 Linux 源中。

在 Fedora/CentOS/RHEL 等發行版中：

```bash
$ sudo dnf install -y skopeo
```
在 Ubuntu/Debian 中：

```bash
$ sudo apt-get update
$ sudo apt-get -y install skopeo
```
如果是 macOS 環境，可以通過 Homebrew 安裝：

```bash
$ brew install skopeo
```

### 17.5.4 基礎用法示例

#### 1. 遠端檢查映像檔

有時候我們只想知道遠端映像檔的詳細資訊，並不想拉取它。下面是檢查 Docker Hub 上的 Alpine 映像檔的例子：

```bash
$ skopeo inspect docker://docker.io/library/alpine:latest
```
這個命令會回傳一段 JSON 格式的資料，其中包含了諸如映像檔摘要（Digest）、建立時間、架構（Architecture）、標籤（Tags）等豐富資訊。在自動化的工具和系統審查環境中，這是一個不可或缺的利器。

#### 2. 同步與複製映像檔

`skopeo copy` 是使用最為廣泛的命令。它可以在不同的倉庫、不同的格式之間無縫搬運映像檔。

例如，從一個公共倉庫直接搬運映像檔到一個私有企業倉庫（無需將其先 `docker pull` 到本地，再 `docker push`）：

```bash
$ skopeo copy docker://docker.io/library/alpine:latest docker://registry.example.com/library/alpine:latest
```
又或者，你可以將遠端映像檔拉取到本地，只為了檢查其拆解後的格式，比如將映像檔解壓到本地某個目錄下以 OCI 規範存放：

```bash
$ skopeo copy docker://docker.io/library/alpine:latest oci:alpine-oci
```
如果我們要將本地的某個目錄下的打包好的映像檔再次推向 Registry 或轉換為其他儲存類型也是完全支持的，諸如：

- `docker://` 遠端 Registry
- `docker-archive:` / `docker-daemon:` Docker 對應的歸檔檔案或本地常駐程式
- `oci:` / `oci-archive:` OCI 相關檔案格式
- `dir:` 本地純目錄

#### 3. 校驗機制與安全

如果你不信任公開倉庫上的映像檔，或是需要通過特定的 TLS 憑證和鑑權，Skopeo 的功能也是能很好的支持的，比如它可以直接傳遞諸如 `--src-creds` 或 `--dest-tls-verify=false` 等參數，這在進行網路隔離的複雜映像檔搬運操作中常常會用到。

對於複雜的容器環境或那些純粹用於映像檔資產管理的節點來說，Skopeo 提供了一個直接而強大的資料“搬運工”。

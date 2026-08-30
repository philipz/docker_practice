## 17.4 Buildah - 容器映像檔建立工具

> **版本說明**：Buildah 與 Podman 和 Skopeo 共同維護。建議查閱 [Buildah 官方文件](https://buildah.io/) 和 [GitHub Releases](https://github.com/podman-container-tools/buildah/releases) 了解最新版本。

本節介紹 Buildah，包括其基礎概念、應用場景以及基本指令。

### 17.4.1 Buildah 簡介

Buildah 是一個用於建立 OCI（Open Container Initiative）相容格式容器映像檔的開源命令列工具。與 Docker 需要一直運行的常駐程式（daemon）不同，Buildah 的設計初衷是無需常駐程式（daemonless）即可工作，並且也不強制要求 root 權限（rootless）。這使得在持續整合/持續部署（CI/CD）環境中建立映像檔時能夠更加輕量且安全。

Buildah 由 Red Hat 主導開發，通常和 Podman、Skopeo 一起使用，被認為是建立、運行和管理容器的一套現代化工具鏈。在很多需要增強安全性和無需依賴常駐程式的場景中，Buildah 是 `docker build` 命令的最佳替代方案。

### 17.4.2 核心特性

- **無常駐程式（Daemonless）**：Buildah 直接通過系統呼叫拉取、建立和推送映像檔，減少了單點故障的風險和資源開銷。
- **建立效率高**：可以掛載映像檔的根檔案系統到本地，並直接利用宿主機的工具對其進行操作，非常靈活。
- **相容性**：不僅支持處理傳統的 Dockerfile，還能完全相容 OCI（Open Container Initiative）標準和 Docker 格式。
- **與 Podman 整合**：Podman 自身建立映像檔的命令 `podman build` 底層實際上也是依賴 Buildah 庫來實現的。

### 17.4.3 安裝 Buildah

在許多主流的 Linux 發行版中都可以通過套件管理器直接安裝 Buildah。

以 Fedora/CentOS/RHEL 為例：

```bash
$ sudo dnf install -y buildah
```
以 Ubuntu/Debian 為例（需引入官方源後）：

```bash
$ sudo apt-get update
$ sudo apt-get -y install buildah
```

### 17.4.4 基礎用法示例

#### 1. 從現有的 Dockerfile 建立映像檔

Buildah 最常見的用法就是像 Docker 一樣根據 `Dockerfile` 來建立映像檔，可以直接使用 `buildah bud`（或者 `buildah build-using-dockerfile`）命令：

```bash
$ buildah bud -t my-app:latest .
```
可以看到在這點上，它與 `docker build` 的體驗完全一致。

#### 2. 互動式從空映像檔開始建立

除了使用 Dockerfile，Buildah 最強大的功能來自於它的互動式和腳本化建立機制。我們可以從一個極簡的映像檔（或基礎映像檔）開始建立：

```bash
# 取得一個基礎映像檔
$ container=$(buildah from alpine:latest)

# 取得掛載點，並查看其路徑
$ mnt=$(buildah mount $container)
$ echo $mnt
/var/lib/containers/storage/overlay/xxx/merged

# 利用宿主機直接建立檔案，而不需要在容器內部運行命令
$ echo "Hello Buildah" > $mnt/hello.txt

# 加入一些設定和命令
$ buildah config --cmd "cat /hello.txt" $container

# 將容器提交為映像檔
$ buildah commit $container my-hello-image:latest

# 建立完成後可以卸載並清理容器上下文
$ buildah unmount $container
$ buildah rm $container
```
這種模式在自動化流水線中極為有用，因為我們可以將上述過程編寫成標準的 bash 腳本，無需為了建立映像檔而撰寫只在其獨立語法中運行的 Dockerfile 指令。

#### 3. 查看和推送映像檔

通過 `buildah images` 可以查看目前環境中的映像檔。推送映像檔到外部 Registry 也十分安全方便：

```bash
# 查看本地建立的映像檔
$ buildah images

# 推送映像檔到 Docker Hub（注意需要先登入）
$ buildah push my-hello-image:latest docker://docker.io/username/my-hello-image:latest
```
結合其無需特權和靈活腳本的優點，Buildah 正變得越來越受到建立和分發 OCI 映像檔的使用者喜愛。

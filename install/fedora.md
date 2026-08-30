## Fedora

Fedora 作為技術前沿的 Linux 發行版，對 Docker 有著良好的支援。本節介紹在 Fedora 上的安裝步驟。

### YUM/DNF 源安裝的策略建議

Fedora 的快速發布週期（每 6 個月發布新版本）決定了它的使用者群體多為開發者和技術愛好者。雖然透過 DNF 可以直接安裝 Docker，但筆者建議仍然透過 Docker 官方 YUM 源進行安裝，原因是：Fedora 官方倉庫的 Docker 版本往往滯後，而官方源能確保你獲得最新的 Docker 功能和安全修補程式。特別是在開發環境需要用到最新 Docker 特性時，這一點顯得尤為重要。

> 警告：切勿在沒有設定 Docker dnf 源的情況下直接使用 dnf 命令安裝 Docker。

### 準備工作

確保你的 Fedora 版本在支援列表中，並清理舊版本。

#### 系統要求

根據 Docker 官方安裝文件，目前受支援的 [Fedora](https://fedoraproject.org/) 版本包括（具體以官方 [安裝文件](https://docs.docker.com/engine/install/fedora/) 為準）：

* Fedora 44
* Fedora 43

#### 解除安裝舊版本

舊版本的 Docker 稱為 `docker` 或者 `docker-engine`，使用以下命令解除安裝舊版本：

```bash
$ sudo dnf remove docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-latest-logrotate \
                  docker-logrotate \
                  docker-selinux \
                  docker-engine-selinux \
                  docker-engine
```

### 使用 dnf 安裝

使用 dnf 套件管理器安裝是推薦的方式，便於後續的更新和管理。

執行以下命令安裝相依套件：

```bash
$ sudo dnf -y install dnf-plugins-core
```
預設建議優先使用 Docker 官方倉庫；如果企業內網維護了受信任映像檔站，可自行替換倉庫 URL。

執行下面的命令新增 `dnf` 軟體源：

```bash
$ sudo dnf config-manager addrepo --from-repofile https://download.docker.com/linux/fedora/docker-ce.repo
```
如果需要測試版本的 Docker 請使用以下命令：

```bash
$ sudo dnf config-manager --set-enabled docker-ce-test
```
你也可以停用測試版本的 Docker

```bash
$ sudo dnf config-manager --set-disabled docker-ce-test
```

#### 安裝 Docker

更新 `dnf` 軟體源快取，並安裝 Docker Engine 及常用 CLI 外掛。

```bash
$ sudo dnf update
$ sudo dnf install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```
你也可以使用以下命令安裝指定版本的 Docker

```bash
$ dnf list docker-ce  --showduplicates | sort -r

docker-ce.x86_64          3:29.4.0-1.fc42                       docker-ce-stable

$ sudo dnf -y install docker-ce-<VERSION_STRING> docker-ce-cli-<VERSION_STRING>
```

### 使用腳本自動安裝

在測試或開發環境中，Docker 官方提供了便捷安裝腳本，但官方明確不建議把它作為生產環境的標準安裝方式。

在真正執行前，建議先用 `--dry-run` 預覽腳本動作：

```bash
$ curl -fsSL https://get.docker.com -o get-docker.sh
$ sudo sh ./get-docker.sh --dry-run

# 若需要測試頻道：
# curl -fsSL https://test.docker.com -o test-docker.sh
# sudo sh ./test-docker.sh
```
確認無誤後，再執行 `sudo sh ./get-docker.sh` 安裝穩定版。

### 啟動 Docker

```bash
$ sudo systemctl enable --now docker
```

### 建立 docker 使用者群組

預設情況下，`docker` 命令會使用 [Unix socket](https://en.wikipedia.org/wiki/Unix_domain_socket) 與 Docker 引擎通訊。而只有 `root` 使用者和 `docker` 群組的使用者才可以存取 Docker 引擎的 Unix socket。出於安全考慮，一般 Linux 系統上不會直接使用 `root` 使用者。因此，更好的做法是將需要使用 `docker` 的使用者加入 `docker` 使用者群組。

> ⚠️ **安全警告：`docker` 使用者群組等同於 `root` 權限**
>
> 將使用者加入 `docker` 群組免去了每次執行 `docker` 命令時輸入 `sudo` 的繁瑣，但這也意味著該使用者可以輕易取得主機的最高 root 權限（例如透過掛載根目錄執行容器）。
> 如果你在一個多使用者共享的生產系統上設定，切勿隨意將普通使用者加入此群組。此時，更安全的替代方案是使用官方提供的 **[Rootless 模式 (Rootless mode)](https://docs.docker.com/engine/security/rootless/)**，它允許在沒有任何 root 權限的情況下執行 Docker 常駐程式和容器。

建立 `docker` 群組：

```bash
$ sudo groupadd docker
```
將目前使用者加入 `docker` 群組：

```bash
$ sudo usermod -aG docker $USER
```
退出目前終端機並重新登入，進行如下測試。

### 測試 Docker 是否安裝正確

```bash
$ docker run --rm hello-world

Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
b8dfde127a29: Pull complete
Digest: sha256:308866a43596e83578c7dfa15e27a73011bdd402185a84c5cd7f32a88b501a24
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/
```
若能正常輸出以上資訊，則說明安裝成功。

### 映像檔加速

如果在使用過程中發現拉取 Docker 映像檔十分緩慢，可以設定 Docker [大陸映像檔加速](mirror.md)。

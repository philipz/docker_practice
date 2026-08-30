## Debian

Debian 以其穩定性著稱，是 Docker 的理想宿主系統。本節將指導你在 Debian 上完成 Docker 的安裝。

### APT 源安裝的必要性

與 Ubuntu 類似，Debian 使用者在安裝 Docker 時同樣應該優先選擇 Docker 官方 APT 倉庫。對於伺服器環境，這種方式更利於版本控制、升級和長期維護。

> 警告：切勿在沒有設定 Docker APT 源的情況下直接使用 apt 命令安裝 Docker。

### 準備工作

安裝前請仔細檢查 Debian 版本支援情況，並解除安裝舊版本以避免衝突。

#### 系統要求

Docker 支援以下版本的 [Debian](https://www.debian.org/intro/about) 作業系統（具體以官方 [安裝文件](https://docs.docker.com/engine/install/debian/) 為準）：

* Debian Trixie 13 (stable)
* Debian Bookworm 12（oldstable，全面支援至 2026 年 6 月 10 日，LTS 至 2028 年 6 月 30 日）
* Debian Bullseye 11（oldoldstable，LTS 支援至 2026 年 8 月 31 日）

> **注意**：Debian Bullseye 11 將於 2026 年 8 月底結束長期支援。建議新部署使用 Bookworm 12 或 Trixie 13。

#### 解除安裝舊版本

Docker 官方建議先解除安裝可能衝突的非官方軟體套件：

```bash
$ for pkg in docker.io docker-compose docker-compose-v2 docker-doc podman-docker containerd runc; do
    sudo apt remove $pkg
done
```

### 使用 APT 安裝

先安裝基礎相依，並準備金鑰目錄：

```bash
$ sudo apt update

$ sudo apt install ca-certificates curl
$ sudo install -m 0755 -d /etc/apt/keyrings
```
如果公司內網維護了受信任映像檔站，可在後續倉庫位址中替換網域名稱；預設建議優先使用 Docker 官方倉庫。

為了確認所下載軟體套件的合法性，需要新增軟體源的 GPG 金鑰。

```bash
$ sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
$ sudo chmod a+r /etc/apt/keyrings/docker.asc
```
然後，我們需要向 `sources.list` 中新增 Docker 軟體源：

> 在一些基於 Debian 的 Linux 發行版中，`$(. /etc/os-release && echo "$VERSION_CODENAME")` 可能不會回傳 Debian 官方倉庫使用的代號，例如 [Kali Linux](https://www.kali.org/docs/policy/kali-linux-relationship-with-debian/) 等衍生發行版。此時請手動替換為對應的 Debian 代號，例如 `bookworm`。

```bash
$ sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/debian
Suites: $(. /etc/os-release && echo "$VERSION_CODENAME")
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF
```
> 如果使用 Kali 等衍生發行版，請把 `Suites` 對應的版本代號替換為映射到的 Debian 代號，例如 `bookworm`。如果需要測試頻道，可將 `Components: stable` 改為 `test`。

更新 APT 快取，並安裝 Docker Engine 及常用 CLI 外掛。

```bash
$ sudo apt update

$ sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
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

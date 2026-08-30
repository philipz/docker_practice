## Raspberry Pi

樹莓派等 ARM 架構裝置在物聯網和邊緣運算領域應用廣泛。本節介紹如何在樹莓派上安裝 Docker。

### 樹莓派執行 Docker 的現實考慮

樹莓派是 Docker 在邊緣運算的一個優秀用例。但在安裝前，筆者建議你了解幾個實際情況：

**效能特性**：

- Raspberry Pi 4 及以上才能流暢執行 Docker 和基本容器
- Raspberry Pi Zero 2 可以執行，但效能受限
- 磁碟 I/O 是主要瓶頸（特別是使用 microSD 卡時）

**映像檔可用性**：

- 並非所有 Docker 映像檔都有 ARM 版本（arm64 或 armv7）
- 官方映像檔通常提供多架構支援，但第三方映像檔可能沒有
- 某些依賴 Intel 特定指令的應用無法在 ARM 上執行

**儲存和記憶體**：

- 容器映像檔會佔用較多儲存空間，128GB microSD 卡建議最多執行 3-4 個中等大小的容器
- 512MB 或 1GB 記憶體的樹莓派執行多個容器會非常吃力

**實踐建議**：樹莓派 Docker 部署最適合輕量級應用——單個微服務、監控代理、Web 伺服器等。複雜多容器應用還是應該部署在效能更強的硬體上。

> 警告：切勿在沒有設定 Docker APT 源的情況下直接使用 apt 命令安裝 Docker。

### 系統要求

Docker 對 ARM 架構有著良好的支援。

Docker 可以執行在多種 CPU 架構上，但本小節**只聚焦 Raspberry Pi OS 32-bit (armhf)** 的官方安裝流程；如果你使用的是 64 位元 Raspberry Pi OS，請直接參考 Debian `arm64` 安裝說明。

Docker 官方目前單獨提供的是 **Raspberry Pi OS 32-bit (armhf)** 安裝頁（具體以官方 [安裝文件](https://docs.docker.com/engine/install/raspberry-pi-os/) 為準），支援情況如下：

* Raspberry Pi OS Bookworm
* Raspberry Pi OS Bullseye

> **重要提醒**：Docker Engine v28 是官方最後一個支援 Raspberry Pi OS 32-bit (armhf) 的大版本。從 v29 開始，32 位元 Raspberry Pi OS 不再提供新主版本軟體套件。若你使用的是 64 位元 Raspberry Pi OS，請直接參考 Debian `arm64` 安裝方式。

*註：*`Raspberry Pi OS` 由樹莓派的開發與維護機構[樹莓派基金會](https://www.raspberrypi.org/)官方支援，並推薦用作樹莓派的首選系統，其基於 `Debian`。

### 使用 APT 安裝

推薦使用 APT 套件管理器進行安裝，以確保版本的穩定性和安全性。

先安裝基礎相依，並準備金鑰目錄：

```bash
$ sudo apt-get update

$ sudo apt-get install \
     ca-certificates \
     curl \
     gnupg
```
預設建議優先使用 Docker 官方倉庫；如果企業內網維護了受信任映像檔站，可自行替換倉庫 URL。

為了確認所下載軟體套件的合法性，需要新增軟體源的 GPG 金鑰。

```bash
$ sudo install -m 0755 -d /etc/apt/keyrings
$ sudo curl -fsSL https://download.docker.com/linux/raspbian/gpg -o /etc/apt/keyrings/docker.asc
$ sudo chmod a+r /etc/apt/keyrings/docker.asc
```
然後，我們需要向 `sources.list` 中新增 Docker 軟體源：

```bash
$ sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/raspbian
Suites: $(. /etc/os-release && echo "$VERSION_CODENAME")
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF
```
> 以上命令會新增穩定版本的 Docker APT 源，如果需要測試版本的 Docker 請將 stable 改為 test。

#### 報錯解決辦法

在 `Raspberry Pi OS Bullseye/Bookworm` 中，如果你使用 `add-apt-repository` 新增源，可能會出現如下報錯。官方目前更推薦的做法是**不要繼續回退到舊式單行 `deb` 設定**，而是直接使用上面的 `docker.sources` 檔案方式寫入倉庫：

```bash
Traceback (most recent call last):
 File "/usr/bin/add-apt-repository", line 95, in <module>
   sp = SoftwareProperties(options=options)
 File "/usr/lib/python3/dist-packages/softwareproperties/SoftwareProperties.py", line 109, in __init__
   self.reload_sourceslist()
 File "/usr/lib/python3/dist-packages/softwareproperties/SoftwareProperties.py", line 599, in reload_sourceslist
   self.distro.get_sources(self.sourceslist)
 File "/usr/lib/python3/dist-packages/aptsources/distro.py", line 91, in get_sources
   raise NoDistroTemplateException(
aptsources.distro.NoDistroTemplateException: Error: could not find a distribution template for Raspbian/bullseye
```
如果之前已經寫入了錯誤的源設定，建議先刪除舊條目，再重新執行本節前面的 `docker.asc + docker.sources` 兩步。

#### 安裝 Docker

更新 apt 軟體套件快取，並安裝 Docker Engine 及常用 CLI 外掛。

```bash
$ sudo apt-get update

$ sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
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
確認無誤後，再執行 `sudo sh ./get-docker.sh` 安裝穩定版。如果你執行的是 64 位元 Raspberry Pi OS，更推薦直接遷移到 Debian `arm64` 安裝路徑，而不是繼續停留在 32 位元 armhf 流程上。

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
4ee5c797bcd7: Pull complete
Digest: sha256:308866a43596e83578c7dfa15e27a73011bdd402185a84c5cd7f32a88b501a24
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (arm32v7)
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

*注意：* ARM 平台不能使用 `x86` 映像檔，查看 Raspberry Pi OS 可使用映像檔請存取 [arm32v7](https://hub.docker.com/u/arm32v7/) 或者 [arm64v8](https://hub.docker.com/u/arm64v8/)。

### 映像檔加速

如果在使用過程中發現拉取 Docker 映像檔十分緩慢，可以設定 Docker [大陸映像檔加速](mirror.md)。

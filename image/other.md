## 其他製作映像檔的方式

除了標準的使用 `Dockerfile` 產生映像檔的方法外，由於各種特殊需求和歷史原因，還提供了一些其他方法用以產生映像檔。

### 從 rootfs 壓縮包匯入

格式：`docker import [選項] <檔案>|<URL>|- [<倉庫名>[:<標籤>]]`

壓縮包可以是本機檔案、遠端 Web 檔案，甚至是從標準輸入中得到。壓縮包將會在映像檔 `/` 目錄展開，並直接作為映像檔第一層提交。

比如我們想要建立一個 [OpenVZ](https://openvz.org) 的 Ubuntu 16.04 [模板](https://wiki.openvz.org/Download/template/precreated)的映像檔：

> **版本提示**：`noble` 對應 Ubuntu 24.04 LTS。實際用於生產環境時，應選擇仍在安全維護期內的發行版，並按團隊的基礎映像檔更新策略定期重建。

```bash
$ docker import \
    http://download.openvz.org/template/precreated/ubuntu-16.04-x86_64.tar.gz \
    openvz/ubuntu:16.04

Downloading from http://download.openvz.org/template/precreated/ubuntu-16.04-x86_64.tar.gz
sha256:412b8fc3e3f786dca0197834a698932b9c51b69bd8cf49e100c35d38c9879213
```
這條命令自動下載了 `ubuntu-16.04-x86_64.tar.gz` 檔案，並且作為根檔案系統展開匯入，並儲存為映像檔 `openvz/ubuntu:16.04`。

匯入成功後，我們可以用 `docker image ls` 看到這個匯入的映像檔：

```bash
$ docker image ls openvz/ubuntu
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
openvz/ubuntu       16.04               412b8fc3e3f7        55 seconds ago      505MB
```
如果我們查看其歷史的話，會看到描述中有匯入的檔案連結：

```bash
$ docker history openvz/ubuntu:16.04
IMAGE               CREATED              CREATED BY          SIZE                COMMENT
f477a6e18e98        About a minute ago                       214.9 MB            Imported from http://download.openvz.org/template/precreated/ubuntu-16.04-x86_64.tar.gz
```

### Docker 映像檔的匯入和匯出 `docker save` 和 `docker load`

Docker 還提供了 `docker save` 和 `docker load` 命令，用以將映像檔儲存為一個檔案，然後傳輸到另一個位置上，再載入進來。這是在沒有 Docker Registry 時的做法，現在已經不推薦，映像檔遷移應該直接使用 Docker Registry，無論是直接使用 Docker Hub 還是使用內網私有 Registry 都可以。

#### 儲存映像檔

使用 `docker save` 命令可以將映像檔儲存為歸檔檔案。

比如我們希望儲存這個 `alpine` 映像檔。

```bash
$ docker image ls alpine
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
alpine              latest              baa5d63471ea        5 weeks ago         4.803 MB
```

> **版本提示**：`alpine:latest` 為最新版本的 Alpine Linux。如果需要特定版本號（如 `alpine:3.20`），可以明確指定以確保可重現性。

儲存映像檔的命令為：

```bash
$ docker save alpine -o filename
$ file filename
filename: POSIX tar archive
```
這裡的 filename 可以為任意名稱甚至任意副檔名，但檔案的本質都是歸檔檔案

**注意：如果同名則會覆蓋（沒有警告）**

若使用 `gzip` 壓縮：

```bash
$ docker save alpine | gzip > alpine-latest.tar.gz
```
然後我們將 `alpine-latest.tar.gz` 檔案複製到了另一台機器上，可以用下面這個命令載入映像檔：

```bash
$ docker load -i alpine-latest.tar.gz
Loaded image: alpine:latest
```
如果我們結合這兩個命令以及 `ssh` 甚至 `pv` 的話，利用 Linux 強大的管道，我們可以寫一個命令完成從一台機器將映像檔遷移到另一台機器，並且帶進度條的功能：

```bash
docker save <映像檔名> | bzip2 | pv | ssh <使用者名稱>@<主機名> 'cat | docker load'
```

> **註**：本節的儲存與載入可另見[儲存和載入映像檔](save_load.md)一節 philipz 特有的實作說明。

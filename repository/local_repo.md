## 私有倉庫

有時候使用 Docker Hub 這樣的公共倉庫可能不方便，使用者可以建立一個本地倉庫供私人使用。

本節介紹如何使用本地倉庫。

[Docker Registry](https://distribution.github.io/distribution/) 是官方提供的工具，可以用於建立私有的映像檔倉庫。本文範例沿用 [distribution/distribution](https://github.com/distribution/distribution) v2.x 相容路徑；新生產部署應評估 Distribution 3.x，並核對設定路徑、遷移說明和生態相容性。

### 安裝執行 docker-registry

#### 容器執行

如果您需要搭建私有倉庫，可以透過官方提供的 `registry` 映像檔快速部署。

你可以使用官方 `registry` 映像檔來執行。

```bash
$ docker run -d -p 5000:5000 --restart=always --name registry registry:2
```

> **版本說明**：使用 `registry:2` 表示 Docker Registry 2.x 相容範例。Distribution 3.x 已發布穩定版本；不要直接把本章 v2 設定原樣套到 v3 生產環境，升級前應閱讀遷移說明並做相容測試。舊版本 Registry 1.x 已停止維護，不建議使用。
這將使用官方的 `registry` 映像檔來啟動私有倉庫。預設情況下，倉庫會被建立在容器的 `/var/lib/registry` 目錄下。你可以透過 `-v` 參數來將映像檔檔案存放在本地的指定路徑。例如下面的例子將上傳的映像檔放到本地的 `/opt/data/registry` 目錄。

```bash
$ docker run -d \
    -p 5000:5000 \
    -v /opt/data/registry:/var/lib/registry \
    registry:2
```

### 在私有倉庫上傳、搜尋、下載映像檔

建立好私有倉庫之後，就可以使用 `docker tag` 來標記一個映像檔，然後推送它到倉庫。例如私有倉庫位址為 `127.0.0.1:5000`。

先在本機查看已有的映像檔。

```bash
$ docker image ls
REPOSITORY                        TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
ubuntu                            latest              ba5877dc9bec        6 weeks ago         192.7 MB
```
使用 `docker tag` 將 `ubuntu:latest` 這個映像檔標記為 `127.0.0.1:5000/ubuntu:latest`。

格式為 `docker tag IMAGE[:TAG] [REGISTRY_HOST[:REGISTRY_PORT]/]REPOSITORY[:TAG]`。

```bash
$ docker tag ubuntu:latest 127.0.0.1:5000/ubuntu:latest
$ docker image ls
REPOSITORY                        TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
ubuntu                            latest              ba5877dc9bec        6 weeks ago         192.7 MB
127.0.0.1:5000/ubuntu             latest              ba5877dc9bec        6 weeks ago         192.7 MB
```
使用 `docker push` 上傳標記的映像檔。

```bash
$ docker push 127.0.0.1:5000/ubuntu:latest
The push refers to repository [127.0.0.1:5000/ubuntu]
373a30c24545: Pushed
a9148f5200b0: Pushed
cdd3de0940ab: Pushed
fc56279bbb33: Pushed
b38367233d37: Pushed
2aebd096e0e2: Pushed
latest: digest: sha256:fe4277621f10b5026266932ddf760f5a756d2facd505a94d2da12f4f52f71f5a size: 1568
```
用 `curl` 查看倉庫中的映像檔。

```bash
$ curl 127.0.0.1:5000/v2/_catalog
{"repositories":["ubuntu"]}
```
這裡可以看到 `{"repositories":["ubuntu"]}`，表明映像檔已經被成功上傳了。

先刪除已有映像檔，再嘗試從私有倉庫中下載這個映像檔。

```bash
$ docker image rm 127.0.0.1:5000/ubuntu:latest

$ docker pull 127.0.0.1:5000/ubuntu:latest
Pulling repository 127.0.0.1:5000/ubuntu:latest
ba5877dc9bec: Download complete
511136ea3c5a: Download complete
9bad880da3d2: Download complete
25f11f5fb0cb: Download complete
ebc34468f71d: Download complete
2318d26665ef: Download complete

$ docker image ls
REPOSITORY                         TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
127.0.0.1:5000/ubuntu              latest              ba5877dc9bec        6 weeks ago         192.7 MB
```

### 設定非 https 倉庫位址

如果你不想使用 `127.0.0.1:5000` 作為倉庫位址，比如想讓本網段的其他主機也能把映像檔推送到私有倉庫。你就得把例如 `192.168.199.100:5000` 這樣的內網位址作為私有倉庫位址，這時你會發現無法成功推送映像檔。

這是因為 Docker 預設不允許非 `HTTPS` 方式推送映像檔。我們可以透過 Docker 的設定選項來取消這個限制，或者查看下一節設定能夠透過 `HTTPS` 存取的私有倉庫。

#### Linux

預設情況下，Docker 強制使用 HTTPS 協定推送映像檔。如果您搭建的私有倉庫是 HTTP 協定，需要進行如下設定。


對於使用 `systemd` 的系統，請在 `/etc/docker/daemon.json` 中寫入如下內容（如果檔案不存在請新建該檔案）

```json
{
  "registry-mirrors": [
    "https://docker.your-mirror.example.com"
  ],
  "insecure-registries": [
    "192.168.199.100:5000"
  ]
}
```
> 注意：該檔案必須符合 `json` 規範，否則 Docker 將不能啟動。映像檔加速器位址請替換為實際可用的源，具體設定參見「安裝」章節的映像檔加速器說明。

### 其他

對於 Docker Desktop for Windows、Docker Desktop for Mac 在設定中的 `Docker Engine` 中進行編輯，增加和上邊一樣的字串即可。

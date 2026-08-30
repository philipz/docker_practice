## 匯出與匯入容器

當我們需要遷移容器或者備份容器時，可以使用 Docker 的匯入和匯出功能。本節將介紹這兩個命令的使用方法。

### 匯出容器

如果要匯出本地某個容器，可以使用 `docker export` 命令。

```bash
$ docker container ls -a
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS                    PORTS               NAMES
7691a814370e        ubuntu:24.04        "/bin/bash"         36 hours ago        Exited (0) 21 hours ago                       test
$ docker export 7691a814370e > ubuntu.tar
```
這樣將匯出容器快照到本地檔案。

> **版本說明**：匯出的容器快照不包含映像檔版本歷史，匯入時可以自訂標籤和版本號。

### 匯入容器快照

可以使用 `docker import` 從容器快照檔案中再匯入為映像檔，例如

```bash
$ cat ubuntu.tar | docker import - test/ubuntu:v1.0
$ docker image ls
REPOSITORY          TAG                 IMAGE ID            CREATED              SIZE
test/ubuntu         v1.0                9d37a6082e97        About a minute ago   171.3 MB
```
此外，也可以透過指定 URL 或者某個目錄來匯入，例如

```bash
$ docker import http://example.com/exampleimage.tgz example/imagerepo
```
*註：使用者既可以使用 `docker load` 來匯入映像檔儲存檔案到本地映像檔庫，也可以使用 `docker import` 來匯入一個容器快照到本地映像檔庫。這兩者的區別在於容器快照檔案將丟棄所有的歷史記錄和中繼資料資訊（即僅儲存容器當時的快照狀態），而映像檔儲存檔案將儲存完整記錄，體積也要大。此外，從容器快照檔案匯入時可以重新指定標籤等中繼資料資訊。*

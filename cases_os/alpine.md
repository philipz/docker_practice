## Alpine

### 簡介

下圖直觀地展示了本節內容：

![Alpine Linux 作業系統](../_images/alpinelinux-logo.png)


`Alpine` 作業系統是一個面向安全的輕型 `Linux` 發行版。它不同於通常 `Linux` 發行版，`Alpine` 採用了 `musl libc` 和 `busybox` 以減小系統的體積和執行期資源消耗，但功能上比 `busybox` 又完善得多，因此得到開源社群越來越多的青睞。在保持瘦身的同時，`Alpine` 還提供了自己的包管理工具 `apk`，可以在 [Alpine Packages](https://pkgs.alpinelinux.org/packages) 網站上查詢包資訊，也可以直接透過 `apk` 命令直接查詢和安裝各種軟體。


`Alpine` 是由非商業組織維護的、支援廣泛場景的 `Linux` 發行版，它特別為資深/重度 `Linux` 使用者而最佳化，關注安全，效能和資源效能。`Alpine` 映像檔可以適用於更多常用場景，並且是一個優秀的可以適用於生產的基礎系統/環境。

`Alpine` Docker 映像檔也繼承了 `Alpine Linux` 發行版的這些優勢。相比於其他 `Docker` 映像檔，它的容量非常小，壓縮後僅約 **5 MB**（對比 `Ubuntu` 系列映像檔約 `28 MB`），且擁有非常友好的包管理機制。官方映像檔來自 `docker-alpine` 專案。

目前 Docker 官方已開始推薦使用 `Alpine` 替代之前的 `Ubuntu` 作為基礎映像檔環境。這樣會帶來多個好處。包括映像檔下載速度加快，映像檔安全性提高，主機之間的切換更方便，占用更少磁碟空間等。

下表是官方映像檔的大小比較（壓縮後大小，實際資料以 Docker Hub 為準）：

```bash
REPOSITORY          TAG           COMPRESSED SIZE
alpine              latest        ~5 MB
debian              latest        ~30 MB
ubuntu              latest        ~28 MB
```

> **提示**：映像檔大小會隨版本更新而變化，精確值請查閱 [Docker Hub](https://hub.docker.com/) 各映像檔的 Tags 頁面。Alpine 的優勢不僅在於體積小，還在於更少的預裝包帶來更小的攻擊面。

### 取得並使用官方映像檔

由於映像檔很小，下載時間往往很短，讀者可以直接使用 `docker run` 指令直接執行一個 `Alpine` 容器，並指定執行的 Linux 指令，例如：

```bash
$ docker run alpine echo '123'
123
```

### 遷移至 Alpine 基礎映像檔

目前，大部分 Docker 官方映像檔都已經支援 `Alpine` 作為基礎映像檔，可以很容易進行遷移。

例如：

* `ubuntu/debian` -> `alpine`
* `python:3` -> `python:3-alpine`
* `ruby:2.6` -> `ruby:2.6-alpine`

另外，如果使用 `Alpine` 映像檔替換 `Ubuntu` 基礎映像檔，安裝軟體包時需要用 `apk` 包管理器替換 `apt` 工具，如

```bash
$ apk add --no-cache <package>
```
`Alpine` 中軟體安裝包的名字可能會與其他發行版有所不同，可以在 `https://pkgs.alpinelinux.org/packages` 網站搜尋並確定安裝包名稱。如果需要的安裝包不在主索引內，但是在測試或社群索引中，那麼可以按照以下方法使用這些安裝包。

```bash
$ echo "http://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories
$ apk --update add --no-cache <package>
```
由於在國內存取 `apk` 倉庫較緩慢，建議在使用 `apk` 之前先替換倉庫地址為國內映像檔。

```docker
RUN sed -i "s/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g" /etc/apk/repositories \
      && apk add --no-cache <package>
```

### 相關資源

* `Alpine` 官網：https://www.alpinelinux.org/
* `Alpine` 官方倉庫：https://github.com/alpinelinux
* `Alpine` 官方映像檔：https://hub.docker.com/\_/alpine/
* `Alpine` 官方映像檔倉庫：https://github.com/alpinelinux/docker-alpine

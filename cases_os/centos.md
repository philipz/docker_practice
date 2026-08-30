## CentOS Fedora

### CentOS 系統簡介

`CentOS` 和 `Fedora` 都是基於 `Redhat` 的常見 Linux 分支。傳統 `CentOS Linux` 曾是企業級伺服器的常用作業系統，但相關 Docker 官方映像檔已停止維護；新部署通常應評估 Rocky Linux、AlmaLinux、CentOS Stream 或直接使用 RHEL/UBI 等替代方案。`Fedora` 則主要面向個人桌面使用者。

![CentOS 作業系統](../_images/centos-logo.png)


CentOS（Community Enterprise Operating System，中文意思是：社群企業作業系統），它是基於 `Red Hat Enterprise Linux` 原始碼編譯而成。由於 `CentOS` 與 `Redhat Linux` 源於相同的程式碼基礎，所以很多成本敏感且需要高穩定性的公司就使用 `CentOS` 來替代商業版 `Red Hat Enterprise Linux`。`CentOS` 自身不包含閉源軟體。

#### 使用 CentOS 官方映像檔

CentOS 官方映像檔的使用非常簡單。


**注意：CentOS 8 已於 2021 年 12 月 31 日停止維護 (EOL)，CentOS 7 已於 2024 年 6 月 30 日停止維護。對於新部署，推薦使用 Rocky Linux、AlmaLinux 或 CentOS Stream 等替代發行版。**

使用 `docker run` 直接執行 `CentOS 7` 映像檔，並登入 `bash`。

```bash
$ docker run -it centos:7 bash
Unable to find image 'centos:7' locally
7: Pulling from library/centos
3d8673bd162a: Pull complete
Digest: sha256:a66ffcb73930584413de83311ca11a4cb4938c9b2521d331026dad970c19adf4
Status: Downloaded newer image for centos:7
[root@43eb3b194d48 /]# cat /etc/redhat-release
CentOS Linux release 7.9.2009 (Core)
```

### Fedora 系統簡介

下圖直觀地展示了本節內容：

![Fedora 作業系統](../_images/fedora-logo.png)


`Fedora` 是由 `Fedora Project` 社群開發、紅帽公司贊助的 `Linux` 發行版。它的目標是建立一套新穎、多功能並且自由和開源的作業系統。`Fedora` 的功能對於使用者而言，它是一套功能完備的，可以更新的免費作業系統，而對贊助商 `Red Hat` 而言，它是許多新技術的測試平台。被認為可用的技術最終會加入到 `Red Hat Enterprise Linux` 中。

#### 使用 Fedora 官方映像檔

使用 `docker run` 命令直接執行 `Fedora` 官方映像檔，並登入 `bash`。

```bash
$ docker run -it fedora bash
Unable to find image 'fedora:latest' locally
latest: Pulling from library/fedora
2bf01635e2a0: Pull complete
Digest: sha256:64a02df6aac27d1200c2572fe4b9949f1970d05f74d367ce4af994ba5dc3669e
Status: Downloaded newer image for fedora:latest
[root@196ca341419b /]# cat /etc/redhat-release
Fedora release 43 (Forty Three)
```

### 相關資源

* `Fedora` 官網：https://fedoraproject.org/
* `Fedora` 官方倉庫：https://github.com/fedora-infra
* `Fedora` 官方映像檔：https://hub.docker.com/\_/fedora/
* `Fedora` 官方映像檔倉庫：https://github.com/fedora-cloud/docker-brew-fedora
* `CentOS` 官網：https://www.centos.org
* `CentOS` 官方倉庫：https://github.com/CentOS
* `CentOS` 官方映像檔：https://hub.docker.com/\_/centos/
* `CentOS` 官方映像檔倉庫：https://github.com/CentOS/CentOS-Dockerfiles

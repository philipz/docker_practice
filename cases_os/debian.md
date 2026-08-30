## Debian Ubuntu

`Debian` 和 `Ubuntu` 都是目前較為流行的 **Debian 系** 的伺服器作業系統，十分適合研發場景。`Docker Hub` 上提供了官方映像檔，國內各大容器雲服務也基本都提供了相應的支援。

### Debian 系統簡介

下圖直觀地展示了本節內容：

![Debian 作業系統](../_images/debian-logo.png)


`Debian` 是由 `GPL` 和其他自由軟體許可協定授權的自由軟體組成的作業系統，由 **Debian 計劃 (Debian Project)** 組織維護。**Debian 計劃** 是一個獨立的、分散的組織，由 `3000` 名志工組成，接受世界多個非營利組織的資金支援，`Software in the Public Interest` 提供支援並持有商標作為保護機構。`Debian` 以其堅守 `Unix` 和自由軟體的精神，以及其給予使用者的眾多選擇而聞名。現時 `Debian` 包括了超過 `25,000` 個軟體包並支援 `12` 個電腦系統結構。

`Debian` 作為一個大的系統組織框架，其下有多種不同作業系統核心的分支計劃，主要為採用 `Linux` 核心的 `Debian GNU/Linux` 系統，其他還有採用 `GNU Hurd` 核心的 `Debian GNU/Hurd` 系統、採用 `FreeBSD` 核心的 `Debian GNU/kFreeBSD` 系統，以及採用 `NetBSD` 核心的 `Debian GNU/NetBSD` 系統。甚至還有利用 `Debian` 的系統架構和工具，採用 `OpenSolaris` 核心建立而成的 `Nexenta OS` 系統。在這些 `Debian` 系統中，以採用 `Linux` 核心的 `Debian GNU/Linux` 最為著名。

眾多的 `Linux` 發行版，例如 `Ubuntu`、`Knoppix` 和 `Linspire` 及 `Xandros` 等，都基於 `Debian GNU/Linux`。

#### 使用 Debian 官方映像檔

Debian 是一個常用的基礎映像檔。


官方提供了大家熟知的 `debian` 映像檔以及面向科研領域的 `neurodebian` 映像檔。可以使用 `docker run` 直接執行 `Debian` 映像檔。

```bash
$ docker run -it debian bash
root@668e178d8d69:/# cat /etc/issue
Debian GNU/Linux 13
```
`Debian` 映像檔很適合作為基礎映像檔，建立自訂映像檔。

### Ubuntu 系統簡介

下圖直觀地展示了本節內容：

![Ubuntu 作業系統](../_images/ubuntu-logo.jpg)


`Ubuntu` 是一個以桌面應用為主的 `GNU/Linux` 作業系統，其名稱來自非洲南部祖魯語或豪薩語的 "ubuntu" 一詞（官方譯名「友幫拓」，另有「吾幫托」、「烏班圖」、「有奔頭」或「烏斑兔」等譯名）。`Ubuntu` 意思是「人性」以及「我的存在是因為大家的存在」，是非洲傳統的一種價值觀，類似華人社會的「仁愛」思想。`Ubuntu` 基於 `Debian` 發行版和 `GNOME/Unity` 桌面環境，與 `Debian` 的不同在於它每 6 個月會發布一個新版本，每 2 年推出一個長期支援 **(Long Term Support，LTS)** 版本；LTS 版本通常提供 5 年標準安全維護，Ubuntu Pro/ESM 可進一步延長安全覆蓋。

#### 使用 Ubuntu 官方映像檔

Ubuntu 是目前最流行的 Linux 發行版之一。


下面以 `ubuntu:26.04` 為例，演示如何使用該映像檔安裝一些常用軟體。

首先使用 `-ti` 參數啟動容器，登入 `bash`，查看 `ubuntu` 的發行版本號。

```bash
$ docker run -ti ubuntu:26.04 /bin/bash
root@7d93de07bf76:/# cat /etc/os-release
PRETTY_NAME="Ubuntu 26.04 LTS"
NAME="Ubuntu"
VERSION_ID="26.04"
VERSION="26.04 LTS (Resolute Raccoon)"
VERSION_CODENAME=resolute
ID=ubuntu
ID_LIKE=debian
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
```
當試圖直接使用 `apt-get` 安裝一個軟體的時候，會提示 `E: Unable to locate package`。

```bash
root@7d93de07bf76:/# apt-get install curl
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
E: Unable to locate package curl
```
這並非系統不支援 `apt-get` 命令。Docker 映像檔在製作時為了精簡清除了 `apt` 倉庫資訊，因此需要先執行 `apt-get update` 命令來更新倉庫資訊。更新資訊後即可成功透過 `apt-get` 命令來安裝軟體。

```bash
root@7d93de07bf76:/# apt-get update
Get:1 http://archive.ubuntu.com/ubuntu resolute InRelease [256 kB]
Get:2 http://security.ubuntu.com/ubuntu resolute-security InRelease [126 kB]
...
Fetched 25.8 MB in 8s (3215 kB/s)
Reading package lists... Done
```
首先，安裝 `curl` 工具。

```bash
root@7d93de07bf76:/# apt-get install curl
Reading package lists... Done
Building dependency tree
Reading state information... Done
The following additional packages will be installed:
  ca-certificates krb5-locales libasn1-8-heimdal libcurl4 libgssapi-krb5-2 libgssapi3-heimdal libhcrypto4-heimdal libheimbase1-heimdal libheimntlm0-heimdal libhx509-5-heimdal
  libk5crypto3 libkeyutils1 libkrb5-26-heimdal libkrb5-3 libkrb5support0 libldap-2.4-2 libldap-common libnghttp2-14 libpsl5 libroken18-heimdal librtmp1 libsasl2-2 libsasl2-modules libsasl2-modules-db libsqlite3-0 libssl1.1 libwind0-heimdal openssl publicsuffix
...
root@7d93de07bf76:/# curl
curl: try 'curl --help' or 'curl --manual' for more information
```
接下來，再安裝 `apache` 服務。

```bash
root@7d93de07bf76:/# apt-get install -y apache2
Reading package lists... Done
Building dependency tree
Reading state information... Done
The following additional packages will be installed:
  apache2-bin apache2-data apache2-utils file libapr1 libaprutil1 libaprutil1-dbd-sqlite3 libaprutil1-ldap libexpat1 libgdbm-compat4 libgdbm5 libicu60 liblua5.2-0 libmagic-mgc libmagic1 libperl5.26 libxml2 mime-support netbase perl perl-modules-5.26 ssl-cert xz-utils
...
```
啟動這個 `apache` 服務，然後使用 `curl` 來測試本地存取。

```bash
root@7d93de07bf76:/# service apache2 start
 * Starting web server apache2                                                                                                                               AH00558: apache2: Could not reliably determine the server's fully qualified domain name, using 172.17.0.2. Set the 'ServerName' directive globally to suppress this message
 *
root@7d93de07bf76:/# curl 127.0.0.1

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <!--
    Modified from the Debian original for Ubuntu
    Last updated: 2016-11-16
    See: https://launchpad.net/bugs/1288690
  -->
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>Apache2 Ubuntu Default Page: It works</title>
    <style type="text/css" media="screen">
...
```
配合使用 `-p` 參數對外映射服務埠號，可以允許容器外來存取該服務。

### 相關資源

* `Debian` 官網：https://www.debian.org/
* `Neuro Debian` 官網：http://neuro.debian.net/
* `Debian` 官方倉庫：https://github.com/Debian
* `Debian` 官方映像檔：https://hub.docker.com/\_/debian/
* `Debian` 官方映像檔倉庫：https://github.com/tianon/docker-brew-debian/
* `Ubuntu` 官網：https://ubuntu.com
* `Ubuntu` 官方倉庫：https://github.com/ubuntu
* `Ubuntu` 官方映像檔：https://hub.docker.com/\_/ubuntu/
* `Ubuntu` 官方映像檔倉庫：https://github.com/tianon/docker-brew-ubuntu-core

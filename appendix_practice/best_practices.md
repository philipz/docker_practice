# 最佳實踐

本附錄是筆者對 Docker 官方文件中 [Building best practices](https://docs.docker.com/build/building/best-practices/) 的理解與翻譯。

### 一般性的指南和建議

#### 容器應該是短暫的

透過 `Dockerfile` 建立的映像檔所啟動的容器應該盡可能短暫（生命週期短）。「短暫」意味著可以停止和銷毀容器，並且建立一個新容器並部署好所需的設定和工作量應該是極小的。

#### 使用 `.dockerignore` 檔案

使用 `Dockerfile` 建立映像檔時最好是將 `Dockerfile` 放置在一個新建的空目錄下。然後將建立映像檔所需要的檔案添加到該目錄中。為了提高建立映像檔的效率，你可以在目錄下新建一個 `.dockerignore` 檔案來指定要忽略的檔案和目錄。`.dockerignore` 檔案的排除模式語法和 Git 的 `.gitignore` 檔案相似。

#### 使用多階段建立

在現代 Docker 版本中，你可以使用[多階段建立](../dockerfile/multistage_builds.md)來減少所建立映像檔的大小。該能力最早在 Docker 17.05 引入，如今已是編寫生產映像檔的預設實踐之一；新專案還應結合 BuildKit 快取掛載、secret 掛載和多平台建立能力一起評估。

#### 避免安裝不必要的套件

為了降低複雜性、減少相依、減小檔案大小、節約建立時間，你應該避免安裝任何不必要的套件。例如，不要在資料庫映像檔中包含一個文字編輯器。

#### 一個容器只執行一個程式

應該保證在一個容器中只執行一個程式。將多個應用解耦到不同容器中，保證了容器的橫向擴充和複用。例如 web 應用應該包含三個容器：web 應用、資料庫、快取。

如果容器互相相依，你可以使用 [Docker 自訂網路](../network/custom_network.md)來把這些容器連線起來。

#### 映像檔層數盡可能少

你需要在 `Dockerfile` 可讀性（也包括長期的可維護性）和減少層數之間做一個平衡。

#### 將多行參數排序

將多行參數按字母順序排序（比如要安裝多個套件時）。這可以幫助你避免重複包含同一個套件，更新套件列表時也更容易。也便於 `PRs` 閱讀和審查。建議在反斜線符號 `\` 之前添加一個空格，以增加可讀性。

下面是來自 `buildpack-deps` 映像檔的例子：

```docker
RUN apt-get update && apt-get install -y \
  bzr \
  cvs \
  git \
  mercurial \
  subversion
```

#### 建立快取

在映像檔的建立過程中，Docker 會遍歷 `Dockerfile` 檔案中的指令，然後按順序執行。在執行每條指令之前，Docker 都會在快取中查找是否已經存在可重用的映像檔，如果有就使用現存的映像檔，不再重複建立。如果你不想在建立過程中使用快取，你可以在 `docker build` 命令中使用 `--no-cache=true` 選項。

但是，如果你想在建立的過程中使用快取，你得明白什麼時候會，什麼時候不會找到匹配的映像檔，遵循的基本規則如下：

* 從一個基礎映像檔開始（`FROM` 指令指定），下一條指令將和該基礎映像檔的所有子映像檔進行匹配，檢查這些子映像檔被建立時使用的指令是否和被檢查的指令完全一樣。如果不是，則快取失效。
* 在大多數情況下，只需要簡單地對比 `Dockerfile` 中的指令和子映像檔。然而，有些指令需要更多的檢查和解釋。
* 對於 `ADD` 和 `COPY` 指令，映像檔中對應檔案的內容也會被檢查，每個檔案都會計算出一個校驗和。檔案的最後修改時間和最後存取時間不會納入校驗。在快取的查找過程中，會將這些校驗和與已存在映像檔中的檔案校驗和進行對比。如果檔案有任何改變，比如內容和中繼資料，則快取失效。
* 除了 `ADD` 和 `COPY` 指令，快取匹配過程不會查看臨時容器中的檔案來決定快取是否匹配。例如，當執行完 `RUN apt-get -y update` 指令後，容器中一些檔案被更新，但 Docker 不會檢查這些檔案。這種情況下，只有指令字串本身被用來匹配快取。

一旦快取失效，所有後續的 `Dockerfile` 指令都將產生新的映像檔，快取不會被使用。

### Dockerfile 指令

下面針對 `Dockerfile` 中各種指令的最佳編寫方式給出建議。

#### FROM

盡可能使用當前官方倉庫作為你建立映像檔的基礎。推薦使用 [Alpine](https://hub.docker.com/_/alpine/) 映像檔，因為它被嚴格控制並保持最小尺寸（目前小於 5 MB），但它仍然是一個完整的發行版。

#### LABEL

你可以給映像檔添加標籤來幫助組織映像檔、記錄許可資訊、輔助自動化建立等。每個標籤一行，由 `LABEL` 開頭加上一個或多個標籤對。下面的示例展示了各種不同的可能格式。`#` 開頭的行是註解內容。

> 注意：如果你的字串中包含空格，必須將字串放入引號中或者對空格使用跳脫。如果字串內容本身就包含引號，必須對引號使用跳脫。

```docker
## Set one or more individual labels

LABEL com.example.version="0.0.1-beta"

LABEL vendor="ACME Incorporated"

LABEL com.example.release-date="2015-02-12"

LABEL com.example.version.is-production=""
```

一個映像檔可以包含多個標籤，但建議將多個標籤放入到一個 `LABEL` 指令中。

```docker
## Set multiple labels at once, using line-continuation characters to break long lines

LABEL vendor=ACME\ Incorporated \
      com.example.is-beta= \
      com.example.is-production="" \
      com.example.version="0.0.1-beta" \
      com.example.release-date="2015-02-12"
```

關於標籤可以接受的鍵值對，參考 [Label keys and values](https://docs.docker.com/engine/manage-resources/labels/#label-keys-and-values)。關於查詢標籤資訊，參考 [Manage labels on objects](https://docs.docker.com/engine/manage-resources/labels/#manage-labels-on-objects)。

#### RUN

為了保持 `Dockerfile` 檔案的可讀性，可理解性，以及可維護性，建議將長的或複雜的 `RUN` 指令用反斜線 `\` 分割成多行。

##### apt-get

`RUN` 指令最常見的用法是安裝套件用的 `apt-get`。因為 `RUN apt-get` 指令會安裝套件，所以有幾個問題需要注意。

不要使用 `RUN apt-get upgrade` 或 `dist-upgrade`，因為許多基礎映像檔中的「必須」套件不會在一個非特權容器中升級。如果基礎映像檔中的某個套件過時了，你應該聯繫它的維護者。如果你確定某個特定的套件，比如 `foo`，需要升級，使用 `apt-get install -y foo` 就行，該指令會自動升級 `foo` 套件。

永遠將 `RUN apt-get update` 和 `apt-get install` 組合成一條 `RUN` 聲明，例如：

```docker
RUN apt-get update && apt-get install -y \
        package-bar \
        package-baz \
        package-foo
```

將 `apt-get update` 放在一條單獨的 `RUN` 聲明中會導致快取問題以及後續的 `apt-get install` 失敗。比如，假設你有一個 `Dockerfile` 檔案：

```docker
FROM ubuntu:24.04

RUN apt-get update

RUN apt-get install -y curl
```

建立映像檔後，所有的層都在 Docker 的快取中。假設你後來又修改了其中的 `apt-get install` 添加了一個套件：

```docker
FROM ubuntu:24.04

RUN apt-get update

RUN apt-get install -y curl nginx
```

Docker 發現修改後的 `RUN apt-get update` 指令和之前的完全一樣。所以，`apt-get update` 不會執行，而是使用之前的快取映像檔。因為 `apt-get update` 沒有執行，後面的 `apt-get install` 可能安裝的是過時的 `curl` 和 `nginx` 版本。

使用 `RUN apt-get update && apt-get install -y` 可以確保你的 Dockerfiles 每次安裝的都是套件的最新的版本，而且這個過程不需要進一步的編碼或額外干預。這項技術叫作 `cache busting`。你也可以顯式指定一個套件的版本號來達到 `cache-busting`，這就是所謂的固定版本，例如：

```docker
RUN apt-get update && apt-get install -y \
    package-bar \
    package-baz \
    package-foo=1.3.*
```

固定版本會迫使建立過程檢索特定的版本，而不管快取中有什麼。這項技術也可以減少因所需套件中未預料到的變化而導致的失敗。

下面是一個 `RUN` 指令的示例模板，展示了所有關於 `apt-get` 的建議。

```docker
RUN apt-get update && apt-get install -y \
    aufs-tools \
    automake \
    build-essential \
    curl \
    dpkg-sig \
    libcap-dev \
    libsqlite3-dev \
    git \
    redis-server \
 && rm -rf /var/lib/apt/lists/*
```

其中 `redis-server` 是示例套件。確保安裝的是最新版本。

另外，清理掉 apt 快取 `var/lib/apt/lists` 可以減小映像檔大小。因為 `RUN` 指令的開頭為 `apt-get update`，套件快取總是會在 `apt-get install` 之前刷新。

> 注意：官方的 Debian 和 Ubuntu 映像檔會自動執行 apt-get clean，所以不需要顯式的呼叫 apt-get clean。

#### CMD

`CMD` 指令用於執行目標映像檔中包含的軟體，可以包含參數。`CMD` 大多數情況下都應該以 `CMD ["executable", "param1", "param2"...]` 的形式使用。因此，如果建立映像檔的目的是為了部署某個服務（比如 `Apache`），你可能會執行類似於 `CMD ["apache2", "-DFOREGROUND"]` 形式的命令。我們建議任何服務映像檔都使用這種形式的命令。

> 注意：exec 形式是 JSON 陣列，**必須用雙引號**。寫成 `CMD ['apache2', '-DFOREGROUND']` 並不會報錯，但 Docker 解析不出 JSON，會退回 shell 形式執行整串字元，導致啟動失敗。參見 [7.4 CMD](../dockerfile/cmd.md)。

多數情況下，`CMD` 都需要一個互動式的 `shell`（bash，Python，perl 等），例如 `CMD ["perl", "-de0"]`，或者 `CMD ["php", "-a"]`。使用這種形式意味著，當你執行類似 `docker run -it python` 時，你會進入一個準備好的 `shell` 中。`CMD` 應該在極少的情況下才能以 `CMD ["param", "param"]` 的形式與 `ENTRYPOINT` 協同使用，除非你和你的映像檔使用者都對 `ENTRYPOINT` 的工作方式十分熟悉。

#### EXPOSE

`EXPOSE` 指令用於指定容器將要監聽的埠號。因此，你應該為你的應用程式使用常見的埠號。例如，提供 `Apache` web 服務的映像檔應該使用 `EXPOSE 80`，而提供 `MongoDB` 服務的映像檔使用 `EXPOSE 27017`。

對於外部存取，使用者可以在執行 `docker run` 時使用一個標誌來指示如何將指定的埠號映射到所選擇的埠號。

#### ENV

為了方便新程式執行，你可以使用 `ENV` 來為容器中安裝的程式更新 `PATH` 環境變數。例如使用 `ENV PATH=/usr/local/nginx/bin:$PATH` 來確保 `CMD ["nginx"]` 能正確執行。

`ENV` 指令也可用於為你想要容器化的服務提供必要的環境變數，比如 Postgres 需要的 `PGDATA`。

最後，`ENV` 也能用於設定常見的版本號，比如下面的示例：

```docker
ENV PG_MAJOR=9.3

ENV PG_VERSION=9.3.4

RUN curl -SL http://example.com/postgres-$PG_VERSION.tar.xz | tar -xJC /usr/src/postgres && …

ENV PATH=/usr/local/postgres-$PG_MAJOR/bin:$PATH
```

類似於程式中的常量，這種方法可以讓你只需改變 `ENV` 指令來自動的改變容器中的軟體版本。

#### ADD 和 COPY

雖然 `ADD` 和 `COPY` 功能類似，但一般優先使用 `COPY`。因為它比 `ADD` 更透明。`COPY` 只支援簡單將本地檔案拷貝到容器中，而 `ADD` 有一些並不明顯的功能（比如本地 tar 提取和遠端 URL 支援）。因此，`ADD` 的最佳用例是將本地 tar 檔案自動提取到映像檔中，例如 `ADD rootfs.tar.xz`。

如果你的 `Dockerfile` 有多個步驟需要使用上下文中不同的檔案。單獨 `COPY` 每個檔案，而不是一次性的 `COPY` 所有檔案，這將保證每個步驟的建立快取只在特定的檔案變化時失效。例如：

```docker
COPY requirements.txt /tmp/

RUN pip install --requirement /tmp/requirements.txt

COPY . /tmp/
```

如果將 `COPY . /tmp/` 放置在 `RUN` 指令之前，只要 `.` 目錄中任何一個檔案變化，都會導致後續指令的快取失效。

為了讓映像檔盡量小，最好不要使用 `ADD` 指令從遠端 URL 取得套件，而是使用 `curl` 和 `wget`。這樣你可以在檔案提取完之後刪掉不再需要的檔案來避免在映像檔中額外添加一層。比如盡量避免下面的用法：

```docker
ADD http://example.com/big.tar.xz /usr/src/things/

RUN tar -xJf /usr/src/things/big.tar.xz -C /usr/src/things

RUN make -C /usr/src/things all
```

而是應該使用下面這種方法：

```docker
RUN mkdir -p /usr/src/things \
    && curl -SL http://example.com/big.tar.xz \
    | tar -xJC /usr/src/things \
    && make -C /usr/src/things all
```

上面使用的管道操作，所以沒有中間檔案需要刪除。

對於其他不需要 `ADD` 的自動提取功能的檔案或目錄，你應該使用 `COPY`。

#### ENTRYPOINT

`ENTRYPOINT` 的最佳用處是設定映像檔的主命令，允許將映像檔當成命令本身來執行（用 `CMD` 提供預設選項）。

例如，下面的示例映像檔提供了命令行工具 `s3cmd`：

```docker
ENTRYPOINT ["s3cmd"]

CMD ["--help"]
```

現在直接執行該映像檔建立的容器會顯示命令幫助：

```bash
$ docker run s3cmd
```

或者提供正確的參數來執行某個命令：

```bash
$ docker run s3cmd ls s3://mybucket
```

這樣映像檔名可以當成命令行的參考。

`ENTRYPOINT` 指令也可以結合一個輔助腳本使用，和前面命令行風格類似，即使啟動工具需要不止一個步驟。

例如，`Postgres` 官方映像檔使用下面的腳本作為 `ENTRYPOINT`：

```bash
#!/bin/bash
set -e

if [ "$1" = 'postgres' ]; then
    chown -R postgres "$PGDATA"

    if [ -z "$(ls -A "$PGDATA")" ]; then
        gosu postgres initdb
    fi

    exec gosu postgres "$@"
fi

exec "$@"
```

> 注意：該腳本使用了 Bash 的內建命令 exec，所以最後執行的程式就是容器的 PID 為 1 的程式。這樣，程式就可以接收到任何發送給容器的 Unix 訊號了。

該輔助腳本被拷貝到容器，並在容器啟動時透過 `ENTRYPOINT` 執行：

```docker
COPY ./docker-entrypoint.sh /

ENTRYPOINT ["/docker-entrypoint.sh"]
```

該腳本可以讓使用者用幾種不同的方式和 `Postgres` 互動。

你可以很簡單地啟動 `Postgres`：

```bash
$ docker run postgres
```

也可以執行 `Postgres` 並傳遞參數：

```bash
$ docker run postgres postgres --help
```

最後，你還可以啟動另外一個完全不同的工具，比如 `Bash`：

```bash
$ docker run --rm -it postgres bash
```

#### VOLUME

`VOLUME` 指令用於暴露任何資料庫儲存檔案，設定檔案，或容器建立的檔案和目錄。強烈建議使用 `VOLUME` 來管理映像檔中的可變部分和使用者可以改變的部分。

#### USER

如果某個服務不需要特權執行，建議使用 `USER` 指令切換到非 root 使用者。先在 `Dockerfile` 中使用類似 `RUN groupadd -r postgres && useradd -r -g postgres postgres` 的指令建立使用者和使用者群組。

> 注意：在映像檔中，使用者和使用者群組每次被分配的 UID/GID 都是不確定的，下次重新建立映像檔時被分配到的 UID/GID 可能會不一樣。如果要依賴確定的 UID/GID，你應該顯式的指定一個 UID/GID。

你應該避免使用 `sudo`，因為它不可預期的 TTY 和訊號轉發行為可能造成的問題比它能解決的問題還多。如果你真的需要和 `sudo` 類似的功能（例如，以 root 權限初始化某個守護程式，以非 root 權限執行它），你可以使用 [gosu](https://github.com/tianon/gosu)。

最後，為了減少層數和複雜度，避免頻繁地使用 `USER` 來回切換使用者。

#### WORKDIR

為了清晰性和可靠性，你應該總是在 `WORKDIR` 中使用絕對路徑。另外，你應該使用 `WORKDIR` 來替代類似於 `RUN cd ... && do-something` 的指令，後者難以閱讀、排錯和維護。

### 官方映像檔示例

這些官方映像檔的 Dockerfile 都是參考典範，詳見 [docker-library/docs](https://github.com/docker-library/docs)。

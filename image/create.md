## 使用 Dockerfile 建立映像檔

從剛才的 `docker commit` 的學習中，我們可以了解到，映像檔的建立實際上就是建立每一層所添加的設定、檔案。如果我們可以把每一層修改、安裝、建立、操作的命令都寫入一個腳本，用這個腳本來建立、建立映像檔，那麼之前提及的無法重複、映像檔建立不透明、體積難以控制等問題就會更容易解決。這個腳本就是 Dockerfile。

Dockerfile 是一個文字檔案，其內包含了一條條的 **指令 (Instruction)**。其中，會修改檔案系統的指令通常會建立新層；而 `LABEL`、`CMD` 這類只修改映像檔中繼資料的指令，則不會新增檔案系統層。每一條指令的內容，都是在描述該映像檔應當如何建立。

### 使用 docker init 快速建立：推薦

Docker 提供了 `docker init` 命令，可以根據專案類型自動產生 `Dockerfile`、`.dockerignore`、`compose.yaml` 和 `README.Docker.md` 等檔案：

```bash
$ docker init
```
該命令會互動式地詢問專案類型（支援 Go、Node.js、Python、Rust、Java、ASP.NET Core、PHP with Apache 等），並產生可作為起點的設定檔案。對於新專案，這是一個很好的起步方式，但產生後的內容仍應結合專案實際情況繼續調整。

### 手動建立 Dockerfile

還以之前建立 `nginx` 映像檔為例，這次我們使用 Dockerfile 來建立。

在一個空白目錄中，建立一個文字檔案，並命名為 `Dockerfile`：

```bash
$ mkdir mynginx
$ cd mynginx
$ touch Dockerfile
```
其內容為：

> **版本提示**：下面範例中 `FROM nginx` 使用的是 `latest` 標籤。在實際應用中應使用明確的版本號（如 `FROM nginx:1.28`），以確保 Dockerfile 的可重現性和穩定性。

```docker
FROM nginx
RUN echo '<h1>Hello, Docker!</h1>' > /usr/share/nginx/html/index.html
```
這個 Dockerfile 很簡單，一共就兩行。涉及到了兩條指令，`FROM` 和 `RUN`。

### FROM 指定基礎映像檔

所謂建立映像檔，那一定是以一個映像檔為基礎，在其上進行建立。就像我們之前執行了一個 `nginx` 映像檔的容器，再進行修改一樣，基礎映像檔是必須指定的。而 `FROM` 就是指定 **基礎映像檔**，因此一個 `Dockerfile` 中 `FROM` 是必備的指令，並且必須是第一條**建立指令**——按官方 Dockerfile 參考，它之前只允許出現 parser 指令、註解和全域作用域的 `ARG`，`ARG` 是唯一能寫在 `FROM` 之前的指令（見 [ARG 建立參數](../dockerfile/arg.md)）。

> **版本號最佳實踐**：在 `FROM` 指令中 **務必指定具體版本號**（如 `FROM ubuntu:24.04` 或 `FROM python:3.12-slim`）而非 `FROM ubuntu` 或 `FROM python:latest`。這樣可以確保 Dockerfile 在不同時間、不同環境下建立出的映像檔內容一致，避免因基礎映像檔更新導致的不可預期的變化。

在 [Docker Hub](https://hub.docker.com/search?q=&type=image&image_filter=official) 上有非常多的高品質的官方映像檔，有可以直接拿來使用的服務類的映像檔，如 [`nginx`](https://hub.docker.com/_/nginx/)、[`redis`](https://hub.docker.com/_/redis/)、[`mongo`](https://hub.docker.com/_/mongo/)、[`mysql`](https://hub.docker.com/_/mysql/)、[`httpd`](https://hub.docker.com/_/httpd/)、[`php`](https://hub.docker.com/_/php/)、[`tomcat`](https://hub.docker.com/_/tomcat/) 等；也有一些方便開發、建立、執行各種語言應用的映像檔，如 [`node`](https://hub.docker.com/_/node)、[`eclipse-temurin`](https://hub.docker.com/_/eclipse-temurin/)、[`python`](https://hub.docker.com/_/python/)、[`ruby`](https://hub.docker.com/_/ruby/)、[`golang`](https://hub.docker.com/_/golang/) 等。可以在其中尋找一個最符合我們最終目標的映像檔為基礎映像檔進行建立。

如果沒有找到對應服務的映像檔，官方映像檔中還提供了一些更為基礎的作業系統映像檔，如 [`ubuntu`](https://hub.docker.com/_/ubuntu/)、[`debian`](https://hub.docker.com/_/debian/)、[`centos`](https://hub.docker.com/_/centos/)、[`fedora`](https://hub.docker.com/_/fedora/)、[`alpine`](https://hub.docker.com/_/alpine/) 等，這些作業系統的軟體庫為我們提供了更廣闊的擴充空間。

除了選擇現有映像檔為基礎映像檔外，Docker 還存在一個特殊的映像檔，名為 `scratch`。這個映像檔是虛擬的概念，並不實際存在，它表示一個空白的映像檔。

```docker
FROM scratch
...
```
如果你以 `scratch` 為基礎映像檔的話，意味著你不以任何映像檔為基礎，接下來所寫的指令將作為映像檔第一層開始存在。

不以任何系統為基礎，直接將可執行檔案複製進映像檔的做法並不罕見，對於 Linux 下靜態編譯的程式來說，並不需要有作業系統提供執行時期支援，所需的一切庫都已經在可執行檔案裡了，因此直接 `FROM scratch` 會讓映像檔體積更加小巧。使用 [Go 語言](https://golang.google.cn/)開發的應用很多會使用這種方式來製作映像檔，這也是有人認為 Go 是特別適合容器微服務架構的語言的原因之一。

### RUN 執行命令

`RUN` 指令是用來執行命令行命令的。由於命令列的強大能力，`RUN` 指令在建立映像檔時是最常用的指令之一。其格式有兩種：

* *shell* 格式：`RUN <命令>`，就像直接在命令行中輸入的命令一樣。剛才寫的 Dockerfile 中的 `RUN` 指令就是這種格式。

```docker
RUN echo '<h1>Hello, Docker!</h1>' > /usr/share/nginx/html/index.html
```

* *exec* 格式：`RUN ["可執行檔案", "參數1", "參數2"]`，這更像是函式呼叫中的格式。

在會修改檔案系統的指令裡，`RUN` 是最典型的一類。每一個 `RUN` 的行為，都可以類比為我們剛才手動建立映像檔的過程：先基於當前結果啟動一個臨時建立環境，在其上執行這些命令，再把這一步產生的檔案系統變化儲存為新的結果層。

> **注意**
>
> 每一個 `RUN` 指令都會產生一個新的映像檔層。為了減少映像檔體積和層數，我們通常會將多個命令合併到一個 `RUN` 指令中執行。
>
> 更多關於 `RUN` 指令的詳細用法、最佳實踐（如清理快取、使用 pipefail 等）及 `Union FS` 的層數限制等內容，請參閱 **[Dockerfile](../dockerfile/README.md)** 章節中的 **[RUN 執行命令](../dockerfile/run.md)** 小節。

要想編寫優秀的 `Dockerfile`，必須了解每一條指令的作用和副作用。在 **[Dockerfile](../dockerfile/README.md)** 章節中，我們將對 `COPY`，`ADD`，`CMD`，`ENTRYPOINT` 等指令進行詳細講解。

### 建立映像檔

好了，讓我們再回到之前建立的 nginx 映像檔的 Dockerfile 來。現在我們明白了這個 Dockerfile 的內容，那麼讓我們來建立這個映像檔吧。

在 `Dockerfile` 檔案所在目錄執行：

```bash
$ docker build -t nginx:v3 .
```

在當前版本的 Docker 中，`docker build` 預設會透過 Buildx 呼叫 BuildKit，因此你更常看到的是 `[+] Building ...` 這類輸出。為了幫助理解「每一步如何形成映像檔歷史」，下面仍展示一種較容易閱讀的經典輸出形式：

```bash
Sending build context to Docker daemon 2.048 kB
Step 1 : FROM nginx
 ---> e43d811ce2f4
Step 2 : RUN echo '<h1>Hello, Docker!</h1>' > /usr/share/nginx/html/index.html
 ---> Running in 9cdc27646c7b
 ---> 44aa4490ce2c
Removing intermediate container 9cdc27646c7b
Successfully built 44aa4490ce2c
```
從命令的輸出結果中，我們可以清晰地看到映像檔的建立過程。在 `Step 2` 中，如同我們之前所說的那樣，`RUN` 指令啟動了一個容器 `9cdc27646c7b`，執行了所要求的命令，並最後提交了這一層 `44aa4490ce2c`，隨後刪除了所用到的這個容器 `9cdc27646c7b`。

這裡我們使用了 `docker build` 命令進行映像檔建立。其格式為：

```bash
docker build [選項] <上下文路徑/URL/->
```
在這裡我們指定了最終映像檔的名稱 `-t nginx:v3`，建立成功後，我們可以像之前執行 `nginx:v2` 那樣來執行這個映像檔，其結果會和 `nginx:v2` 一樣。

### 映像檔建立上下文

如果注意，會看到 `docker build` 命令最後有一個 `.`。`.` 表示當前目錄，而 `Dockerfile` 就在當前目錄，因此不少初學者以為這個路徑是在指定 `Dockerfile` 所在路徑，這麼理解其實是不準確的。如果對應上面的命令格式，你可能會發現，這是在指定 **上下文路徑**。那麼什麼是上下文呢？

首先要理解 `docker build` 的工作原理。今天的 `docker build` 預設會透過 Buildx 向 BuildKit 後端發起建立請求；無論後端執行在本機還是遠端，位置參數指定的都是 **建立上下文**，也就是建立器可以存取到的檔案集合。

當我們進行映像檔建立的時候，並非所有建立都會透過 `RUN` 指令完成，經常還需要把本機檔案複製進映像檔，比如透過 `COPY` 指令、`ADD` 指令等。因此，建立器必須能夠存取這些檔案，而它能存取的範圍正是你傳給 `docker build` 的那個上下文。

如果上下文是本機目錄，那麼這個目錄中的檔案和子目錄就會成為可用輸入；如果上下文是遠端 Git 倉庫或 tar 包，那麼建立器會直接取得對應內容。對於本機目錄，BuildKit 會按需讀取建立過程中真正需要的檔案，而不是讓 Dockerfile 任意存取宿主主機上的任意路徑。

如果在 `Dockerfile` 中這麼寫：

```docker
COPY ./package.json /app/
```
這並不是要複製執行 `docker build` 命令所在的目錄下的 `package.json`，也不是複製 `Dockerfile` 所在目錄下的 `package.json`，而是複製 **上下文 (context)** 目錄下的 `package.json`。

因此，`COPY` 這類指令中的來源檔案路徑都應該以建立上下文為基準來理解。對於 legacy builder，像 `COPY ../package.json /app` 這樣的寫法會直接報錯；而在 BuildKit 下，前導的越界 `../` 會被剝離並重新解釋為上下文內路徑。無論是哪種情況，建立器都無法讀取上下文之外的宿主主機檔案；如果真的需要那些檔案，應該先把它們放進上下文目錄，或重新選擇合適的上下文。

現在就可以理解剛才的命令 `docker build -t nginx:v3 .` 中的這個 `.`，實際上是在指定上下文目錄，而不是單純指定 `Dockerfile` 所在目錄。

如果觀察 `docker build` 的經典輸出，或 BuildKit 輸出中的 `transferring context` 提示，我們其實都能看到上下文傳輸的過程：

```bash
$ docker build -t nginx:v3 .
Sending build context to Docker daemon 2.048 kB
...
```
理解建立上下文對於映像檔建立是很重要的，避免犯一些不應該的錯誤。比如有些初學者在發現需要的檔案不在上下文裡後，乾脆把上下文切到硬碟根目錄去建立。這樣做即使在 BuildKit 下也會讓可見上下文變得過大，並且在使用 `COPY . .`、`ADD . /app` 之類寫法時，仍可能觸發大規模上下文傳輸，導致建立緩慢甚至失敗。這顯然是使用錯誤。

一般來說，應該會將 `Dockerfile` 置於一個空目錄下，或者專案根目錄下。如果該目錄下沒有所需檔案，那麼應該把所需檔案複製一份過來。如果目錄下有些東西確實不希望建立時傳給 Docker 引擎，那麼可以用 `.gitignore` 一樣的語法寫一個 `.dockerignore`，該檔案是用於剔除不需要作為上下文傳遞給 Docker 引擎的。

那麼為什麼會有人誤以為 `.` 是指定 `Dockerfile` 所在目錄呢？這是因為在預設情況下，如果不額外指定 `Dockerfile` 的話，會將上下文目錄下的名為 `Dockerfile` 的檔案作為 Dockerfile。

這只是預設行為，實際上 `Dockerfile` 的檔案名並不要求必須為 `Dockerfile`，而且並不要求必須位於上下文目錄中，比如可以用 `-f ../Dockerfile.php` 參數指定某個檔案作為 `Dockerfile`。

當然，一般大家習慣性的會使用預設的檔案名 `Dockerfile`，以及會將其置於映像檔建立上下文目錄中。

### 其他 `docker build` 的用法

#### 直接用 Git repo 進行建立

或許你已經注意到了，`docker build` 還支援從 URL 建立，也就是直接把遠端 Git 倉庫作為上下文。傳統寫法可以使用 URL 片段 `#ref:dir`，例如：

```bash
$ docker build https://github.com/user/myrepo.git#mybranch:docker
```
這行命令表示：把 Git 倉庫作為建立上下文，使用 `mybranch` 分支中的 `docker/` 子目錄來建立。在較新的 Buildx 中，也可以改用結構更清晰的查詢參數寫法，例如 `?branch=mybranch&subdir=docker`。

#### 用給定的 tar 壓縮包建立

```bash
$ docker build http://server/context.tar.gz
```
如果所給出的 URL 不是個 Git repo，而是個 `tar` 壓縮包，那麼 Docker 引擎會下載這個包，並自動解壓縮，以其作為上下文，開始建立。

#### 從標準輸入中讀取 Dockerfile 進行建立

```bash
docker build - < Dockerfile
```
或

```bash
cat Dockerfile | docker build -
```
如果標準輸入傳入的是文字檔案，則將其視為 `Dockerfile`，並開始建立。這種形式由於直接從標準輸入中讀取 Dockerfile 的內容，它沒有上下文，因此不可以像其他方法那樣可以將本機檔案 `COPY` 進映像檔之類的事情。

#### 從標準輸入中讀取上下文壓縮包進行建立

```bash
$ docker build - < context.tar.gz
```
如果發現標準輸入的檔案格式是 `gzip`、`bzip2` 以及 `xz` 的話，將會將其視為上下文壓縮包，直接將其展開，將裡面視為上下文，並開始建立。

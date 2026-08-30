## 客戶端命令 - docker

### 客戶端命令選項

* `--config=""`：指定客戶端設定檔案，預設為 `~/.docker`；
* `-D=true|false`：是否使用 debug 模式。預設不開啟；
* `-H, --host=[]`：指定命令對應 Docker 守護程式的監聽介面，可以為 unix 套接字 `unix:///path/to/socket`，檔案句柄 `fd://socketfd` 或 tcp 套接字 `tcp://[host[:port]]`，預設為 `unix:///var/run/docker.sock`；
* `-c, --context=""`：指定連線守護程式時使用的上下文名稱，優先於 `DOCKER_HOST` 環境變數和 `docker context use` 設定的預設上下文；
* `-l, --log-level="debug|info|warn|error|fatal"`：指定日誌輸出級別；
* `--tls=true|false`：是否對 Docker 守護程式啟用 TLS 安全機制，預設為否；
* `--tlscacert=~/.docker/ca.pem`：TLS CA 簽章的可信憑證檔案路徑；
* `--tlscert=~/.docker/cert.pem`：TLS 可信憑證檔案路徑；
* `--tlskey=~/.docker/key.pem`：TLS 金鑰檔案路徑；
* `--tlsverify=true|false`：啟用 TLS 校驗，預設為否。

### 客戶端命令

可以透過 `docker COMMAND --help` 來查看這些命令的具體用法。

* `attach`：依附到一個正在執行的容器中；
* `build`：從一個 Dockerfile 建立一個映像檔；
* `builder`：管理建立器與建立快取，包括查看、清理等；
* `buildx`：擴充建立能力 (BuildKit)，支援多平台建立、建立快取匯入匯出等（CLI 外掛程式，詳見第 10 章）；
* `checkpoint`：管理容器檢查點，用於保存和恢復容器執行狀態（實驗特性）；
* `commit`：從一個容器的修改中建立一個新的映像檔；
* `compose`：定義並執行多容器應用（CLI 外掛程式，詳見第 11 章）；
* `config`：管理 swarm 集群中的設定項，包括建立、查看、刪除等；
* `container`：管理容器，`run`、`ps`、`exec` 等均是其子命令的快捷形式；
* `context`：管理連線上下文，在多個 Docker 守護程式之間切換；
* `cp`：在容器和本地宿主系統之間複製檔案；
* `create`：建立一個新容器，但並不執行它；
* `diff`：檢查一個容器內檔案系統的修改，包括修改和增加；
* `events`：從服務端取得即時的事件；
* `exec`：在執行的容器內執行命令；
* `export`：匯出容器內容為一個 `tar` 包；
* `history`：顯示一個映像檔的歷史資訊；
* `image`：管理映像檔，`images`、`pull`、`build` 等均是其子命令的快捷形式；
* `images`：列出存在的映像檔；
* `import`：匯入一個檔案（典型為 `tar` 包）路徑或目錄來建立一個本地映像檔；
* `info`：顯示一些相關的系統資訊；
* `init`：為專案產生 Dockerfile、compose.yaml 等初始檔案（CLI 外掛程式）；
* `inspect`：顯示一個容器的具體設定資訊；
* `kill`：關閉一個執行中的容器（包括程式和所有相關資源）；
* `load`：從一個 tar 包中載入一個映像檔；
* `login`：註冊或登錄到一個 Docker 的倉庫伺服器；
* `logout`：從 Docker 的倉庫伺服器登出；
* `logs`：取得容器的 log 資訊；
* `manifest`：管理映像檔的 manifest 與 manifest list，用於發布多架構映像檔；
* `network`：管理 Docker 的網路，包括查看、建立、刪除、掛載、卸載等；
* `node`：管理 swarm 集群中的節點，包括查看、更新、刪除、提升/取消管理節點等；
* `pause`：暫停一個容器中的所有程式；
* `plugin`：管理 Docker 外掛程式，包括安裝、啟用、停用、刪除等；
* `port`：查找一個 nat 到一個私有網口的公共口；
* `ps`：列出主機上的容器；
* `pull`：從一個 Docker 的倉庫伺服器下拉一個映像檔或倉庫；
* `push`：將一個映像檔或者倉庫推送到一個 Docker 的註冊伺服器；
* `rename`：重新命名一個容器；
* `restart`：重新啟動一個執行中的容器；
* `rm`：刪除給定的若干個容器；
* `rmi`：刪除給定的若干個映像檔；
* `run`：建立一個新容器，並在其中執行給定命令；
* `save`：保存一個映像檔為 tar 包檔案；
* `scout`：分析映像檔的軟體成分與已知漏洞（CLI 外掛程式）；
* `search`：在 Docker Hub 中搜尋映像檔；
* `secret`：管理 swarm 集群中的金鑰，包括建立、查看、刪除等；
* `service`：管理 Docker 所啟動的應用服務，包括建立、更新、刪除等；
* `stack`：管理 swarm 集群中的應用棧，包括部署、查看、刪除等；
* `start`：啟動一個容器；
* `stats`：輸出（一個或多個）容器的資源使用統計資訊；
* `stop`：終止一個執行中的容器；
* `swarm`：管理 Docker swarm 集群，包括建立、加入、退出、更新等；
* `system`：管理 Docker 本身，包括查看磁碟占用、清理無用資料、訂閱事件等；
* `tag`：為一個映像檔打標籤；
* `top`：查看一個容器中的正在執行的程式資訊；
* `unpause`：將一個容器內所有的程式從暫停狀態中恢復；
* `update`：更新指定的若干容器的設定資訊；
* `version`：輸出 Docker 的版本資訊；
* `volume`：管理 Docker volume，包括查看、建立、刪除等；
* `wait`：阻塞直到一個容器終止，然後輸出它的退出符。

### 一張圖總結 Docker 的命令

如圖 A-1 所示，Docker 常用客戶端命令可按功能分組理解。

![Docker 命令總結](../_images/cmd_logic.jpg)

圖 A-1：Docker 客戶端命令分類示意圖

### 參考

* [官方文件](https://docs.docker.com/reference/cli/docker/)

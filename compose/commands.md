## 命令說明

Docker Compose 提供了豐富的命令來管理專案和容器。本節將詳細介紹這些命令的使用格式和常用選項。

### 何時用哪個命令：場景化指南

在學習具體命令前，讓我們從使用場景出發，這樣可以幫助你更快地找到需要的命令：

**專案啟動與停止**：

- `docker compose up`：第一次啟動專案，拉取映像檔、建立容器
- `docker compose start`：啟動已停止的容器（專案已存在）
- `docker compose stop`：優雅地停止容器（不刪除容器）
- `docker compose down`：完全清理，刪除容器和網路（開發時常用）

**除錯與查看**：

- `docker compose ps`：查看專案中的容器狀態
- `docker compose logs`：查看容器日誌（排查問題的第一步）
- `docker compose exec`：進入正在執行的容器執行命令

**建立與更新**：

- `docker compose build`：重新建立映像檔（修改 Dockerfile 後）
- `docker compose pull`：更新所有映像檔到最新版本

**設定驗證**：

- `docker compose config`：驗證 docker-compose.yml 格式是否正確

### 命令物件與格式

對於 Compose 來說，大部分命令的物件既可以是專案本身，也可以指定為專案中的服務或者容器。如果沒有特別的說明，命令物件將是專案，這意味著專案中所有的服務都會受到命令影響。

執行 `docker compose [COMMAND] --help` 或者 `docker compose help [COMMAND]` 可以查看具體某個命令的使用格式。

`docker compose` 命令的基本的使用格式是

```bash
docker compose [-f=<arg>...] [options] [COMMAND] [ARGS...]
```

### 命令選項

* `-f, --file FILE` 指定使用的 Compose 模板檔案。預設會自動識別 `compose.yaml`（也相容 `docker-compose.yml` 等），並且可以多次指定。

* `-p, --project-name NAME` 指定專案名稱，預設將使用所在目錄名稱作為專案名。

* `--verbose` 輸出更多除錯資訊。（Compose V2 中該選項仍然生效，但已從 `--help` 中隱藏，不再是推薦用法；請改用 `docker --log-level debug compose ...`。）

* `-v, --version` 印出版本並退出。

### 命令使用說明

#### `build`

格式為 `docker compose build [options] [SERVICE...]`。

建立（重新建立）專案中的服務容器。

服務容器一旦建立後，將會帶上一個標記名，例如對於 web 專案中的一個 db 服務，建立出的映像檔是 `web-db`。（Compose V1 用底線拼接為 `web_db`，V2 起統一改為連字元，只有加 `--compatibility` 才會回到底線。）

可以隨時在專案目錄下執行 `docker compose build` 來重新建立服務。

選項包括：

* `--force-rm` 刪除建立過程中的臨時容器。

* `--no-cache` 建立映像檔過程中不使用 cache（這將加長建立過程）。

* `--pull` 始終嘗試透過 pull 來取得更新版本的映像檔。

#### `config`

驗證 Compose 檔案格式是否正確，若正確則顯示設定，若格式錯誤顯示錯誤原因。

#### `down`

此命令將會停止 `up` 命令所啟動的容器，並移除網路

#### `exec`

進入指定的容器。

#### `help`

獲得一個命令的幫助。

#### `images`

列出 Compose 檔案中包含的映像檔。

#### `kill`

格式為 `docker compose kill [options] [SERVICE...]`。

透過傳送 `SIGKILL` 訊號來強制停止服務容器。

支援透過 `-s` 參數來指定傳送的訊號，例如透過如下指令傳送 `SIGINT` 訊號。

```bash
$ docker compose kill -s SIGINT
```

#### `logs`

格式為 `docker compose logs [options] [SERVICE...]`。

查看服務容器的輸出。預設情況下，docker compose 將對不同的服務輸出使用不同的顏色來區分。可以透過 `--no-color` 來關閉顏色。

該命令在除錯問題的時候十分有用。

#### `pause`

格式為 `docker compose pause [SERVICE...]`。

暫停一個服務容器。

#### `port`

格式為 `docker compose port [options] SERVICE PRIVATE_PORT`。

印出某個容器埠號所映射的公共埠號。

選項：

* `--protocol=proto` 指定埠號協定，tcp（預設值）或者 udp。

* `--index=index` 如果同一服務存在多個容器，指定命令物件容器的序號（預設為 1）。

#### `ps`

格式為 `docker compose ps [options] [SERVICE...]`。

列出專案中目前的所有容器。

選項：

* `-q` 只印出容器的 ID 資訊。

#### `pull`

格式為 `docker compose pull [options] [SERVICE...]`。

拉取服務依賴的映像檔。

選項：

* `--ignore-pull-failures` 忽略拉取映像檔過程中的錯誤。

#### `push`

推送服務依賴的映像檔到 Docker 映像檔倉庫。

#### `restart`

格式為 `docker compose restart [options] [SERVICE...]`。

重啟專案中的服務。

選項：

* `-t, --timeout TIMEOUT` 指定重啟前停止容器的逾時（預設為 10 秒）。

#### `rm`

格式為 `docker compose rm [options] [SERVICE...]`。

刪除所有（停止狀態的）服務容器。推薦先執行 `docker compose stop` 命令來停止容器。

選項：

* `-f, --force` 強制直接刪除，包括非停止狀態的容器。一般儘量不要使用該選項。

* `-v` 刪除容器所掛載的資料卷。

#### `run`

格式為 `docker compose run [options] [-p PORT...] [-e KEY=VAL...] SERVICE [COMMAND] [ARGS...]`。

在指定服務上執行一個命令。

例如：

```bash
$ docker compose run ubuntu ping docker.com
```
將會啟動一個 ubuntu 服務容器，並執行 `ping docker.com` 命令。

預設情況下，如果存在關聯，則所有關聯的服務將會自動被啟動，除非這些服務已經在執行中。

該命令類似啟動容器後執行指定的命令，相關卷、連結等等都將會按照設定自動建立。

兩個不同點：

* 給定命令將會覆蓋原有的自動執行命令；

* 不會自動建立埠號，以避免衝突。

如果不希望自動啟動關聯的容器，可以使用 `--no-deps` 選項，例如

```bash
$ docker compose run --no-deps web python manage.py shell
```
將不會啟動 web 容器所關聯的其他容器。

選項：

* `-d` 背景執行容器。

* `--name NAME` 為容器指定一個名字。

* `--entrypoint CMD` 覆蓋預設的容器啟動指令。

* `-e KEY=VAL` 設定環境變數值，可多次使用選項來設定多個環境變數。

* `-u, --user=""` 指定執行容器的使用者名稱或者 uid。

* `--no-deps` 不自動啟動關聯的服務容器。

* `--rm` 執行命令後自動刪除容器，`d` 模式下將忽略。

* `-p, --publish=[]` 映射容器埠號到本地主機。

* `--service-ports` 設定服務埠號並映射到本地主機。

* `-T` 不分配偽 tty，意味著依賴 tty 的指令將無法執行。

#### `scale`

目前 Compose CLI 仍支援 `docker compose scale`。實際使用中，更常見也更便於和建立/重建流程放在一起的寫法是透過 `docker compose up --scale` 完成。

例如：

```bash
$ docker compose up -d --scale web=3 --scale db=2
```

將啟動 3 個容器執行 `web` 服務，2 個容器執行 `db` 服務。

> **說明**：如果 Compose 檔案為服務指定了 `container_name`，該服務無法擴展到多個容器。需要擴縮容的服務應使用 Compose 自動產生的容器名，並透過服務名做 DNS 存取。

一般的，當指定數目多於該服務目前實際執行容器，將新建立並啟動容器；反之，將停止容器。

常用搭配選項：

* `-d` 背景啟動。
* `--scale SERVICE=NUM` 指定服務實例數量，可重複使用。

#### `start`

格式為 `docker compose start [SERVICE...]`。

啟動已經存在的服務容器。

#### `stop`

格式為 `docker compose stop [options] [SERVICE...]`。

停止已經處於執行狀態的容器，但不刪除它。透過 `docker compose start` 可以再次啟動這些容器。

選項：

* `-t, --timeout TIMEOUT` 停止容器時候的逾時（預設為 10 秒）。

#### `top`

查看各個服務容器內執行的程式。

#### `unpause`

格式為 `docker compose unpause [SERVICE...]`。

恢復處於暫停狀態中的服務。

#### `up`

格式為 `docker compose up [options] [SERVICE...]`。

該命令十分強大，它將嘗試自動完成包括建立映像檔，（重新）建立服務，啟動服務，並關聯服務相關容器的一系列操作。

連結的服務都將會被自動啟動，除非已經處於執行狀態。

可以說，大部分時候都可以直接透過該命令來啟動一個專案。

預設情況，`docker compose up` 啟動的容器都在前景，控制檯將會同時印出所有容器的輸出資訊，可以很方便進行除錯。

當透過 `Ctrl-C` 停止命令時，所有容器將會停止。

如果使用 `docker compose up -d`，將會在背景啟動並執行所有的容器。一般推薦生產環境下使用該選項。

預設情況，如果服務容器已經存在，`docker compose up` 將會嘗試停止容器，然後重新建立（保持使用 `volumes-from` 掛載的卷），以保證新啟動的服務匹配 Compose 檔案的最新內容。如果使用者不希望容器被停止並重新建立，可以使用 `docker compose up --no-recreate`。這樣將只會啟動處於停止狀態的容器，而忽略已經執行的服務。如果使用者只想重新部署某個服務，可以使用 `docker compose up --no-deps -d <SERVICE_NAME>` 來重新建立服務並背景停止舊服務，啟動新服務，並不會影響到其所依賴的服務。

選項：

* `-d` 在背景執行服務容器。

* `--no-color` 不使用顏色來區分不同的服務的控制檯輸出。

* `--no-deps` 不啟動服務所連結的容器。

* `--force-recreate` 強制重新建立容器，不能與 `--no-recreate` 同時使用。

* `--no-recreate` 如果容器已經存在了，則不重新建立，不能與 `--force-recreate` 同時使用。

* `--no-build` 不自動建立缺失的服務映像檔。

* `-t, --timeout TIMEOUT` 停止容器時候的逾時（預設為 10 秒）。

#### `version`

格式為 `docker compose version`。

印出版本資訊。

#### `watch`

格式為 `docker compose watch [options] [SERVICE...]`。

啟用開發模式，自動監視原始碼並在檔案發生變化時重新整理服務。這需要專案中有 `compose.yaml`（或 `docker-compose.yml`），且定義了 `x-develop` 或 `develop` 設定段。

例如：

```yaml
services:
  web:
    build: .
    develop:
      watch:
        - action: sync
          path: ./web
          target: /src/web
          ignore:
            - node_modules/
        - action: rebuild
          path: package.json
```
選項：

* `--no-up` 不自動啟動服務。

* `--quiet` 靜默模式。

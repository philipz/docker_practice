# 常見問題與錯誤速查

### 映像檔相關

#### 如何批次清理臨時映像檔檔案？

答：可以使用 `docker image prune` 命令。

#### 如何查看映像檔支援的環境變數？

答：可以使用 `docker run IMAGE env` 命令。

#### 本地的映像檔檔案都存放在哪裡？

答：與 Docker 相關的本地資源預設存放在 `/var/lib/docker/` 目錄下，以 `overlay2` 檔案系統為例，其中 `containers` 目錄存放容器資訊，`image` 目錄存放映像檔資訊，`overlay2` 目錄下存放具體的映像檔層檔案。

#### 建立 Docker 映像檔應該遵循哪些原則？

答：整體原則上，盡量保持映像檔功能的明確和內容的精簡，要點包括

* 盡量選取滿足需求但較小的基礎系統映像檔，例如大部分時候可以選擇 `alpine` 映像檔，僅有不足六兆大小；
* 清理編譯產生檔案、安裝套件的快取等臨時檔案；
* 安裝各個軟體時候要指定準確的版本號，並避免引入不需要的相依；
* 從安全角度考慮，應用要盡量使用系統的庫和相依；
* 如果安裝應用時候需要設定一些特殊的環境變數，在安裝後要還原不需要保持的變數值；
* 使用 Dockerfile 建立映像檔時候要添加 .dockerignore 檔案或使用乾淨的工作目錄。

更多內容請查看 [最佳實踐](best_practices.md)

#### 碰到網路問題，無法 pull 映像檔，命令行指定 http\_proxy 無效？

答：先區分代理要作用在哪一層。Docker daemon 拉取映像檔時，推薦在 `daemon.json` 的 `proxies` 欄位或 systemd drop-in 中設定 `HTTP_PROXY` / `HTTPS_PROXY` / `NO_PROXY`，然後重新啟動 Docker 服務。Docker CLI、建立過程和容器內應用的代理應分別使用 `~/.docker/config.json`、`--build-arg` 或 `docker run --env` 設定；不要把 `export http_proxy=...` 當作 `daemon.json` 內容寫入。

### 容器相關

#### 容器退出後，透過 docker container ls 命令查看不到，資料會丟失麼？

答：容器退出後會處於終止 (exited) 狀態，此時可以透過 `docker container ls -a` 查看。其中的資料也不會丟失，還可以透過 `docker start` 命令來啟動它。只有刪除掉容器才會清除所有資料。

#### 如何停止所有正在執行的容器？

答：可以使用 `docker stop $(docker container ls -q)` 命令。

#### 如何批次清理已經停止的容器？

答：可以使用 `docker container prune` 命令。

#### 如何取得某個容器的 PID 資訊？

答：可以使用

```bash
docker inspect --format '{{ .State.Pid }}' <CONTAINER ID or NAME>
```

#### 如何取得某個容器的 IP 位址？

答：可以使用

```bash
docker inspect --format '{{ .NetworkSettings.IPAddress }}' <CONTAINER ID or NAME>
```

#### 如何給容器指定一個固定 IP 位址，而不是每次重新啟動容器 IP 位址都會變？

答：使用以下命令啟動容器可以使容器 IP 固定不變

```bash
$ docker network create -d bridge --subnet 172.25.0.0/16 my-net

$ docker run --network=my-net --ip=172.25.3.3 -itd --name=my-container busybox
```

這個固定 IP 主要用於同一 Docker daemon 內的容器間通訊。Docker Desktop 上不要依賴宿主機直接存取 Linux 容器 IP；宿主機存取容器服務仍應使用埠號映射或 `host.docker.internal` 等機制。

#### 如何臨時退出一個正在互動的容器的終端，而不終止它？

答：按 `Ctrl-p Ctrl-q`。如果按 `Ctrl-c` 往往會讓容器內應用程式終止，進而會終止容器。

#### 使用 `docker port` 命令映射容器的埠號時，系統報錯「Error：No public port ‘80’ published for xxx」？

答：

* 建立容器時用 `-p HOST_PORT:CONTAINER_PORT` 或 `--publish` 顯式發布埠號，例如 `docker run -p 8080:80 nginx`；
* 只想把映像檔聲明的 `EXPOSE` 埠號隨機發布到宿主機埠號時，用 `-P` / `--publish-all`，之後透過 `docker ps` 查看實際埠號；
* `Dockerfile` 中的 `EXPOSE` 只是映像檔中繼資料，不會自動發布埠號。

#### 可以在一個容器中同時執行多個應用程式麼？

答：一般並不推薦在同一個容器內執行多個應用程式。如果有類似需求，可以透過一些額外的程式管理機制，比如 `supervisord` 來管理所執行的程式。可以參考 [Docker 官方說明](https://docs.docker.com/engine/containers/multi-service_container/)。

#### 如何控制容器占用 CPU、記憶體等系統資源的份額？

答：在使用 `docker create` 命令建立容器或使用 `docker run` 建立並啟動容器的時候，可以使用 -c|--cpu-shares\[=0] 參數來調整容器使用 CPU 的權重；使用 -m|--memory\[=MEMORY] 參數來調整容器使用記憶體的大小。

### 倉庫相關

#### 倉庫、註冊伺服器、註冊索引有何關係？

首先，倉庫是存放一組關聯映像檔的集合，比如同一個應用的不同版本的映像檔。

註冊伺服器是存放實際的映像檔檔案的地方。註冊索引則負責維護使用者的帳號、權限、搜尋、標籤等的管理。因此，註冊伺服器利用註冊索引來實現認證等管理。

### 設定相關

#### Docker 的設定檔案放在哪裡，如何修改設定？

答：使用 `systemd` 的系統（如 Ubuntu 22.04+、Debian 12+、Rocky/Alma/CentOS Stream 9+）的設定檔案在 `/etc/docker/daemon.json`。

#### 如何更改 Docker 的預設儲存位置？

答：Docker 的預設儲存位置是 `/var/lib/docker`，如果希望將 Docker 的本地檔案儲存到其他分割區，可以使用 Linux 軟連線的方式來完成，或者修改設定檔案 `/etc/docker/daemon.json` 的 `data-root` 項。可以使用 `docker info | grep "Docker Root Dir"` 查看當前使用的儲存位置。

例如，如下操作將預設儲存位置遷移到 /storage/docker。

```bash
[root@s26 ~]# df -h
Filesystem                    Size  Used Avail Use% Mounted on
/dev/mapper/VolGroup-lv_root   50G  5.3G   42G  12% /
tmpfs                          48G  228K   48G   1% /dev/shm
/dev/sda1                     485M   40M  420M   9% /boot
/dev/mapper/VolGroup-lv_home  222G  188M  210G   1% /home
/dev/sdb2                     2.7T  323G  2.3T  13% /storage
[root@s26 ~]# service docker stop
[root@s26 ~]# cd /var/lib/
[root@s26 lib]# mv docker /storage/
[root@s26 lib]# ln -s /storage/docker/ docker
[root@s26 lib]# ls -la docker
lrwxrwxrwx. 1 root root 15 11月 17 13:43 docker -> /storage/docker
[root@s26 lib]# service docker start
```

#### 使用記憶體和 swap 限制啟動容器時候報核心不支援警告？

答：如果遇到 `WARNING: Your kernel does not support cgroup swap limit` 等警告，這是因為系統預設沒有開啟對記憶體和 swap 使用的統計功能，引入該功能會帶來效能的下降。要開啟該功能，可以採取如下操作：

* 編輯 `/etc/default/grub` 檔案（Ubuntu 系統為例），設定 `GRUB_CMDLINE_LINUX="cgroup_enable=memory swapaccount=1"`
* 更新 grub：`$ sudo update-grub`
* 重新啟動系統，即可。

### Docker 與虛擬化

#### Docker 與 LXC 有何不同？

答：LXC 利用 Linux 上相關技術實現了容器。Docker 則在如下的幾個方面進行了改進：

* 移植性：透過抽象容器設定，容器可以實現從一個平台移植到另一個平台；
* 映像檔系統：基於 OverlayFS 的映像檔系統為容器的分發帶來了很多的便利，同時共同的映像檔層只需要儲存一份，實現高效率的儲存；
* 版本管理：類似於 Git 的版本管理理念，使用者可以更方便的建立、管理映像檔檔案；
* 倉庫系統：倉庫系統大大降低了映像檔的分發和管理的成本；
* 周邊工具：各種現有工具（設定管理、雲端平台）對 Docker 的支援，以及基於 Docker 的 PaaS、CI 等系統，讓 Docker 的應用更加方便和多樣化。

#### Docker 與 Vagrant 有何不同？

答：兩者的定位完全不同。

* Vagrant 類似 Boot2Docker（一款執行 Docker 的最小核心），是一套虛擬機器的管理環境。Vagrant 可以在多種系統上和虛擬機器軟體中執行，可以在 Windows，Mac 等非 Linux 平台上為 Docker 提供支援，自身具有較好的包裝性和移植性。
* 原生的 Docker 自身只能執行在 Linux 平台上，但啟動和執行的效能都比虛擬機器要快，往往更適合快速開發和部署應用的場景。

簡單說：Vagrant 適合用來管理虛擬機器，而 Docker 適合用來管理應用環境。

#### 開發環境中 Docker 和 Vagrant 該如何選擇？

答：Docker 不是虛擬機器，而是程式隔離，對於資源的消耗很少，但是目前需要 Linux 環境支援。Vagrant 是虛擬機器上做的封裝，虛擬機器本身會消耗資源。

如果本地使用的 Linux 環境，推薦都使用 Docker。

如果本地使用的是 macOS 或者 Windows 環境，那就需要開虛擬機器，單一開發環境下 Vagrant 更簡單；多環境開發下推薦在 Vagrant 裡面再使用 Docker 進行環境隔離。

### 其他

#### Docker 能在非 Linux 平台上執行麼？比如 Windows 或 macOS

答：完全可以。安裝方法請查看[安裝 Docker](../install/README.md) 一節

#### 如何將一台宿主主機的 Docker 環境遷移到另外一台宿主主機？

答：停止 Docker 服務。將整個 Docker 儲存資料夾複製到另外一台宿主主機，然後調整另外一台宿主主機的設定即可。

#### 如何進入 Docker 容器的網路命名空間？

答：Docker 在建立容器後，刪除了宿主主機上 `/var/run/netns` 目錄中的相關的網路命名空間檔案。因此，在宿主主機上是無法看到或存取容器的網路命名空間的。

使用者可以透過如下方法來手動恢復它。

首先，使用下面的命令查看容器程式資訊，比如這裡的 1234。

```bash
$ docker inspect --format='{{ .State.Pid }}' $container_id
1234
```

接下來，在 `/proc` 目錄下，把對應的網路命名空間檔案連結到 `/var/run/netns` 目錄。

```bash
$ sudo ln -s /proc/1234/ns/net /var/run/netns/
```

然後，在宿主主機上就可以看到容器的網路命名空間資訊。例如

```bash
$ sudo ip netns show
1234
```

此時，使用者可以透過正常的系統命令來查看或操作容器的命名空間了。例如修改容器的 IP 位址資訊為 `172.17.0.100/16`。

```bash
$ sudo ip netns exec 1234 ifconfig eth0 172.17.0.100/16
```

#### 如何取得容器綁定到本地哪個 veth 介面上？

答：Docker 容器啟動後，會透過 veth 介面對連線到本地網橋，veth 介面命名跟容器命名毫無關係，十分難以找到對應關係。

最簡單的一種方式是透過查看介面的索引號，在容器中執行 `ip a` 命令，查看到本地介面最前面的介面索引號，如 `205`，將此值加上 1，即 `206`，然後在本地主機執行 `ip a` 命令，查找介面索引號為 `206` 的介面，兩者即為連線的 veth 介面對。

## 常見錯誤處理

| 錯誤資訊 / 現象 | 可能原因 | 解決方案 |
| :--- | :--- | :--- |
| `Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?` | Docker 服務未啟動 | Linux: `sudo systemctl start docker`<br>Mac/Win: 啟動 Docker Desktop |
| `permission denied while trying to connect to the Docker daemon socket` | 當前使用者無權存取 Docker socket | 臨時使用 `sudo docker ...`，或確認風險後執行 `sudo usermod -aG docker $USER` 並重新登入；`docker` 使用者群組等同授予 root 級權限，安全要求較高的環境優先評估 Rootless mode |
| `manifest for ... not found: manifest unknown` | 映像檔 tag 不存在 | 檢查 Docker Hub 該映像檔是否存在該 tag，或拼寫是否正確 |
| `connection refused` (pull image) | 網路不通或映像檔源無法存取 | 檢查網路，設定[映像檔加速器](../install/README.md) |
| `Bind for 0.0.0.0:8080 failed: port is already allocated` | 埠號被占用 | 檢查占用埠號的程式 (`lsof -i:8080`) 並殺掉，或換個埠號映射 (`-p 8081:80`) |
| `exec user process caused "exec format error"` | 架構不匹配（如在 x86 上跑 ARM 映像檔）| 使用 `docker buildx` 建立多架構映像檔，或拉取對應架構的映像檔 |
| `standard_init_linux.go:211: exec user process caused "no such file or directory"` | 找不到直譯器或相依庫 | 檢查 `ENTRYPOINT`/`CMD` 腳本開頭的 shebang (`#!/bin/sh` vs `#!/bin/bash`)，或確認二進位檔案是否相依缺失（Alpine 常見缺少 glibc）|
| `iptables: No chain/target/match by that name` | 防火牆規則缺失或衝突 | 重新啟動 Docker 服務重置 iptables 鏈: `sudo systemctl restart docker` |
| 容器內無法存取外網 | DNS 設定或轉發問題 | 檢查 `/etc/docker/daemon.json` 中的 DNS 設定 |

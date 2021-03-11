## Docker 網路實作

Docker 的網路實作其實就是利用了 Linux 上的網路命名空間和虛擬網路設備（特別是 veth pair）。建議先熟悉了解這兩部分的基本概念再閱讀本章。

### 基本原理
首先，要實作網路通信界面，機器需要至少一個網路界面（物理界面或虛擬界面）來收發資料包；此外，如果不同子網之間要進行通信，需要路由機制。

Docker 中的網路界面預設都是虛擬的界面。虛擬界面的優勢之一是轉發效率較高。
Linux 透過在核心中進行資料複製來實作虛擬界面之間的資料轉發，發送界面的發送緩存中的資料包被直接複製到接收界面的接收緩存中。對於本地系統和容器內系統看來就像是一個正常的乙太網卡，只是它不需要真正同外部網路設備通信，速度要快很多。

Docker 容器網路就利用了這項技術。它在本地主機和容器內分別建立一個虛擬界面，並讓它們彼此連通（這樣的一對界面叫做 `veth pair`）。

### 建立網路參數
Docker 建立一個容器的時候，會執行以下操作：
* 建立一對虛擬界面，分別放到本地主機和新容器中；
* 本地主機一端橋接到預設的 docker0 或指定橋接器上，並具有一個唯一的名字，如 veth65f9；
* 容器一端放到新容器中，並修改名字作為 eth0，這個界面只在容器的命名空間可見；
* 從橋接器可用位址段中取得一個未使用位址分配給容器的 eth0，並設定預設路由到橋接網卡 veth65f9。

完成這些之後，容器就可以使用 eth0 虛擬網卡來連接其他容器和其他網路。

可以在 `docker run` 的時候透過 `--net` 參數來指定容器的網路設定，有4個可選值：
* `--net=bridge` 這個是預設值，連接到預設的橋接器。
* `--net=host` 告訴 Docker 不要將容器網路放到隔離的命名空間中，即不要容器化容器內的網路。此時容器使用本地主機的網路，它擁有完全的本地主機界面存取權限。容器程式可以跟主機其它 root 程式一樣可以打開低範圍的連接埠，可以存取本地網路服務比如 D-bus，還可以讓容器做一些影響整個主機系統的事情，比如重啟主機。因此使用這個選項的時候要非常小心。如果進一步的使用 `--privileged=true`，容器會被允許直接設定主機的網路堆棧。
* `--net=container:NAME_or_ID` 讓 Docker 將新建容器的程式放到一個已存在容器的網路堆疊中，新容器程式有自己的檔案系統、程式列表和資源限制，但會和已存在的容器共享 IP 位址和連接埠等網路資源，兩者程式可以直接透過 `lo` 迴路界面通信。
* `--net=none` 讓 Docker 將新容器放到隔離的網路堆疊中，但是不進行網路設定。之後，使用者可以自己進行設定。

### 網路設定細節
使用者使用 `--net=none` 後，可以自行設定網路，讓容器達到跟平常一樣具有存取網路的權限。透過這個過程，可以了解 Docker 設定網路的細節。

首先，啟動一個 `/bin/bash` 容器，指定 `--net=none` 參數。
```bash
$ sudo docker run -i -t --rm --net=none base /bin/bash
root@63f36fc01b5f:/#
```
在本地主機查找容器的程式 id，並為它建立網路命名空間。
```bash
$ sudo docker inspect -f '{{.State.Pid}}' 63f36fc01b5f
2778
$ pid=2778
$ sudo mkdir -p /var/run/netns
$ sudo ln -s /proc/$pid/ns/net /var/run/netns/$pid
```
檢查橋接網卡的 IP 和子網遮罩訊息。
```bash
$ ip addr show docker0
21: docker0: ...
inet 172.17.42.1/16 scope global docker0
...
```
建立一對 “veth pair” 界面 A 和 B，綁定 A 到橋接器 `docker0`，並啟用它
```bash
$ sudo ip link add A type veth peer name B
$ sudo brctl addif docker0 A
$ sudo ip link set A up
```
將B放到容器的網路命名空間，命名為 eth0，啟動它並設定一個可用 IP（橋接網段）和預設網關。
```bash
$ sudo ip link set B netns $pid
$ sudo ip netns exec $pid ip link set dev B name eth0
$ sudo ip netns exec $pid ip link set eth0 up
$ sudo ip netns exec $pid ip addr add 172.17.42.99/16 dev eth0
$ sudo ip netns exec $pid ip route add default via 172.17.42.1
```
以上，就是 Docker 設定網路的具體過程。

當容器結束後，Docker 會清空容器，容器內的 eth0 會隨網路命名空間一起被清除，A 界面也被自動從 `docker0` 卸載。

此外，使用者可以使用 `ip netns exec` 命令來在指定網路命名空間中進行設定，從而設定容器內的網路。

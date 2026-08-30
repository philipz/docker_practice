## 命名空間

命名空間是 Linux 核心一個強大的特性。每個容器都有自己單獨的命名空間，執行在其中的應用都像是在獨立的作業系統中執行一樣。命名空間保證了容器之間彼此互不影響。

### 什麼是 Namespace

> **Namespace 是 Linux 核心提供的資源隔離機制，它讓容器內的程式彷彿執行在獨立的作業系統中。** Namespace 是容器技術的核心基礎之一。它回答了一個關鍵問題：**如何讓一個程式 「以為」 自己獨占整個系統？**

```mermaid
flowchart LR
    subgraph Host ["宿主機視角"]
        direction TB
        H1["PID 1: systemd"]
        H2["PID 2: sshd"]
        H3["PID 3: dockerd"]
        H4["PID 1234: nginx"]
        H5["PID 1235: nginx worker"]
    end

    subgraph Container ["容器內視角"]
        direction TB
        C1["PID 1: nginx<br/>← 容器認為自己是 PID 1"]
        C2["PID 2: nginx worker"]
    end

    H4 -. "（實際是宿主機的 1234）" .- C1
```

### Namespace 的類型

Linux 核心（5.6+）共提供 8 種 Namespace。Docker 容器預設啟用其中的 PID、NET、MNT、UTS、IPC（在 cgroup v2 主機上還包括 Cgroup）；USER Namespace 預設**不**啟用，需要透過 `daemon.json` 的 `userns-remap` 顯式開啟（詳見第 18.1 節），Time Namespace 則未被使用：

| Namespace | 隔離內容 | 容器中的效果 |
|-----------|---------|-------------|
| **PID** | 程式 ID | 容器內 PID 從 1 開始，看不到其他容器和宿主機程式 |
| **NET** | 網路堆疊 | 獨立的網卡、IP 位址、埠號、路由表 |
| **MNT** | 掛載點 | 獨立的檔案系統視圖，自己的根目錄 |
| **UTS** | 主機名 | 獨立的主機名和域名 |
| **IPC** | 程式間通訊 | 獨立的訊號量、消息佇列、共享記憶體 |
| **USER** | 使用者/組 ID | 容器內的 root 可以映射為宿主機的普通使用者（預設不啟用，需 `userns-remap` 顯式開啟）|
| **Cgroup** | Cgroup 根目錄 | 隔離 cgroup 層級視圖 (Linux 4.6+)|
| **Time** | 系統時鐘 | 隔離 CLOCK_MONOTONIC 和 CLOCK_BOOTTIME (Linux 5.6+)|

---

### PID Namespace

PID Namespace 負責程式 ID 的隔離，使得容器內的程式彼此不可見。

#### PID 的作用

隔離程式 ID，讓每個容器有自己的程式編號空間。

#### PID 隔離效果

```bash
## 宿主機上查看程式

$ ps aux | grep nginx
root     12345  0.0  0.1  nginx: master process
root     12346  0.0  0.1  nginx: worker process

## 容器內查看程式

$ docker exec mycontainer ps aux
PID   USER     COMMAND
  1   root     nginx: master process    ← 在容器內是 PID 1
  2   root     nginx: worker process
```

#### PID 關鍵點

- 容器內的 PID 1 程式特殊重要——它是容器的主程式，退出則容器停止
- 容器內無法看到宿主機或其他容器的程式
- 宿主機可以看到所有容器內的程式（但 PID 不同）

---

### NET Namespace

NET Namespace 負責網路堆疊的隔離，包括網卡、路由表和 iptables 規則等。

#### NET 的作用

隔離網路堆疊，每個容器擁有獨立的網路環境。

#### NET 隔離效果

```mermaid
flowchart LR
    subgraph Host ["宿主機"]
        direction TB
        H1["eth0: 192.168.1.10<br/>埠號 80 可用"]
        H2["docker0: 172.17.0.1"]
    end

    subgraph Container ["容器"]
        direction TB
        C1["eth0: 172.17.0.2<br/>埠號 80 可用"]
        C2["(veth pair 連線)"]
    end

    H2 <--> C2
```

#### NET 關鍵點

- 每個容器有獨立的網卡、IP、路由表、iptables 規則
- 多個容器可以監聽相同埠號（如都監聽 80）
- Docker 使用 veth pair 連線容器網路和宿主機網橋

---

### MNT Namespace

MNT Namespace 負責檔案系統掛載點的隔離，確保容器看到獨立的檔案系統視圖。

#### MNT 的作用

隔離檔案系統掛載點，每個容器有自己的根目錄。

#### MNT 隔離效果

```bash
宿主機檔案系統：                  容器內看到的：
/                               /  ← 容器的根目錄
├── bin/                        ├── bin/
├── home/                       ├── home/
├── var/                        ├── var/
│   └── lib/                    │   └── lib/
│       └── docker/             │
│           └── overlay2/       │
│               └── merged/ ────┼─── 這個目錄成為容器的 /
└── ...                         └── ...
```

#### 與 chroot 的區別

| 特性 | chroot | MNT Namespace |
|------|--------|---------------|
| 安全性 | 可以逃逸 | 更安全 |
| 掛載隔離 | 無 | 完全隔離 |
| /proc/mounts | 共享 | 獨立 |

---

### UTS Namespace

UTS Namespace 主要用於隔離主機名和域名。

#### UTS 的作用

隔離主機名和域名，讓每個容器可以有自己的主機名。

#### UTS 隔離效果

```bash
## 宿主機

$ hostname
my-server

## 容器內

$ docker run --hostname mycontainer ubuntu hostname
mycontainer
```
UTS = 「UNIX Time-sharing System」，是歷史遺留的名稱。

---

### IPC Namespace

IPC Namespace 用於隔離程式間通訊資源，如 System V IPC 和 POSIX 消息佇列。

#### IPC 的作用

隔離 System V IPC 和 POSIX 消息佇列。

#### 隔離的資源

- 訊號量 (semaphores)
- 消息佇列 (message queues)
- 共享記憶體 (shared memory)

#### IPC 關鍵點

- 同一容器內的程式可以透過 IPC 通訊
- 不同容器的程式無法透過 IPC 通訊（除非顯式共享）

---

### USER Namespace

USER Namespace 允許將容器內的使用者 ID 映射到宿主機的不同使用者 ID。

#### USER 的作用

隔離使用者和組 ID，實作權限隔離。

#### USER 隔離效果

```mermaid
flowchart LR
    subgraph Container ["容器內"]
        direction TB
        C1["UID 0 (root)"]
        C2["UID 1 (daemon)"]
    end

    subgraph Host ["宿主機"]
        direction TB
        H1["UID 100000<br/>← 非特權使用者"]
        H2["UID 100001"]
    end

    C1 -- 映射 --> H1
    C2 -- 映射 --> H2
```

#### 安全意義

容器內的 root 使用者可以映射為宿主機上的普通使用者，即使容器被突破，攻擊者在宿主機上也只有普通權限。

> 💡 筆者建議：生產環境建議啟用 User Namespace，增強安全性。

---

### 動手實驗：體驗 Namespace

使用 `unshare` 命令可以在不使用 Docker 的情況下體驗 Namespace：

#### 實驗 1：UTS Namespace

```bash
## 建立新的 UTS namespace 並啟動 shell

$ sudo unshare --uts /bin/bash

## 修改主機名（只影響這個 namespace）

$ hostname container-test
$ hostname
container-test

## 退出後查看宿主機主機名（未改變）

$ exit
$ hostname
my-server
```

#### 實驗 2：PID Namespace

```bash
## 建立新的 PID 和 MNT namespace

$ sudo unshare --pid --mount --fork /bin/bash

## 掛載新的 /proc

$ mount -t proc proc /proc

## 查看程式（只能看到目前 shell）

$ ps aux
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.0   8960  4516 pts/0    S    10:00   0:00 /bin/bash
root         8  0.0  0.0  10072  3200 pts/0    R+   10:00   0:00 ps aux
```

#### 實驗 3：NET Namespace

```bash
## 建立新的網路 namespace

$ sudo unshare --net /bin/bash

## 查看網路介面（只有 lo）

$ ip addr
1: lo: <LOOPBACK> mtu 65536 qdisc noop state DOWN
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
```
---

### Namespace 的侷限性

Namespace 提供了隔離但不是安全邊界：

| 方面 | 說明 |
|------|------|
| **共享核心** | 所有容器共享宿主機核心，核心漏洞可能影響所有容器 |
| **部分資源未隔離** | /proc、/sys 部分內容仍可見；Time Namespace (Linux 5.6+) 雖已可用，但 Docker 預設不啟用 |
| **非虛擬化** | 比虛擬機隔離性弱 |

> 需要更強隔離時，可考慮 gVisor、Kata Containers 等安全容器方案。

---

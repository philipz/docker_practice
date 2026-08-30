## 其他安全特性

除了上述的命名空間、控制組以及能力機制，Linux 核心與雲原生生態還提供了大量安全增強功能，它們共同築成了一道防禦縱深的「馬奇諾防線」。本節主要介紹強制存取控制、系統呼叫攔截以及自動化的容器漏洞掃描技術。

### 系統呼叫過濾

`Seccomp`（Secure Computing mode）是 Linux 核心的一個安全機制，用於限制程式能夠發起的系統呼叫數量。

一個普通的 Linux 核心提供了 300 多個系統呼叫，而一個正常執行的容器化應用（例如 Nginx 服務）通常只會用到幾十個呼叫，這就給攻擊者留下了大量的閒置入口點來進行核心層的緩衝區溢位攻擊。

Docker 預設啟用了 Seccomp，並使用預置的 [預設設定檔案](https://docs.docker.com/engine/security/seccomp/) 作為 allowlist：預設拒絕未明確允許的系統呼叫，並額外允許常見應用所需的呼叫。Docker 官方文件將其描述為預設禁用約 44 個系統呼叫（核心與 Docker 版本不同會有差異），例如與核心模組、系統重新啟動或特權命名空間操作相關的呼叫。

如果你對應用的系統呼叫特徵瞭如指掌，你可以為容器自訂專屬規則。

#### 實戰：禁用 chmod 系統呼叫過濾

首先，編寫一個 `no-chmod.json` 的策略檔案：
```json
{
    "defaultAction": "SCMP_ACT_ALLOW",
    "syscalls": [
        {
            "name": "chmod",
            "action": "SCMP_ACT_ERRNO"
        }
    ]
}
```
在啟動時告訴 Docker 載入這套過濾設定：

```bash
$ docker run --rm -it \
  --security-opt seccomp=no-chmod.json \
  alpine sh

/ # chmod 777 /etc/passwd
chmod: /etc/passwd: Operation not permitted
```
應用只要被劫持進行越界嘗試，其作業系統層命令便會立刻吃癟。

### 強制存取控制：AppArmor / SELinux

傳統的 Linux 模型遵循 DAC（自主存取控制），這意味著如果一個檔案被賦予了全員讀寫權限（`777`），普通隔離下任何人便都能修改。但 **MAC（強制存取控制）** 技術，諸如 `AppArmor`（常用於 Ubuntu/Debian）或 `SELinux`（常用於 CentOS/RHEL），可以制定比「檔案所有權」更宏觀且優先的策略控制模組。

在開啟了上述機制的機器上：

- **AppArmor**: 在啟用 AppArmor 的系統上，Docker 預設為容器載入 `docker-default` profile；如果需要自訂策略，先用 `apparmor_parser` 載入 profile，再透過 `--security-opt apparmor=<profile>` 指定。
- **SELinux**: 在啟用 SELinux 整合的系統上，容器與掛載目錄需要正確的 SELinux label。綁定掛載時常用 `:z` 表示多個容器共享，`:Z` 表示該掛載只給單個容器使用；不要對 `/home`、`/usr` 等系統目錄隨意使用 `:Z`，否則可能破壞宿主機標籤。

如果想為某些受信任應用施加特定的外部強化檔案策略，可以透過如下方法指派規則表：

```bash
$ docker run --rm -it \
  --security-opt apparmor=custom-nginx-profile \
  nginx

$ docker run --rm -it \
  -v "$PWD/html":/usr/share/nginx/html:Z \
  nginx
```

### 容器映像檔漏洞靜態掃描

現代防護的防禦已經不僅僅在執行階段，而向「左」延伸至了建立與分發時期控制。很多安全隱患並不是使用者程式碼中的直接邏輯異常，而是打包環境或者引入庫的基礎 `APT` 安裝層面潛伏了開源界眾所周知的歷史漏洞。

#### 使用 Trivy 識別風險

[Trivy](https://github.com/aquasecurity/trivy) 是由 Aqua Security 發行的一款針對容器技術的快速映像檔漏洞掃描利器。在分發應用前透過它的掃描可以規避絕大多數風險。

```bash
## 如果使用本地命令行掃描容器映像檔
$ trivy image alpine:3.20

2024-03-01T10:05:07.124Z	INFO	Number of language-specific files: 1
2024-03-01T10:05:07.124Z	INFO	Detecting vulnerabilities...

alpine:3.20 (alpine 3.20.0)
===========================
Total: 2 (UNKNOWN: 0, LOW: 0, MEDIUM: 1, HIGH: 1, CRITICAL: 0)

+---------+------------------+----------+-------------------+---------------+---------------------------------------+
| LIBRARY | VULNERABILITY ID | SEVERITY | INSTALLED VERSION | FIXED VERSION | TITLE                                 |
+---------+------------------+----------+-------------------+---------------+---------------------------------------+
| busybox | CVE-2022-28391   | HIGH     | 1.30.1-r3         | 1.30.1-r4     | busybox: out-of-bounds read in...     |
...
```
只要確保所有上傳給私有或公共倉庫分發服務的產物先被引入至 CI/CD 流水線，如果出現 `HIGH` 及 `CRITICAL` 嚴重的報錯記錄強行阻攔部署，這本身便是建立環節極其有力的自動化安全大門保障。除 Trivy 外，最新的 Docker 版本也已內建支援官方掃描利刃 **Docker Scout**。

### 容器核心層基石結語

到這裡，Docker 為保障宿主和容器界限安全的幾個護城河：從 **資源剝離限制**(`Cgroups`) 到 **程式/網路/身分蒙蔽**(`Namespace`)、到 **特權能力回收**(`Capabilities`) 再到 **核心強制策略攔截管制**(`Seccomp`/`AppArmor`) 已悉數交代完畢。雖然絕沒有「100% 免疫網路穿刺的防線」，只要開發者牢記 **權限最小化原則** ，容器的堡壘就可以做到令攻擊者望洋興嘆。

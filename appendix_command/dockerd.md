## 服務端命令 - dockerd

### 使用說明

`dockerd` 參數會隨版本變化。建議優先在目標機器上執行 `dockerd --help`，並以 `daemon.json` 為主進行持久化設定。

### 常用選項：Docker Engine 29.x

* `--config-file="/etc/docker/daemon.json"`：指定 daemon 設定檔案路徑；
* `--data-root=""`：Docker 資料目錄（預設 `/var/lib/docker`）；
* `-H, --host=[]`：指定 daemon 監聽位址 (Unix socket / TCP)；
* `-D, --debug`：開啟除錯日誌；
* `-l, --log-level="debug|info|warn|error|fatal"`：日誌級別；
* `--group=""`：Unix socket 所屬使用者群組（預設 `docker`）；
* `--containerd=""`：指定 containerd socket；
* `--exec-opt=[]`：執行時期執行選項（如 cgroup 驅動）；
* `--default-ulimit=[]`：設定容器預設 ulimit；
* `--dns=[]` / `--dns-search=[]` / `--dns-opt=[]`：DNS 設定；
* `--registry-mirror=[]`：映像檔加速位址；
* `--insecure-registry=[]`：允許存取不安全倉庫；
* `--iptables=true|false` / `--ip-forward=true|false` / `--ip-masq=true|false`：網路轉發與 NAT 規則控制；
* `--ipv6=true|false`：啟用 IPv6；
* `--storage-driver=""` / `--storage-opt=[]`：儲存驅動及參數；
* `--log-driver=""` / `--log-opt=[]`：容器日誌驅動與參數；
* `--authorization-plugin=[]`：鑑權外掛程式；
* `--selinux-enabled=true|false`：啟用 SELinux 整合（依賴發行版策略）；
* `--userns-remap=...`：使用者命名空間映射；
* `--tls` / `--tlscacert` / `--tlscert` / `--tlskey` / `--tlsverify`：TLS 安全設定。

### 歷史參數提示

以下參數已移除或不建議繼續使用：

* `--graph`：請改用 `--data-root`；
* `--cluster-store` / `--cluster-advertise` / `--cluster-store-opt`：已移除；
* `--disable-legacy-registry`：已移除。

### 參考

* [官方文件](https://docs.docker.com/reference/cli/dockerd/)

## 15.2 安裝

本節將介紹 etcd 的幾種常見安裝方式，包括二進位安裝、Docker 映像檔執行以及在 macOS 上的安裝。

`etcd` 基於 `Go` 語言實現，因此，使用者可以從[專案主頁](https://github.com/etcd-io/etcd)下載原始碼自行編譯，也可以下載編譯好的二進位檔案，甚至直接使用製作好的 `Docker` 映像檔來體驗。

> 注意：etcd 3.7.0 於 2026 年 7 月釋出，官方仍在維護 3.5、3.6、3.7 三個釋出分支。etcd 3.4 已隨 2026 年 6 月的 v3.4.45 結束支援（EOL），仍在使用的使用者應儘快升級。本章示例基於 etcd `3.5.x` 版本編寫，etcd 3.6.x/3.7.x 可用於新部署。請存取 [etcd 官方釋出頁](https://github.com/etcd-io/etcd/releases) 取得最新版本。

### 15.2.1 二進位檔案方式下載

編譯好的二進位檔案都在 [github.com/etcd-io/etcd/releases](https://github.com/etcd-io/etcd/releases/) 頁面，使用者可以選擇需要的版本，或透過下載工具下載。

例如，使用 `curl` 工具下載壓縮包，並解壓。

```bash
# 下載 etcd v3.5.29 版本（請存取 https://github.com/etcd-io/etcd/releases 取得最新版本）
$ curl -L https://github.com/etcd-io/etcd/releases/download/v3.5.29/etcd-v3.5.29-linux-amd64.tar.gz -o etcd-v3.5.29-linux-amd64.tar.gz

## 國內使用者可選擇就近的網路加速方式（以可用映像站為準）

$ tar xzvf etcd-v3.5.29-linux-amd64.tar.gz
$ cd etcd-v3.5.29-linux-amd64
```
解壓後，可以看到檔案包括

```bash
$ ls
Documentation README-etcdctl.md README.md READMEv2-etcdctl.md etcd etcdctl
```
其中 `etcd` 是服務主檔案，`etcdctl` 是提供給使用者的命令客戶端，其他檔案是支援文件。

下面將 `etcd` `etcdctl` 檔案放到系統可執行目錄（例如 `/usr/local/bin/`）。

```bash
$ sudo cp etcd* /usr/local/bin/
```
預設 `2379` 埠號處理客戶端的請求，`2380` 埠號用於集群各成員間的通訊。啟動 `etcd` 顯示類似如下的資訊：

```bash
$ etcd
...
2017-12-03 11:18:34.411579 I | embed: listening for peers on http://localhost:2380
2017-12-03 11:18:34.411938 I | embed: listening for client requests on localhost:2379
```
此時，可以使用 `etcdctl` 命令進行測試，設定和取得鍵值 `testkey: "hello world"`，檢查 `etcd` 服務是否啟動成功：

```bash
$ ETCDCTL_API=3 etcdctl member list
8e9e05c52164694d, started, default, http://localhost:2380, http://localhost:2379

$ ETCDCTL_API=3 etcdctl put testkey "hello world"
OK

$ ETCDCTL_API=3 etcdctl get testkey
testkey
hello world
```
說明 etcd 服務已經成功啟動了。

### 15.2.2 Docker 映像檔方式執行

映像檔名稱為 `quay.io/coreos/etcd`，可以透過下面的命令啟動單機實驗用 `etcd` 服務，並只把 `2379` 和 `2380` 映射到宿主機回環地址。

> **版本說明：** 示例中使用 `v3.5.29` 標籤。請存取 [etcd 官方釋出頁](https://github.com/etcd-io/etcd/releases) 取得最新可用版本標籤。

```bash
$ docker run \
-p 127.0.0.1:2379:2379 \
-p 127.0.0.1:2380:2380 \
--mount type=bind,source=/tmp/etcd-data.tmp,destination=/etcd-data \
--name etcd-gcr-v3.5.29 \
quay.io/coreos/etcd:v3.5.29 \
/usr/local/bin/etcd \
--name s1 \
--data-dir /etcd-data \
--listen-client-urls http://0.0.0.0:2379 \
--advertise-client-urls http://127.0.0.1:2379 \
--listen-peer-urls http://0.0.0.0:2380 \
--initial-advertise-peer-urls http://127.0.0.1:2380 \
--initial-cluster s1=http://127.0.0.1:2380 \
--initial-cluster-token tkn \
--initial-cluster-state new \
--log-level info \
--logger zap \
--log-outputs stderr
```

上面示例僅用於單機實驗：宿主機埠號限定在 `127.0.0.1`，因此不會把未啟用 TLS 的 etcd 直接暴露到外部網路。容器內部的 `listen-*` 可以繫結 `0.0.0.0` 監聽容器網卡，但 `advertise-*` 應填寫其他節點或客戶端**實際可存取的主機地址**，不能直接寫成 `0.0.0.0`。生產或多節點環境不要使用明文 HTTP 暴露 etcd，應結合固定內網地址、TLS、客戶端憑證認證和防火牆存取控制。

開啟新的終端按照上一步的方法測試 `etcd` 是否成功啟動。

### 15.2.3 macOS 中執行

```bash
$ brew install etcd

$ etcd

$ ETCDCTL_API=3 etcdctl member list
```

# 如何除錯 Docker

### 開啟 Debug 模式

在 dockerd 設定檔案 daemon.json（預設位於 /etc/docker/）中添加

```json
{
  "debug": true
}
```

重新啟動守護程式。

```bash
$ sudo kill -SIGHUP $(pidof dockerd)
```

此時 dockerd 會在日誌中輸出更多資訊供分析。

### 檢查核心日誌

```bash
$ sudo dmesg |grep dockerd
$ sudo dmesg |grep runc
```

### Docker 不回應時處理

可以殺死 dockerd 程式查看其堆疊呼叫情況。

```bash
$ sudo kill -SIGUSR1 $(pidof dockerd)
```

### 重置 Docker 本地資料

*注意，本操作會移除所有的 Docker 本地資料，包括映像檔和容器等。*

更安全的替代方式是優先使用以下命令進行清理：

```bash
$ docker system prune
```

如果你只是想「恢復出廠設定」，在 Docker Desktop 裡也提供了相應入口。

只有在確認要丟棄本機全部映像檔、容器、卷和建立快取，並且已經停止 Docker 服務、完成備份或匯出後，才考慮刪除 Docker 資料目錄：

```bash
$ sudo systemctl stop docker containerd
$ sudo cp -a /var/lib/docker /var/lib/docker.backup
$ sudo rm -rf /var/lib/docker
$ sudo systemctl start docker
```

### 常見故障排查

#### 容器啟動失敗

如果容器啟動後立即退出，可以使用 `docker logs` 查看原因。

* **Exit Code 1**：應用程式錯誤。通常是設定錯誤或相依缺失。
* **Exit Code 137**：OOM (Out Of Memory)。容器記憶體不足被核心殺掉。
  * 檢查宿主機記憶體。
  * 調整容器記憶體限制 (`--memory`)。
* **Exit Code 127**：命令未找到。可能是 `ENTRYPOINT` 或 `CMD` 指定的命令不存在。

#### 網路連線問題

##### 容器內部無法聯網

1. 檢查 Docker DNS 設定 (`/etc/docker/daemon.json`)。
2. 檢查宿主機防火牆 (iptables/firewalld) 是否攔截了轉發。
3. 容器內測試：`ping 8.8.8.8`（測試連通性），`nslookup google.com`（測試 DNS）。

##### 埠號映射不通

1. 檢查容器埠號是否正確監聽：`netstat -tunlp`（宿主機）或 `docker exec <container> netstat -tunlp`。
2. 確認應用監聽位址是 `0.0.0.0` 而不是 `127.0.0.1`。
   * 如果應用監聽在 `127.0.0.1`，只有容器內部能存取，映射到宿主機外部也無法被外部請求存取。

#### 映像檔拉取失敗

* **connection refused**：檢查網路或代理設定。
* **image not found**：檢查映像檔名稱和 Tag 拼寫。
* **EOF / timeout**：網路不穩定，嘗試設定映像檔加速器。

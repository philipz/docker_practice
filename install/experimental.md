## 開啟實驗特性

一些 docker 命令或功能僅當 **實驗特性** 開啟時才能使用，請按照以下方法進行設定。

### Docker CLI 的實驗特性

CLI 的實驗特性通常包含仍在開發中的新功能。幸運的是，在較新版本中這些特性已經更加易用。

從 `v20.10` 及更高版本開始，Docker CLI 所有實驗特性的命令均預設開啟，無需再進行設定或設定系統環境變數。

### 開啟 dockerd 的實驗特性

編輯 `/etc/docker/daemon.json`，新增如下條目

```json
{
  "experimental": true
}
```

儲存後重啟 Docker 常駐程式：

```bash
$ sudo systemctl restart docker
```

然後執行下面的命令驗證服務端實驗特性已經生效：

```bash
$ docker version
```

若輸出中的 `Server` / `Engine` 部分出現 `Experimental: true`，說明 daemon 端實驗特性已經啟用。

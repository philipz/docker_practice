## 安裝與移除

`Compose` 是 Docker 官方的開源專案，負責實作本地或單機多容器應用的快速編排。跨主機集群編排應使用 Swarm、Kubernetes 或雲廠商託管服務。

目前的 Compose 以 `docker compose` 子命令的形式提供。Docker Desktop 在 macOS、Windows 和 Linux 上預設包含它；如果你已經在 Linux 上單獨安裝了 Docker Engine 和 Docker CLI，也可以再安裝 Compose CLI 外掛。

### Linux

在 Linux 上，預設建議透過 Docker 官方軟體倉庫安裝 Compose CLI 外掛，這樣可以隨系統套件管理器更新。

Ubuntu / Debian：

```bash
$ sudo apt-get update
$ sudo apt-get install docker-compose-plugin
```

Fedora / CentOS / RHEL 相容發行版：

```bash
$ sudo dnf install docker-compose-plugin
```

如果是離線環境、需要鎖定特定版本，或套件管理器暫不覆蓋你的架構，可以從 Docker 官方發佈頁手工安裝。手工安裝不會自動更新；下載 URL 中的版本號和架構（如 `x86_64`、`aarch64`）需要按目標機器替換。

```bash
$ DOCKER_CONFIG=${DOCKER_CONFIG:-$HOME/.docker}
$ mkdir -p $DOCKER_CONFIG/cli-plugins
$ curl -SL https://github.com/docker/compose/releases/download/v5.1.2/docker-compose-linux-x86_64 -o $DOCKER_CONFIG/cli-plugins/docker-compose
$ chmod +x $DOCKER_CONFIG/cli-plugins/docker-compose
```

### 測試安裝

```bash
$ docker compose version
Docker Compose version v5.x.x
```

### 移除

如果是倉庫方式安裝，使用套件管理器移除；如果是二進位套件方式安裝，刪除二進位檔案即可。

```bash
$ sudo apt-get remove docker-compose-plugin
# 或
$ sudo dnf remove docker-compose-plugin

$ rm $DOCKER_CONFIG/cli-plugins/docker-compose
```

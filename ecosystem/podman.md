## 17.3 Podman - 下一代 Linux 容器工具

> **版本說明**：Podman 保持活躍的開發和發佈週期。建議存取 [Podman 官方文件](https://podman.io/docs) 和 [GitHub Releases](https://github.com/podman-container-tools/podman/releases) 取得最新版本。

[Podman](https://github.com/podman-container-tools/podman) 是一個無常駐程式、與 Docker 命令高度相容的下一代 Linux 容器工具。它由 Red Hat 開發，旨在提供一個更安全的容器運行環境。

### 17.3.1 Podman vs Docker

Podman 和 Docker 在設計理念上存在顯著差異，主要體現在架構和權限模型上。

| 特性 | Docker | Podman |
| :--- | :--- | :--- |
| **架構** | C/S 架構，依賴常駐程式 (`dockerd`) | 無常駐程式 (Daemonless) |
| **權限** | 預設需要 root 權限（雖有 Rootless 模式）| 預設支持 Rootless（非 root 使用者運行）|
| **生態** | 完整的生態系統 (Compose, Swarm) | 專注單機容器，配合 Kubernetes 使用 |
| **映像檔建立** | `docker build` | `podman build` 或 `buildah` |

### 17.3.2 安裝

Podman 支持多種作業系統，安裝過程也相對簡單。

#### CentOS / RHEL

```bash
$ sudo yum -y install podman
```

#### macOS

macOS 上需要安裝 Podman Desktop 或通過 Homebrew 安裝：

```bash
$ brew install podman
$ podman machine init
$ podman machine start
```

### 17.3.3 基本使用

`podman` 的命令列幾乎與 `docker` 完全相容，大多數情況下，你只需將 `docker` 替換為 `podman` 即可。

#### 運行容器

```bash
## $ docker run -d -p 80:80 nginx:alpine

$ podman run -d -p 80:80 nginx:alpine
```

#### 列出容器

```bash
$ podman ps
```

#### 建立映像檔

```bash
$ podman build -t myimage .
```

### 17.3.4 Pods 的概念

與 Docker 不同，Podman 支持“Pod”的概念（類似於 Kubernetes 的 Pod），允許你在同一個網路命名空間中運行多個容器。

```bash
## 建立一個 Pod

$ podman pod create --name mypod -p 8080:80

## 在 Pod 中運行容器

$ podman run -d --pod mypod --name webbing nginx
```

### 17.3.5 遷移到 Podman

如果你習慣使用 `docker` 命令，可以簡單地設定別名：

```bash
$ alias docker=podman
```

#### Systemd 整合

Podman 可以產生 systemd 單元檔案，讓容器像普通系統服務一樣管理。

```bash
## 建立容器

$ podman run -d --name myweb -p 8080:80 nginx

## 產生 systemd 檔案

$ podman generate systemd --name myweb --files --new

## 啟用並啟動服務

$ systemctl --user enable --now container-myweb.service
```

#### Podman Compose

雖然 Podman 相容 Docker Compose，但在某些場景下你可能需要明確使用 `podman-compose`。

```bash
$ pip3 install podman-compose
$ podman-compose up -d
```

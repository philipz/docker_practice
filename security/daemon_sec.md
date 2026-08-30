## 伺服端防護

Docker 守護程式（`dockerd`）是容器生命週期的核心驅動力。預設情況下，Docker 服務的執行需要極高的系統特權（root 權限），因此其安全性關係到整台宿主機的生死存亡。

如果 Docker 守護程式的存取控制沒有做好，惡意攻擊者可以透過 Docker API 輕易地啟動一個特權容器，並將宿主機的根目錄（`/`）掛載到容器中，從而完全接管伺服器。

為了加強對服務端的保護，我們需要從存取控制、通訊加密和權限最小化三個維度進行加固。

### 限制 API 存取

Docker 客戶端（`docker` 命令）透過 REST API 與守護程式進行通訊。

在早期版本中，Docker 有時會綁定在 `127.0.0.1` 的 TCP 套接字上，但這容易遭遇跨站腳本（跨協定）攻擊。現在的發行版預設使用 Unix Domain Socket（`/var/run/docker.sock`）並依賴檔案系統的權限控制。

#### 原則 1：決不可將無認證的 TCP 埠號暴露在公網

這是最常見的 Docker 被入侵抓去挖礦的原因！絕不能在沒有任何安全控制的情況下強行開啟 `-H tcp://0.0.0.0:2375`。

如果業務確實需要遠端存取 Docker 守護程式，**必須啟用 TLS 認證機制**，讓客戶端和服務端互相進行證書校驗。

#### 開啟 TLS 認證雙向加密

利用安全機制，確保只有經過授權的主機網路，並在強證書保護下進行通訊：

1. 首先使用 `openssl` 或基於本地 CA 工具生成一套客戶端與伺服器的證書。
2. 設定 Docker 守護程式（通常是 `daemon.json` 或 `dockerd` 啟動參數），指定證書路徑：

```bash
dockerd \
  --tlsverify \
  --tlscacert=ca.pem \
  --tlscert=server-cert.pem \
  --tlskey=server-key.pem \
  -H=0.0.0.0:2376
```

3. 客戶端想要連接時，也必須出示客戶端證書。

> [!TIP]
> 設定 TLS 生成證書的完整步驟可以查閱 [Docker 官方 TLS 文件](https://docs.docker.com/engine/security/protect-access/)。在現代編排系統（如 Kubernetes）中，通常會有自動化方案管理這些憑證。

### 保護本地 Socket 存取

哪怕不開啟網路埠號，本地的 `/var/run/docker.sock` 也需要謹慎對待。

任何被授予該 Socket 讀寫權限的使用者（通常被加入 `docker` 使用者群組），等同於擁有了對宿主機的零成本提權途徑，即「無需密碼的免密 `sudo` 權限」。

> [!CAUTION]
> 永遠不要將不可信的普通使用者加入到 `docker` 使用者群組中。同樣，在容器編排時盡量避免將宿主機的 `/var/run/docker.sock` 直接映射給普通容器使用，這種模式被稱為 Docker-in-Docker (DinD) 或 Docker-out-of-Docker (DooD)，存在極高的越權風險。

### Rootless 模式：非特權執行

為了從根本上解決「擁有 Docker socket 就是 root」的問題，Docker 自 19.03 版本（2019 年）起提供了 **Rootless 模式**。

Rootless 模式允許在完全侷限於非 `root` 使用者的環境中執行 Docker 守護程式（`dockerd`）和容器。該模式利用了現代 Linux 核心的 User Namespace 技術和非特權網路命名空間實作。

#### 設定執行 Rootless Docker

要在非 root 環境中執行 Docker，需要先滿足宿主機條件：安裝 `newuidmap` / `newgidmap`，並在 `/etc/subuid` 與 `/etc/subgid` 中為該使用者分配足夠的 subordinate UID/GID。若系統級 Docker daemon 仍在執行，命令行也仍可能連到 rootful socket，因此應明確切換 Docker context 或 `DOCKER_HOST`。

1. 安裝必要的依賴（通常是 `uidmap` 工具包以便系統支援 `newuidmap` 和 `newgidmap`）：
```bash
$ sudo apt-get install uidmap
```

2. 切換到一個沒有任何 `sudo` 權限的普通使用者（假設使用者名為 `testuser`）：
```bash
$ su - testuser
```

3. 下載並檢查 Docker 官方提供的 Rootless 安裝腳本，確認來源和內容後再執行：
```bash
$ curl -fsSL https://get.docker.com/rootless -o install-rootless-docker.sh
$ less install-rootless-docker.sh
$ sh install-rootless-docker.sh
```

4. 設定環境變數指向新建立的私有 socket：
```bash
$ export DOCKER_HOST=unix:///run/user/1000/docker.sock
$ docker version
```
安裝並暴露相應的設定後，該使用者的環境將能獨立啟動屬於他自己的 Docker Daemon。即使由於某些未知 0-Day 漏洞使得攻擊者突破了容器，他們也只會受限於 `testuser` 這個非特權使用者所在的有限系統環境內。

> [!NOTE]
> Rootless 模式不是無條件替代 rootful Docker。埠號綁定、網路、cgroup、儲存驅動程式和系統服務自啟動能力都受發行版、核心與 systemd 使用者服務設定影響；生產環境應先驗證具體工作負載，並用 `loginctl enable-linger <user>` 等方式明確設定開機自啟動。

### 授權外掛程式（Authorization Plugin）與存取策略

在企業環境中，對 Docker 守護程式的存取控制往往不僅限於檔案系統權限，還需要更細緻的授權策略。**Authorization Plugin** 機制允許在 API 層級對請求進行攔截和審批。

常見的授權外掛程式包括：

- **OPA/Conftest**：開放策略引擎，支援宣告式策略定義。
- **Prisma Cloud（Twistlock）**：商業容器安全平台。
- 自訂腳本：根據請求內容（映像檔、命令、使用者等）做出允許/拒絕決定。

#### 設定 Authorization Plugin

在 `daemon.json` 中指定授權外掛程式：

```json
{
  "authorization-plugins": ["myauthorizer"]
}
```

此後，Docker 守護程式會在執行任何 API 請求前，將請求轉發給授權外掛程式進行審批。

> [!CAUTION]
> 重要的安全事項：在設定 Authorization Plugin 時，務必確保外掛程式本身的可靠性和及時更新。歷史上已發現多個 AuthZ 驗證繞過漏洞，可能導致攻擊者繞過授權檢查並取得宿主機存取權限。建議：
> - 定期審計授權外掛程式的日誌，檢查是否有可疑的請求被錯誤允許。
> - 使用來自可信來源的授權外掛程式，並保持其版本最新。
> - 將授權檢查結果與其他安全措施（如 TLS 認證、Rootless 模式）結合使用，建立縱深防禦。

### 結語

保障 Docker 服務端的安全主要是做減法：關閉不必要的網路監聽點，嚴管 Socket 存取權限。在基礎系統、網路和儲存約束都驗證通過後，Rootless 模式是一項值得優先評估的安全加固選擇。

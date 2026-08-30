## Docker Hub

### 什麼是 Docker Hub

Docker Hub 是 Docker 的中央映像檔倉庫，透過它您可以輕鬆地分享和取得 Docker 映像檔。


[Docker Hub](https://hub.docker.com/) 是 Docker 官方維護的公共映像檔倉庫，也是全球最大的容器映像檔庫。

它提供了：

- **官方映像檔**：由 Docker 官方和軟體廠商（如 Nginx，MySQL，Node.js）維護的高品質映像檔。
- **個人/組織倉庫**：使用者可以上傳自己的映像檔。
- **自動建立**：與 GitHub/Bitbucket 整合的歷史功能，Docker 已標記為 deprecated，並計劃於 2027-04-01 完全退役。
- **Webhooks**：映像檔更新時觸發回呼。

---

### 核心功能

#### 1. 搜尋映像檔

我們可以透過 `docker search` 命令來查詢官方倉庫中的映像檔，並利用 `docker pull` 命令來將它下載到本地。


除了網頁搜尋，也可以使用命令行：

```bash
$ docker search centos
NAME      DESCRIPTION                                  STARS     OFFICIAL
centos    DEPRECATED; The official build of CentOS.    7000+     [OK]
```
> **技巧**：始終優先使用 `OFFICIAL` 標記為 `[OK]` 的映像檔，安全性更有保障。

#### 2. 拉取映像檔

```bash
$ docker pull nginx:alpine
```

#### 3. 推送映像檔

需要先登入：

```bash
$ docker login

## 預設情況下，不帶其他參數進行 docker login 會自動走 Device Code Web Flow (瀏覽器認證)
## 若在非互動 CI 環境中，推薦結合 --username 與 --password-stdin 參數使用

...
```
打標籤並推送：

```bash
## 1. 標記映像檔

$ docker tag myapp:v1 username/myapp:v1

## 2. 推送

$ docker push username/myapp:v1
```
---

### 限制與配額

#### 映像檔拉取限制

Docker Hub 對不同類型使用者實施拉取速率限制（基於 6 小時週期）：

| 使用者類型 | 限制 |
|---------|------|
| **匿名使用者**（未登入）| 每 6 小時 100 次請求 |
| **免費帳戶**（已登入）| 每 6 小時 200 次請求 |
| **Pro/Team/Business 帳戶** | 無限制（公平使用政策） |

> **注意**：Docker 曾計劃於 2025 年 4 月調整拉取限制策略，但在 2025 年 2 月宣布取消該計劃。目前付費訂閱使用者享有無限制拉取額度，匿名使用者和免費帳戶的限制保持不變。建議在 CI/CD 環境中始終設定 `docker login` 以獲得更高的拉取額度。

#### 濫用限流

除了上述針對特定帳號拉取映像檔數量的 Pull Rate Limit 之外，Docker Hub 對所有使用者（包含已認證及付費使用者）還實施了 **濫用保護限流 (Abuse Rate Limiting)**。它是根據網路出口 IP（IPv4 或 IPv6 /64 子網）計算整體請求頻率，閾值動態觸發（通常為每分鐘數千級別請求）。

**兩類的差異與排查方法**：

- **Pull Rate Limit**：針對拉取量達到上限。報錯回傳 `429 Too Many Requests`，並且 HTTP 回傳體/CLI 錯誤提示中會帶有明確的 `toomanyrequests: You have reached your pull rate limit` 提示，常附有帳戶升級連結。
- **Abuse Rate Limit**：防範介面頻率打擊。報錯僅回傳簡化的 `429 Too Many Requests`。這一限流不分付費與否，常發生在「多終端共享出口 IP」的企業區域網路或者第三方雲 CI 服務（如 GitHub Actions 等）中，即使你已正常設定 `docker login` 也依舊可能觸發。

> **提示**：如果在 CI/CD 等環境遇到 429 錯誤，建議：
> 1. 先甄別具體是哪類限流：普通的 pull rate limit 只要在 CI 中設定 `docker login`（並使用有效帳號）就能解除匿名限制。
> 2. 如果是 Abuse 頻控導致，應考慮搭建私有倉庫作為拉取快取代理 (Registry pull-through cache)，避免頻繁直接請求官方 Hub。
> 3. 使用國內映像檔加速器。

---

### 安全最佳實踐

#### 1. 啟用 2FA：雙因素認證

為了保護您的 Docker Hub 帳號安全，我們建議採取以下措施。


在 Account Settings -> Security 中啟用 2FA，保護帳號安全。啟用後，CLI 登入需要使用 **Access Token** 而非密碼。

#### 2. 使用 Access Token

> **⚠️ 警告**：絕不要在腳本或 CI/CD 系統中，直接使用 `-p` 參數傳遞密碼或 Token（類似 `docker login -p xxx`）！這會導致憑證直接暴露在系統的命令歷史、程式列表和終端輸出中。

1. 在 Docker Hub -> Account Settings -> Security -> Access Tokens 建立 Token (PAT)。
2. 將 Token 保存在權限受限的本地檔案或 CI secret 中，再透過標準輸入 (stdin) 傳遞給 Docker，避免把真實 Token 寫進腳本、命令歷史或日誌：

```bash
$ chmod 600 "$HOME/.dockerhub-token"
$ cat "$HOME/.dockerhub-token" | docker login --username username --password-stdin
```

#### 3. 關注映像檔漏洞

Docker Hub 提供 Docker Scout 安全掃描功能。官方映像檔的漏洞掃描結果對所有使用者免費可見。Docker Scout 的持續掃描功能在免費層可以覆蓋 1 個私有倉庫，付費使用者可以掃描更多倉庫。在映像檔標籤頁可以看到漏洞掃描結果。

---

### Webhooks

當映像檔被推送時，可以自動觸發 HTTP 回呼（例如通知 CI 系統部署）。

**設定方法**：
倉庫頁面 -> Webhooks -> Create Webhook。

---

### 自動建立

> ⚠️ Docker Hub Automated Builds 已被 Docker 標記為 deprecated，並計劃於 2027-04-01 完全退役；新專案應優先使用 GitHub Actions、Buildx 或自有 CI 建立並推送映像檔。

對於仍在遷移期內的舊倉庫，連結 GitHub/Bitbucket 倉庫後，當程式碼有提交或打標籤時，Docker Hub 會自動執行建立。不要把它作為新架構的預設方案。

---

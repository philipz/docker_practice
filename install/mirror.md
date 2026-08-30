## 映像檔加速器

大陸從 Docker Hub 拉取映像檔有時會遇到困難，此時可以設定映像檔加速器。

> ⚠️ **注意**：映像檔加速器的可用性經常變化。設定前請先存取 [docker-practice/docker-registry-cn-mirror-test](https://github.com/docker-practice/docker-registry-cn-mirror-test/actions) 查看各映像檔站的即時狀態。

### 推薦設定方案

針對不同的使用情境，我們推薦以下幾種映像檔加速設定方案，以確保最佳的拉取速度。

> ⚠️ **重要提示**：大陸大多數 Docker Hub 加速服務已於 2024 年中旬關閉（包括阿里雲、騰訊雲、網易雲、百度雲等）。如下推薦的映像檔源可用性因人而異，建議先測試可用性再設定。

1. **雲伺服器使用者**：優先使用所在雲平台提供的內部加速器（見本頁末尾「雲服務商」部分）
2. **本地開發使用者**：優先使用自建 pull-through cache；如果必須依賴社群映像檔，請先用上面的測試倉庫確認即時可用性
3. **代理方案**：如有條件，可設定 HTTP 代理直接存取 Docker Hub

更穩妥的長期方案是使用**自己控制的 pull-through cache / registry mirror**，或者優先使用雲廠商提供的內網映像檔。下文統一用 `https://<your-registry-mirror>` 作為佔位符；如果你選擇第三方公共站，請先確認可用性、服務條款和快取策略。

### Ubuntu 22.04+、Debian 12+、Rocky/Alma/CentOS Stream 9+

目前主流 Linux 發行版均已使用 [systemd](https://systemd.io/) 進行服務管理，這裡介紹如何在使用 systemd 的 Linux 發行版中設定映像檔加速器。

請首先執行以下命令，查看是否在 `docker.service` 檔案中設定過映像檔位址。

```bash
$ systemctl cat docker | grep '\-\-registry\-mirror'
```
如果該命令有輸出，那麼請執行 `$ systemctl cat docker` 查看 `ExecStart=` 出現的位置，修改對應的檔案內容去掉 `--registry-mirror` 參數及其值，並按接下來的步驟進行設定。

如果以上命令沒有任何輸出，那麼就可以在 `/etc/docker/daemon.json` 中寫入如下內容（如果檔案不存在請新建該檔案）：

```json
{
  "registry-mirrors": [
    "https://<your-registry-mirror>"
  ]
}
```
> 注意，一定要保證該檔案符合 json 規範，否則 Docker 將不能啟動。

之後重新啟動服務。

```bash
$ sudo systemctl daemon-reload
$ sudo systemctl restart docker
```

### Windows 10/11

對於使用 `Windows 10/11` 的使用者，在工作列托盤 Docker 圖示內開啟 `Settings`，在左側導覽選單選擇 `Docker Engine`，在右側像下邊一樣編輯 JSON 檔案，之後點擊 `Apply & Restart` 儲存後 Docker 就會重啟並應用設定的映像檔位址了。

```json
{
  "registry-mirrors": [
    "https://<your-registry-mirror>"
  ]
}
```

### macOS

對於使用 macOS 的使用者，在工作列點擊 Docker Desktop 應用圖示 -> `Settings...`，在左側導覽選單選擇 `Docker Engine`，在右側像下邊一樣編輯 json 檔案。修改完成之後，點擊 `Apply & restart` 按鈕，Docker 就會重啟並應用設定的映像檔位址了。

```json
{
  "registry-mirrors": [
    "https://<your-registry-mirror>"
  ]
}
```

### 檢查加速器是否生效

執行 `$ docker info`，如果從結果中看到了如下內容，說明設定成功。

```bash
Registry Mirrors:
 https://<your-registry-mirror>/
```

### Kubernetes 官方映像檔位址遷移

Kubernetes 社群已將官方映像檔位址從 `k8s.gcr.io` 遷移到 `registry.k8s.io`。建議優先使用新位址。若需查找大陸可用的替代映像檔，可以登入 [阿里雲容器映像檔服務](https://www.aliyun.com/product/acr)，在 **映像檔中心** -> **映像檔搜尋** 中查找對應映像檔。

一般情況下有如下對應關係：

```bash
$ docker pull registry.k8s.io/xxx
```

### 已停止服務的映像檔列表

以下映像檔源已停止服務，新增無用的映像檔加速器會拖慢拉取速度，請從設定中刪除：

* https://hub.atomgit.com （已於 2024 年底關閉）
* https://registry.cn-hangzhou.aliyuncs.com （阿里雲 Docker 加速已於 2024 年關閉）
* https://dockerhub.azk8s.cn （已轉為私有）
* https://reg-mirror.qiniu.com （已停止服務）
* https://registry.docker-cn.com （已停止服務）
* https://hub-mirror.c.163.com （網易雲映像檔已於 2024 年關閉）
* https://mirror.baidubce.com （百度雲映像檔已停止）

建議 **watch（頁面右上角）** [映像檔測試倉庫](https://github.com/docker-practice/docker-registry-cn-mirror-test) 這個 GitHub 倉庫，我們會持續更新各映像檔源的可用狀態。

### 雲服務商

某些雲服務商提供了 **僅供內部** 存取的映像檔服務，當您的 Docker 執行在雲平台時可以選擇它們。

* [騰訊雲 `https://mirror.ccs.tencentyun.com`](https://cloud.tencent.com/product/tke)

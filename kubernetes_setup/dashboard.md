## 14.7 視覺化管理介面

[Kubernetes Dashboard](https://github.com/kubernetes-retired/dashboard) 是歷史上常用的 Kubernetes Web UI，但專案已停止維護。

> **注意**：Kubernetes 官方文件已將 Dashboard 標記為 deprecated and unmaintained，新安裝建議考慮 [Headlamp](https://headlamp.dev/) 等仍在維護的替代方案。以下 Dashboard 內容僅供歷史遷移或存量環境參考。

![圖](../_images/kubernetes-dashboard-ui.png)

### 14.7.1 推薦替代：Headlamp

Headlamp 是 Kubernetes SIG UI 下的現代 Web UI，可透過 Helm 安裝：

```bash
$ helm repo add headlamp https://kubernetes-sigs.github.io/headlamp/
$ helm install headlamp headlamp/headlamp --namespace kube-system
```

本地存取時優先使用埠號轉發，避免直接把管理介面暴露到公網：

```bash
$ kubectl -n kube-system port-forward svc/headlamp 4466:80
```

### 14.7.2 歷史 Dashboard 部署

Dashboard 7.0+ 版本僅支援透過 Helm 安裝：

```bash
$ helm repo add kubernetes-dashboard https://kubernetes-retired.github.io/dashboard/

$ helm upgrade --install kubernetes-dashboard kubernetes-dashboard/kubernetes-dashboard \
  --create-namespace --namespace kubernetes-dashboard
```

### 14.7.3 存取

透過埠號轉發存取 Dashboard：

```bash
$ kubectl -n kubernetes-dashboard port-forward svc/kubernetes-dashboard-kong-proxy 8443:443
```

然後在瀏覽器開啟 `https://localhost:8443` 即可存取。

### 14.7.4 登入

為歷史 Dashboard 建立只讀服務帳戶並取得短期登入令牌。不要為 Dashboard 建立 `cluster-admin` 繫結；如果確實需要臨時管理員權限，應走單獨的 break-glass 審批和審計流程。

```bash
$ kubectl create sa dashboard-readonly -n kubernetes-dashboard

$ kubectl create clusterrolebinding dashboard-readonly \
  --clusterrole=view \
  --serviceaccount=kubernetes-dashboard:dashboard-readonly

$ kubectl create token dashboard-readonly -n kubernetes-dashboard --duration=1h
```

將輸出的令牌貼上到登入頁面，即可登入。

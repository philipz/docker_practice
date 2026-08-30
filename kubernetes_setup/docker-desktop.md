## 14.3 在 Docker Desktop 使用

使用 Docker Desktop 可以很方便的啟用 Kubernetes。

### 14.3.1 啟用 Kubernetes

在 Docker Desktop 設定頁面，進入 `Kubernetes`，建立或啟用集群。較新的 Docker Desktop 可選擇 `kind` 或 `kubeadm` 作為集群建立方式；日常本地開發優先選擇 `kind`，因為它支援多節點和版本選擇。

![圖](../_images/settings-kubernetes.png)

> 注意：Docker Desktop Kubernetes 的控制平面映像檔預設從 Docker Hub 拉取，例如 `docker.io/docker/desktop-*` 或 `docker.io/kindest/node:<tag>`。如果企業網路不能存取 Docker Hub，應按 Docker Desktop 的 `KubernetesImagesRepository` 設定映像檔倉庫，並用 `docker desktop kubernetes images list`（Docker Desktop 4.44+）或 `docker ps` 確認實際映像檔標籤。普通 Docker Engine 的 `registry-mirrors` 不會自動改寫這些控制平面映像檔。

### 14.3.2 測試

```bash
$ kubectl version
$ kubectl config use-context docker-desktop
$ kubectl get nodes
```
如果 `kubectl get nodes` 顯示節點為 `Ready`，則證明 Kubernetes 成功啟動。

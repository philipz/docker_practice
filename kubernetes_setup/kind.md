## 14.4 Kind - Kubernetes IN Docker

[Kind](https://kind.sigs.k8s.io/) (Kubernetes in Docker) 是一個使用 Docker 容器作為節點執行本地 Kubernetes 集群的工具。主要用於測試 Kubernetes 本身，也非常適合本地開發和 CI 環境。

> **版本說明**：本文檔基於 Kind v0.31.0 編寫。Kind 會根據下載時的預設行為自動拉取對應的 Kubernetes 版本。建議定期更新 Kind 到最新版本以獲得最新的 Kubernetes 支援。詳見 [Kind Releases](https://github.com/kubernetes-sigs/kind/releases)。

### 14.4.1 為什麼選擇 Kind

Kind 相比其他本地集群方案（如 Minikube）有以下顯著優勢：

*   **輕量便捷**：只要有 Docker 環境即可，無需額外虛擬機。
*   **多集群支援**：可以輕鬆在本地啟動多個集群。
*   **多版本支援**：支援指定 Kubernetes 版本進行測試。
*   **HA 支援**：支援模擬高可用集群（多 Control Plane）。

### 14.4.2 安裝 Kind

Kind 是一個二進位檔案，放到 PATH 中即可使用。以下是不同系統的安裝方法。

#### macOS

```bash
brew install kind
```

#### Linux / Windows

可以下載二進位檔案：

```bash
# Linux AMD64
# 注意：v0.31.0 為編寫本文檔時的最新版本，請根據需要替換為目前版本
# 參見 https://github.com/kubernetes-sigs/kind/releases

curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.31.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind
```

### 14.4.3 建立集群

最簡單的建立方式：

```bash
kind create cluster
```
指定集群名稱：

```bash
kind create cluster --name my-cluster
```

### 14.4.4 與集群互動

Kind 會自動將 kubeconfig 合併到 `~/.kube/config`。

```bash
kubectl cluster-info --context kind-kind
kubectl get nodes
```

### 14.4.5 進階用法：設定集群

建立一個 `kind-config.yaml` 來定製集群，例如映射埠號到宿主機：

```yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  extraPortMappings:
  - containerPort: 80
    hostPort: 8080
    protocol: TCP
- role: worker
- role: worker
```
應用設定：

```bash
kind create cluster --config kind-config.yaml
```

### 14.4.6 刪除集群

```bash
kind delete cluster
```

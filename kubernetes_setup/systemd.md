## 14.6 一步步部署 Kubernetes 集群

### 14.6.1 概述

部署 Kubernetes 集群涉及多個元件的安裝和設定，包括 Master 節點和 Worker 節點。本章介紹如何使用 systemd 管理這些服務的生命週期。

### 14.6.2 Kubernetes 主要元件

#### Master 節點元件

- **kube-apiserver**：API 伺服器，Kubernetes 集群的中心
- **kube-controller-manager**：控制器管理器
- **kube-scheduler**：調度器，負責 Pod 調度
- **etcd**：分散式鍵值儲存，儲存集群資料

#### Worker 節點元件

- **kubelet**：節點代理，管理容器生命週期
- **kube-proxy**：網路代理，處理服務網路
- **Container Runtime**：容器執行時（Docker、containerd 等）

### 14.6.3 使用 systemd 管理 Kubernetes 服務

#### 服務單元檔案

為了讓 systemd 管理 Kubernetes 服務，需要建立相應的 `.service` 檔案，例如：

```text
/etc/systemd/system/kubelet.service
/etc/systemd/system/kube-proxy.service
/etc/systemd/system/kube-apiserver.service
```

#### 常用命令

```bash
# 啟動服務
sudo systemctl start kubelet

# 停止服務
sudo systemctl stop kubelet

# 重啟服務
sudo systemctl restart kubelet

# 查看服務狀態
sudo systemctl status kubelet

# 設定開機自啟
sudo systemctl enable kubelet
```

如果希望查看更完整的 systemd 部署案例，可以參考 `opsnull/follow-me-install-kubernetes-cluster` 這類社群專案，再結合本章前文的 kubeadm 與元件設定說明理解整體流程。

### 14.6.4 推薦學習路徑

1. 理解 Kubernetes 架構和各元件的作用
2. 準備所需的系統環境（Linux 主機、網路設定等）
3. 按步驟安裝各個 Kubernetes 元件
4. 設定 systemd 服務單元檔案
5. 驗證集群健康狀態

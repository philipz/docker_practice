## 14.5 K3s - 輕量級 Kubernetes

[K3s](https://k3s.io/) 是一個輕量級的 Kubernetes 發行版，由 Rancher Labs 開發。它專為邊緣運算、物聯網、CI、ARM 等資源受限的環境設計。K3s 被打包為單個二進位檔案，只有不到 100MB，但通過了 CNCF 的一致性測試。

> **版本說明**：K3s 版本與 Kubernetes 版本對應。安裝指令碼會自動拉取最新穩定版本。如需指定特定版本，可在安裝時設定 `INSTALL_K3S_VERSION` 環境變數。詳見 [K3s Releases](https://github.com/k3s-io/k3s/releases)。

### 14.5.1 核心特性

*   **輕量級**：移除過時的、非必須的 Kubernetes 功能（如傳統的雲提供商外掛），使用 SQLite 作為預設資料儲存（也支援 Etcd/MySQL/Postgres）。
*   **單一二進位**：所有元件 (API Server，Controller Manager，Scheduler，Kubelet，Kube-proxy) 打包在一個程式中執行。
*   **開箱即用**：內建 Helm Controller、Traefik Ingress controller、ServiceLB、Local-Path-Provisioner。
*   **安全**：預設啟用安全設定，基於 TLS 通訊。

### 14.5.2 安裝

K3s 的安裝非常簡單，官方提供了便捷的安裝指令碼。

#### 指令碼安裝

K3s 提供了極為便捷的安裝指令碼。該命令會從網路下載指令碼並直接交給 `sh` 執行，生產環境建議先下載審查指令碼內容，並按官方文件固定版本或安裝引數：

```bash
curl -sfL https://get.k3s.io | sh -
```
安裝完成後，K3s 會自動啟動並設定好 `systemd` 服務。

#### 查看狀態

```bash
sudo k3s kubectl get nodes
```
輸出類似：
```bash
NAME          STATUS   ROLES                  AGE   VERSION
k3s-master    Ready    control-plane,master   1m    v1.36.0+k3s1
```

> **版本說明**：輸出中的 `v1.36.0+k3s1` 為編寫本文檔時的版本示例。實際輸出版本號取決於你所安裝的 K3s 版本。更多資訊請參見 [K3s Releases](https://github.com/k3s-io/k3s/releases)。

### 14.5.3 快速使用

K3s 內建了 `kubectl` 命令（透過 `k3s kubectl` 呼叫），為了方便，通常會建立別名或設定 `KUBECONFIG`。

```bash
## 讀取 K3s 的設定檔案

export KUBECONFIG=/etc/rancher/k3s/k3s.yaml

## 現在可以直接使用 kubectl

kubectl get pods -A
```

### 14.5.4 清理解除安裝

```bash
/usr/local/bin/k3s-uninstall.sh
```

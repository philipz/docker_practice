## 14.2 使用 kubeadm 部署 Kubernetes：使用 Docker

`kubeadm` 提供了 `kubeadm init` 以及 `kubeadm join` 這兩個命令，作為快速建立 `Kubernetes` 集群的最佳實務。

> **版本說明**：本文檔基於 Kubernetes v1.36 編寫。Kubernetes 版本更新較快（約每 4 個月一個新版本），本文檔中的第三方工具版本（如 cri-dockerd、flannel）僅為示例，請根據實際需求更新至目前版本。更完整的安裝和相容性說明請以 [Kubernetes 官方文件](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/) 為準。

> ⚠️ **強烈提示：Docker 與 Kubernetes 環境的時代分界**
>
> 自 Kubernetes v1.24 起，內建的 `dockershim` 元件已被正式移除。這意味著 **Kubernetes 不再將 Docker Engine 作為預設內建的容器執行時**。雖然 Docker 仍然是你本地建立、管理映像檔的絕佳工具，但它已不再是 kubelet 的預設執行時選項。
>
> 因此，**強烈推薦** 讀者直接參考同目錄下的《[使用 kubeadm 部署 Kubernetes（CRI 使用 containerd）](kubeadm.md)》作為主要的部署路線。
>
> 本文檔保留，主要用於歷史環境維護或特殊需求場景：如果你必須在較新的 Kubernetes 集群中繼續使用 Docker Engine 作為底層執行時，你必須理解 CRI 層機制，額外部署並設定第三方相容層 `cri-dockerd`，同時在部署時手動補充 `--cri-socket` 等引數約束。

### 14.2.1 安裝 Docker

參考[安裝 Docker](../install/README.md) 一節安裝 Docker。

### 14.2.2 安裝並設定 cri-dockerd

由於 Kubernetes v1.24 移除了內建的 dockershim，需要額外安裝 **cri-dockerd** 作為 Docker 與 kubelet 之間的 CRI（Container Runtime Interface）適配層。

#### Ubuntu/Debian

```bash
# 安裝 cri-dockerd
# 注意：以下以 v0.4.3 為示例；安裝前請到 releases 頁面核驗目前版本和校驗值
# 參見 https://github.com/Mirantis/cri-dockerd/releases

$ cd /tmp
$ wget https://github.com/Mirantis/cri-dockerd/releases/download/v0.4.3/cri-dockerd-0.4.3.amd64.tgz
$ tar xzvf cri-dockerd-0.4.3.amd64.tgz
$ sudo mv cri-dockerd/cri-dockerd /usr/local/bin/

# 下載並安裝 systemd service 檔案

$ wget https://raw.githubusercontent.com/Mirantis/cri-dockerd/master/packaging/systemd/cri-docker.service
$ wget https://raw.githubusercontent.com/Mirantis/cri-dockerd/master/packaging/systemd/cri-docker.socket
$ sed -i -e 's,/usr/bin/cri-dockerd,/usr/local/bin/cri-dockerd,' cri-docker.service
$ sudo mv cri-docker.service cri-docker.socket /etc/systemd/system/

# 啟動 cri-dockerd

$ sudo systemctl daemon-reload
$ sudo systemctl enable cri-docker
$ sudo systemctl start cri-docker

# 驗證安裝

$ sudo /usr/local/bin/cri-dockerd --version
```

#### CentOS/Fedora

```bash
# 安裝 cri-dockerd
# 注意：以下以 v0.4.3 為示例；安裝前請到 releases 頁面核驗目前版本和校驗值
# 參見 https://github.com/Mirantis/cri-dockerd/releases

$ cd /tmp
$ wget https://github.com/Mirantis/cri-dockerd/releases/download/v0.4.3/cri-dockerd-0.4.3.amd64.tgz
$ tar xzvf cri-dockerd-0.4.3.amd64.tgz
$ sudo mv cri-dockerd/cri-dockerd /usr/local/bin/

# 下載並安裝 systemd service 檔案

$ wget https://raw.githubusercontent.com/Mirantis/cri-dockerd/master/packaging/systemd/cri-docker.service
$ wget https://raw.githubusercontent.com/Mirantis/cri-dockerd/master/packaging/systemd/cri-docker.socket
$ sed -i -e 's,/usr/bin/cri-dockerd,/usr/local/bin/cri-dockerd,' cri-docker.service
$ sudo mv cri-docker.service cri-docker.socket /etc/systemd/system/

# 啟動 cri-dockerd

$ sudo systemctl daemon-reload
$ sudo systemctl enable cri-docker
$ sudo systemctl start cri-docker
```

### 14.2.3 安裝 **kubelet**、**kubeadm**、**kubectl**

需要在每台機器上安裝以下的軟體套件：

#### Ubuntu/Debian

```bash
$ K8S_MINOR="v1.36"

$ sudo apt-get update
$ sudo apt-get install -y ca-certificates curl gpg

$ sudo install -m 0755 -d /etc/apt/keyrings
$ curl -fsSL "https://pkgs.k8s.io/core:/stable:/${K8S_MINOR}/deb/Release.key" | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
$ sudo chmod a+r /etc/apt/keyrings/kubernetes-apt-keyring.gpg

$ echo "deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/${K8S_MINOR}/deb/ /" | sudo tee /etc/apt/sources.list.d/kubernetes.list > /dev/null

$ sudo apt-get update
$ sudo apt-get install -y kubelet kubeadm kubectl

$ sudo apt-mark hold kubelet kubeadm kubectl
```

#### CentOS/Fedora

```bash
$ K8S_MINOR="v1.36"

$ cat <<EOF | sudo tee /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://pkgs.k8s.io/core:/stable:/${K8S_MINOR}/rpm/
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://pkgs.k8s.io/core:/stable:/${K8S_MINOR}/rpm/repodata/repomd.xml.key
EOF

$ sudo yum install -y kubelet kubeadm kubectl
```

### 14.2.4 修改核心的執行引數

#### cgroup v2 要求：必須

Kubernetes v1.36 預設要求節點使用 cgroup v2。kubelet 在 cgroup v1 節點上預設會拒絕啟動，但管理員可以在 kubelet 設定中設定 `failCgroupV1: false` 來相容 cgroup v1（僅建議用於遺留系統過渡期）。驗證節點是否支援 cgroup v2：

```bash
$ mount | grep cgroup2
```

如果輸出包含 `cgroup2`，則系統已支援 cgroup v2。對於仍在使用 cgroup v1 的系統（如較舊的 RHEL 8），建議升級核心或更新系統設定以啟用 cgroup v2。

#### 載入核心模組

```bash
$ cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF

$ sudo modprobe overlay
$ sudo modprobe br_netfilter
```

#### swap 設定：現代集群仍建議優先關閉

在現代 Kubernetes 中，Linux 節點已經支援更細粒度的 swap 行為控制。對於多數 `kubeadm` 教學環境，**優先關閉 swap 仍然是最穩妥的預設做法**，因為這樣最接近常見生產基線，也能避免不同發行版和 kubelet 設定差異帶來的排障成本。

如果你明確要在啟用 swap 的前提下執行節點，則應額外核對 kubelet 的 `NoSwap` / `LimitedSwap` 設定與目前 Kubernetes 版本文檔，而不要把「開著 swap 也能跑」直接當作通用預設路徑。

```bash
$ sudo swapoff -a

# 如需永久禁用，可在 /etc/fstab 中註解 swap 對應行
```
```bash
$ cat <<EOF | sudo tee /etc/sysctl.d/99-kubernetes-cri.conf
net.bridge.bridge-nf-call-iptables  = 1
net.ipv4.ip_forward                 = 1
net.bridge.bridge-nf-call-ip6tables = 1
EOF

# 應用設定

$ sudo sysctl --system
```

### 14.2.5 設定 kubelet

為了讓 kubelet 正確執行，我們需要對其進行一些必要的設定。

#### 修改 `kubelet.service`（可選：IPVS 模式）

> **注意**：kube-proxy 的 IPVS 模式已在 Kubernetes 1.35 中被標記為棄用；Kubernetes 1.36 文件仍將其列為已棄用模式，並推薦遷移到 nftables。新部署應使用預設的 iptables 模式或 nftables 模式（Kubernetes 1.33+ 穩定）。以下 IPVS 設定僅供舊環境參考。

`/etc/systemd/system/kubelet.service.d/10-proxy-ipvs.conf` 寫入以下內容

```bash
# 啟用 ipvs 相關核心模組（已棄用，建議遷移至 nftables）

[Service]
ExecStartPre=-/sbin/modprobe ip_vs
ExecStartPre=-/sbin/modprobe ip_vs_rr
ExecStartPre=-/sbin/modprobe ip_vs_wrr
ExecStartPre=-/sbin/modprobe ip_vs_sh
```
執行以下命令應用設定。

```bash
$ sudo systemctl daemon-reload
```

### 14.2.6 部署

安裝設定完成後，我們將分別在 Master 節點和 Worker 節點上進行部署操作。

#### master

```bash
$ sudo kubeadm init --pod-network-cidr 10.244.0.0/16 \
      --cri-socket unix:///var/run/cri-dockerd.sock \
      --v 5
```

* `--cri-socket unix:///var/run/cri-dockerd.sock` 引數指定使用 cri-dockerd 作為容器執行時介面。
* `--pod-network-cidr 10.244.0.0/16` 引數與後續 CNI 外掛有關，這裡以 `flannel` 為例，若後續部署其他型別的網路外掛請更改此引數。
* kubeadm 預設使用 `registry.k8s.io` 拉取 Kubernetes 控制平面映像檔。受限網路環境可透過 kubeadm 設定檔案中的 `imageRepository` 指向受信任映像檔倉庫；不要把第三方映像檔倉庫當成通用預設值。

> 若 `kubeadm` 預檢失敗，應按提示修復缺失依賴、核心引數、swap 或執行時設定。實驗環境確需忽略預檢時，只忽略明確理解且可接受的單項檢查，不建議使用 `--ignore-preflight-errors=all`。

執行成功會輸出

```bash
...
[addons] Applied essential addon: CoreDNS
I1116 12:35:13.270407   86677 request.go:538] Throttling request took 181.409184ms, request: POST:https://<CONTROL_PLANE_HOST>:6443/api/v1/namespaces/kube-system/serviceaccounts
I1116 12:35:13.470292   86677 request.go:538] Throttling request took 186.088112ms, request: POST:https://<CONTROL_PLANE_HOST>:6443/api/v1/namespaces/kube-system/configmaps
[addons] Applied essential addon: kube-proxy

Your Kubernetes control-plane has initialized successfully!

To start using your cluster, you need to run the following as a regular user:

  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config

You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  https://kubernetes.io/docs/concepts/cluster-administration/addons/

Then you can join any number of worker nodes by running the following on each as root:

kubeadm join <CONTROL_PLANE_HOST>:6443 --token <TOKEN> \
    --discovery-token-ca-cert-hash sha256:<DISCOVERY_TOKEN_CA_CERT_HASH>
```

#### node 工作節點

在 **另一主機** 重複 **部署** 小節以前的步驟，安裝設定好 kubelet。根據提示，加入到集群。

```bash
$ kubeadm join <CONTROL_PLANE_HOST>:6443 --token <TOKEN> \
    --discovery-token-ca-cert-hash sha256:<DISCOVERY_TOKEN_CA_CERT_HASH> \
    --cri-socket unix:///var/run/cri-dockerd.sock
```

其中 `<CONTROL_PLANE_HOST>`、`<TOKEN>` 和 `<DISCOVERY_TOKEN_CA_CERT_HASH>` 應使用你自己的 `kubeadm init` 輸出，不要複用示例值。

### 14.2.7 查看服務

所有服務啟動後，查看本地實際執行的 Docker 容器。這些服務大概分為三類：主節點服務、工作節點服務和其他服務。

#### 主節點服務

* `apiserver` 是整個系統的對外介面，提供 RESTful 方式供客戶端和其他元件呼叫；

* `scheduler` 負責對資源進行調度，分配某個 pod 到某個節點上；

* `controller-manager` 負責管理控制器，包括 endpoint-controller（重新整理服務和 pod 的關聯資訊）和 replication-controller（維護某個 pod 的複製為設定的數值）。

#### 工作節點服務

* `proxy` 為 pod 上的服務提供存取的代理。

#### 其他服務

* Etcd 是所有狀態的儲存資料庫；

### 14.2.8 使用

將 `/etc/kubernetes/admin.conf` 複製到 `~/.kube/config`

執行 `$ kubectl get all -A` 查看啟動的服務。

由於未部署 CNI 外掛，CoreDNS 未正常啟動。如何使用 Kubernetes，請參考後續章節。

### 14.2.9 部署 CNI

這裡以 `flannel` 為例進行介紹。

#### flannel

檢查 podCIDR 設定

```bash
$ kubectl get node -o yaml | grep CIDR

# 輸出

    podCIDR: 10.244.0.0/16
    podCIDRs:
```
```bash
# 注意：以下以 v0.28.4 為示例；安裝前請到 releases 頁面核驗目前版本
# 參見 https://github.com/flannel-io/flannel/releases
$ kubectl apply -f https://raw.githubusercontent.com/flannel-io/flannel/v0.28.4/Documentation/kube-flannel.yml
```

### 14.2.10 master 節點預設不能執行 pod

如果用 `kubeadm` 部署一個單節點集群，預設情況下無法使用，請執行以下命令解除限制

```bash
$ kubectl taint nodes --all node-role.kubernetes.io/control-plane-

# 較舊版本使用 master taint

# $ kubectl taint nodes --all node-role.kubernetes.io/master-

# 恢復預設值

# $ kubectl taint nodes NODE_NAME node-role.kubernetes.io/control-plane=true:NoSchedule

...
```

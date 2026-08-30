# 第十三章 容器編排基礎

`Kubernetes` 是 Google 發起的開源容器編排系統，它支援多種雲平台與私有資料中心。

`Kubernetes` 負責對容器工作負載進行調度與編排，其目的是讓使用者透過集群宣告式地管理應用，而無需手動介入每個容器的生命週期細節。

Kubernetes 的最小調度單位是 `Pod`。一個 `Pod` 由一組緊密協作的容器構成，它們共享網路命名空間、IP 以及部分儲存資源，也可以根據需要對 Pod 進行埠號映射。

如果你已經熟悉 Docker，可以用以下對照來理解 Kubernetes 的核心概念：Docker 中的「容器」對應 Kubernetes 的 `Pod`（一個或多個容器的組合）；`docker-compose.yml` 的角色類似於 Kubernetes 的 `Deployment` + `Service` 宣告；`docker run` 的埠號映射和網路設定，在 Kubernetes 中由 `Service` 和 `Ingress` 接管。掌握這些映射關係，有助於從單機 Docker 平滑過渡到集群編排。

本章將分為 5 節介紹 `Kubernetes`：

* [簡介](intro.md)
* [基本概念](concepts.md)
* [架構設計](design.md)
* [進階特性](advanced.md)
* [實戰練習](practice.md)

## 本章小結

Kubernetes 是當前最主流的容器編排平台，其宣告式管理模型和豐富的 API 為大規模容器化應用提供了堅實的基礎。

| 概念 | 要點 |
|------|------|
| **Pod** | 最小調度單位，包含一組共享網路和儲存的容器 |
| **Deployment** | 管理無狀態應用的 Pod 副本集，支援滾動更新和回滾 |
| **StatefulSet** | 管理有狀態應用，提供穩定的網路標識和持久化儲存 |
| **DaemonSet** | 確保每個節點執行一個 Pod 副本，適用於日誌、監控等場景 |
| **Job/CronJob** | 執行一次性或定時任務，確保任務成功完成 |
| **Service** | 為 Pod 提供穩定的網路存取入口和負載均衡 |
| **Namespace** | 資源隔離和多租戶支援 |
| **ConfigMap/Secret** | 設定與敏感資訊的管理 |
| **Master 節點** | 執行 API Server、Scheduler、Controller Manager |
| **Worker 節點** | 執行 kubelet、kube-proxy 和容器執行時 |

### 延伸閱讀

- [部署 Kubernetes](../kubernetes_setup/README.md)：搭建 Kubernetes 集群
- [Etcd](../etcd/README.md)：Kubernetes 使用的分散式儲存
- [底層實作](../underly/README.md)：容器技術原理

## 16.1 簡介

> **版本說明**：各雲平台的容器服務版本更新頻繁。本章示例適用於常見的 Kubernetes API 版本。建議存取各雲廠商官方文件（如 [AWS EKS](https://aws.amazon.com/eks/)、[Azure AKS](https://azure.microsoft.com/en-us/products/kubernetes-service/)、[Google GKE](https://cloud.google.com/kubernetes-engine)、[阿里雲 ACK](https://www.aliyun.com/product/ack)、[騰訊雲 TKE](https://cloud.tencent.com/product/tke)）取得最新資訊。

隨著容器技術的普及，目前主流的雲端運算服務商都提供了成熟的容器服務。與容器相關的雲端運算服務主要分為以下幾種類型：

### 16.1.1 容器編排託管服務

這是目前最主流的形式。雲廠商託管 Kubernetes 的控制平面（Master 節點），使用者只需管理工作節點 (Worker Node)。

* **優勢**：降低了 Kubernetes 集群的維護成本，高可用性由廠商保證。
* **典型服務**：AWS EKS，Azure AKS，Google GKE，阿里雲 ACK，騰訊雲 TKE。

### 16.1.2 容器實例服務

這一類服務通常被稱為 CaaS (Container as a Service)。使用者無需管理底層伺服器 (EC2/CVM)，只需提供映像檔和設定即可運行容器。

* **優勢**：極致的彈性，按秒計費，零維運。
* **典型服務**：AWS Fargate，Azure Container Instances，Google Cloud Run，阿里雲 ECI。

### 16.1.3 映像檔倉庫服務

提供安全、可靠的私有 Docker 映像檔儲存服務，通常與雲廠商的 CI/CD 流水線深度整合。

* **典型服務**：AWS ECR，Azure ACR，Google GCR/GAR，阿里雲 ACR。

本章將介紹如何在幾個主流雲平台上使用 Docker 和 Kubernetes 服務。

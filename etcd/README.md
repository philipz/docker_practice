# 第十五章 Etcd 專案

`etcd` 是 `CoreOS` 團隊發起的一個管理設定資訊和服務發現 (`Service Discovery`) 的專案，在這一章裡面，我們將基於 `etcd 3.5 系列`版本介紹該專案的目標、安裝和使用，以及實現的技術。

> **版本說明：** 本章示例基於 etcd 3.5 系列版本編寫。etcd 3.7.0 於 2026 年 7 月釋出，官方仍在維護 3.5、3.6、3.7 三個釋出分支。請存取 [etcd 官方釋出頁](https://github.com/etcd-io/etcd/releases) 取得最新版本資訊。

## 本章內容

* [簡介](intro.md)
* [安裝](install.md)
* [集群](cluster.md)
* [使用 etcdctl](etcdctl.md)

## 本章小結

etcd 是 Kubernetes 的核心儲存元件，為分散式系統提供可靠的鍵值儲存和服務發現能力。

| 概念 | 要點 |
|------|------|
| **定位** | 分散式鍵值儲存系統，用於設定管理和服務發現 |
| **協定** | 基於 Raft 一致性演算法，保證資料強一致 |
| **API** | 提供 gRPC 和 HTTP API |
| **集群** | 建議使用奇數節點（3 或 5 個）部署 |
| **etcdctl** | 命令行管理工具，支援 put/get/del/watch 等操作 |
| **安全** | 支援 TLS 加密通訊和 RBAC 存取控制 |

### 延伸閱讀

- [容器編排基礎](../kubernetes/README.md)：Kubernetes 如何使用 etcd
- [部署 Kubernetes](../kubernetes_setup/README.md)：在集群中部署 etcd

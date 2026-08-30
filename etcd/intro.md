## 15.1 簡介

> **版本說明：** 本章內容基於 etcd 3.5 系列版本編寫。etcd 3.7.0 於 2026 年 7 月釋出，官方仍在維護 3.5、3.6、3.7 三個釋出分支。請存取 [etcd 官方釋出頁](https://github.com/etcd-io/etcd/releases) 取得最新版本資訊。

如圖 15-1 所示，etcd 專案使用該標識。

![etcd 標識](./_images/etcd_logo.png)

圖 15-1：etcd 專案標識

`etcd` 是 `CoreOS` 團隊於 2013 年 6 月發起的開源專案，它的目標是建立一個高可用的分散式鍵值 (`key-value`) 資料庫，基於 `Go` 語言實現。我們知道，在分散式系統中，各種服務的設定資訊的管理分享、服務的發現是一個很基本同時也是很重要的問題。`CoreOS` 專案就希望基於 `etcd` 來解決這一問題。

`etcd` 目前在 [github.com/etcd-io/etcd](https://github.com/etcd-io/etcd) 進行維護。

受到 [Apache ZooKeeper](https://zookeeper.apache.org/) 專案和 [doozer](https://github.com/ha/doozerd) 專案的啟發，`etcd` 在設計的時候重點考慮了下面四個要素：

* 簡單：具有定義良好、面向使用者的 `API` ([gRPC](https://github.com/grpc/grpc))
* 安全：支援 `HTTPS` 方式的存取
* 快速：支援併發 `10 k/s` 的寫操作
* 可靠：支援分散式結構，基於 `Raft` 的一致性演算法

_Apache ZooKeeper 是一套知名的分散式系統中進行同步和一致性管理的工具。_

_doozer 是一個一致性分散式資料庫。_

[_Raft_](https://raft.github.io/) _是一套透過選舉主節點來實現分散式系統一致性的演算法，相比於大名鼎鼎的 Paxos 演算法，它的過程更容易被人理解，由 Stanford 大學的 Diego Ongaro 和 John Ousterhout 提出。更多細節可以參考_ [_raftconsensus.github.io_](http://raftconsensus.github.io)_。_

一般情況下，使用者使用 `etcd` 可以在多個節點上啟動多個例項，並加入它們為一個集群。同一個集群中的 `etcd` 例項將會保持彼此資訊的一致性。

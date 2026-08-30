## 17.7 安全容器執行時期

> **版本說明**：Kata Containers、gVisor 和 Firecracker 均為活躍開發的專案。建議查閱各專案官方文件取得最新版本和相容性資訊：[Kata Containers](https://katacontainers.io/)、[gVisor](https://gvisor.dev/)、[Firecracker](https://firecracker-microvm.github.io/)。

本節介紹容器技術生態中的安全執行時期機制，主要探討在隔離性和安全性上比標準 Linux 容器更進一步的方案，重點介紹 Kata Containers 和 gVisor。

### 17.7.1 為什麼需要安全容器？

標準的 Linux 容器（如 Docker、Podman 或基礎的 containerd/runc 所提供的）依賴於 Linux 核心的 **Namespace（命名空間）** 和 **Cgroups（控制組）** 來實現程式級別的隔離與資源限制。這種輕量級的虛擬化方式共享同一個宿主機的核心。

儘管這種方式在效能和啟動速度上擁有巨大優勢，但也帶來了一個顯著的缺點：**隔離性（Isolation）不足**。如果某個容器內的惡意程式利用了宿主機核心的漏洞完成了越獄（Privilege Escalation），它將對整個宿主機以及其上運行的所有其他容器造成毀滅性威脅。

如果在公有雲環境（多租戶場景）或運行不可信的第三方程式碼時，共享核心顯然是不夠安全的。為了解決這一問題，社群推出了“安全容器（Secure Containers/Sandboxed Containers）”的概念。安全容器的核心理念是：提供類似虛擬機的強隔離性，同時保持類似容器的輕量、快速啟動和標準化管理。

### 17.7.2 什麼是 Kata Containers？

[Kata Containers](https://katacontainers.io/) 是一個開源專案，由 OpenStack Foundation（現更名為 OpenInfra Foundation）託管。它將早期的兩個專案——Intel Clear Containers 和 Hyper runV 結合而成。

Kata Containers 的核心思路是：**使用輕量級的虛擬機（Lightweight VM）來運行每一個容器或者 Pod**。

#### 工作原理

當使用 Kata Containers 時，它不是在宿主機上啟動一個普通的獨立程式，而是呼叫一個精簡高度最佳化的虛擬機管理程式（如 QEMU、Firecracker 或 Cloud Hypervisor）啟動一個小型的虛擬機。容器內的應用程式運行在這個虛擬機擁有獨立特製核心的沙箱中。

- **高度隔離**：因為擁有自己的獨立核心，即使容器內的應用利用核心漏洞溢出，它也只能破壞虛擬機虛擬出來的核心，根本無法觸及宿主機真正的核心。
- **相容性**：Kata Containers 完全實現了 OCI（Open Container Initiative）規範和 CRI（Container Runtime Interface）標準。這意味著它可以作為 `containerd` 或 `Docker` 的底層執行時期無縫替換預設的 `runc`。
- **與 Kubernetes 整合**：在 Kubernetes 中，你可以為一個特定的 Pod 指定 `runtimeClassName: kata`，讓高敏感的任務自動運行在虛擬機級別的隔離環境中。

### 17.7.3 什麼是 gVisor？

[gVisor](https://gvisor.dev/) 是由 Google 開發並開源的一種不同流派的沙箱容器執行時期方案。

它採取了與 Kata Containers 完全不同的技術路線，它不是啟動完整的虛擬機，而是提供了一個 **應用態核心（User-space Kernel）**。

#### 工作原理

gVisor 的核心元件是一個名為 **Sentry** 的使用者空間程式。Sentry 扮演了一個“核心代理”的角色。

- 當容器內的應用想要進行系統呼叫（System Call，比如讀寫檔案、網路通訊）時，這些呼叫會被 Sentry 攔截並進行一層虛擬化處理，然後再由 Sentry 把經過安全過濾和轉換的請求轉發給宿主機核心。
- 因為 Sentry 在使用者態實現了一套 Linux 系統呼叫介面，它極大減少了應用直接接觸底層作業系統核心的表面積。這樣就有效防禦了利用底層核心漏洞突破隔離的攻擊方式。
- gVisor 同樣相容 OCI 規範，其核心執行時期元件稱為 `runsc`，可以作為底層執行時期與 Docker 或 Kubernetes 進行整合。

### 17.7.4 總結與對比

| 特性 | 標準 Linux 容器 (runc) | Kata Containers | gVisor (runsc) |
| :--- | :--- | :--- | :--- |
| **隔離技術** | Namespace & Cgroups | 輕量級虛擬機（獨立核心）| 使用者態核心（系統呼叫攔截）|
| **安全性** | 較低（共享宿主機核心） | 極高（硬體級虛擬化隔離） | 高（減少核心攻擊面） |
| **效能開銷** | 極小（原生程式） | 中等（因輕量化而優於傳統 VM） | 中等到較高（取決於系統呼叫頻率開銷） |
| **啟動速度** | 極快（毫秒/秒級） | 快（秒級之內） | 快（接近原生容器） |
| **相容性** | 完美（所有系統呼叫均支持原始實現） | 極好（擁有完整核心） | 好（但在極少數複雜的未被攔截支持的系統呼叫中可能報錯） |

如今，諸如 AWS 這樣的雲廠商也推出了針對無伺服器容器功能（Serverless Containers）的高度最佳化的輕量級虛擬機管理器 **Firecracker**，可以看作是安全容器生態中與 Kata 類似方案的底層基石。

對於普通的微服務開發來說可能不需要考慮使用安全容器，但在提供多租戶平台即服務（PaaS）、運行無狀態邊緣計算函式（FaaS）等對安全隔離要求極高的場景中，以 Kata Containers 和 gVisor 為代表的安全容器技術展現出了巨大的價值。

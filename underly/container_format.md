## 容器格式

### Docker 容器格式的演進

最初，Docker 採用了 `LXC` 中的容器格式。從 0.7 版本以後開始去除 LXC 的相依，轉而使用自行開發的 [libcontainer](https://github.com/docker/libcontainer)。從 1.11 開始，則進一步演進為使用 [runC](https://github.com/opencontainers/runc) 和 [containerd](https://github.com/containerd/containerd)。

### 關鍵元件說明

#### LXC

Docker 早期版本（0.1-0.7）直接使用 LXC 作為容器執行時期，利用 Linux Namespaces 和 Cgroups 實作容器隔離。

#### libcontainer

- Docker 自行開發的容器函式庫
- 提供了容器的通用介面
- 不依賴於特定的 Linux 容器實作
- 更靈活和可控

#### runC

- OCI（Open Container Initiative）標準實作
- 輕量級的容器執行時期
- 獨立的二進制檔案，可單獨使用
- 基於 libcontainer 發展而來

#### containerd

- Docker 開源的容器執行時期
- 提供了容器的完整生命週期管理
- 支援 runC 和其他 OCI 相容的執行時期
- 在 Kubernetes 等編排系統中廣泛使用

### 容器規範標準

Docker 積極參與 Open Container Initiative (OCI) 的制定，推動了以下規範的發展：

- **Image Spec**：容器映像檔格式規範
- **Runtime Spec**：容器執行時期介面規範
- **Distribution Spec**：容器映像檔分發規範

### 架構演變的優勢

從 LXC → libcontainer → runC/containerd 的演變提供了以下優勢：

1. 減少外部相依
2. 提高執行效率
3. 遵循業界標準（OCI）
4. 增強可移植性和互操作性
5. 支援多種容器執行時期選擇

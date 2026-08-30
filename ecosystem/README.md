# 第十七章 容器其他生態

> **版本說明**：本章介紹的工具和執行時期（Podman、Buildah、Skopeo、containerd、Kata Containers、gVisor、WasmEdge 等）都保持活躍的開發。建議：
> - 查閱各專案官方文件取得最新版本
> - 在生產環境使用前驗證版本相容性
> - 關注官方發佈說明了解重大變更

本章將介紹 Docker 和 Kubernetes 之外的容器生態技術。

同時，Docker 自身的生態也在向雲端建立、AI 本地推理和企業級桌面安全擴展。目前需要額外關注：

* **Docker Model Runner**：在 Docker Desktop / Docker Engine 中管理、運行和服務本地 AI 模型，支持 OpenAI 與 Ollama 相容 API，並可將 GGUF、Safetensors 等模型檔案作為 OCI Artifact 管理。
* **Docker Build Cloud**：通過遠端 BuildKit 和共享建立快取加速本地與 CI 建立，適合多平台映像檔和團隊共享快取場景。
* **Docker Offload**：把容器建立和運行卸載到雲端，適合 VDI、受限本機或不支持巢狀虛擬化的開發環境。
* **Hardened Docker Desktop / Enhanced Container Isolation (ECI)**：通過更強的命名空間隔離、敏感掛載保護和系統呼叫限制降低桌面容器逃逸風險。

## 本章內容

* [Fedora CoreOS 簡介](coreos-intro.md)
  * 專為容器化工作負載設計的作業系統。

* [Fedora CoreOS 安裝與設定](coreos-install.md)
  * CoreOS 的安裝方式與基本設定。

* [Podman](podman.md)
  * 相容 Docker CLI 的下一代無常駐程式容器引擎。

* [Buildah](buildah.md)
  * 無需常駐程式的 OCI 容器映像檔建立工具。

* [Skopeo](skopeo.md)
  * 遠端檢查和管理容器映像檔的利器。

* [containerd](containerd.md)
  * 作為現代容器生態基石的核心容器執行時期。

* [安全容器執行時期](secure-runtime.md)
  * 通過提供更強隔離性來保證安全的技術方案（如 Kata Containers、gVisor）。

* [WebAssembly](wasm.md)
  * 一種極具潛力的輕量級跨平台二進位指令格式。

## 本章總結

Docker 並非容器生態的唯一選擇，了解其他工具有助於根據場景做出合適的技術選型。

| 專案 | 定位 | 特點 |
|------|------|------|
| **Fedora CoreOS** | 容器化作業系統 | 自動更新、不可變基礎設施、專為運行容器設計 |
| **Podman** | 容器管理引擎 | 無常駐程式、相容 Docker CLI、支持 Rootless 模式、支持原生 Pod |
| **Buildah** | 映像檔建立工具 | Daemonless 工作模式、靈活的腳本化建立能力 |
| **Skopeo** | 映像檔倉庫管理 | 無需拉取即可檢查遠端映像檔、跨倉庫/格式無縫遷移映像檔 |
| **containerd** | 核心底層執行時期 | 穩定高效、符合 CRI 規範、是 Docker 的基石之一 |
| **安全容器** | 強隔離沙箱運行 | 利用輕量級虛擬機 (Kata) 或使用者態核心 (gVisor) 防止越獄，極其安全 |
| **Wasm** | 新型工作負載 | 體積極小、冷啟動超快且具備跨平台及高度特徵化沙盒能力的後端架構新方向 |

### Podman vs Docker

兩者的主要區別：

| 對比項 | Docker | Podman |
|--------|--------|--------|
| **常駐程式** | 需要 dockerd | 無需常駐程式 |
| **權限** | 預設需要 root | 原生支持 Rootless |
| **CLI 相容** | - | 與 Docker 命令相容 |
| **Pod 支持** | 不支持 | 原生支持 Pod 概念 |
| **Compose** | docker compose | podman-compose 或相容模式 |

### 延伸閱讀

- [底層實作](../underly/README.md)：容器技術的核心基礎
- [安全](../security/README.md)：容器安全實務

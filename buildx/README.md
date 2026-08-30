# 第十章 Docker Buildx

Docker Buildx 是一個 docker CLI 外掛程式，它擴充了 docker 命令，支援 [Moby BuildKit](buildkit.md) 提供的功能。提供與 docker build 相同的使用者體驗，並增加了許多新功能。

> Buildx 需要 Docker v23.0+（此版本起 BuildKit 變成預設建立引擎）。建議使用 Docker v28 及以上版本以獲得最完整的 Buildx 功能支援。

## 本章內容

本章將詳細介紹 Docker Buildx 的使用，包括：

* [使用 BuildKit 建立映像檔](buildkit.md)
* [使用 Buildx 建立映像檔](buildx.md)
* [建立多種系統架構支援的 Docker 映像檔](multi-arch-images.md)

> **供應鏈安全與儲存後端前瞻**：現代軟體供應鏈中，映像檔來源證明（Provenance，在 BuildKit 中預設以 `mode=min` 加入）和軟體物料清單（SBOM，可透過 `--sbom=true` 明確開啟）已經成為極其重要的建立產出。這些 Attestations 資料會作為 manifest 附加在 **映像檔索引 (Image Index)** 上。
> 正是基於此訴求，自 Docker Engine 29 起在**新安裝情境**預設啟用的 `containerd image store` 提供對 Image Index 的完整本地支援能力，解決了傳統經典儲存後端（Classic Store）無法有效處理帶 Attestations 映像檔索引的瓶頸。這使得你可以利用 `docker buildx imagetools inspect` 等手段，甚至做到無需拉取完整映像檔內容即可在 Registry 或本地高效驗證映像檔的安全中繼資料。

## 本章小結

Docker Buildx 是 Docker 建立系統的重要進化，提供了高效、安全且支援多平台的映像檔建立能力。

| 概念 | 要點 |
|------|------|
| **BuildKit** | 下一代建立引擎，Docker 23+ 預設啟用 |
| **快取掛載** | `RUN --mount=type=cache` 加速依賴安裝 |
| **Secret 掛載** | `RUN --mount=type=secret` 安全傳遞金鑰 |
| **buildx build** | 替代 `docker build`，支援更多建立功能 |
| **建立檢查** | `--check` 可在不執行建立的情況下檢查 Dockerfile 與建立參數 |
| **多架構建立** | `--platform` 參數一鍵建立多種架構映像檔 |
| **Manifest List** | 多架構映像檔的索引檔 |
| **SBOM** | 透過 `--sbom=true` 產生軟體物料清單 |

### 延伸閱讀

- [Dockerfile 指令詳解](../dockerfile/README.md)：Dockerfile 編寫基礎
- [多階段建立](../dockerfile/build_image.md)：最佳化映像檔體積
- [Dockerfile 最佳實務](../appendix_resources/README.md)：編寫高效 Dockerfile

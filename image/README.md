# Docker 映像檔

在之前的介紹中，我們知道映像檔是 Docker 的三大元件之一。

Docker 執行容器前需要本地端存在對應的映像檔，如果本地端不存在該映像檔，Docker 會從映像檔倉庫下載該映像檔。

## 本章內容

本章將介紹更多關於映像檔的內容，包括：

* [從倉庫取得映像檔](pull.md)
* [列出映像檔](list.md)
* [移除本機映像檔](rmi.md)
* [利用 commit 理解映像檔構成](commit.md)
* [使用 Dockerfile 建立映像檔](create.md)
* [其他製作映像檔的方式](other.md)
* [映像檔的實作原理](internal.md)
* [儲存和載入映像檔](save_load.md)

> **版本提示：映像檔儲存後端的變遷**
>
> 在 Docker Engine v29 及後續版本中，Docker 在**全新安裝場景**預設啟用 **containerd image store**（替代傳統 classic store 路徑）。這一底層架構級別的變遷，意味著 Docker 解鎖了對 OCI Image Index 和 Attestations（例如原生的 provenance 來源證明與 SBOM 軟體物料清單）的全量本地端支援。
> 讀者在執行類似 `docker buildx build --provenance=mode=min --sbom=true` 甚至使用後續審查工具（如 `docker buildx imagetools inspect`）時，其中繼資料能夠與映像檔資料一併完好地管理於本地端儲存系統中，為供應鏈安全驗證補齊了最後一塊拼圖。

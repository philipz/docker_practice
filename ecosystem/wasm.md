## 17.8 WebAssembly 與容器

> **版本說明**：WebAssembly 和相關的 Wasm 執行時期（如 WasmEdge、Spin）處於快速演進階段。建議查閱 [WebAssembly 官方文件](https://webassembly.org/)、[WasmEdge](https://wasmedge.org/) 和 [Spin](https://spinframework.dev/) 官方文件取得最新資訊。

本節介紹 WebAssembly（簡寫為 Wasm）以及它為何成為現代容器生態中備受矚目的前沿技術路線。

### 17.8.1 什麼是 WebAssembly？

[WebAssembly (Wasm)](https://webassembly.org/) 最初是由 W3C 主導的一項為了解決網頁中 JavaScript 效能瓶頸而發明的技術標準。它是一種小體積的、載入極快的、提供安全沙盒的高效二進位格式的指令集架構。通過將 C/C++、Rust、Go 等高階語言編譯成 `.wasm` 格式，這些程式可以直接在所有現代的瀏覽器中以接近原生的速度安全地運行。

然而，一項原本用於前端領域的技術，為何如今卻與容器雲端運算生態產生了強烈的化學反應？

因為開源社群很快意識到，Wasm 所具備的核心特性完美契合了雲原生後端的訴求。人們制定了諸如 **WASI (WebAssembly System Interface)** 這樣的標準，將其能力從瀏覽器擴展到了伺服器端作業系統上。

### 17.8.2 Wasm 與容器特性的完美契合

將 Wasm 應用於服務端時，它展現出了一些可能比傳統 Linux 容器更為優異的特性：

1. **極速的冷啟動效能**：
   傳統 Linux 容器雖然比虛擬機輕量很多，但它啟動依然需要建立 Namespace 和 Cgroups 以及一整套檔案系統，通常需要近百毫秒到幾秒。而 Wasm 模組不需要這樣龐雜的環境初始化，能夠在幾毫秒之內完成從載入到執行，這對於無伺服器函式（Serverless Functions）而言是巨大的提升。

2. **跨平台性 (Write Once, Run Anywhere)**：
   我們知道 Docker 等容器通常是綁定架構的。如果是 x86_64 平台上打出的映像檔，通常無法直接在基於 ARM 的系統（如蘋果 M 系列晶片甚至樹莓派）上直接運行原生程式碼，除非使用 QEMU 進行低效轉譯或者專門建立多架構（Multi-arch）映像檔和 manifests。
   而 Wasm 二進位本身是平台無關的平台中間語言程式碼形式！你編譯出來的一份 `.wasm` 可執行模組，不用做任何修改，就可以在 x86 的 Linux 伺服器、ARM 的邊緣設備、甚至是 Windows 和 macOS 上直接通過 Wasm 執行時期來驅動和執行。真正做到了“編寫一次，到處運行”。

3. **天然的安全沙箱機制**：
   Wasm 設計之初就是在不被信任的瀏覽器沙盒環境中運行未知程式碼的，因此執行環境非常安全，採用了極好的能力導向安全模型。應用只能存取它被明確授予權限的檔案或能力。其預設安全隔離性比起依靠 Namespaces 機制的共享核心的 Linux 容器更加堅固。

4. **極小的套件體積**：
   Linux 容器需要打包一整套依賴甚至是簡化的 OS 根目錄結構。而一個編譯好的功能完善的 Wasm 模組體積常常不到幾兆甚至僅僅幾十 Kb，極大地加快了儲存及網路利用效率。

### 17.8.3 當 Docker 遇上 WebAssembly

在現代的容器生態系統中，Wasm 並不被看作是要取代傳統 Docker 或者 Kubernetes 的技術，而是成為了一種 **與 Linux 容器互補並且共生** 的全新工作負載類型。

目前，這通過 OCI (Open Container Initiative) 和 CRI 標準實現了整合上的統一：

1. **將 Wasm 打包為 OCI 映像檔**：雖然內容並非傳統的 Linux RootFS，但是通過標準化的打包工具同樣可以將應用程式及其 `.wasm` 建立結果轉化為一個可以被推送至 Docker Hub 或其他 registry 的標準化映像檔規範。
2. **通過容器執行時期直接執行**：Docker 已經與如 [WasmEdge](https://wasmedge.org/) 和 [Spin](https://spinframework.dev/) 等高效能的企業級 Wasm 執行時期進行了官方整合合作。

如今在 Docker Desktop 或者整合了 `containerd` 的環境中，我們可以十分簡易地以類似普通映像檔的形式去拉取並運行一個基於 Wasm 編譯的後端服務（通過指定相應的 `--platform` 或者是特別的 `--runtime=io.containerd.wasmedge.v1` 設定），將其如同對待一個標準應用程式一樣讓 Docker 為其接管日誌、設定相關的網路埠號映射，甚至通過 Docker Compose 將一個普通的資料庫容器實例與一個 Wasm 微服務實例協同起來混布。

### 17.8.4 總結

隨著技術底座如 WASI 規範不斷的成熟完善（例如提供完備的套接字網路支持以及系統資源存取支持），我們有理由相信不僅是邊緣計算與無伺服器呼叫，會有越來越多對於速度和安全性有極高指標要求的雲原生後端微服務開始採用這一顛覆傳統邊界的輕量級“微型智慧體”架構。在可見的將來，Wasm 勢必成為雲原生與 Docker 生態的重要拼圖。

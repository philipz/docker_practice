# Dockerfile 指令詳解

## 什麼是 Dockerfile

Dockerfile 是一個文字檔案，其內包含了一條條的 **指令 (Instruction)**，每一條指令建立一層，因此每一條指令的內容，就是描述該層應當如何建立。

在[映像檔](../image/README.md)章節中，我們透過 `docker commit` 學習了映像檔的構成。但是，手動 `commit` 只能作為臨時修補，並不適合作為生產環境映像檔的建立方式。

使用 Dockerfile 建立映像檔有以下優勢：

*   **自動化**：可以透過 `docker build` 命令自動建立映像檔。
*   **可重複性**：由於 Dockerfile 是文字檔案，可以確保每次建立的結果一致。
*   **版本控制**：Dockerfile 可以納入版本控制系統（如 Git），便於追蹤變更。
*   **透明性**：任何人都可以透過閱讀 Dockerfile 了解映像檔的建立過程。

## Dockerfile 編寫哲學

在深入每個指令的細節之前，筆者想強調一個至關重要的原則：**Dockerfile 不是腳本，而是映像檔的「設計圖」**。這個區別決定了你如何思考每條指令的作用。

相比編寫 Bash 腳本的思維（「按順序執行這些命令」），Dockerfile 的思維應該是（「這一層映像檔應該如何建立，下一層如何分層」）。這個思維轉變會影響你的決策：

- **合併命令**：一個 `RUN apt-get update && apt-get install ...` 應該寫在一起，而不是分開成多個 `RUN` 指令，因為它們是同一個「層」的邏輯
- **選擇合適的指令**：`COPY` vs `ADD`、`CMD` vs `ENTRYPOINT` 這些選擇不是隨意的，而是根據映像檔分層的語義來決定的
- **最佳化映像檔大小**：最後才清理快取、刪除臨時檔案，讓這些「瘦身」操作在同一層完成

這個章節將詳細介紹各個指令。在學習指令語法時，請始終思考：「這個指令為什麼要以這樣的方式工作？如果我是 Docker，我應該如何設計它？」

## Dockerfile 基本結構

Dockerfile 一般分為四部分：基底映像檔資訊、維護者資訊、映像檔操作指令和容器啟動時執行指令。

可執行 `docker buildx build --check` 校驗的完整 Dockerfile 範例使用 `scratch`，因此結構檢查不會解析遠端基底映像檔中繼資料。

```dockerfile
FROM scratch

COPY index.html /index.html
```

### 指令詳解

本章將詳細講解 Dockerfile 中的各個指令：

*   [RUN 執行命令](run.md)
*   [COPY 複製檔案](copy.md)
*   [ADD 更進階的複製檔案](add.md)
*   [CMD 容器啟動命令](cmd.md)
*   [ENTRYPOINT 入口點](entrypoint.md)
*   [ENV 設定環境變數](env.md)
*   [ARG 建立參數](arg.md)
*   [VOLUME 定義匿名卷](volume.md)
*   [EXPOSE 暴露埠號](expose.md)
*   [WORKDIR 指定工作目錄](workdir.md)
*   [USER 指定目前使用者](user.md)
*   [HEALTHCHECK 健康檢查](healthcheck.md)
*   [ONBUILD 為他人作嫁衣裳](onbuild.md)
*   [LABEL 為映像檔新增中繼資料](label.md)
*   [SHELL 指令](shell.md)

### 進階特性

本章還將介紹 Dockerfile 的進階特性：

*   [多階段建立](multistage_builds.md)
*   [多階段建立實戰：Laravel 應用](multistage_builds_laravel.md)

### 參考與最佳實務

此外，我們還將介紹 Dockerfile 的最佳實務和常見問題。

*   [參考文件](references.md)

## 使用 Dockerfile 建立映像檔

建立映像檔的基本命令格式為：

```bash
docker build [選項] <上下文路徑/URL/->
```
例如，在 Dockerfile 所在目錄執行：

```bash
docker build -t my-image:1.0 .
```

### 關於版本號最佳實務

本章中的 Dockerfile 範例使用的基底映像檔標籤遵循以下原則：

- **通用標籤**（如 `ubuntu:24.04`、`alpine`、`nginx`）：保持原樣，無需修改
- **基底映像檔版本號**（如 `node:22`、`python:3.12`）：使用主或次版本號而非完整版本號（patch），這樣可以自動取得最新的修補版本，確保獲得安全更新
- **避免**：不建議使用 `latest` 標籤和完整的 patch 版本號（如 `20.10.0`）作為基底映像檔，因為這會導致建立的不可重現性或安全風險

讀者在使用這些範例時，應根據實際生產環境需求選擇合適的版本號。

更多關於 `docker build` 的用法，我們在實戰中會結合具體指令進行演示。

## 本章小結

本章詳細介紹了 Dockerfile 的所有核心指令，以下是各指令要點的速查表。

| 指令 | 作用 | 關鍵要點 |
|------|------|---------|
| **FROM** | 指定基底映像檔 | 必須是第一條建立指令；只有全域 `ARG` 能寫在它之前 |
| **RUN** | 在新層執行命令 | 合併命令、清理快取以減小體積 |
| **COPY** | 複製檔案 | 優先使用，支援 `--from` |
| **ADD** | 更進階的複製 | 自動解壓 tar；公開遠端 artifact 應配合 `--checksum` |
| **CMD** | 容器啟動預設命令 | 可被 `docker run` 參數覆蓋 |
| **ENTRYPOINT** | 容器入口點 | 固定啟動命令，CMD 作為預設參數 |
| **ENV** | 設定環境變數 | 建立時 + 執行時均生效 |
| **ARG** | 建立參數 | 僅建立時生效，FROM 後需重新宣告 |
| **VOLUME** | 定義匿名卷 | 執行時掛載會遮蔽映像檔內目錄；建立後續寫入語義依賴 builder |
| **EXPOSE** | 宣告埠號 | 僅文件作用，不自動映射 |
| **WORKDIR** | 指定工作目錄 | 替代 `RUN cd`，目錄不存在會自動建立 |
| **USER** | 指定執行使用者 | 使用者必須已存在，推薦 gosu |
| **HEALTHCHECK** | 健康檢查 | 支援 starting/healthy/unhealthy 狀態 |
| **ONBUILD** | 延遲執行指令 | 只繼承一次，不可級聯 |
| **LABEL** | 新增中繼資料 | 推薦 OCI 標準標籤，替代 MAINTAINER |
| **SHELL** | 更改預設 shell | 推薦 `["/bin/bash", "-o", "pipefail", "-c"]` |

### 生產映像檔快速檢查清單

在將映像檔推向生產之前，建議逐條過一遍以下清單：

- [ ] 基底映像檔選擇了最小化版本（如 `alpine`、`distroless`）
- [ ] 使用了[多階段建立](multistage_builds.md)，最終映像檔不含編譯工具鏈
- [ ] 以非 root 使用者執行（`USER` 指令）
- [ ] `COPY` 優先於 `ADD`，且僅複製必要檔案
- [ ] `RUN` 指令合併了 `apt-get update && install && rm -rf /var/lib/apt/lists/*`
- [ ] 設定了 `HEALTHCHECK`
- [ ] 使用了 `.dockerignore` 排除 `.git`、`node_modules` 等無關檔案
- [ ] 映像檔標籤使用了具體版本號或 commit hash，而非 `latest`

> 更完整的編寫指南見[附錄：Dockerfile 最佳實務](../appendix_resources/README.md)。

### 延伸閱讀

- [建立](../image/create.md)：Dockerfile 入門
- [多階段建立](multistage_builds.md)：最佳化映像檔大小
- [Dockerfile 最佳實務](../appendix_resources/README.md)：編寫指南
- [安全](../security/README.md)：容器安全實務
- [Compose 模板檔案](../compose/compose_file.md)：Compose 中的設定

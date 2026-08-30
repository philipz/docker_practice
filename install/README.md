# 安裝

Docker Engine 主要提供 `stable` 和 `test` 兩個更新頻道；`test.docker.com` 對應測試頻道，適合預發布驗證，不建議直接用於生產環境。

官方網站上有各種環境下的[安裝指南](https://docs.docker.com/get-started/get-docker/)，這裡主要介紹 Docker 在 `Linux`、`Windows 10/11` 和 `macOS` 上的安裝。

## 安裝方式選擇指南

在開始安裝前，筆者建議你根據以下決策樹選擇最合適的安裝方式：

### 生產環境 vs 開發環境

**生產環境**（伺服器部署）：

- 優先使用**官方 APT/YUM 源安裝**（Ubuntu、Debian、Fedora、CentOS）
- 優勢：獲得官方安全更新、長期技術支援、版本管理清晰
- 安裝步驟稍多一些，但這種「麻煩」是值得的——它為你的生產系統爭取了穩定性和可維護性

**開發環境**（本地開發機、測試伺服器）：

- 設定 **Docker 官方源後** 使用套件管理器安裝，或在一次性測試環境使用官方腳本自動安裝
- 如果你想快速上手，官方腳本（`get.docker.com`）是最便捷的選擇
- 大陸使用者注意：這一步一定要選對映像檔源，否則網路卡頓會嚴重影響體驗

### 大陸使用者的網路最佳化建議

值得注意的是，大陸直接存取 Docker 官方源速度較慢，建議：

- **安裝過程**：使用阿里雲、騰訊雲等大陸映像檔源
- **映像檔拉取**：安裝完成後設定 Docker 映像檔加速器（詳見 [映像檔加速器](mirror.md)），這一步對日常開發的體驗提升最明顯

### 特殊情境

- **Raspberry Pi/ARM 平台**：見 [Raspberry Pi](raspberry-pi.md)
- **離線環境**：見 [Linux 離線安裝](offline.md)
- **macOS/Windows**：Docker Desktop 是官方推薦的一站式解決方案
- **需要實驗特性**：見 [開啟實驗特性](experimental.md)

## 詳細安裝指南

* [Ubuntu](ubuntu.md)
* [Debian](debian.md)
* [Fedora](fedora.md)
* [CentOS](centos.md)
* [Raspberry Pi](raspberry-pi.md)
* [Linux 離線安裝](offline.md)
* [macOS](mac.md)
* [Windows 10/11](windows.md)
* [映像檔加速器](mirror.md)
* [開啟實驗特性](experimental.md)

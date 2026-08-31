# 修訂記錄

* 1.9.2 2026-05-16
  * 刷新 Docker 生態說明，更新 Fedora CoreOS、Podman、containerd 等章節中的維護狀態
  * 修復映像檔事實、演示 TLS 金鑰等後續審閱發現的問題

* 1.9.1 2026-05-08
  * 使用 `browser-actions/setup-chrome` 替代 Ubuntu runner 上不穩定的 Chromium snap 安裝
  * 修正 Docker Engine 29 日期、TLS 協定、healthcheck 與互動式除錯示例

* 1.9.0 2026-05-02
  * 更新 Docker Engine 29、nginx、MySQL 8.4 LTS、Node.js 22 LTS 與 Kubernetes 相關版本說明
  * 補充 ipvlan、nftables、Gateway API、Docker Scout、映像檔安全與供應鏈安全內容
  * 修復 Docker Hub 限流、etcdctl API、Compose healthcheck、Docker Debug 等時效性內容

* 1.8.0 2026-04-27
  * 補全 Dockerfile 指令參考與多處章節編號、標題層級、程式碼區塊和表格格式
  * 增加預覽 PDF 自動發布流程，修復 mdpress 埠號和匯出相關設定

* 1.7.5 2026-04-05
  * 將失效的 AtomHub 映像檔替換為可用映像檔源

* 1.7.4 2026-03-31
  * 修復標題層級格式

* 1.7.3 2026-03-29
  * 修復 Wikipedia URL 編碼

* 1.7.2 2026-03-28
  * 修正 macOS、Windows、Compose 與 Kubernetes 章節中的時效性內容和錯誤前提
  * 收縮越界網路內容，補充 bind mount、tmpfs 與埠號映射的關鍵限制說明
  * 統一 numbered section 的標題層級，清理正文末尾分散的參考資料小節
  * 補充產生物忽略規則，避免 `.mdpress` 與本地 HTML 匯出誤提交

* 1.7.1 2026-03-28
  * 對齊附錄首頁與目錄結構，補全學習路線入口
  * 重組資源連結頁，統一官方一手入口
  * 完善附錄二導航頁，提升熱門映像檔查閱體驗

* 1.7.0 2026-03-25
  * 精簡 CI 流程，移除遺留的 vuepress 建立，統一使用 mdpress
  * 升級 etcd 集群示例從 v3.4.0 到 v3.5.17
  * 更新 npm 映像檔為 npmmirror.com，PHP 升級到 8.3
  * 移除 Compose 已廢棄的 version 欄位
  * 升級所有 CI Actions 到最新版本

* 1.6.1 2026-02-28
  * 修正資料卷 `--mount` 與 `-v` 的行為差異及資料卷管理說明
  * 補充 Docker Hub 限流機制說明，區分 pull rate limit 與 abuse rate limit
  * 完善安全權限警告，強化使用者加入 docker 群組等同於 root 的風險意識
  * 增補 Docker Engine v29 containerd image store 與 BuildKit provenance attestations 預設行為說明

* 1.6.0 2026-02-20
  * 全面統一使用 `docker compose` (V2) 為預設標準，提供 V1 遷移說明
  * 修復全書大量排版錯誤，建立附錄與正文的雙向索引與引用
  * 更新 Kubernetes 至 1.35 相容說明及執行時期環境提示

* 1.5.4 2026-02-15
  * 移除 combine.py
  * 修復若干問題


* 1.5.3 2026-02-15
  * 修復 CI 流程中的圖片引用路徑錯誤
  * 修復 CODEOWNERS 檔案路徑匹配問題
  * 更新專案設定版本號

* 1.5.0 2026-02-05
  * 全面重構章節目錄結構 (01-15)
  * 支援 Docker Engine v29.x
  * 最佳化文件圖片引用路徑

* 1.4.0 2026-01-11
  * 全面支援 Docker Engine v29 新版本
  * 更新 Docker Compose 至 v2.40.x
  * 更新 Kubernetes 相關章節至 1.35 版本
  * BuildKit 已成為預設穩定建構器，移除實驗特性說明
  * 新增 Docker Scout、Docker Init 相關內容
  * 更新映像檔加速器設定
  * 新增 CentOS EOL 警告，推薦使用 Rocky Linux/AlmaLinux
  * 擴充安全章節和底層架構章節內容

* 1.3.0 2021-12-31
  * 全面支援 Docker v20.10 新版本
  * 新增 Docker Compose v2
  * Docker Hub 自動建構轉為付費功能

* 1.2.0 2020-12-20
  * 錯誤修復

* 1.1.0 2019-12-31
  * 全面支援 Docker v19.03 新版本
  * 增加 `BuildKit`
  * 增加 `docker buildx` 命令使用說明
  * 增加 `docker manifest` 命令使用說明
  * 移除 `Ubuntu 14.04` `Debian 8` `Debian 7`

* 1.0.0: 2018-12-31
  * 全面支援 Docker v18.x 新版本
  * 新增如何除錯 Docker
  * 錯誤修正

* 0.9.0: 2017-12-31
  * 對 v1.13.x 舊版本的最後支援

* 0.9.0-rc2: 2017-12-10

  * 增加 Docker 中文資源連結
  * 增加介紹基於 Docker 的 CI/CD 工具 `Drone`
  * 增加 `docker secret` 相關內容
  * 增加 `docker config` 相關內容
  * 增加 `LinuxKit` 相關內容

  * 更新 `CoreOS` 章節
  * 更新 `etcd` 章節，基於 3.x 版本

  * 刪除 `Docker Compose` 中的 `links` 指令

  * 替換 `docker daemon` 命令為 `dockerd`
  * 替換 `docker ps` 命令為 `docker container ls`
  * 替換 `docker images` 命令為 `docker image ls`

  * 修改 `安裝 Docker` 一節中部分文字表述

  * 移除歷史遺留檔案和錯誤的檔案
  * 最佳化文字排版
  * 調整目錄結構
  * 修復內容邏輯錯誤
  * 修復 `404` 連結

* 0.9.0-rc1: 2017-11-29

  * 根據最新版本 (v17.09) 修訂內容

  * 增加 `Dockerfile` 多階段建立 (`multistage builds`) `Docker 17.05` 新增特性
  * 增加 `docker exec` 子命令介紹
  * 增加 `docker` 管理子命令 `container` `image` `network` `volume` 介紹
  * 增加 `樹莓派單片電腦` 安裝 Docker
  * 增加 Docker 儲存驅動 `OverlayFS` 相關內容

  * 更新 `Docker CE` `v17.x` 安裝說明
  * 更新 `Docker 網路` 一節
  * 更新 `Docker Machine` 基於 0.13.0 版本
  * 更新 `Docker Compose` 基於 3 檔案格式

  * 刪除 `Docker Swarm` 相關內容，替換為 `Swarm mode` `Docker 1.12.0` 新增特性
  * 刪除 `docker run` `--link` 參數

  * 精簡 `Docker Registry` 一節

  * 替換 `docker run` `-v` 參數為 `--mount`

  * 修復 `404` 連結
  * 最佳化文字排版
  * 增加離線閱讀功能

* 0.8.0: 2017-01-08

  * 修正文字內容
  * 根據最新版本 (1.12) 修訂安裝使用
  * 補充附錄章節

* 0.7.0: 2016-06-12

  * 根據最新版本進行命令調整
  * 修正若干文字描述

* 0.6.0: 2015-12-24

  * 補充 Machine 專案
  * 修正若干 bug

* 0.5.0: 2015-06-29

  * 新增 Compose 專案
  * 新增 Machine 專案
  * 新增 Swarm 專案
  * 完善 Kubernetes 專案內容
  * 新增 Mesos 專案內容

* 0.4.0: 2015-05-08

  * 新增 Etcd 專案
  * 新增 Fig 專案
  * 新增 CoreOS 專案
  * 新增 Kubernetes 專案

* 0.3.0: 2014-11-25

  * 完成倉庫章節
  * 重寫安全章節
  * 修正底層實作章節的架構、命名空間、控制組、檔案系統、容器格式等內容
  * 新增對常見倉庫和映像檔的介紹
  * 新增 Dockerfile 的介紹
  * 重新校訂中英文混排格式
  * 修訂文字表達
  * 發布繁體版本分支：zh-Hant

* 0.2.0: 2014-09-18

  * 對照官方文件重寫介紹、基本概念、安裝、映像檔、容器、倉庫、資料管理、網路等章節
  * 新增底層實作章節
  * 新增命令查詢和資源連結章節
  * 其它修正

* 0.1.0: 2014-09-05

  * 新增基本內容
  * 修正錯別字和表達不通順的地方

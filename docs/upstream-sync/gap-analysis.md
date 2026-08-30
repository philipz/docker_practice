# 上游差距分析與後續批次規劃

本文件記錄 philipz/docker_practice 與上游 [yeasy/docker_practice](https://github.com/yeasy/docker_practice) master 分支的內容差距，作為「簡轉繁翻譯＋合併」流程的差距地圖。

## 背景

philipz/docker_practice（正體中文 Docker 教學書）目前停留在 2014 年 v0.2.9 內容，共 83 個 Markdown 檔、約 2,853 行；上游 yeasy/docker_practice master 分支已有 206 個 Markdown 檔、約 25,885 行。本工作項以 yeasy master 為翻譯來源，將簡體中文內容翻譯為正體中文並合併回 philipz/docker_practice 的 software-factory 分支，採分階段執行。

## 差距表

### 完全缺失章節

| 章節 | 檔案數 | 行數 |
|------|-------|------|
| 10_buildx | 5 | 383 |
| 11_compose | 12 | 2,168 |
| 13_kubernetes_concepts | 7 | 791 |
| 14_kubernetes_setup | 10 | 1,252 |
| 15_etcd | 6 | 442 |
| 16_cloud | 7 | 582 |
| 17_ecosystem | 10 | 594 |
| 19_observability | 5 | 1,185 |
| 20_cases_os | 6 | 460 |
| 21_case_devops | 9 | 1,407 |

### 嚴重過時章節

| 章節 | 上游（檔數/行數） | 現有（檔數） |
|------|------------------|-------------|
| 07_dockerfile | 20 檔 / 3,969 行 | 5 檔 |
| 12_implementation | 8 檔 / 1,122 行 | 7 檔（underly） |
| 18_security | 8 檔 / 1,132 行 | 7 檔 |
| appendix | 22 檔 / 2,175 行 | 11 檔 |
| 01–09 各章 | 內容已大幅改寫 | 例如 03_install 上游 10 節 vs 現有 2 節 |

## 後續批次規劃

| Phase | 內容 |
|-------|------|
| Phase 1 | 10_buildx（本工作項，已完成） |
| Phase 2 | 11_compose |
| Phase 3 | 07_dockerfile 擴充 |
| Phase 4 | Kubernetes 13+14+15 |
| Phase 5 | 16_cloud + 17_ecosystem + 19_observability |
| Phase 6 | 20_cases_os + 21_case_devops + 18_security 更新 |
| Phase 7 | appendix + 01–09 更新 |

## 翻譯與合併流程

1. 從 yeasy master 取得章節原始檔（簡體中文）。
2. 依 philipz 慣例（英文檔名、無編號）存放於對應章節目錄。
3. 簡轉繁翻譯，保留程式碼、指令、路徑、URL 原樣；內容忠於原文。
4. 更新 SUMMARY.md 目錄。
5. 執行 `tools/check-zh-hant.py` 到綠燈，驗證簡體字、術語、目錄完整性與相對連結。

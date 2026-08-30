# Docker 學習路線圖與知識體系

本附錄為學習者提供清晰的學習路線、知識點相依關係、認證指南和常見面試題，幫助快速成長為 Docker 和 DevOps 專家。

### 學習階段劃分

Docker 學習可分為四個遞進階段，每個階段都有明確的學習目標和時間投入。

#### 第一階段：基礎入門（0-2 週）

**學習目標：**

- 理解容器化的基本概念
- 能夠執行、管理基本的容器
- 了解映像檔和倉庫的基本操作

**核心內容：**
```text
Docker 簡介
├── 為什麼需要 Docker
├── 容器 vs 虛擬機器 vs 雲端運算
└── Docker 的三大核心概念
    ├── 映像檔（Image）
    ├── 容器（Container）
    └── 倉庫（Repository）

基礎命令
├── docker run / create / start / stop / rm
├── docker ps / logs / exec / inspect
├── docker pull / push / tag
└── docker build -t

Docker 安裝設定
├── Linux 平台安裝
├── macOS 和 Windows 安裝
├── 映像檔加速器設定
└── 權限和使用者設定
```
**學習資源：**

- [官方教學](https://docs.docker.com/get-started/)
- 本書第 1-3 章：入門篇基礎概念
- [Docker CLI 參考](https://docs.docker.com/reference/cli/docker/)

**時間投入：**

- 理論學習：3-4 小時
- 實操練習：8-10 小時
- 總計：2 週

**驗證學習成果：**
```bash
# 完成以下任務說明基礎入門完成
1. 執行官方 nginx 映像檔，存取 http://localhost
2. 使用 docker exec 進入容器修改首頁
3. 提交修改為新映像檔
4. 推送映像檔到 Docker Hub（需建立帳戶）
```

#### 第二階段：核心開發（2-6 週）

**學習目標：**

- 掌握 Dockerfile 編寫
- 能夠建立自己的應用映像檔
- 理解資料管理和網路設定
- 熟悉 Docker Compose 編排

**核心內容：**
```text
Dockerfile 指令詳解
├── FROM / RUN / COPY / ADD
├── WORKDIR / ENV / ARG
├── EXPOSE / CMD / ENTRYPOINT
├── VOLUME / USER / HEALTHCHECK
└── 最佳實踐和效能最佳化
    ├── 分層快取機制
    ├── 減少映像檔體積
    ├── 多階段建立
    └── 安全最佳實踐

容器資料管理
├── 資料卷（Volume）
│   ├── 命名卷
│   ├── 匿名卷
│   └── 卷掛載最佳實踐
├── 綁定掛載（Bind Mount）
│   ├── 宿主機路徑映射
│   └── 權限和隔離
└── tmpfs 掛載
    └── 臨時檔案系統

容器網路
├── 網路類型
│   ├── bridge（預設）
│   ├── host
│   ├── overlay
│   └── macvlan
├── 埠號映射
├── 容器互連
├── DNS 設定
└── 自訂網路

Docker Compose
├── compose.yml/docker-compose.yml 編寫
├── services 定義
├── volumes 設定
├── networks 設定
├── 相依關係
├── 環境變數
└── 命令操作
    ├── up / down / ps / logs
    ├── exec / run
    └── build / push
```
**學習資源：**

- 本書第 4-11 章：進階篇
- [Docker 官方最佳實踐](https://docs.docker.com/build/building/best-practices/)
- [Dockerfile 參考](https://docs.docker.com/reference/dockerfile/)

**時間投入：**

- 理論學習：8-10 小時
- 實操練習：30-40 小時（多個實戰專案）
- 總計：4-6 週

**專案實戰：**
```text
專案 1: Python Web 應用（Flask/Django）
- 編寫多階段 Dockerfile
- 使用 Compose 設定資料庫
- 實現熱重載開發環境

專案 2: Node.js 微服務
- 最佳化映像檔大小
- 設定 Compose 多個服務
- 設定網路和環境變數

專案 3: 資料庫容器化
- PostgreSQL/MySQL 設定
- 資料持久化
- 備份恢復策略
```

#### 第三階段：生產最佳化（6-12 週）

**學習目標：**

- 掌握容器安全最佳實踐
- 理解效能監控和最佳化
- 學會容器編排（Kubernetes 基礎）
- 熟悉 CI/CD 整合

**核心內容：**
```text
容器安全
├── 映像檔安全
│   ├── 漏洞掃描（Trivy/Grype/Snyk）
│   ├── 映像檔簽章和驗證（Cosign）
│   ├── SBOM 產生和管理
│   └── 供應鏈安全
├── 執行時期安全
│   ├── 使用者和權限
│   ├── Linux 能力機制
│   ├── AppArmor 和 SELinux
│   ├── Rootless 容器
│   └── 安全的 Docker socket 存取
└── 宿主機安全
    ├── API 存取控制
    ├── TLS 認證
    └── 稽核日誌

效能監控和最佳化
├── 監控指標體系
│   ├── CPU / 記憶體 / 網路 / I/O
│   └── 應用級指標
├── 監控工具
│   ├── docker stats
│   ├── cAdvisor
│   ├── Prometheus
│   └── Grafana
├── 效能最佳化
│   ├── 映像檔大小最佳化
│   ├── 記憶體和 CPU 限制
│   ├── OOM 診斷和處理
│   └── 網路效能最佳化
└── 日誌管理
    ├── 日誌驅動設定
    ├── ELK Stack
    └── 日誌聚合

容器編排基礎
├── Kubernetes 核心概念
│   ├── Pod / Deployment / Service
│   ├── ConfigMap / Secret
│   └── 健康檢查和自動恢復
├── 容器執行環境
│   ├── containerd
│   ├── CRI-O
│   └── Docker
├── 網路外掛程式
│   ├── CNI 標準
│   ├── Calico / Flannel / Cilium
│   └── 網路策略
└── 儲存和有狀態應用
    ├── PV / PVC
    ├── StorageClass
    └── StatefulSet

CI/CD 整合
├── GitHub Actions
│   ├── 映像檔建立和推送
│   ├── 安全掃描
│   └── 自動化測試
├── GitLab CI
├── Jenkins Docker 整合
└── Drone

生態工具
├── Buildx（多架構建立）
├── Skopeo（映像檔管理）
├── Podman（替代方案）
└── Buildah（映像檔建立）
```
**學習資源：**

- 本書第 12-21 章：深入篇和實戰篇
- [Kubernetes 官方文件](https://kubernetes.io/docs/)
- [CNCF 學習路線](https://landscape.cncf.io/)

**時間投入：**

- 理論學習：15-20 小時
- 實操練習：60-80 小時（多個生產級專案）
- 總計：6-12 週

**專案實戰：**
```text
專案 1: 安全映像檔建立流程
- 整合 Trivy 掃描
- 映像檔簽章和驗證
- 產生 SBOM 文件

專案 2: 完整監控棧
- 搭建 Prometheus + Grafana
- 設定告警規則
- 效能資料採集和分析

專案 3: CI/CD 流程
- GitHub Actions 或 GitLab CI 設定
- 自動化映像檔建立
- 安全掃描和合規檢查
- 自動化部署到 Kubernetes

專案 4: Kubernetes 集群部署
- 本地 K3s/Kind 集群
- 部署有狀態應用
- 設定持久化儲存
```

#### 第四階段：專家深造（12+ 週）

**學習目標：**

- 掌握 Kubernetes 高級特性
- 理解容器執行時期底層實現
- 能夠設計和最佳化大規模容器平台
- 貢獻開源社群

**核心內容：**
```text
Kubernetes 高級特性
├── 集群管理
│   ├── 節點管理和驅逐
│   ├── 集群自動擴縮容
│   └── 節點親和性和污點容忍
├── 儲存編排
│   ├── 動態儲存設定
│   ├── 有狀態應用管理（StatefulSet）
│   └── 備份和災難恢復
├── 服務網格（Service Mesh）
│   ├── Istio / Linkerd / Cilium
│   ├── 流量管理
│   └── 可觀測性增強
├── 安全和多租戶
│   ├── RBAC（角色存取控制）
│   ├── Network Policy 深入
│   ├── Pod Security Policy
│   └── 准入控制器（Admission Controller）
└── 效能和擴充性
    ├── 大規模集群最佳化
    ├── 自訂 Operator
    └── 集群聯邦

容器執行時期底層
├── Linux 核心機制
│   ├── Namespace 詳解
│   ├── Cgroup v1 和 v2
│   ├── OverlayFS 和 UnionFS
│   └── SELinux 和 AppArmor
├── 容器執行時期
│   ├── containerd 原始碼閱讀
│   ├── runc 實現
│   ├── gVisor 和 Kata
│   └── Firecracker
└── OCI 標準
    ├── Image Spec
    └── Runtime Spec

DevOps 工程化
├── 大規模集群管理
│   ├── Helm / Kustomize
│   ├── GitOps（Flux / ArgoCD）
│   └── 設定管理
├── 災難恢復和高可用
│   ├── 多集群部署
│   ├── 故障轉移
│   └── 備份策略
├── 成本最佳化
│   ├── 資源申請和限制
│   ├── 自動擴縮容
│   └── 成本監控
└── 團隊協作
    ├── GitFlow 工作流
    ├── 程式碼審查
    └── 文件和最佳實踐傳播
```
**貢獻機會：**

- [Kubernetes](https://github.com/kubernetes/kubernetes)
- [Cilium](https://github.com/cilium/cilium)
- [Prometheus](https://github.com/prometheus/prometheus)
- [Docker/Moby](https://github.com/moby/moby)

### 知識點相依關係

```text
基礎概念 (Week 0-2)
├── 容器 vs 虛擬機器
├── Docker 三大概念
└── 基礎命令
    ↓
Dockerfile 和映像檔建立 (Week 2-4)
├── Dockerfile 指令
├── 多階段建立
└── 映像檔最佳化
    ↓ ↓ ↓
資料管理 ← 網路設定 ← Docker Compose (Week 4-6)
├── Volume    ├── Bridge    ├── YAML 編寫
├── Bind Mount├── Overlay   ├── 多容器編排
└── tmpfs     └── 自訂網路└── 開發工作流
    ↓            ↓            ↓
    └─────────────────────────┘
          實戰專案開發 (Week 6-10)
          ├── Web 應用容器化
          ├── 資料庫容器化
          ├── 微服務架構
          └── 本地開發環境
              ↓
容器安全 ← 效能最佳化 ← 監控和日誌 (Week 10-14)
├── 映像檔掃描  ├── 大小最佳化  ├── Prometheus
├── 漏洞管理  ├── 記憶體最佳化  ├── Grafana
├── 映像檔簽章  ├── CPU 最佳化  └── ELK Stack
└── SBOM    └── 診斷工具
    ↓          ↓          ↓
    └─────────────────────┘
          安全生產環境 (Week 14-18)
          ├── CI/CD 流程
          ├── 映像檔倉庫
          ├── 日誌集中
          └── 告警系統
              ↓
Kubernetes 基礎 (Week 18-24)
├── Pod / Service / Deployment
├── 資源管理
├── 儲存管理
└── 網路策略
    ↓
Kubernetes 進階 (Week 24-36)
├── StatefulSet / DaemonSet
├── Operator 開發
├── 集群管理
└── 服務網格
    ↓
企業級平台設計 (Week 36+)
├── 多集群管理
├── GitOps 工作流
├── 成本最佳化
└── 開源貢獻
```

### 推薦學習資源

#### 官方文件

| 資源 | URL | 推薦程度 |
|------|-----|--------|
| Docker 官方文件 | [docs.docker.com](https://docs.docker.com) | ⭐⭐⭐⭐⭐ |
| Docker Hub | [hub.docker.com](https://hub.docker.com) | ⭐⭐⭐⭐⭐ |
| Kubernetes 官方 | [kubernetes.io/docs](https://kubernetes.io/docs) | ⭐⭐⭐⭐⭐ |
| CNCF 景觀 | [landscape.cncf.io](https://landscape.cncf.io) | ⭐⭐⭐⭐ |

#### 線上課程

- **Udemy**：Docker 和 Kubernetes 完整課程（70-100 小時）
- **Linux Academy**：Linux 和容器管理
- **A Cloud Guru**：AWS/Azure 容器服務
- **Pluralsight**：Docker 和容器生態系統

#### 書籍推薦

- 《Docker 深入淺出》- 本書的原版
- 《Kubernetes 權威指南》- 深入 Kubernetes 的必讀書
- 《容器技術核心技術與應用》- 理解底層實現
- 《SRE Google 運維之道》- 生產環境最佳實踐

#### 部落格和社群

- [Docker 官方部落格](https://www.docker.com/blog/)
- [Kubernetes 官方部落格](https://kubernetes.io/blog/)
- [CNCF 部落格](https://www.cncf.io/blog/)
- [DZone Cloud Architecture](https://dzone.com/cloud-architecture)

### 認證指南

#### Docker 認證

**Docker Certified Associate (DCA)**

考試資訊：

- 題目數：55 道
- 時間限制：90 分鐘
- 及格分數：73%（約 41 道題）
- 費用：$199 USD
- 有效期：2 年

考試內容比例：
```text
映像檔和倉庫（20%）
- 映像檔建立和管理
- 映像檔層和快取
- 私有倉庫設定

容器執行（15%）
- 容器生命週期
- 資源限制
- 容器隔離

網路（15%）
- 網路驅動
- 容器通訊
- 埠號映射

儲存（10%）
- Volume 管理
- 資料持久化
- 綁定掛載

編排（20%）
- Docker Compose
- Docker Swarm 基礎

安全（15%）
- 使用者和權限
- 金鑰管理
- 映像檔安全
- 守護程式安全

和日誌（5%）
- Logging drivers
- 事件處理
```
準備建議：
```bash
# 1. 學習本書第 1-11 章（基礎到中級）
# 2. 完成 20+ 個實戰專案
# 3. 參考官方學習指南
# 參考 Docker 官方學習入口：https://www.docker.com/resources/

# 4. 模擬考試
- Linux Academy DCA 練習題
- Whizlabs DCA 模擬考試

# 5. 重點掌握的命令
docker build / push / pull / tag
docker run / exec / logs / inspect / ps
docker volume / network / service
docker compose up / down / logs / ps
docker stats / events / inspect
```

#### Kubernetes 認證

**認證路徑：**

1. **CKA - Certified Kubernetes Administrator**
   - 難度：高
   - 時間：3 小時（實操）
   - 費用：$395
   - 內容：集群安裝、管理、故障排查

2. **CKAD - Certified Kubernetes Application Developer**
   - 難度：中
   - 時間：2 小時（實操）
   - 費用：$395
   - 內容：應用開發和部署

3. **CKS - Certified Kubernetes Security Specialist**
   - 難度：很高
   - 時間：2 小時（實操）
   - 費用：$395
   - 內容：安全最佳實踐

### 常見面試題與答案要點

#### 基礎概念面試題

**Q1: Docker 容器和虛擬機器有什麼區別？**

A（要點）：
```text
虛擬機器：
- 完整的作業系統環境（GB 級）
- 啟動時間：分鐘級
- 隔離級別：完全硬體隔離
- 效能開銷：高（5-20%）

容器：
- 共享核心，包含應用和相依（MB 級）
- 啟動時間：秒級
- 隔離級別：程式級隔離（Namespace/Cgroup）
- 效能開銷：低（1-5%）

總結：容器更輕量、更快、密度更高
```
**Q2: 什麼是 Docker 映像檔？它如何儲存的？**

A（要點）：
```text
映像檔本質：
- 唯讀的檔案系統快照
- 分層儲存結構
- 每一層是前一層的增量

儲存方式：
- Union FS：多個唯讀層 + 一個可寫層
- 每個 RUN/COPY/ADD 指令建立一層
- 層之間透過 diff 增量儲存，節省空間

優點：
- 共享基礎層減少儲存
- 層級快取加快建立
- 支援高效分發
```
**Q3: 容器如何實現隔離？**

A（要點）：
```text
技術手段：
1. Namespace（資源隔離）：
   - PID Namespace：程式隔離
   - Network Namespace：網路隔離
   - Mount Namespace：檔案系統隔離
   - UTS Namespace：主機名隔離
   - IPC Namespace：程式間通訊隔離

2. Cgroup（資源限制）：
   - 限制 CPU 使用
   - 限制記憶體使用
   - 限制磁碟 I/O
   - 限制網路頻寬

3. Linux 能力機制（權限控制）：
   - 削減不必要的 root 權限
   - 限制容器能力

4. SELinux / AppArmor（強制存取控制）
```

#### Dockerfile 面試題

**Q4: 如何最佳化 Docker 映像檔大小？**

A（要點）：
```text
1. 選擇合適的基礎映像檔：
   scratch < alpine:3.21 < python:3.14-slim < python:3.14

2. 多階段建立：
   - 建立階段只保留編譯工具
   - 執行階段只包含最終二進位檔案
   - 典型場景：Go、Node.js、Java

3. 清理套件管理器快取：
   apt-get clean && rm -rf /var/lib/apt/lists/*
   yum clean all && rm -rf /var/cache/yum
   pip install --no-cache-dir

4. 合併 RUN 指令：
   減少映像檔層數

5. 使用 .dockerignore：
   排除不必要的建立上下文

6. 去除除錯符號：
   Go: -ldflags="-w -s"
   C/C++: strip binary

7. 壓縮資源：
   gzip 靜態檔案，壓縮圖片
```
**Q5: CMD 和 ENTRYPOINT 有什麼區別？**

A（要點）：
```text
CMD：
- 定義容器預設命令
- 容器執行時可被覆蓋：docker run image_name custom_cmd
- 可以有多個 CMD，只有最後一個生效

ENTRYPOINT：
- 定義容器的可執行程式
- 容器執行時參數追加而非覆蓋
- 與 CMD 配合使用

推薦用法：
ENTRYPOINT ["python", "app.py"]
CMD ["--port", "8000"]

# 執行 docker run image --debug 會執行：
# python app.py --debug
```

#### 網路和儲存面試題

**Q6: Docker 網路驅動的區別？**

A（要點）：
```text
Bridge（預設）：
- 虛擬網橋，容器間透過網橋通訊
- 支援埠號映射
- 隔離性好，效能適中

Host：
- 使用宿主機網路棧
- 效能最優，隔離性最差
- 容器埠號直接映射到宿主機

Overlay：
- 跨主機通訊，基於 VXLAN
- Docker overlay 網路預設使用 UDP 4789 傳輸資料
- Swarm 標準；Kubernetes 通常由 CNI 外掛程式實現跨主機網路
- 效能略低，支援分散式

macvlan：
- 容器獲得 MAC 位址
- 表現為物理機，效能好
- 用於物理網路整合

None：
- 無網路，完全隔離
```
**Q7: Volume 和 Bind Mount 有什麼區別？**

A（要點）：
```text
Volume：
- Docker 管理，儲存位置：/var/lib/docker/volumes/
- 跨平台相容，隔離性好
- 支援驅動，可擴充
- 推薦在生產環境使用

Bind Mount：
- 宿主機管理，任意位置
- 跨平台相容性一般
- 效能好，用於開發環境
- 權限管理複雜

tmpfs：
- 記憶體檔案系統，不持久化
- 用於臨時檔案、敏感資料
- 效能最好，重新啟動丟失
```

#### 安全和生產面試題

**Q8: 如何提高 Docker 安全性？**

A（要點）：
```text
映像檔安全：
- 使用官方映像檔或可信映像檔源
- 定期掃描漏洞（Trivy/Grype）
- 映像檔簽章驗證（Cosign）
- 產生和管理 SBOM

容器執行：
- 以非 root 使用者執行
- 使用 read-only 檔案系統
- 限制 Linux 能力
- 使用 AppArmor 或 SELinux

宿主機安全：
- 啟用 TLS 認證 API
- 不暴露 /var/run/docker.sock
- 使用 Rootless 容器
- 定期更新 Docker

網路安全：
- 使用自訂網路隔離
- 設定網路策略
- 限制出入站流量
```
**Q9: 容器被 OOM 殺死，如何診斷和解決？**

A（要點）：
```text
診斷：
1. 檢查容器是否被 OOM 殺死：
   docker inspect <container> | grep OOMKilled

2. 查看宿主機日誌：
   dmesg | grep -i oom
   journalctl -u docker | grep -i oom

3. 監控記憶體使用：
   docker stats <container>
   docker exec <container> ps aux --sort=-%mem

解決：
1. 增加記憶體限制：
   docker update -m 2g <container>

2. 檢查記憶體洩漏：
   使用記憶體分析工具（heapdump、pprof）

3. 最佳化應用：
   - 增加垃圾回收頻率
   - 減少快取大小
   - 使用物件池模式

4. 使用記憶體交換（最後手段）：
   docker run -m 512m --memory-swap 1g
```
**Q10: 如何在 CI/CD 中整合 Docker？**

A（要點）：
```text
建立階段：
- 觸發器：Push / PR 事件
- 建立映像檔：docker build
- 標記：git sha、版本號
- 掃描：Trivy 漏洞掃描
- 簽章：Cosign 映像檔簽章

儲存階段：
- 推送到映像檔倉庫：docker push
- 記錄 SBOM 和掃描報告

部署階段：
- 驗證映像檔簽章
- 取得映像檔摘要
- 更新部署設定
- 觸發 GitOps 工作流

監控階段：
- 收集應用日誌
- 監控效能指標
- 告警異常情況

示例工作流：
1. GitHub Actions / GitLab CI 監聽 push
2. 執行單元測試
3. 建立 Docker 映像檔
4. 推送到 Docker Hub / ECR
5. 觸發 ArgoCD / Flux 自動部署
6. 監控部署狀態
```

### 學習進度跟蹤模板

```markdown
# Docker 學習進度跟蹤

## 第一階段：基礎入門（目標：2 週）
- [ ] 學完第 1-3 章（6 小時）
- [ ] 完成基礎命令練習（10 小時）
- [ ] 執行官方映像檔
- [ ] 建立和推送第一個映像檔到 Docker Hub
- [ ] 完成度：___%

## 第二階段：核心開發（目標：4-6 週）
- [ ] 學完第 4-11 章（15 小時）
- [ ] 完成 3 個 Dockerfile 最佳實踐專案
- [ ] 掌握 Docker Compose（5 個專案）
- [ ] 學習資料管理和網路（8 小時）
- [ ] 完成度：___%

## 第三階段：生產最佳化（目標：6-12 週）
- [ ] 學完第 12-21 章（25 小時）
- [ ] 映像檔安全掃描和簽章
- [ ] 搭建完整監控棧
- [ ] 設定 CI/CD 流程
- [ ] Kubernetes 基礎（30 小時）
- [ ] 完成度：___%

## 第四階段：專家深造（目標：12+ 週）
- [ ] Kubernetes 高級特性
- [ ] 服務網格學習
- [ ] 底層實現研究
- [ ] 貢獻開源專案
- [ ] 完成度：___%

## 證書目標
- [ ] Docker DCA 認證
- [ ] CKA 認證
- [ ] CKAD 認證

## 實戰專案清單
- [ ] Python Web 應用容器化
- [ ] Node.js 微服務
- [ ] 資料庫容器化
- [ ] 完整微服務架構
- [ ] 監控和日誌系統
- [ ] CI/CD 流程實現
```

### 快速參考速查表

**常用命令速查：**

```bash
# 映像檔管理
docker build -t image:tag .              # 建立映像檔
docker images                             # 列出映像檔
docker rmi image:tag                      # 刪除映像檔
docker tag source:tag target:tag          # 標記映像檔
docker push registry/image:tag            # 推送映像檔
docker pull image:tag                     # 拉取映像檔
docker history image:tag                  # 查看映像檔歷史
docker inspect image:tag                  # 查看映像檔詳情

# 容器管理
docker run [OPTIONS] image                # 執行容器
docker ps [-a]                            # 列出容器
docker stop/start/restart container       # 容器生命週期
docker rm container                       # 刪除容器
docker logs [-f] container                # 查看日誌
docker exec -it container cmd             # 進入容器
docker inspect container                  # 查看容器詳情
docker stats [container]                  # 查看資源使用

# 網路管理
docker network ls                         # 列出網路
docker network create name                # 建立網路
docker network connect/disconnect         # 連線/斷開網路
docker network inspect name               # 查看網路詳情

# 卷管理
docker volume ls                          # 列出卷
docker volume create name                 # 建立卷
docker volume rm name                     # 刪除卷
docker volume inspect name                # 查看卷詳情

# Docker Compose
docker compose up [-d]                    # 啟動服務
docker compose down                       # 停止服務
docker compose ps                         # 列出服務
docker compose logs [-f] [service]        # 查看日誌
docker compose exec service cmd           # 在服務中執行命令
docker compose build                      # 建立服務映像檔
```

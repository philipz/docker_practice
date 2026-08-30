## 16.5 多雲部署策略

企業在選擇容器雲平台時，通常會在 AWS EKS，Azure AKS，Google GKE 以及國內的阿里雲 ACK，騰訊雲 TKE 之間進行權衡。

### 16.5.1 三大公有雲 Kubernetes 服務對比

| 特性 | Google GKE | AWS EKS | Azure AKS |
| :--- | :--- | :--- | :--- |
| **版本更新** | 最快，通常是 K8s 新特性的首發地 | 相對保守，注重穩定性 | 跟隨社群，更新速度適中 |
| **控制平面管理** | 全託管，自動升級，$0.10/h（有 Free Tier 抵扣）| 託管，$0.10/h | 全託管；Free 層適合開發/測試，Standard/Premium 層預設包含 Uptime SLA |
| **節點管理** | GKE Autopilot 模式完全託管節點 | Managed Node Groups 簡化管理 | Virtual Machine Scale Sets |
| **網路模型** | VPC-native, 效能優秀 | AWS VPC CNI, Pod 直接取得 VPC IP | Azure CNI（消耗 IP 多）或 Kubenet |
| **整合度** | 與 GCP 資料分析、AI 服務整合緊密 | 與 AWS IAM, ALB, CloudWatch 整合深度高 | 與 Active Directory, Azure DevOps 整合好 |

### 16.5.2 多雲部署策略

隨著企業業務的擴展，單一雲平台可能無法滿足所有需求，多雲部署成為趨勢。

#### 1. 跨雲災備：Active-Passive

主要業務運行在一個雲（如 AWS），資料即時複製到另一個雲（如阿里雲）。當主雲發生故障時，流量切換到備雲。

* **優點**：架構相對簡單，資料一致性好控制。
* **缺點**：資源閒置浪費，切換可能有 RTO。

#### 2. 多活部署：Active-Active

業務同時在多個雲上運行，通過全域流量管理 (DNS/GSLB) 分發流量。

* **優點**：高可用，就近接入提升使用者體驗。
* **缺點**：資料同步複雜，跨雲網路延遲問題。

#### 3. 混合雲

核心資料和敏感業務保留在私有雲 (IDC)，彈性業務或前端業務部署在公有雲。

* **工具**：Google Anthos，AWS Outposts，Azure Arc 都是為了解決混合雲統一管理而生。

### 16.5.3 建議

* **技術選型**：儘量使用標準的 Kubernetes API，避免過度依賴特定雲廠商的 CRD 或專有服務，以保持應用的可移植性。
* **IaC 管理**：使用 Terraform 或 Pulumi 等工具統一管理多雲基礎設施。

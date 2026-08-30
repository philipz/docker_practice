## 13.4 進階特性

掌握了 Kubernetes 的核心概念 (Pod，Service，Deployment) 後，我們需要了解更多進階特性以建立生產級應用。

### 13.4.1 Helm - 套件管理工具

[Helm](https://helm.sh/) 被稱為 Kubernetes 的套件管理器（類似於 Linux 的 apt/yum）。它將一組 Kubernetes 資源定義檔案打包為一個 **Chart**。

*   **安裝應用**：`helm install my-release bitnami/mysql`
*   **版本管理**：輕鬆回滾應用的釋出版本。
*   **模板化**：支援複雜的應用部署邏輯設定。

### 13.4.2 Gateway API 與 Ingress

Service 雖然提供了負載均衡，但通常是 4 層 (TCP/UDP)。集群需要 7 層 (HTTP/HTTPS) 路由能力來充當閘道器。

#### Gateway API（推薦）

> **重要**：Kubernetes 社群推薦使用 [Gateway API](https://gateway-api.sigs.k8s.io/) 作為新一代流量管理標準。原 `kubernetes/ingress-nginx` 專案已於 2026 年 3 月退役停止維護，不再接收安全更新。

Gateway API 基於 CRD 實現，提供了比 Ingress 更強大和標準化的流量管理能力：

*   **GatewayClass**：定義閘道器實現（類似 IngressClass）。
*   **Gateway**：定義監聽埠號和協定（由基礎設施團隊管理）。
*   **HTTPRoute**：定義 HTTP 路由規則（由應用團隊管理）。
*   **職責分離**：基礎設施、集群運維和應用開發者各管各的資源。

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: my-route
spec:
  parentRefs:
  - name: my-gateway
  hostnames:
  - "api.example.com"
  rules:
  - matches:
    - path:
        type: PathPrefix
        value: /api
    backendRefs:
    - name: api-svc
      port: 80
```

常見的 Gateway API 實現有 Envoy Gateway、Istio、Cilium、Traefik、Kong 等。

#### Ingress（傳統方案）

Ingress 資源仍可正常使用，但建議新專案直接採用 Gateway API。已有 Ingress 設定可按需逐步遷移。

*   **域名路由**：基於 Host 將請求轉發不同服務。
*   **路徑路由**：基於 Path 將請求轉發。
*   **SSL/TLS**：集中管理憑證。

### 13.4.3 Persistent Volume 與 StorageClass

容器內的檔案是臨時的。對於有狀態應用（如資料庫），需要持久化儲存。

*   **PVC (Persistent Volume Claim)**：使用者申請儲存的宣告。
*   **PV (Persistent Volume)**：實際的儲存資源（NFS，AWS EBS，Ceph 等）。
*   **StorageClass**：定義儲存類，支援動態建立 PV。
*   **VolumeAttributesClass**：Kubernetes 1.34 起 GA，用於在 CSI 驅動支援 `ModifyVolume` 時動態調整卷屬性，例如效能等級或服務品質引數。

### 13.4.4 Horizontal Pod Autoscaling

HPA 根據 CPU 利用率或其他指標（如記憶體、自訂指標）自動擴縮 Deployment 或 ReplicaSet 中的 Pod 數量。

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: php-apache
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: php-apache
  minReplicas: 1
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 50
```

### 13.4.5 ConfigMap 與 Secret

*   **ConfigMap**：儲存非機密的設定資料（設定檔案、環境變數）。
*   **Secret**：儲存機密資料（密碼、Token、憑證）。Secret 值預設只是 Base64 編碼並存入 etcd；生產環境應顯式啟用 etcd 靜態加密或 KMS。

透過將設定與映像檔分離，保證了容器的可移植性。

### 13.4.6 Pod Security Standards

> **注意**：PodSecurityPolicy (PSP) 已在 Kubernetes 1.25 中完全移除。

Kubernetes 使用 **Pod Security Standards** 定義三個安全級別，透過內建的 Pod Security Admission 控制器在命名空間級別執行：

*   **Privileged**：不受限制，適用於系統級和基礎設施工作負載。
*   **Baseline**：防止已知的權限提升，適用於大多數工作負載。
*   **Restricted**：嚴格限制，遵循 Pod 安全加固最佳實務。

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: my-app
  labels:
    pod-security.kubernetes.io/enforce: baseline
    pod-security.kubernetes.io/warn: restricted
```

### 13.4.7 Sidecar Containers

Kubernetes 1.33 起 Sidecar Containers 進入 GA。它們透過 `initContainers` 中帶 `restartPolicy: Always` 的容器表達，既保留 init container 的啟動順序，又會在主容器生命週期內持續執行。對於舊集群或不需要啟動順序控制的場景，仍可使用普通多容器 Pod。

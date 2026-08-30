## 19.1 Prometheus

Prometheus 和 Grafana 是目前最流行的開源監控組合，前者負責資料採集與儲存，後者負責資料視覺化。

[Prometheus](https://prometheus.io/) 是一個開源的系統監控和報警工具包。它受 Google Borgmon 的啟發，由 SoundCloud 在 2012 年建立。

### 19.1.1 架構簡介

Prometheus 的主要元件包括：

* **Prometheus Server**：核心元件，負責收集和儲存時間序列資料。
* **Exporters**：負責向 Prometheus 暴露監控資料（如 Node Exporter，cAdvisor）。
* **Alertmanager**：處理報警發送。
* **Pushgateway**：用於支持短生命週期的 Job 推送資料。

### 19.1.2 快速部署

我們可以使用 Docker Compose 快速部署一套 Prometheus + Grafana 監控環境。

本節示例使用了：

* `node-exporter`：採集宿主機指標（CPU、記憶體、磁碟、網路等）。
* `cAdvisor`：採集容器指標（容器 CPU/記憶體/網路 IO、檔案系統等）。

在生產環境中，建議將 Prometheus 的資料目錄做持久化，並顯式設定資料保留週期。

#### 1. 準備設定檔案

建立 `prometheus.yml`：

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']

  - job_name: 'cadvisor'
    static_configs:
      - targets: ['cadvisor:8080']

rule_files:
  - /etc/prometheus/rules.yml
```

#### 2. 編寫 Docker Compose 檔案

建立 `compose.yaml`（或 `docker-compose.yml`）。下面示例使用的是相對較新的穩定版本。**映像檔版本提示**：本示例中 Prometheus、Grafana、node-exporter、cAdvisor 的版本號僅為參考。生產環境部署前，請查閱以下官方資源確認最新推薦版本：
- [Prometheus 官方文件](https://prometheus.io/docs/prometheus/latest/installation/)
- [Grafana 官方發佈](https://grafana.com/grafana/download)
- [node-exporter 發佈頁](https://github.com/prometheus/node_exporter/releases)
- [cAdvisor 發佈頁](https://github.com/google/cadvisor/releases)

```yaml
services:
  prometheus:
    image: prom/prometheus:v3.11.2
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - ./rules.yml:/etc/prometheus/rules.yml
      - prometheus_data:/prometheus
    ports:
      - "127.0.0.1:9090:9090"
    command:
      - --config.file=/etc/prometheus/prometheus.yml
      - --storage.tsdb.path=/prometheus
      - --storage.tsdb.retention.time=15d
    networks:
      - monitoring

  grafana:
    image: grafana/grafana:13.0.1
    ports:
      - "127.0.0.1:3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_ADMIN_PASSWORD:?set GRAFANA_ADMIN_PASSWORD}
    networks:
      - monitoring
    depends_on:
      - prometheus

  node-exporter:
    image: prom/node-exporter:v1.11.1
    ports:
      - "127.0.0.1:9100:9100"
    networks:
      - monitoring

  cadvisor:
    image: ghcr.io/google/cadvisor:v0.56.2
    ports:
      - "127.0.0.1:8080:8080"
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
    networks:
      - monitoring

networks:
  monitoring:

volumes:
  prometheus_data:
```

#### 3. 啟動服務

```bash
$ docker compose up -d
```
啟動後，存取以下位址：

* Prometheus: `http://localhost:9090`
* Grafana：`http://localhost:3000`（帳號為 `admin`，密碼來自 `GRAFANA_ADMIN_PASSWORD`）

> 安全提示：cAdvisor 需要讀取宿主機 `/sys`、`/var/run`、Docker 資料目錄等路徑才能採集容器指標；即使是唯讀掛載，也會暴露宿主機和容器中繼資料。只在受控監控節點使用，並把 Prometheus、Grafana、cAdvisor 埠號綁定到本機或受保護網路。

### 19.1.3 設定 Grafana 面板

1. 在 Grafana 中新增 Prometheus 資料源，URL 填寫 `http://prometheus:9090`。
2. 匯入現成的 Dashboard 模板，例如 [Node Exporter Full](https://grafana.com/grafana/dashboards/1860) (ID：1860) 和 [Docker Container](https://grafana.com/grafana/dashboards/193) (ID：193)。

這樣，你就擁有了一個直觀的容器監控大屏。

### 19.1.4 生產要點與告警閉環

完成部署後，建議補齊以下生產要點。

#### 指標採集的“最小閉環”

1. 在 Prometheus 頁面打開 **Status -> Targets**，確認 `prometheus`、`node-exporter`、`cadvisor` 的 `State` 均為 `UP`。
2. 在 **Graph** 中嘗試查詢：

   * `up`
   * `rate(container_cpu_usage_seconds_total[5m])`

3. 在 Grafana Dashboard 中重點關注：

   * 宿主機 CPU/Load/記憶體/磁碟
   * 容器 CPU/記憶體使用率、容器重新啟動次數

如果你發現“面板為空”，通常不是 Grafana 的問題，而是 Prometheus 沒抓到資料或查詢標籤與 Dashboard 不匹配。

#### 常見問題排查

* **Target down**：檢查容器網路是否互通，埠號是否暴露到同一網路，以及 exporter 是否在容器內正常監聽。
* **cAdvisor 無資料或報錯**：確認掛載了 Docker 目錄與宿主機的 `/sys`、`/var/run` 等路徑，並確保宿主機上 Docker 運行正常。
* **指標缺失**：確認你的 Docker/核心版本與 cAdvisor 相容；對於 containerd 等執行時期，採集方式會不同。

#### 關鍵指標速查：節點/容器

在生產環境排障時，建議優先關注下面幾類指標，並在 Grafana 面板中建立對應的常用視圖。

* **節點 CPU 使用率**：`100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)`
* **節點記憶體使用率**：`(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100`
* **節點磁碟空間使用率**：`(1 - (node_filesystem_avail_bytes{fstype!~"tmpfs|overlay"} / node_filesystem_size_bytes{fstype!~"tmpfs|overlay"})) * 100`
* **容器 CPU**：`sum by (namespace, pod, container) (rate(container_cpu_usage_seconds_total[5m]))`
* **容器記憶體**：`sum by (namespace, pod, container) (container_memory_working_set_bytes)`

說明：不同採集路徑的 label 命名不同。Docker Compose 中獨立部署的 cAdvisor 常見容器標籤是 `name`；Kubernetes kubelet 的 `/metrics/cadvisor` 中，`container_cpu_usage_seconds_total` 等穩定指標使用 `container`、`pod`、`namespace`。如果查詢為空，先直接查詢 `container_cpu_usage_seconds_total` 樣本並在 Prometheus 圖形介面查看實際 label，不要假設存在 `container_name`。

#### Targets down 排錯清單

當 **Status -> Targets** 出現 `DOWN` 時，建議按以下順序排查：

1. **網路連通性**：Prometheus 容器是否能解析並存取目標（同一 Docker network、DNS、埠號）。
2. **埠號/路徑**：確認 exporter 監聽埠號與 Prometheus 設定一致；必要時在 Prometheus 容器內 `curl http://node-exporter:9100/metrics`。
3. **權限/掛載**：cAdvisor 需要存取宿主機 `/sys`、`/var/lib/docker` 等掛載路徑，缺失會導致指標不全或報錯。
4. **時間問題**：宿主機與容器時間偏差過大可能導致“資料看起來斷檔”，需要檢查 NTP/時區設定。
5. **目標本身異常**：確認 exporter 容器是否在重新啟動，查看 `docker logs`。

#### Alertmanager 告警建議

生產環境建議引入 Alertmanager 做告警聚合與路由，並在 Prometheus 中設定 `alerting` 與 `rule_files`。

為了保持“最小告警閉環”，建議至少覆蓋兩類告警：

* **採集鏈路告警**：例如 `up == 0`，用於發現 exporter 或網路故障。
* **資源風險告警**：例如節點磁碟空間不足，用於提前發現容量風險。

##### 1. 準備告警規則檔案

建立 `rules.yml`：

```yaml
groups:
  - name: docker_practice
    rules:
      - alert: PrometheusTargetDown
        expr: up == 0
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "Prometheus 抓取目標不可達"
          description: "Job={{ $labels.job }}, Instance={{ $labels.instance }}"

      - alert: HostDiskSpaceLow
        expr: |
          (node_filesystem_avail_bytes{fstype!~"tmpfs|overlay"} / node_filesystem_size_bytes{fstype!~"tmpfs|overlay"}) < 0.10
        for: 10m
        labels:
          severity: critical
        annotations:
          summary: "磁碟可用空間不足"
          description: "Instance={{ $labels.instance }}, Mountpoint={{ $labels.mountpoint }}"
```
說明：這裡的規則是“可用空間低於 10%”的閾值告警，並非“未來 24 小時寫滿”的預測。生產環境建議針對特定檔案系統與掛載點做更精確的過濾。

##### 2. 設定 Prometheus 載入規則並接入 Alertmanager

修改 `prometheus.yml`，增加：

```yaml
rule_files:
  - /etc/prometheus/rules.yml

alerting:
  alertmanagers:
    - static_configs:
        - targets: ["alertmanager:9093"]
```
並在 Compose 中掛載規則檔案。

##### 3. 部署 Alertmanager

建立 `alertmanager.yml`：

```yaml
route:
  receiver: default

receivers:
  - name: default
    webhook_configs:
      - url: http://example.com/webhook
```
再在 `compose.yaml` 增加服務：

```yaml
  alertmanager:
    image: prom/alertmanager:v0.32.0
    volumes:
      - ./alertmanager.yml:/etc/alertmanager/alertmanager.yml
    ports:
      - "9093:9093"
    networks:
      - monitoring
```
生產環境中，建議將告警發送到可追蹤的渠道（如 IM 機器人、事件平台、工單系統），並在告警中附帶 Dashboard 連結與排障入口，避免告警成為噪聲。

#### 建議的檔案清單

為了避免示例難以復現，建議在同一目錄下準備以下檔案：

* `compose.yaml`：Prometheus、Grafana、exporters、Alertmanager 的部署檔案
* `prometheus.yml`：Prometheus 抓取設定與告警設定
* `rules.yml`：告警規則
* `alertmanager.yml`：告警路由與接收器設定

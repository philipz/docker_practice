## 19.2 ELK 套件

ELK (Elasticsearch，Logstash，Kibana) 是目前業界最流行的開源日誌解決方案。而在容器領域，由於 Fluentd 更加輕量級且對容器支持更好，EFK (Elasticsearch，Fluentd，Kibana) 組合也變得非常流行。

### 19.2.1 方案架構

我們將採用以下架構：

1. **Docker Container**：容器將日誌輸出到標準輸出 (stdout/stderr)。
2. **Fluentd**：作為 Docker 的 Logging Driver 或運行爲常駐容器，收集容器日誌。
3. **Elasticsearch**：儲存從 Fluentd 接收到的日誌資料。
4. **Kibana**：從 Elasticsearch 讀取資料並進行視覺化展示。

### 19.2.2 部署流程

我們將使用 Docker Compose 來一鍵部署整個日誌堆疊。

#### 1. 編寫 Compose 檔案

1. 編寫 `compose.yaml`（或 `docker-compose.yml`）設定如下。**版本提示**：本示例使用 Elasticsearch 9.x、Kibana 9.x、Fluentd 等元件的特定版本號，僅作為參考。生產環境部署前，請查閱 [Elastic 官方文件](https://www.elastic.co/docs/) 和 [Fluentd 官方文件](https://docs.fluentd.org/) 確認最新版本與設定相容性。

```yaml
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:9.4.0
    container_name: elasticsearch
    environment:
      - "discovery.type=single-node"
      - "xpack.security.enabled=false"
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    ports:
      - "9200:9200"
    volumes:
      - es_data:/usr/share/elasticsearch/data
    networks:
      - logging

  kibana:
    image: docker.elastic.co/kibana/kibana:9.4.0
    container_name: kibana
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
    ports:
      - "5601:5601"
    networks:
      - logging

  fluentd:
    # elasticsearch8 外掛程式通過 REST API 與 ES 9.x 相容
    image: fluent/fluentd-kubernetes-daemonset:v1.17-debian-elasticsearch8-1
    container_name: fluentd
    environment:
      - "FLUENT_ELASTICSEARCH_HOST=elasticsearch"
      - "FLUENT_ELASTICSEARCH_PORT=9200"
      - "FLUENT_ELASTICSEARCH_SCHEME=http"
      - "FLUENT_UID=0"
    ports:
      - "24224:24224"
      - "24224:24224/udp"
    volumes:
      - ./fluentd/conf:/fluentd/etc
    networks:
      - logging

volumes:
  es_data:

networks:
  logging:
```

#### 2. 設定 Fluentd

建立 `fluentd/conf/fluent.conf`：

```ini
<source>
  @type forward
  port 24224
  bind 0.0.0.0
</source>

<match *.**>
  @type copy
  <store>
    @type elasticsearch
    host elasticsearch
    port 9200
    logstash_format true
    logstash_prefix docker
    logstash_dateformat %Y%m%d
    include_tag_key true
    tag_key @log_name
    flush_interval 1s
  </store>
  <store>
    @type stdout
  </store>
</match>
```

#### 3. 設定應用容器使用 fluentd 驅動

啟動一個測試容器，指定日誌驅動為 `fluentd`：

```bash
docker run -d \
  --log-driver=fluentd \
  --log-opt fluentd-address=localhost:24224 \
  --log-opt tag=nginx-test \
  --name nginx-test \
  nginx
```
**注意**：確保 `fluentd` 容器已經啟動並監聽在 `localhost:24224`。在生產環境中，如果你是在不同機器上，需要將 `localhost` 替換為運行 fluentd 的主機 IP。

#### 4. 在 Kibana 中查看日誌

1. 存取 `http://localhost:5601`。
2. 進入 **Management**->**Kibana**->**Index Patterns**。
3. 建立新的 Index Pattern，輸入 `docker-*`（我們在 fluent.conf 中設定的前綴）。
4. 選擇 `@timestamp` 作為時間欄位。
5. 去 **Discover** 頁面，你就能看到 Nginx 容器的日誌了。

#### Kibana 建索引模式常見坑

首次接入 EFK/ELK 時，“Elasticsearch 有資料但 Kibana 看不到”很常見，通常是 Kibana 設定或時間視窗問題：

* **Index Pattern 不匹配**：確認 Kibana 的 Index Pattern 與實際索引前綴一致。可以先用 `_cat/indices` 查看真實索引名。
* **時間欄位選擇錯誤**：若索引裡包含 `@timestamp`，一般選擇它；如果選擇了錯誤的欄位，會導致 Discover 無法按時間篩選。
* **時間視窗/時區**：Discover 右上角的時間範圍預設可能是最近 15 分鐘，且時區可能影響顯示。建議先把範圍擴大到最近 24 小時再驗證。
* **資料解析失敗**：若日誌是非結構化文字，仍可入庫但欄位不可用；生產環境建議輸出 JSON 並在採集端解析。

#### 5. 驗證日誌是否寫入 Elasticsearch：生產排錯必備

當你在 Kibana 看不到日誌時，建議先跳過 UI，從儲存端直接驗證“日誌是否入庫”。

1. 查看索引是否建立：

   ```bash
   curl -s http://localhost:9200/_cat/indices?v
   ```

   如果 Fluentd 使用了 `logstash_format true` 且 `logstash_prefix docker`，通常會看到形如 `docker-YYYY.MM.DD` 的索引。

2. 查看最近一段時間的日誌文件：

   ```bash
   curl -s -H 'Content-Type: application/json' \
     http://localhost:9200/docker-*/_search \
     -d '{"size":1,"sort":[{"@timestamp":"desc"}]}'
   ```

如果 Elasticsearch 中已經有文件，但 Kibana 仍然為空，常見原因是：

* Index Pattern 沒匹配到索引（例如寫成了 `docker-*` 但實際索引前綴不同）。
* 時間欄位沒選對或時區不一致，導致 Discover 時間視窗內看不到資料。

### 19.2.3 總結

通過 Docker 的日誌驅動機制，結合 ELK/EFK 強大的收集和分析能力，我們可以輕鬆建立一個能夠處理海量日誌的監控平台，這對於排查生產問題至關重要。

### 19.2.4 生產要點

在生產環境中，日誌系統往往比監控系統更容易因為“容量與寫入壓力”出問題，建議特別關注：

* **容量規劃**：日誌增長速度與磁碟佔用直接相關。建議設定日誌保留週期與索引生命週期策略 (ILM)，避免 Elasticsearch 因磁碟水位觸發唯讀或不可用。
* **資源設定**：Elasticsearch 對 JVM Heap 較敏感。除示例中的 `ES_JAVA_OPTS` 外，生產環境需要結合節點記憶體、分片規模、查詢壓力做評估。
* **鏈路可靠性**：採集端到儲存端要考慮網路抖動、背壓與重試策略；當 Elasticsearch 寫入變慢時，採集端的緩衝與落盤策略決定了是否會丟日誌。
* **日誌格式**：推薦應用輸出結構化日誌 (JSON) 並包含關鍵欄位（如 `trace_id`、`request_id`、`service`、`env`），以便快速過濾與關聯分析。

#### 索引與保留策略的落地建議

無論是 EFK 還是 ELK，生產上都需要回答兩個問題：

* 日誌保留多久？
* 保留期內的日誌如何保證可查詢、不過度佔用儲存？

建議按環境與業務重要性對日誌分層，並制定不同的保留週期，例如：

* **生產環境**：7～30 天
* **測試環境**：1～7 天

實現方式通常有兩類：

* **按天滾動索引**：如 `docker-YYYY.MM.DD`，再定期刪除過期索引。
* **使用 ILM**：定義 Hot/Warm/Cold/刪除階段，按時間與容量自動滾動與回收。

對於中小規模集群，先把“按天滾動 + 過期刪除”做扎實，往往就能解決 80% 的容量問題；當日誌量上來、查詢壓力變大後，再逐步引入 ILM、分層儲存與更精細的分片規劃。

#### 最小可用的“過期索引清理”示例

如果你採用按天滾動索引（例如 `docker-YYYY.MM.DD`），可以通過 Elasticsearch API 定期清理過期索引。

下面示例僅用於演示思路：取得所有 `docker-` 前綴索引並刪除指定索引。生產環境建議基於日期計算、灰度驗證與權限控制後再執行自動化清理。

1. 列出索引：

   ```bash
   curl -s http://localhost:9200/_cat/indices/docker-*?v
   ```

2. 刪除某個過期索引（示例）：

   ```bash
   curl -X DELETE http://localhost:9200/docker-2026.02.01
   ```

如果你希望更自動化的治理能力，可以進一步使用 ILM 為索引設定滾動與刪除策略。

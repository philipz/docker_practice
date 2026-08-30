## 實戰 WordPress

> **版本說明**：本範例使用以下映像檔版本：
> - MySQL：8.4（可替換為其他 8.x 版本，或使用 MariaDB 替代）
> - WordPress：latest（建議在生產環境指定具體版本，如 6.x）

WordPress 是全球最流行的內容管理系統 (CMS)。使用 Docker Compose 可以在幾分鐘內搭建一個包含資料庫、Web 服務和持久化儲存的本地練習/單機演示環境。

---

### 專案結構

```bash
wordpress/
├── compose.yaml
├── .env                # 非敏感環境變數（如版本、埠號）
├── secrets/            # 本地金鑰檔案，生產環境應由金鑰管理系統提供
│   ├── db_root_password.txt
│   └── db_password.txt
└── nginx/              # 可選：反向代理設定
    └── nginx.conf
```
---

### 編寫 `compose.yaml`

這是一個可執行的單機最小設定，不是完整生產安全基線。正式部署前應固定映像檔版本、放在反向代理/TLS 後面、限制公開埠號、設定備份與監控，並按 WordPress 與外掛生命週期做升級測試。

```yaml
services:
  # 資料庫服務

  db:
    image: mysql:8.4
    container_name: wordpress_db
    restart: always
    command:
      # 啟用原生密碼認證（MySQL 8.4 預設禁用，舊版 WP 相容性需要）

      - --mysql-native-password=ON
      - --character-set-server=utf8mb4
      - --collation-server=utf8mb4_unicode_ci
    environment:
      MYSQL_ROOT_PASSWORD_FILE: /run/secrets/db_root_password
      MYSQL_DATABASE: wordpress
      MYSQL_USER: wordpress
      MYSQL_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_root_password
      - db_password
    volumes:
      - db_data:/var/lib/mysql
    networks:
      - wp_net

  # WordPress 服務

  wordpress:
    # 範例保留 latest 以便讀者快速體驗；生產環境請固定到經過測試的明確版本標籤
    image: wordpress:latest
    container_name: wordpress_app
    restart: always
    ports:
      # 本機除錯入口；生產環境請透過反向代理發佈 HTTPS
      - "127.0.0.1:8000:80"
    environment:
      WORDPRESS_DB_HOST: db:3306
      WORDPRESS_DB_USER: wordpress
      WORDPRESS_DB_PASSWORD_FILE: /run/secrets/db_password
      WORDPRESS_DB_NAME: wordpress
    secrets:
      - db_password
    volumes:
      - wp_data:/var/www/html
      # 增加上傳檔案大小限制

      - ./uploads.ini:/usr/local/etc/php/conf.d/uploads.ini
    depends_on:
      - db
    networks:
      - wp_net

volumes:
  db_data:  # 資料庫持久化
  wp_data:  # WordPress 檔案(外掛/主題/上傳)持久化

networks:
  wp_net:

secrets:
  db_root_password:
    file: ./secrets/db_root_password.txt
  db_password:
    file: ./secrets/db_password.txt
```
---

### 設定檔案詳解

#### 1. 金鑰檔案

不要把資料庫密碼寫入 `compose.yaml`、`.env`、命令列或 Git。Compose 官方建議敏感值使用 secrets；本地練習可用只讀金鑰檔案模擬：

```bash
mkdir -p secrets
printf '%s\n' 'somestrongrootpassword' > secrets/db_root_password.txt
printf '%s\n' 'somestronguserpassword' > secrets/db_password.txt
chmod 600 secrets/*.txt
```

把 `secrets/` 加入 `.gitignore`。生產環境應改用平台金鑰管理能力，而不是把真實密碼放在專案目錄。

#### 2. 資料持久化

我們定義了兩個命名卷：

- `db_data`：確保 MySQL 容器重建後資料不丟失
- `wp_data`：保存 WordPress 的核心檔案、外掛、主題和上傳的媒體檔案

#### 3. PHP 設定最佳化

預設的 WordPress 映像檔上傳檔案限制較小（通常 2MB）。建立 `uploads.ini`：

```ini
file_uploads = On
memory_limit = 256M
upload_max_filesize = 64M
post_max_size = 64M
max_execution_time = 600
```
---

### 啟動與執行

1. 啟動服務：

```bash
$ docker compose up -d
```

2. 存取安裝介面：
   開啟瀏覽器存取 `http://localhost:8000`

3. 查看日誌：

```bash
$ docker compose logs -f
```
---

### 生產環境最佳實務

#### 1. 資料庫備份

不要只依賴 Volume。建議定期備份資料庫：

```bash
## 匯出 SQL

$ docker compose exec -T db sh -c 'tmp=$(mktemp) && printf "[client]\nuser=wordpress\npassword=%s\n" "$(cat /run/secrets/db_password)" > "$tmp" && mysqldump --defaults-extra-file="$tmp" wordpress; rc=$?; rm -f "$tmp"; exit "$rc"' > backup.sql
```
或者新增一個自動備份容器：

```yaml
  backup:
    image: tiredofit/db-backup
    volumes:
      - ./backups:/backup
    environment:
      # tiredofit/db-backup 4.x 起按 DB01_ 前綴設定備份任務，並原生支援 _FILE 讀密
      - DB01_TYPE=mysql
      - DB01_HOST=db
      - DB01_NAME=wordpress
      - DB01_USER=wordpress
      - DB01_PASS_FILE=/run/secrets/db_password
      - DB01_BACKUP_INTERVAL=1440 # 每天備份一次（單位：分鐘）
    secrets:
      - db_password
    depends_on:
      - db
    networks:
      - wp_net
```

#### 2. 使用 Nginx 反向代理

在生產環境中，不要直接暴露 WordPress 埠號，而是透過 Nginx 進行反向代理並設定 SSL。

#### 3. 使用 Redis 快取

WordPress 支援 Redis 快取以提高效能。

```yaml
  redis:
    image: redis:alpine
    restart: always
    networks:
      - wp_net
```
在 WordPress 容器環境變數中新增：
```yaml
      WORDPRESS_REDIS_HOST: redis
```
並安裝 Redis Object Cache 外掛。

---

### 常見問題

#### Q：資料庫連線錯誤

**現象**：存取頁面顯示 「Error establishing a database connection」。**排查**：

1. 檢查 `docker compose logs wordpress`
2. 確認 `secrets/db_password.txt` 的內容正確，且與資料庫初始化時使用的密碼一致（改密碼後需要重建 db 資料卷）
3. 確認 `WORDPRESS_DB_HOST` 也是 `db`（服務名）
4. MySQL 8.4 可能需要幾秒鐘啟動，WordPress 會自動重試，稍等片刻即可。

#### Q：無法上傳大檔案

**解決**：確保掛載了 `uploads.ini` 設定，並且重啟了容器：
```bash
$ docker compose restart wordpress
```
---

### 延伸閱讀

- [Compose 模板檔案](compose_file.md)：深入瞭解設定項
- [資料卷](../data_management/volume.md)：理解資料持久化
- [Docker Hub WordPress](https://hub.docker.com/_/wordpress)：官方映像檔文件

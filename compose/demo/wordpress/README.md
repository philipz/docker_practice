# WordPress Compose 範例

本範例使用 Docker Compose secrets 管理資料庫密碼，啟動前需要先建立金鑰檔案（參見書中 WordPress 一節）：

```bash
mkdir -p secrets
printf '%s\n' 'somestrongrootpassword' > secrets/db_root_password.txt
printf '%s\n' 'somestronguserpassword' > secrets/db_password.txt
chmod 600 secrets/*.txt
```

然後啟動：

```bash
docker compose up -d
```

注意：`secrets/` 目錄不要提交到版本庫；生產環境應改用平台的金鑰管理能力。

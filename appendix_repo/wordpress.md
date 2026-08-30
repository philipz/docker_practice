## WordPress

### 基本資訊

[WordPress](https://en.wikipedia.org/wiki/WordPress) 是開源的 Blog 和內容管理系統框架，它基於 PHP 和 MySQL。

該倉庫位於 `https://hub.docker.com/_/wordpress/`。具體可用版本以 Docker Hub 上的 tags 列表為準。

### 使用方法

啟動容器需要 MySQL 的支援，預設埠號為 `80`。

首先建立網路

```bash
$ docker network create my-wordpress-net
```

啟動 MySQL 容器

```bash
$ docker run --name some-mysql -d --network my-wordpress-net -e MYSQL_ROOT_PASSWORD=mysecretpassword mysql
```

啟動 WordPress 容器

```bash
$ docker run --name some-wordpress -d --network my-wordpress-net -e WORDPRESS_DB_HOST=some-mysql -e WORDPRESS_DB_PASSWORD=mysecretpassword wordpress
```

啟動 WordPress 容器時可以指定的一些環境變數包括：

* `WORDPRESS_DB_HOST`：MySQL 服務的主機名
* `WORDPRESS_DB_USER`：MySQL 資料庫的使用者名稱
* `WORDPRESS_DB_PASSWORD`：MySQL 資料庫的密碼
* `WORDPRESS_DB_NAME`：WordPress 要使用的資料庫名

### Dockerfile

請到 [WordPress 官方映像檔文件目錄](https://github.com/docker-library/docs/tree/master/wordpress) 查看。

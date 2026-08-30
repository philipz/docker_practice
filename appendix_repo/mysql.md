## MySQL

### 基本資訊

[MySQL](https://en.wikipedia.org/wiki/MySQL) 是開源的關聯資料庫實作。

該倉庫位於 [Docker Hub 的 MySQL 官方映像檔頁](https://hub.docker.com/_/mysql/)。具體可用版本以 Docker Hub 上的 tags 列表為準。

### 使用方法

預設會在 `3306` 埠號啟動資料庫。

```bash
$ docker run --name some-mysql -e MYSQL_ROOT_PASSWORD=mysecretpassword -d mysql
```

之後就可以使用其他應用來連線到該容器。

首先建立網路

```bash
$ docker network create my-mysql-net
```

然後啟動 MySQL 容器

```bash
$ docker run --name some-mysql -d --network my-mysql-net -e MYSQL_ROOT_PASSWORD=mysecretpassword mysql
```

最後啟動應用容器

```bash
$ docker run --name some-app -d --network my-mysql-net application-that-uses-mysql
```

或者透過 `mysql` 命令行連線。

```bash
$ docker run -it --rm \
    --network my-mysql-net \
    mysql \
    sh -c 'exec mysql -hsome-mysql -P3306 -uroot -p'
```

### Dockerfile

請到 [MySQL 官方映像檔文件目錄](https://github.com/docker-library/docs/tree/master/mysql) 查看。

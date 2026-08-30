## MongoDB

### 基本資訊

[MongoDB](https://en.wikipedia.org/wiki/MongoDB) 是開源的 NoSQL 資料庫實作。

該倉庫位於 `https://hub.docker.com/_/mongo/`。具體可用版本以 Docker Hub 上的 tags 列表為準。

### 使用方法

預設會在 `27017` 埠號啟動資料庫。

```bash
$ docker run --name mongo -d mongo
```

使用其他應用連線到容器，首先建立網路

```bash
$ docker network create my-mongo-net
```

然後啟動 MongoDB 容器

```bash
$ docker run --name some-mongo -d --network my-mongo-net mongo
```

最後啟動應用容器

```bash
$ docker run --name some-app -d --network my-mongo-net application-that-uses-mongo
```

或者透過 `mongosh`（MongoDB 6.0+ 已移除舊版 `mongo` 命令行工具）

```bash
$ docker run -it --rm \
    --network my-mongo-net \
    mongo \
    mongosh "some-mongo:27017/test"
```

### Dockerfile

請到 [Mongo 官方映像檔文件目錄](https://github.com/docker-library/docs/tree/master/mongo) 查看。

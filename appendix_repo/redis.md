## Redis

### 基本資訊

[Redis](https://en.wikipedia.org/wiki/Redis) 是開源的記憶體 Key-Value 資料庫實作。

該倉庫位於 [Docker Hub 的 Redis 官方映像檔頁](https://hub.docker.com/_/redis/)。具體可用版本以 Docker Hub 上的 tags 列表為準。

### 使用方法

預設會在 `6379` 埠號啟動資料庫。

```bash
$ docker run --name some-redis -d -p 6379:6379 redis
```

另外還可以啟用[持久儲存](https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/)。

```bash
$ docker run --name some-redis -d -p 6379:6379 redis redis-server --appendonly yes
```

預設資料儲存位置在 `VOLUME/data`。可以使用 `--volumes-from some-volume-container` 或 `-v /docker/host/dir:/data` 將資料存放到本地。

使用其他應用連線到容器，首先建立網路

```bash
$ docker network create my-redis-net
```

然後啟動 redis 容器

```bash
$ docker run --name some-redis -d --network my-redis-net redis
```

最後啟動應用容器

```bash
$ docker run --name some-app -d --network my-redis-net application-that-uses-redis
```

或者透過 `redis-cli`

```bash
$ docker run -it --rm \
    --network my-redis-net \
    redis \
    sh -c 'exec redis-cli -h some-redis'
```

### Dockerfile

請到 [Redis 官方映像檔文件目錄](https://github.com/docker-library/docs/tree/master/redis) 查看。

## Ubuntu

### 基本資訊

[Ubuntu](https://en.wikipedia.org/wiki/Ubuntu) 是流行的 Linux 發行版，其自帶軟體版本往往較新一些。

該倉庫位於 [Docker Hub 的 Ubuntu 官方映像檔頁](https://hub.docker.com/_/ubuntu/)。具體可用版本以 Docker Hub 上的 tags 列表為準。

### 使用方法

預設會啟動一個最小化的 Ubuntu 環境。

```bash
$ docker run --name some-ubuntu -it ubuntu:24.04
root@523c70904d54:/#
```

### Dockerfile

請到 [Ubuntu 官方映像檔文件目錄](https://github.com/docker-library/docs/tree/master/ubuntu) 查看。

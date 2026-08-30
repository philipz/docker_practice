## Nginx

### 基本資訊

[Nginx](https://en.wikipedia.org/wiki/Nginx) 是開源的高效的 Web 伺服器實作，支援 HTTP、HTTPS、SMTP、POP3、IMAP 等協定。

該倉庫位於 [Docker Hub 的 Nginx 官方映像檔頁](https://hub.docker.com/_/nginx/)。具體可用版本以 Docker Hub 上的 tags 列表為準。

### 使用方法

下面的命令將作為一個靜態頁面伺服器啟動。

```bash
$ docker run --name some-nginx -v /some/content:/usr/share/nginx/html:ro -d nginx
```

使用者也可以不使用這種映射方式，透過利用 Dockerfile 來直接將靜態頁面內容放到映像檔中，內容為

```docker
FROM nginx
COPY static-html-directory /usr/share/nginx/html
```

之後產生新的映像檔，並啟動一個容器。

```bash
$ docker build -t some-content-nginx .
$ docker run --name some-nginx -d some-content-nginx
```

開放埠號，並映射到本地的 `8080` 埠號。

```bash
$ docker run --name some-nginx -d -p 8080:80 some-content-nginx
```

Nginx 的預設設定檔案路徑為 `/etc/nginx/nginx.conf`，可以透過映射它來使用本地的設定檔案，例如

```bash
$ docker run -d \
    --name some-nginx \
    -p 8080:80 \
    -v /path/nginx.conf:/etc/nginx/nginx.conf:ro \
    nginx
```

### Dockerfile

請到 [Nginx 官方映像檔文件目錄](https://github.com/docker-library/docs/tree/master/nginx) 查看。

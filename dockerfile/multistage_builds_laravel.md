## 實戰多階段建立 Laravel 映像檔

> 本節適用於 PHP 開發者閱讀。`Laravel` 基於 8.x 版本，各個版本的檔案結構可能會有差異，請根據實際自行修改。

### 準備

新建一個 `Laravel` 專案或在已有的 `Laravel` 專案根目錄下新建 `Dockerfile` `.dockerignore` `laravel.conf` 檔案。

在 `.dockerignore` 檔案中寫入以下內容。

```bash
.idea/
.git/

vendor/

node_modules/

public/js/
public/css/
public/mix-manifest.json

yarn-error.log

bootstrap/cache/*
storage/

## 自行新增其他需要排除的檔案，例如 .env.* 檔案

...
```
在 `laravel.conf` 檔案中寫入 nginx 設定。

```nginx
server {
  listen 80 default_server;
  root /app/laravel/public;
  index index.php index.html;

  location / {
      try_files $uri $uri/ /index.php?$query_string;
  }

  location ~ .*\.php(\/.*)*$ {
    fastcgi_pass   laravel:9000;
    include        fastcgi.conf;

    # fastcgi_connect_timeout 300;

    # fastcgi_send_timeout 300;

    # fastcgi_read_timeout 300;

  }
}
```

### 前端建立

第一階段進行前端建立。

```docker
# 注：node 映像檔推薦使用具體的版本標籤（如 node:22-alpine）
FROM node:22-alpine as frontend

COPY package.json /app/

RUN set -x ; cd /app \
      && npm install --registry=https://registry.npmmirror.com

COPY webpack.mix.js webpack.config.js tailwind.config.js /app/
COPY resources/ /app/resources/

RUN set -x ; cd /app \
      && touch artisan \
      && mkdir -p public \
      && npm run production
```

### 安裝 Composer 依賴

第二階段安裝 Composer 依賴。

```docker
# 注：composer 映像檔推薦使用具體的版本標籤（如 composer:2.x）
FROM composer:2 as composer

COPY database/ /app/database/
COPY composer.json composer.lock /app/

RUN set -x ; cd /app \
      && composer config -g repo.packagist composer https://mirrors.aliyun.com/composer/ \
      && composer install \
           --ignore-platform-reqs \
           --no-interaction \
           --no-plugins \
           --no-scripts \
           --prefer-dist
```

### 整合以上階段所產生的檔案

第三階段對以上階段產生的檔案進行整合。

```docker
# 注：php 映像檔版本號已包含 major.minor（8.3），生產環境可根據需要調整
FROM php:8.3-fpm-alpine as laravel

ARG LARAVEL_PATH=/app/laravel

COPY --from=composer /app/vendor/ ${LARAVEL_PATH}/vendor/
COPY . ${LARAVEL_PATH}
COPY --from=frontend /app/public/js/ ${LARAVEL_PATH}/public/js/
COPY --from=frontend /app/public/css/ ${LARAVEL_PATH}/public/css/
COPY --from=frontend /app/public/mix-manifest.json ${LARAVEL_PATH}/public/mix-manifest.json

RUN set -x ; cd ${LARAVEL_PATH} \
      && mkdir -p storage \
      && mkdir -p storage/framework/cache \
      && mkdir -p storage/framework/sessions \
      && mkdir -p storage/framework/testing \
      && mkdir -p storage/framework/views \
      && mkdir -p storage/logs \
      && chown -R www-data:www-data storage \
      && chmod -R 775 storage \
      && php artisan package:discover
```

### 最後一個階段建立 NGINX 映像檔

```docker
# 注：nginx 映像檔推薦使用具體的版本標籤（如 nginx:1.28-alpine）
FROM nginx:1.28-alpine as nginx

ARG LARAVEL_PATH=/app/laravel

COPY laravel.conf /etc/nginx/conf.d/
COPY --from=laravel ${LARAVEL_PATH}/public ${LARAVEL_PATH}/public
```

### 建立 Laravel 及 Nginx 映像檔

使用 `docker build` 命令建立映像檔。

```bash
$ docker build -t my/laravel --target=laravel .

$ docker build -t my/nginx --target=nginx .
```

### 啟動容器並測試

新建 Docker 網路

```bash
$ docker network create laravel
```
啟動 laravel 容器，`--name=laravel` 參數設定的名字必須與 `nginx` 設定檔案中的 `fastcgi_pass   laravel:9000;` 一致

```bash
$ docker run -dit --rm --name=laravel --network=laravel my/laravel
```
啟動 nginx 容器

```bash
$ docker run -dit --rm --network=laravel -p 8080:80 my/nginx
```
瀏覽器存取 `127.0.0.1:8080` 可以看到 Laravel 專案首頁。

> 也許 Laravel 專案依賴其他外部服務，例如 redis、MySQL，請自行啟動這些服務之後再進行測試，本小節不再贅述。

### 生產環境最佳化

本小節內容為了方便測試，將設定檔案直接放到了映像檔中，實際在使用時 **建議** 將設定檔案作為 `config` 或 `secret` 掛載到容器中，請讀者自行學習 `Kubernetes` 的相關內容。

由於篇幅所限本小節只是簡單列出，更多內容可以參考 [khs1994-docker/laravel-demo](https://github.com/khs1994-docker/laravel-demo) 專案。

### 附錄

完整的 `Dockerfile` 檔案如下。

```docker
# 注：生產環境推薦使用具體的版本標籤，如 node:22-alpine、composer:2.x、php:8.3-fpm-alpine、nginx:1.28-alpine
FROM node:22-alpine as frontend

COPY package.json /app/

RUN set -x ; cd /app \
      && npm install --registry=https://registry.npmmirror.com

COPY webpack.mix.js webpack.config.js tailwind.config.js /app/
COPY resources/ /app/resources/

RUN set -x ; cd /app \
      && touch artisan \
      && mkdir -p public \
      && npm run production

FROM composer:2 as composer

COPY database/ /app/database/
COPY composer.json composer.lock /app/

RUN set -x ; cd /app \
      && composer config -g repo.packagist composer https://mirrors.aliyun.com/composer/ \
      && composer install \
           --ignore-platform-reqs \
           --no-interaction \
           --no-plugins \
           --no-scripts \
           --prefer-dist

FROM php:8.3-fpm-alpine as laravel

ARG LARAVEL_PATH=/app/laravel

COPY --from=composer /app/vendor/ ${LARAVEL_PATH}/vendor/
COPY . ${LARAVEL_PATH}
COPY --from=frontend /app/public/js/ ${LARAVEL_PATH}/public/js/
COPY --from=frontend /app/public/css/ ${LARAVEL_PATH}/public/css/
COPY --from=frontend /app/public/mix-manifest.json ${LARAVEL_PATH}/public/mix-manifest.json

RUN set -x ; cd ${LARAVEL_PATH} \
      && mkdir -p storage \
      && mkdir -p storage/framework/cache \
      && mkdir -p storage/framework/sessions \
      && mkdir -p storage/framework/testing \
      && mkdir -p storage/framework/views \
      && mkdir -p storage/logs \
      && chown -R www-data:www-data storage \
      && chmod -R 775 storage \
      && php artisan package:discover

FROM nginx:1.28-alpine as nginx

ARG LARAVEL_PATH=/app/laravel

COPY laravel.conf /etc/nginx/conf.d/
COPY --from=laravel ${LARAVEL_PATH}/public ${LARAVEL_PATH}/public
```

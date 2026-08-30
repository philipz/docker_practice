## 容器互連

容器之間的網路通訊是 Docker 網路的核心功能之一。本節介紹容器互連的幾種方式。

### 同一網路內的容器

同一自訂網路內的容器可以直接透過容器名通訊，這是推薦的容器互連方式：

```bash
## 建立網路

$ docker network create app-net

## 啟動應用和資料庫

$ docker run -d --name redis --network app-net redis
$ docker run -d --name app --network app-net myapp

## app 容器中可以用 redis:6379 連接 Redis

...
```

### 連接到多個網路

一個容器可以同時連接到多個網路，這對於需要跨網路通訊的中間件容器特別有用：

```bash
## 啟動容器

$ docker run -d --name multi-net-container --network frontend nginx

## 再連接到另一個網路

$ docker network connect backend multi-net-container

## 查看容器的網路

$ docker inspect multi-net-container --format '{{json .NetworkSettings.Networks}}'
```

### ⚠️ --link 已廢棄

`--link` 是 Docker 早期用於容器互連的方式，**已經被廢棄**，不建議在新專案中使用。請使用自訂網路替代：

```bash
## 舊方式（不推薦）

$ docker run --link db:database myapp

## 新方式（推薦）

$ docker network create mynet
$ docker run --network mynet --name db postgres
$ docker run --network mynet --name app myapp
```
使用自訂網路的優勢在於：

- 原生支援 DNS 解析
- 不需要在容器啟動時顯式聲明依賴
- 更靈活，可以動態 connect/disconnect

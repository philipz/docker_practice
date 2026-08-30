## 刪除容器

隨著容器的建立和停止，系統中會積累大量的容器。本節將介紹如何刪除不再需要的容器，以及如何清理所有停止的容器。

### 基本用法

使用 `docker rm` 刪除已停止的容器：

```bash
$ docker rm 容器名或ID
```
> 💡 `docker rm` 是 `docker container rm` 的簡寫，兩者等效。

---

### 刪除選項

| 選項 | 說明 | 範例 |
|------|------|------|
| 無參數 | 刪除已停止的容器 | `docker rm mycontainer` |
| `-f` | 強制刪除執行中的容器 | `docker rm -f mycontainer` |
| `-v` | 同時刪除關聯的匿名卷 | `docker rm -v mycontainer` |

#### 刪除已停止的容器

```bash
$ docker rm mycontainer
mycontainer
```

#### 強制刪除執行中的容器

```bash
## 不加 -f 會報錯

$ docker rm running_container
Error: cannot remove running container

## 加 -f 強制刪除

$ docker rm -f running_container
running_container
```
> ⚠️ 強制刪除會向容器傳送 SIGKILL 訊號，可能導致資料遺失。建議先 `docker stop` 優雅停止。

#### 刪除容器及其資料卷

```bash
## 刪除容器時同時刪除其匿名卷

$ docker rm -v mycontainer
```
> 注意：只刪除匿名卷，命名卷不會被刪除。

---

### 批次刪除

#### 刪除所有已停止的容器

```bash
## 方式一：使用 prune 命令（推薦）

$ docker container prune

WARNING! This will remove all stopped containers.
Are you sure you want to continue? [y/N] y
Deleted Containers:
abc123...
def456...
Total reclaimed space: 150MB

## 方式二：不提示確認

$ docker container prune -f
```

#### 刪除所有容器：包括執行中的

```bash
## 先停止所有容器，再刪除

$ docker stop $(docker ps -q)
$ docker rm $(docker ps -aq)

## 或者直接強制刪除

$ docker rm -f $(docker ps -aq)
```

#### 按條件刪除

```bash
## 刪除所有已退出的容器

$ docker rm $(docker ps -aq -f status=exited)

## 刪除名稱包含 "test" 的容器

$ docker rm $(docker ps -aq -f name=test)

## 刪除 24 小時前建立的容器

$ docker container prune --filter "until=24h"
```
---

### 常用過濾條件

`docker ps` 的過濾條件可以配合 `rm` 使用：

| 過濾條件 | 說明 | 範例 |
|---------|------|------|
| `status=exited` | 已退出的容器 | `-f status=exited` |
| `status=created` | 已建立未啟動 | `-f status=created` |
| `name=xxx` | 名稱匹配 | `-f name=myapp` |
| `ancestor=xxx` | 基於某映像檔建立 | `-f ancestor=nginx` |
| `before=xxx` | 在某容器之前建立 | `-f before=mycontainer` |
| `since=xxx` | 在某容器之後建立 | `-f since=mycontainer` |

#### 範例

```bash
## 刪除所有基於 nginx 映像檔的容器

$ docker rm $(docker ps -aq -f ancestor=nginx)

## 刪除所有建立後未啟動的容器

$ docker rm $(docker ps -aq -f status=created)
```
---

### 容器與映像檔的相依關係

> 有容器相依的映像檔無法刪除。

```bash
## 嘗試刪除有容器相依的映像檔

$ docker image rm nginx
Error: image is being used by stopped container abc123

## 需要先刪除依賴該映像檔的容器

$ docker rm abc123
$ docker image rm nginx
```
---

### 清理策略建議

#### 開發環境

```bash
## 定期清理已停止的容器

$ docker container prune -f

## 一鍵清理所有未使用資源

$ docker system prune -f
```

#### 生產環境

```bash
## 使用 --rm 參數執行臨時容器

$ docker run --rm ubuntu echo "Hello"

## 容器退出後自動刪除

## 定期清理（設定保留時間）

$ docker container prune --filter "until=168h"  # 保留 7 天內的
```

#### 完整清理腳本

```bash
#!/bin/bash

## cleanup.sh - Docker 資源清理腳本

echo "清理已停止的容器..."
docker container prune -f

echo "清理未使用的映像檔..."
docker image prune -f

echo "清理未使用的資料卷..."
docker volume prune -f

echo "清理未使用的網路..."
docker network prune -f

echo "清理完成！"
docker system df
```
---

### 常見問題

#### Q：容器無法刪除

```bash
Error: container is running
```
解決：先停止容器，或使用 `-f` 強制刪除

```bash
$ docker stop mycontainer
$ docker rm mycontainer

## 或

$ docker rm -f mycontainer
```

#### Q：刪除後磁碟空間沒釋放

可能原因：

1. 容器的資料卷未刪除（使用 `-v` 參數）
2. 映像檔未刪除
3. 建立快取未清理

解決：

```bash
## 查看空間佔用

$ docker system df

## 完整清理

$ docker system prune -a --volumes
```
---

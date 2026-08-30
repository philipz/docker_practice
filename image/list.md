## 列出映像檔

在下載了映像檔後，我們可以使用 `docker image ls` 命令列出本地端主機上的映像檔。

### 基本用法

查看本地端已下載的映像檔：

```bash
$ docker image ls
REPOSITORY   TAG       IMAGE ID       CREATED        SIZE
redis        latest    5f515359c7f8   5 days ago     183MB
nginx        latest    05a60462f8ba   5 days ago     181MB
ubuntu       24.04     329ed837d508   3 days ago     78MB
ubuntu       noble     329ed837d508   3 days ago     78MB
```
> 💡 `docker images` 是 `docker image ls` 的簡寫，兩者等效。

---

### 輸出欄位說明

`docker image ls` 命令預設輸出的列表包含倉庫名、標籤、映像檔 ID、建立時間和佔用空間等資訊。

| 欄位 | 說明 |
|------|------|
| **REPOSITORY** | 倉庫名 |
| **TAG** | 標籤（版本）|
| **IMAGE ID** | 映像檔唯一標識（短 ID，前 12 位）|
| **CREATED** | 建立時間 |
| **SIZE** | 本地端佔用空間 |

#### 同一映像檔多個標籤

注意上面的 `ubuntu:24.04` 和 `ubuntu:noble` 擁有相同的 IMAGE ID——它們是同一個映像檔的不同標籤，只佔用一份儲存空間。

> **版本說明**：`ubuntu:24.04` 是具體版本號，`ubuntu:noble` 是發行代號（Ubuntu 24.04 的代號）。在 Dockerfile 中應優先使用版本號（如 `ubuntu:24.04`）而非發行代號，因為版本號在將來更易理解。

---

### 理解映像檔大小

Docker 映像檔的大小可能與我們通常理解的檔案大小有所不同，這涉及到分層儲存的概念。

#### 本地端大小 vs Hub 顯示大小

| 位置 | 顯示大小 | 說明 |
|------|---------|------|
| Docker Hub | 29MB | 壓縮後的網路傳輸大小 |
| docker image ls | 78MB | 本地端解壓後的實際大小 |

#### 實際磁碟佔用

由於映像檔是分層儲存，不同映像檔可能共享相同的層：

```bash
ubuntu:24.04    nginx:latest    redis:latest
    │               │                │
    └───────┬───────┘                │
            ▼                        │
       共享基礎層 ◄───────────────────┘
```
因此，`docker image ls` 中各映像檔大小之和 > 實際磁碟佔用。

#### 查看實際空間佔用

```bash
$ docker system df
TYPE            TOTAL   ACTIVE   SIZE      RECLAIMABLE
Images          15      3        2.5GB     1.8GB (72%)
Containers      5       2        100MB     80MB (80%)
Local Volumes   8       2        500MB     400MB (80%)
Build Cache     0       0        0B        0B
```
---

### 過濾映像檔

隨著本地端映像檔數量的增加，我們需要更有效的方式來尋找特定的映像檔。Docker 提供了多種過濾方式。

#### 按倉庫名過濾

```bash
## 列出所有 ubuntu 映像檔

$ docker images ubuntu
REPOSITORY   TAG     IMAGE ID       SIZE
ubuntu       24.04   329ed837d508   78MB
ubuntu       noble   329ed837d508   78MB
ubuntu       22.04   a1b2c3d4e5f6   72MB
```

#### 按倉庫名和標籤過濾

```bash
$ docker images ubuntu:24.04
REPOSITORY   TAG     IMAGE ID       SIZE
ubuntu       24.04   329ed837d508   78MB
```

#### 使用過濾器 --filter

| 過濾條件 | 說明 | 範例 |
|---------|------|------|
| `dangling=true` | 虛懸映像檔 | `-f dangling=true` |
| `before=映像檔` | 在某映像檔之前建立 | `-f before=nginx:latest` |
| `since=映像檔` | 在某映像檔之後建立 | `-f since=nginx:latest` |
| `label=key=value` | 按 LABEL 過濾 | `-f label=version=1.0` |
| `reference=pattern` | 按名稱模式 | `-f reference='*:latest'` |

```bash
## 列出 nginx 之後建立的映像檔

$ docker images -f since=nginx:latest

## 列出所有帶 latest 標籤的映像檔

$ docker images -f reference='*:latest'

## 列出帶特定 LABEL 的映像檔

$ docker images -f label=maintainer=example@email.com
```
---

### 虛懸映像檔

倉庫名和標籤都為 `<none>` 的映像檔被稱為虛懸映像檔。自 Docker Engine 29 起，`docker image ls` 預設不再列出它們，需要 `-a` 或 `dangling=true` 過濾器才能看到。

#### 什麼是虛懸映像檔

倉庫名和標籤都顯示為 `<none>` 的映像檔：

```bash
$ docker images -f dangling=true
REPOSITORY   TAG       IMAGE ID       SIZE
<none>       <none>    00285df0df87   342MB
```

#### 產生原因

1. **映像檔重新建立**：新映像檔使用了舊映像檔的標籤，舊映像檔標籤被移除
2. **docker pull 更新**：取得更新版本時，舊版本失去標籤

#### 處理虛懸映像檔

```bash
## 列出虛懸映像檔

$ docker images -f dangling=true

## 刪除虛懸映像檔

$ docker image prune
```
---

### 中間層映像檔

`docker image ls` 預設列出的只是有標籤的頂層映像檔。除了虛懸映像檔，被隱藏的還有一類為了加速映像檔建立、重複利用資源而存在的中間層映像檔。

#### 查看所有映像檔：包含中間層

```bash
$ docker images -a
```
會顯示預設隱藏的映像檔：建立過程中產生的中間層，以及上面提到的虛懸映像檔。中間層被其他映像檔相依。

> ⚠️ 不要刪除中間層映像檔。它們是其他映像檔的相依，刪除會導致上層映像檔無法使用。刪除頂層映像檔時會自動清理不再需要的中間層。

---

### 格式化輸出

為了配合腳本使用或展示更關注的資訊，我們可以使用 `--format` 參數來自訂輸出格式。

#### 只輸出 ID

```bash
$ docker images -q
5f515359c7f8
05a60462f8ba
329ed837d508
```
常用於配合其他命令：

```bash
## 刪除所有映像檔

$ docker rmi $(docker images -q)

## 刪除所有 redis 映像檔

$ docker rmi $(docker images -q redis)
```

#### 顯示完整 ID

```bash
$ docker images --no-trunc
```

#### 顯示摘要

```bash
$ docker images --digests
REPOSITORY   TAG     DIGEST                    IMAGE ID
nginx        latest  sha256:b4f0e0bdeb5...    e43d811ce2f4
```

#### 自訂格式

使用 Go 模板語法自訂輸出：

```bash
## 只顯示 ID 和倉庫名

$ docker images --format "{{.ID}}: {{.Repository}}"
5f515359c7f8: redis
05a60462f8ba: nginx
329ed837d508: ubuntu

## 表格形式（帶標題）

$ docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"
REPOSITORY   TAG       SIZE
redis        latest    183MB
nginx        latest    181MB
ubuntu       24.04     78MB
```

#### 可用模板欄位

| 欄位 | 說明 |
|------|------|
| `.ID` | 映像檔 ID |
| `.Repository` | 倉庫名 |
| `.Tag` | 標籤 |
| `.Digest` | 摘要 |
| `.CreatedSince` | 建立後經過的時間 |
| `.CreatedAt` | 建立時間 |
| `.Size` | 大小 |

---

### 常用命令組合

```bash
## 列出所有映像檔及其大小，按大小排序（需要系統 sort 命令）

$ docker images --format "{{.Size}}\t{{.Repository}}:{{.Tag}}" | sort -h

## 查找大於 500MB 的映像檔

$ docker images --format "{{.Size}}\t{{.Repository}}:{{.Tag}}" | grep -E "^[0-9]+(\.[0-9]+)?GB|^[5-9][0-9]{2}MB"

## 匯出映像檔列表

$ docker images --format "{{.Repository}}:{{.Tag}}" > images.txt
```
---

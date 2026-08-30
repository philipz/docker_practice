## ADD 更進階的複製檔案

### 何時使用 ADD？何時用 COPY？

在開始前，讓我們直言不諱：**在大多數情況下，你應該使用 COPY，而不是 ADD**。

`ADD` 在 `COPY` 基礎上增加了兩個額外功能。它不是 `COPY` 的通用替代品，但在少數場景中更合適：

1. 自動解壓 tar 壓縮檔（有時你想複製一個 .tar.gz 本身，而 ADD 會意外地解壓它）
2. 支援從 URL 下載公開遠端檔案，並可配合 `--checksum` 做校驗

**實務中的建議**：本地普通檔案預設用 COPY；本地 tar 自動解壓或公開遠端 artifact 下載並校驗時用 ADD；需要認證、請求標頭、重試或自訂解壓流程時用 `RUN curl/wget`。

### 基本語法

```docker
ADD [選項] <來源路徑>... <目標路徑>
ADD [選項] ["<來源路徑>", ... "<目標路徑>"]
```
`ADD` 在 `COPY` 基礎上增加了兩個功能：

1. 自動解壓 tar 壓縮檔
2. 支援從 URL 下載檔案

---

### ADD vs COPY 詳細對比

| 特性 | COPY | ADD |
|------|------|-----|
| 複製本地檔案 | ✅ | ✅ |
| 自動解壓 tar | ❌ | ✅ |
| 支援 URL | ❌ | ✅（公開 artifact 可配合校驗使用）|
| 行為可預測性 | ✅ 高 | ⚠️ 低 |
| 推薦程度 | ✅ **普通複製優先使用** | 解壓、本地 Git/公開遠端 artifact |

> **筆者建議**：普通複製始終優先 COPY；只有當你明確需要 ADD 的額外語義時再使用 ADD，並把意圖寫清楚。

---

### 自動解壓功能

#### 基本用法：自動解壓本地 tar

```docker
## 自動解壓 tar.gz 到目標目錄

ADD app.tar.gz /app/
```
ADD 會識別並解壓以下格式：

- `.tar`
- `.tar.gz` / `.tgz`
- `.tar.bz2` / `.tbz2`
- `.tar.xz` / `.txz`

#### 實際應用

官方基底映像檔通常使用 ADD 解壓根檔案系統：

```docker
FROM scratch
ADD ubuntu-noble-core-cloudimg-amd64-root.tar.gz /
```

#### 解壓過程

```bash
ADD app.tar.gz /app/
        │
        ├─ 識別 .tar.gz 格式
        ├─ 自動解壓
        └─ 內容放入 /app/

app.tar.gz 包含：        /app/ 目錄結果：
├── src/                 ├── src/
│   └── main.py          │   └── main.py
└── config.json          └── config.json
```
---

### URL 下載功能：謹慎使用

#### 基本用法

```docker
## 從 URL 下載檔案

ADD https://example.com/app.zip /app/app.zip
```

#### 使用邊界

| 場景 | 建議 |
|------|------|
| 公開、版本固定的遠端 artifact | 使用 `ADD --checksum=sha256:... URL dest` |
| 需要認證、請求標頭或複雜重試 | 使用 `RUN curl/wget` |
| 下載後需要複雜解壓、校驗或清理 | 使用 `RUN curl/wget`，把流程顯式寫出 |
| URL 內容可變但無校驗 | 不建議直接寫入 Dockerfile |

#### 推薦寫法

```docker
## ✅ 公開 artifact：使用 ADD 並固定校驗值

ADD --checksum=sha256:<digest> https://example.com/app.tar.gz /tmp/app.tar.gz
RUN tar -xzf /tmp/app.tar.gz -C /app && rm /tmp/app.tar.gz

## ✅ 需要認證、請求標頭或特殊處理：使用 RUN + curl

RUN curl -fsSL https://example.com/app.tar.gz | tar -xz -C /app
```
`ADD --checksum` 的優勢是快取更精確，並且校驗值直接綁定到 Dockerfile。`RUN curl/wget` 的優勢是控制力更強，適合企業內網、認證下載或複雜處理。


---

### 修改檔案擁有者

```docker
ADD --chown=node:node app.tar.gz /app/
ADD --chown=1000:1000 files/ /app/
```
---

### 何時使用 ADD

#### ✅ 適合使用 ADD

```docker
## 解壓本地 tar 檔案

FROM scratch
ADD rootfs.tar.gz /

## 解壓應用套件

ADD dist.tar.gz /app/

## 下載公開 artifact 並校驗

ADD --checksum=sha256:<digest> https://example.com/app.tar.gz /tmp/app.tar.gz
```

#### ❌ 不適合使用 ADD

```docker
## 複製普通檔案（用 COPY）

ADD package.json /app/          # ❌
COPY package.json /app/         # ✅

## 需要認證或複雜下載邏輯（用 RUN + curl/wget）

ADD https://example.com/file /  # ❌ 無法傳認證資訊，也沒有顯式處理
RUN curl -fsSL ... -o /file     # ✅

## 需要保留 tar 不解壓（用 COPY）

ADD archive.tar.gz /archives/   # ❌ 會解壓
COPY archive.tar.gz /archives/  # ✅ 保持原樣
```
---

### 快取行為

ADD 可能導致建立快取失效：

```docker
## 如果 app.tar.gz 內容變化，此層及後續層都需重建

ADD app.tar.gz /app/
RUN npm install
```
**最佳化建議**：

```docker
## 先複製相依檔案

COPY package*.json /app/
RUN npm install

## 再新增應用程式碼

ADD app.tar.gz /app/
```
---

### 最佳實務

#### 1. 預設使用 COPY

```docker
## ✅ 大多數場景使用 COPY

COPY . /app/
```

#### 2. 僅在需要解壓時使用 ADD

```docker
## ✅ 自動解壓場景

ADD app.tar.gz /app/
```

#### 3. 遠端 artifact 使用 ADD 時必須固定校驗值

```docker
## ✅ 公開 artifact

ADD --checksum=sha256:<digest> https://example.com/file.tar.gz /tmp/file.tar.gz

## ✅ 認證下載或複雜處理

RUN curl -fsSL https://example.com/file.tar.gz | tar -xz -C /app
```

#### 4. 解壓後清理

```docker
## 如果需要控制解壓過程

COPY app.tar.gz /tmp/
RUN tar -xzf /tmp/app.tar.gz -C /app && \
    rm /tmp/app.tar.gz
```
---

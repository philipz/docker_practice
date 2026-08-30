## COPY 複製檔案

### 何時使用 COPY

`COPY` 是在建立映像檔時，將建立上下文（Dockerfile 所在目錄及其子目錄）中的檔案或目錄複製到容器內的指令。它是處理應用程式碼、設定檔案最常用的方式。

典型場景：

- 複製應用程式原始碼：`COPY . /app`
- 複製設定檔案：`COPY nginx.conf /etc/nginx/nginx.conf`
- 複製靜態資源：`COPY public /app/public`

**為什麼 COPY 比 ADD 更值得推薦？** 筆者建議在 90% 的情況下使用 COPY。原因是 COPY 的語義更清晰——它就是簡單地複製檔案。而 ADD 有額外的功能（自動解壓、支援 URL），這些功能往往會帶來意外的行為。除非你明確需要 ADD 的自動解壓功能，否則用 COPY。詳見 [ADD 指令](add.md) 中的詳細對比。

### 基本語法

```docker
COPY [選項] <來源路徑>... <目標路徑>
COPY [選項] ["<來源路徑1>", "<來源路徑2>", ... "<目標路徑>"]
```
`COPY` 指令將建立上下文中的檔案或目錄複製到映像檔內。

---

### 基本用法

#### 複製單一檔案

```docker
## 複製檔案到指定目錄

COPY package.json /app/

## 複製檔案並重新命名

COPY config.json /app/settings.json
```

#### 複製多個檔案

```docker
## 複製多個指定檔案

COPY package.json package-lock.json /app/

## 使用萬用字元

COPY *.json /app/
COPY src/*.js /app/src/
```

#### 複製目錄

```docker
## 複製整個目錄的內容（不是目錄本身）

COPY src/ /app/src/
```
> ⚠️ **注意**：複製目錄時，複製的是目錄的 **內容**，不包含目錄本身。

```bash
建立上下文：                映像檔內：
src/                     /app/src/
├── index.js      →      ├── index.js
└── utils.js             └── utils.js
```
---

### 萬用字元規則

COPY 支援 Go 的 `filepath.Match` 萬用字元規則：

| 萬用字元 | 說明 | 範例 |
|--------|------|------|
| `*` | 匹配任意字元序列 | `*.json` |
| `?` | 匹配單一字元 | `config?.json` |
| `[abc]` | 匹配括號內任一字元 | `[abc].txt` |
| `[a-z]` | 匹配範圍內字元 | `file[0-9].txt` |

```docker
COPY hom* /mydir/       # home.txt, homework.md 等
COPY hom?.txt /mydir/   # home.txt, homy.txt 等
COPY app[0-9].js /app/  # app0.js ~ app9.js
```
---

### 目標路徑

#### 絕對路徑

```docker
COPY app.js /usr/src/app/
```

#### 相對路徑：基於 WORKDIR

```docker
WORKDIR /app
COPY package.json ./        # 複製到 /app/package.json
COPY src/ ./src/            # 複製到 /app/src/
```

#### 自動建立目錄

如果目標目錄不存在，Docker 會自動建立：

```docker
## /app/config/ 不存在也會自動建立

COPY settings.json /app/config/
```
---

### 修改檔案擁有者

使用 `--chown` 選項設定檔案的使用者和群組：

```docker
## 使用使用者名稱和群組名

COPY --chown=node:node package.json /app/

## 使用 UID 和 GID

COPY --chown=1000:1000 . /app/

## 只指定使用者

COPY --chown=node . /app/
```
> 💡 結合 `USER` 指令使用，確保應用程式以非 root 使用者執行。

---

### 保留檔案中繼資料

COPY 會保留來源檔案的中繼資料：

- 讀、寫、執行權限
- 修改時間

這對於腳本檔案特別重要：

```docker
## start.sh 的可執行權限會被保留

COPY start.sh /app/
```
---

### COPY vs ADD

| 特性 | COPY | ADD |
|------|------|-----|
| 複製本地檔案 | ✅ | ✅ |
| 自動解壓 tar | ❌ | ✅ |
| 支援 URL | ❌ | ✅（不推薦）|
| 推薦程度 | ✅ **推薦** | ⚠️ 特殊場景使用 |

```docker
## 推薦：使用 COPY

COPY app.tar.gz /app/
RUN tar -xzf /app/app.tar.gz

## ADD 會自動解壓（行為不明顯，不推薦）

ADD app.tar.gz /app/
```
> 筆者建議：除非需要自動解壓 tar 檔案，否則始終使用 COPY。明確的行為比隱式的魔法更好。

---

### 多階段建立中的 COPY

#### 從其他建立階段複製

```docker
## 建立階段

FROM node:22 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

## 生產階段

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
```

#### 使用 --link 最佳化快取

```docker
## 使用 --link 後，檔案以獨立層新增，不依賴前序指令

COPY --link --from=builder /app/dist /usr/share/nginx/html
```
`--link` 的優勢：

- 更高效利用建立快取
- 平行化建立過程
- 加速多階段建立

> ⚠️ **注意**：使用 `--link` 需要滿足以下條件：
> - 啟用 BuildKit（Docker Engine 23.0+ 預設啟用）
> - Dockerfile 語法版本 1.4 或更高（在首行宣告 `# syntax=docker/dockerfile:1`）
> - 目標路徑在前序指令中應不存在或為空目錄

---

### dockerignore

使用 `.dockerignore` 排除不需要複製的檔案：

```text
## .dockerignore

node_modules
.git
.env
*.log
Dockerfile
.dockerignore
```
這可以：

- 減小建立上下文大小
- 加速建立
- 避免複製敏感檔案

---

### 最佳實務

#### 1. 利用快取，先複製相依檔案

```docker
## ✅ 好：先複製相依定義，再安裝，最後複製程式碼

COPY package.json package-lock.json ./
RUN npm install
COPY . .

## ❌ 差：一次性複製所有檔案，程式碼變更會導致重新 npm install

COPY . .
RUN npm install
```

#### 2. 使用 .dockerignore

```docker
## 確保 node_modules 不被複製

COPY . .

## .dockerignore 中應包含 node_modules

...
```

#### 3. 明確複製路徑

```docker
## ✅ 好：明確的路徑

COPY src/ /app/src/
COPY package.json /app/

## ❌ 差：過於寬泛

COPY . .
```
---

> **🔥 踩坑實錄**
>
> 某公司在最佳化 Node.js 應用的 Docker 映像檔時，發現建立出來的映像檔體積超過了 2GB，遠遠超過生產部署的需求。排查發現，Dockerfile 中使用了 `COPY . .` 把整個建立上下文複製進映像檔，導致 `node_modules/`、`.git/` 目錄和大量測試資料全部被打包進映像檔。最初他們沒有建立 `.dockerignore` 檔案，預設會複製所有檔案。解決方案是新增一個 `.dockerignore` 檔案，排除這些不必要的目錄，使映像檔縮小到了 200MB。這個教訓深刻地說明了：`.dockerignore` 和 `.gitignore` 一樣重要，應該在專案初始化時就建立，而不是等到出現問題時才想起來。建議的標準做法是先複製 `package.json` 和 `package-lock.json` 安裝相依，再複製應用程式碼，同時在 `.dockerignore` 中明確列出 `node_modules`、`.git`、test 目錄等。

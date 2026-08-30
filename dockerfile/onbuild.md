## ONBUILD 為他人作嫁衣裳

### 基本語法

```docker
ONBUILD <其他指令>
```
`ONBUILD` 是一個特殊的指令，它後面跟的是其他指令（如 `RUN`，`COPY` 等），這些指令 **在目前映像檔建立時不會執行**，只有當以目前映像檔為基礎映像檔去建立下一級映像檔時才會被執行。

---

### 為什麼需要 ONBUILD

`ONBUILD` 主要用於製作 **語言棧基礎映像檔** 或 **框架基礎映像檔**。

#### 場景：維護 Node.js 專案

假設你有多個 Node.js 專案，它們的建立流程都一樣：

1. 建立目錄
2. 複製 `package.json`
3. 執行 `npm install`
4. 複製源碼
5. 啟動應用

如果不使用 `ONBUILD`，每個專案的 Dockerfile 都要重複這些步驟，且透過 `COPY` 複製檔案時，基礎映像檔無法預知子專案的檔案名。

#### 使用 ONBUILD 的解決方案

**基礎映像檔 (my-node-base)**：

```docker
FROM node:22-alpine
WORKDIR /app

## 這些指令將在子映像檔建立時執行

ONBUILD COPY package*.json ./
ONBUILD RUN npm install
ONBUILD COPY . .

CMD ["npm", "start"]
```
**子專案 Dockerfile**：

```docker
FROM my-node-base

## 只需要一行！

## 建立時會自動執行 COPY 和 RUN

...
```
---

### 執行機制

```bash
基礎映像檔建立：
Dockerfile (含 ONBUILD) ──build──> 基礎映像檔 (記錄了 ONBUILD 觸發器)
                                    (指令未執行)

子映像檔建立：
FROM 基礎映像檔 ──build──> 讀取基礎映像檔觸發器 ──> 執行觸發器指令 ──> 繼續執行子 Dockerfile
```
---

### 常見使用場景

#### 1. 自動處理依賴安裝

```docker
## Python 基礎映像檔

ONBUILD COPY requirements.txt ./
ONBUILD RUN pip install -r requirements.txt
```

#### 2. 自動編譯程式碼

```docker
## Go 基礎映像檔

ONBUILD COPY . .
ONBUILD RUN go build -o app main.go
```

#### 3. 處理靜態資源

```docker
## Nginx 靜態網站基礎映像檔

ONBUILD COPY dist/ /usr/share/nginx/html/
```
---

### 注意事項

#### 1. 繼承性限制

`ONBUILD` 指令 **只會繼承一次**。

- 映像檔 A（含 ONBUILD）
- 映像檔 B (FROM A) -> 觸發 ONBUILD
- 映像檔 C (FROM B) -> **不會** 再次觸發 ONBUILD

#### 2. 建立上下文

子映像檔建立時，`ONBUILD COPY . .` 中的 `.` 指的是 **子專案** 的建立上下文，而不是基礎映像檔的上下文。

#### 3. 不允許級聯

`ONBUILD ONBUILD` 是非法的。你不能寫 `ONBUILD ONBUILD COPY ...`。

#### 4. 可能會導致建立失敗

由於 `ONBUILD` 實際上是在子映像檔中執行指令，如果子專案的上下文不滿足要求（例如缺少 `package.json`），會導致子映像檔建立失敗，且錯誤資訊可能比較隱晦。

---

### 最佳實踐

#### 1. 命名規範

建議在映像檔標籤中加入 `-onbuild` 後綴，明確告知使用者該映像檔包含觸發器。

```bash
node:22-onbuild
python:3.12-onbuild
```

#### 2. 避免執行耗時操作

盡量不要在 `ONBUILD` 中執行過於耗時或不確定的操作（如更新系統軟體），這會讓子映像檔建立變得緩慢且不可控。

#### 3. 清理工作

如果 `ONBUILD` 指令產生了臨時檔案，最好在同一個指令鏈中清理，或者提供機制讓子映像檔清理。

---

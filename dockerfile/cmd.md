## CMD 容器啟動命令

### 何時使用 CMD，何時使用 ENTRYPOINT？

在深入 CMD 的細節之前，我們需要理解一個關鍵問題：**CMD 和 ENTRYPOINT 應該在什麼時候使用？**

這是 Dockerfile 使用中最常見的困惑之一。簡單的答案是：

- **CMD**：定義容器的「預設命令」。如果使用者在 `docker run` 時提供命令，CMD 會被覆蓋
- **ENTRYPOINT**：定義容器的「入口腳本」。通常用於啟動應用的某個特定部分

**決策樹**：

1. **你的容器是否有不可變的啟動邏輯？** 比如需要先做一些初始化工作，然後才執行應用 → 使用 ENTRYPOINT
2. **使用者經常會在 `docker run` 時傳入不同的命令嗎？** → 使用 CMD（讓使用者靈活覆蓋）
3. **大多數情況下，你希望容器始終以相同的方式啟動？** → 使用 ENTRYPOINT

更多細節見 [ENTRYPOINT 指令](entrypoint.md)。

### 什麼是 CMD

`CMD` 指令用於指定容器啟動時預設執行的命令。它定義了容器的「主程式」。

> **核心概念**：容器的生命週期 = 主程式的生命週期。CMD 指定的命令就是這個主程式。

---

### 語法格式

CMD 有三種格式：

| 格式 | 語法 | 推薦程度 |
|------|------|---------|
| **exec 格式**| `CMD ["可執行檔案", "參數1", "參數2"]` | ✅**推薦** |
| **shell 格式** | `CMD 命令 參數1 參數2` | ⚠️ 簡單場景 |
| **參數格式** | `CMD ["參數1", "參數2"]` | 配合 ENTRYPOINT |

#### exec 格式：推薦

```docker
CMD ["nginx", "-g", "daemon off;"]
CMD ["python", "app.py"]
CMD ["node", "server.js"]
```
**優點**：

- 直接執行指定程式，是容器的 PID 1
- 正確接收訊號（如 SIGTERM）
- 無需 shell 解析

#### shell 格式

```docker
CMD echo "Hello World"
CMD nginx -g "daemon off;"
```
**實際執行**：會被包裝為 `sh -c`

```docker
## 你寫的

CMD echo $HOME

## 實際執行的

CMD ["sh", "-c", "echo $HOME"]
```
**優點**：可以使用 `$HOME` 這類 shell 變數展開、管線等 shell 特性

**缺點**：主程式是 sh，訊號無法正確傳遞給應用

---

### exec 格式 vs shell 格式

| 特性 | exec 格式 | shell 格式 |
|------|----------|-----------|
| 主程式 | 指定的程式 | `/bin/sh` |
| 訊號傳遞 | ✅ 正確 | ❌ 無法傳遞 |
| `$VAR` shell 展開 | ❌ 不自動展開；環境變數仍會傳入程式 | ✅ 自動展開 |
| 推薦使用 | ✅ 大多數場景 | 需要 shell 特性時 |

#### 訊號傳遞問題範例

```docker
## ❌ shell 格式：docker stop 會逾時

CMD node server.js

## 實際是 sh -c "node server.js"

## SIGTERM 發給 sh，不會傳遞給 node

## ✅ exec 格式：docker stop 正常工作

CMD ["node", "server.js"]

## SIGTERM 直接發給 node

...
```
---

### 執行時覆蓋 CMD

`docker run` 後的命令會覆蓋 Dockerfile 中的 CMD：

```bash
## ubuntu 預設 CMD 是 /bin/bash

$ docker run -it ubuntu        # 進入 bash
$ docker run ubuntu cat /etc/os-release  # 覆蓋為 cat 命令
```
```bash
Dockerfile:              docker run 命令:
CMD ["/bin/bash"]   +    cat /etc/os-release
        │                        │
        └───────► 被覆蓋 ◄───────┘
                    ↓
           執行: cat /etc/os-release
```
---

### 經典錯誤：容器立即退出

#### 錯誤範例

```docker
## ❌ 容器啟動後立即退出

CMD service nginx start
```

#### 原因分析

```bash
1. CMD service nginx start
   ↓ 被轉換為
2. CMD ["sh", "-c", "service nginx start"]
   ↓
3. sh 啟動，執行 service 命令
   ↓
4. service 命令將 nginx 放到背景
   ↓
5. service 命令結束，sh 退出
   ↓
6. 容器主程式（sh）退出 → 容器停止
```

#### 正確做法

```docker
## ✅ 讓 nginx 在前景執行

CMD ["nginx", "-g", "daemon off;"]
```
---

### CMD vs ENTRYPOINT

| 指令 | 用途 | 執行時行為 |
|------|------|-----------|
| **CMD**| 預設命令 | `docker run` 參數會 **覆蓋** 它 |
| **ENTRYPOINT**| 入口點 | `docker run` 參數會 **追加** 到它後面 |

#### 單獨使用 CMD

```docker
## Dockerfile

CMD ["curl", "-s", "http://example.com"]
```
```bash
$ docker run myimage              # 執行預設命令
$ docker run myimage curl -v ...  # 完全覆蓋
```

#### 搭配 ENTRYPOINT

```docker
## Dockerfile

ENTRYPOINT ["curl", "-s"]
CMD ["http://example.com"]
```
```bash
$ docker run myimage              # curl -s http://example.com
$ docker run myimage http://other.com  # curl -s http://other.com（參數覆蓋）
```
詳見 [ENTRYPOINT 入口點](entrypoint.md) 章節。

---

### 最佳實務

#### 1. 優先使用 exec 格式

```docker
## ✅ 推薦

CMD ["python", "app.py"]

## ⚠️ 僅在需要 shell 特性時使用

CMD ["sh", "-c", "echo $PATH && python app.py"]
```

#### 2. 確保應用程式在前景執行

```docker
## ✅ 前景執行

CMD ["nginx", "-g", "daemon off;"]
CMD ["apache2ctl", "-D", "FOREGROUND"]
CMD ["java", "-jar", "app.jar"]

## ❌ 不要使用背景服務命令

CMD service nginx start
CMD systemctl start nginx
```

#### 3. 使用雙引號

```docker
## ✅ 正確：雙引號

CMD ["node", "server.js"]

## ❌ 錯誤：單引號（JSON 不支援）

CMD ['node', 'server.js']
```

#### 4. 配合 ENTRYPOINT 使用

```docker
## 用於可設定參數的場景

ENTRYPOINT ["python", "app.py"]
CMD ["--port", "8080"]

## 執行時可以覆蓋埠號

$ docker run myapp --port 9000

...
```
---

### 常見問題

#### Q：CMD 可以寫多個嗎？

不可以。多個 CMD 只有最後一個生效：

```docker
CMD ["echo", "first"]
CMD ["echo", "second"]  # 只有這個生效
```

#### Q：如何在 CMD 中使用環境變數？

```docker
## 方法1：使用 shell 格式

CMD echo "Port is $PORT"

## 方法2：顯式使用 sh -c

CMD ["sh", "-c", "echo Port is $PORT"]
```

#### Q：為什麼我的容器不回應 Ctrl+C？

可能是使用了 shell 格式，訊號被 sh 吃掉了：

```docker
## ❌ 訊號無法傳遞

CMD python app.py

## ✅ 訊號正確傳遞

CMD ["python", "app.py"]
```
---

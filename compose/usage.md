## 使用

本節將透過一個具體的 Web 應用案例，介紹 Docker Compose 的基本概念和常用操作。

### 術語

首先介紹幾個術語。

* 服務 (`service`)：一個應用容器，實際上可以執行多個相同映像檔的實例。

* 專案 (`project`)：由一組相關聯的應用容器組成的一個完整業務單元。

可見，一個專案可以由多個服務（容器）關聯而成，`Compose` 面向專案進行管理。

### 準備範例

下面建立一個由 `web` 和 `redis` 組成的簡單範例專案。

#### 應用程式碼

新建資料夾，在該目錄中編寫 `app.py` 檔案

```python
from flask import Flask
from redis import Redis

app = Flask(__name__)
redis = Redis(host='redis', port=6379)

@app.route('/')
def hello():
    count = redis.incr('hits')
    return 'Hello World! 該頁面已被存取 {} 次。\n'.format(count)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
```

#### Dockerfile

編寫 `Dockerfile` 檔案，內容為

```docker
FROM python:3.12-alpine
COPY . /code
WORKDIR /code
RUN pip install redis flask
CMD ["python", "app.py"]
```

#### compose.yaml

編寫 `compose.yaml` 檔案，這是 Compose 推薦使用的主模板檔案（也相容 `docker-compose.yml` 等歷史檔案名）。

```yaml
services:
  web:
    build: .
    ports:
      - "5000:5000"

  redis:
    image: "redis:alpine"
```

### 啟動與驗證

#### 啟動專案

```bash
$ docker compose up
```
此時存取本地 `5000` 埠號，每次重新整理頁面，計數就會加 1。

按下 `Ctrl-C` 停止專案。

#### 背景執行與停止

```bash
$ docker compose up -d
$ docker compose stop
```

#### 查看日誌

```bash
$ docker compose logs -f
```

#### 進入服務

```bash
$ docker compose exec redis sh
/data # redis-cli
127.0.0.1:6379> get hits
"9"
```

### 常用命令

#### 建立與重建

```bash
$ docker compose build
$ docker compose start
```

#### 執行一次性命令

```bash
$ docker compose run web python app.py
```

#### 驗證與清理

```bash
$ docker compose config
$ docker compose down
```

> 💡 `docker compose down` 預設會刪除容器和網路，但 **保留資料卷**。如需同時刪除資料卷，請使用 `docker compose down -v`。

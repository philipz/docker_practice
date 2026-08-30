## Node.js

### 基本資訊

[Node.js](https://en.wikipedia.org/wiki/Node.js) 是基於 JavaScript 的可擴充服務端和網路軟體開發平台。

該倉庫位於 `https://hub.docker.com/_/node/`。具體可用版本以 Docker Hub 上的 tags 列表為準。

### 使用方法

在專案中建立一個 Dockerfile。

```docker
FROM node:22

## replace this with your application's default port

EXPOSE 8888
```

然後建立映像檔，並啟動容器。

```bash
$ docker build -t my-nodejs-app .
$ docker run -it --rm --name my-running-app my-nodejs-app
```

也可以直接執行一個簡單容器。

```bash
$ docker run -it --rm \
    --name my-running-script \
    --mount type=bind,src="$(pwd)",target=/usr/src/myapp \
    -w /usr/src/myapp \
    node:22-alpine \
    node your-daemon-or-script.js
```

### Dockerfile

請到 [Node 官方映像檔文件目錄](https://github.com/docker-library/docs/tree/master/node) 查看。

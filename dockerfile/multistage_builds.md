## 多階段建立

在 Docker 17.05 版本之前，我們建立 Docker 映像檔時，通常會採用兩種方式：

### 全部放入一個 Dockerfile

一種方式是將所有的建立過程包含在一個 `Dockerfile` 中，包括專案及其依賴庫的編譯、測試、打包等流程，這裡可能會帶來的一些問題：

  * 映像檔層次多，映像檔體積較大，部署時間變長

  * 原始碼存在洩露的風險

例如，編寫 `app.go` 檔案，該程式輸出 `Hello World!`

```go
package main

import "fmt"

func main(){
    fmt.Printf("Hello World!");
}
```
編寫 `Dockerfile.one` 檔案

```docker
FROM golang:alpine

RUN apk --no-cache add git ca-certificates

WORKDIR /go/src/github.com/go/helloworld/

COPY app.go .

RUN go mod init helloworld \
  && go get github.com/go-sql-driver/mysql \
  && CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o app . \
  && cp /go/src/github.com/go/helloworld/app /root

WORKDIR /root/

CMD ["./app"]
```
建立映像檔

```bash
$ docker build -t go/helloworld:1 -f Dockerfile.one .
```

### 分散到多個 Dockerfile

另一種方式，就是我們事先在一個 `Dockerfile` 將專案及其依賴庫編譯測試打包好後，再將其拷貝到執行環境中，這種方式需要我們編寫兩個 `Dockerfile` 和一些編譯腳本才能將其兩個階段自動整合起來，這種方式雖然可以很好地規避第一種方式存在的風險，但明顯部署過程較複雜。

例如，編寫 `Dockerfile.build` 檔案

```docker
FROM golang:alpine

RUN apk --no-cache add git

WORKDIR /go/src/github.com/go/helloworld

COPY app.go .

RUN go mod init helloworld \
  && go get github.com/go-sql-driver/mysql \
  && CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o app .
```
編寫 `Dockerfile.copy` 檔案

```docker
FROM alpine:3

RUN apk --no-cache add ca-certificates

WORKDIR /root/

COPY app .

CMD ["./app"]
```
新建 `build.sh`

```bash
#!/bin/sh
echo Building go/helloworld:build

docker build -t go/helloworld:build . -f Dockerfile.build

docker create --name extract go/helloworld:build
docker cp extract:/go/src/github.com/go/helloworld/app ./app
docker rm -f extract

echo Building go/helloworld:2

docker build --no-cache -t go/helloworld:2 . -f Dockerfile.copy
rm ./app
```
現在執行腳本即可建立映像檔

```bash
$ chmod +x build.sh

$ ./build.sh
```
對比兩種方式產生的映像檔大小

```bash
$ docker image ls

REPOSITORY      TAG    IMAGE ID        CREATED         SIZE
go/helloworld   2      f7cf3465432c    22 seconds ago  6.47MB
go/helloworld   1      f55d3e16affc    2 minutes ago   295MB
```

### 使用多階段建立

為解決以上問題，Docker v17.05 開始支援多階段建立 (`multistage builds`)。使用多階段建立我們就可以很容易解決前面提到的問題，並且只需要編寫一個 `Dockerfile`：

例如，編寫 `Dockerfile` 檔案

```docker
FROM golang:alpine as builder

RUN apk --no-cache add git

WORKDIR /go/src/github.com/go/helloworld/

RUN go mod init helloworld \
  && go get github.com/go-sql-driver/mysql

COPY app.go .

RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o app .

FROM alpine:3 as prod

RUN apk --no-cache add ca-certificates

WORKDIR /root/

COPY --from=builder /go/src/github.com/go/helloworld/app .

CMD ["./app"]
```
建立映像檔

```bash
$ docker build -t go/helloworld:3 .
```
對比三個映像檔大小

```bash
$ docker image ls

REPOSITORY        TAG   IMAGE ID         CREATED            SIZE
go/helloworld     3     d6911ed9c846     7 seconds ago      6.47MB
go/helloworld     2     f7cf3465432c     22 seconds ago     6.47MB
go/helloworld     1     f55d3e16affc     2 minutes ago      295MB
```
很明顯使用多階段建立的映像檔體積小，同時也完美解決了上邊提到的問題。

> **Go Modules 最佳實踐**：上述範例為簡化演示在 Dockerfile 中臨時執行 `go mod init`。在實際專案中，通常已在程式碼倉庫中維護好 `go.mod` 和 `go.sum` 檔案。推薦的 Dockerfile 寫法是先拷貝這兩個檔案並執行 `go mod download` 以利用 Docker 層快取，再拷貝原始碼並建立：
>
> ```docker
> COPY go.mod go.sum ./
> RUN go mod download
> COPY . .
> RUN go build -o app .
> ```

### 只建立某一階段的映像檔

我們可以使用 `as` 來為某一階段命名，例如

```docker
FROM golang:alpine as builder
```
例如當我們只想建立 `builder` 階段的映像檔時，增加 `--target=builder` 參數即可

```bash
$ docker build --target builder -t username/imagename:tag .
```

### 建立時從其他映像檔複製檔案

上面例子中我們使用 `COPY --from=builder /go/src/github.com/go/helloworld/app .` 透過已命名階段（`as builder`）從上一階段的映像檔中複製檔案（命名引用比 `--from=0` 這種位置索引更易讀，也是目前官方推薦的最佳實踐）；我們也可以複製任意映像檔中的檔案。

```docker
COPY --from=nginx:1.28-alpine /etc/nginx/nginx.conf /nginx.conf
```

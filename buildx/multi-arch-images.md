## 使用 buildx 構建多種系統架構支援的 Docker 映像檔

Docker 映像檔可以支援多種系統架構，這意味著你可以在 `x86_64`、`arm64` 等不同架構的機器上執行同一個映像檔。這是透過一個名為 “manifest list”（或稱為 “fat manifest”）的檔案來實作的。

### Manifest List 是什麼？

為了理解多架構映像檔的原理，我們需要先了解 Manifest List 的概念。

Manifest list 是一個包含了多個指向不同架構映像檔的 manifest 的檔案。當你拉取一個支援多架構的映像檔時，Docker 會自動根據你目前的系統架構選擇並拉取對應的映像檔。

例如，官方的 `hello-world` 映像檔就支援多種架構。你可以使用 `docker manifest inspect` 命令來查看它的 manifest list：

```bash
$ docker manifest inspect hello-world
{
   "schemaVersion": 2,
   "mediaType": "application/vnd.docker.distribution.manifest.list.v2+json",
   "manifests": [
      {
         "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
         "size": 525,
         "digest": "sha256:80852a401a974d9e923719a948cc5335a0a4435be8778b475844a7153a2382e5",
         "platform": {
            "architecture": "amd64",
            "os": "linux"
         }
      },
      {
         "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
         "size": 525,
         "digest": "sha256:3adea81344be1724b383d501736c3852939b33b3903d02474373700b25e5d6e3",
         "platform": {
            "architecture": "arm",
            "os": "linux",
            "variant": "v5"
         }
      },
      // ... more architectures
   ]
}
```

### 使用 `docker buildx` 構建多架構映像檔

`docker buildx` 是構建多架構映像檔的最佳實務工具，它遮罩了底層的複雜性，提供了一鍵構建多架構映像檔的能力。

在 Docker 19.03+ 版本中，`docker buildx` 是建議的用於構建多架構映像檔的工具。它使用 `BuildKit` 作為後端，可以大大簡化構建過程（Docker 23+ 預設啟用 BuildKit）。

#### 新建 `builder` 執行個體

首先，你需要建立一個新的 `builder` 執行個體，因為它支援同時為多個平台構建。

```bash
$ docker buildx create --name mybuilder --use
$ docker buildx inspect --bootstrap
```

#### 構建和推送

使用 `docker buildx build` 命令並指定 `--platform` 參數，可以同時構建支援多種架構的映像檔。`--push` 參數會將構建好的映像檔和 manifest list 推送到 Docker 倉庫。

```dockerfile
## Dockerfile

FROM --platform=$TARGETPLATFORM alpine

RUN uname -a > /os.txt

CMD cat /os.txt
```
```bash
$ docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v7 -t your-username/multi-arch-image . --push
```
構建完成後，你就可以在不同架構的機器上拉取並執行 `your-username/multi-arch-image` 這個映像檔了。

#### 架構相關的構建參數

在 `Dockerfile` 中，你可以使用一些預定義的構建參數來根據目標平台客製構建過程：

*   `TARGETPLATFORM`：構建映像檔的目標平台，例如 `linux/amd64`。
*   `TARGETOS`：目標平台的作業系統，例如 `linux`。
*   `TARGETARCH`：目標平台的架構，例如 `amd64`。
*   `TARGETVARIANT`：目標平台的變種，例如 `v7`。
*   `BUILDPLATFORM`：構建環境的平台。
*   `BUILDOS`：構建環境的作業系統。
*   `BUILDARCH`：構建環境的架構。
*   `BUILDVARIANT`：構建環境的變種。

例如，你可以這樣編寫 `Dockerfile` 來複製特定架構的二進位檔案：

```dockerfile
FROM scratch

ARG TARGETOS
ARG TARGETARCH

COPY bin/dist-${TARGETOS}-${TARGETARCH} /dist

ENTRYPOINT ["/dist"]
```

### 使用 `docker manifest`：底層工具

除了 `docker buildx`，我們也可以直接操作 Manifest List 來手動組合不同架構的映像檔。

`docker manifest` 是一個更底層的命令，可以用來建立、檢查和推送 manifest list。雖然 `docker buildx` 在大多數情況下更方便，但了解 `docker manifest` 仍然有助於理解其工作原理。

#### 建立 manifest list

```bash
## 首先，為每個架構構建並推送映像檔

$ docker buildx build --platform linux/amd64 -t your-username/my-app:amd64 . --push
$ docker buildx build --platform linux/arm64 -t your-username/my-app:arm64 . --push

## 然後，建立一個 manifest list，將它們組合在一起

$ docker manifest create your-username/my-app:latest \
    --amend your-username/my-app:amd64 \
    --amend your-username/my-app:arm64

## 最後，推送 manifest list

$ docker manifest push your-username/my-app:latest
```

#### 檢查 manifest list

你可以使用 `docker manifest inspect` 來查看一個 manifest list 的詳細資訊，如上文所示。

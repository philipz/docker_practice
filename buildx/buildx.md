## 使用 buildx 建立映像檔

### 使用

Buildx 的使用非常直觀，絕大多數情況下可以替代 `docker build` 命令。

你可以直接使用 `docker buildx build` 命令建立映像檔。

```bash
$ docker buildx build .
[+] Building 8.4s (23/32)
 => ...
```
Buildx 使用 [BuildKit 引擎](buildkit.md)進行建立，支援許多新的功能，具體參考 [Buildkit](buildkit.md) 一節。

需要注意的是，預設 `docker` driver 會把建立結果載入到本地映像檔儲存；使用 `docker-container`、remote、cloud 等 builder 時，如未指定 `--load`、`--push` 或 `--output`，結果通常只保留在建立快取中。

#### 建立前檢查

Buildx 0.15 起支援建立檢查：常規建立會預設檢查 Dockerfile 與建立參數；如果只想做檢查而不真正建立，可以使用 `--check`：

```bash
$ docker buildx build --check .
```
這適合作為 CI 的快速門禁：普通建立中的檢查告警預設不會讓建立失敗，但 `--check` 發現問題會以非零狀態退出；需要把告警提升為錯誤時，可在 Dockerfile 頂部配合 `# check=error=true`。

#### 使用 `bake`

`docker buildx bake` 是一個高階建立命令，支援從 HCL、JSON 或 Compose 檔案中定義建立目標，實作複雜的流水線建立。

```bash
## 從 Compose 檔案建立所有服務

$ docker buildx bake

## 僅建立指定目標

$ docker buildx bake web
```

#### 產生 SBOM

Buildx 支援在建立時直接產生 SBOM (Software Bill of Materials)，這對於軟體供應鏈安全至關重要。

```bash
$ docker buildx build --sbom=true -t myimage .
```
該命令會把 SBOM 作為建立 attestation 附加到建立結果中；BuildKit 預設使用 SPDX SBOM attestation。需要 CycloneDX 檔案時，可使用 Syft、Docker Scout 等工具另行產生或轉換。

> **⚠️ 注意與失敗模式**：
> 要使 SBOM（或其他 attestation 中繼資料）成功附加並可見，對底層的儲存格式有前置要求：預設的 classic image store 不支援 manifest list/index 這種存放 attestation 的結構。
>
> 如果只簡單執行上述命令，你可能會面臨 **「命令成功執行，但本地映像檔中看不到 SBOM」** 的體會落差。
>
> **正確的解決路徑有兩條**：
> 1. **推送到遠端倉庫**：使用 `docker buildx build --sbom=true --push -t myimage:tag` 時，SBOM 會正確儲存到遠端倉庫。遠端 OCI 相容的映像檔倉庫能夠完整儲存這些中繼資料。
> 2. **啟用 containerd image store**：在 Docker 守護程式中啟用 `containerd image store` 特性（Docker 29+，新安裝情境預設啟用，Docker Desktop 上也更容易直接使用），可以在本地查看和管理 SBOM 等 attestation 中繼資料。

### 官方文件

* [Docker buildx 命令文件](https://docs.docker.com/reference/cli/docker/buildx/)

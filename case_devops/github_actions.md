## GitHub Actions

GitHub [Actions](https://github.com/features/actions) 是 GitHub 推出的一款 CI/CD 工具。

我們可以在每個 `job` 的 `step` 中使用 Docker 執行建立步驟。

### 最小可用示例

更多語法、權限模型和可用 action，請以 [GitHub Actions 官方文件](https://docs.github.com/en/actions) 為準。

在倉庫根目錄建立 `.github/workflows/ci.yml`：

```yaml
name: CI

on:
  push:
  pull_request:

permissions:
  contents: read

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: docker/setup-buildx-action@v4
      - uses: docker/build-push-action@v7
        with:
          context: .
          push: false
          tags: local/test:ci
```
該示例會在 GitHub Actions 中建立目前倉庫的 Docker 映像檔（不推送到 registry）。

下面的完整圍欄與倉庫檔案由測試強制保持一致，並校驗下載工具的 SHA-256：

```yaml
name: Validate container examples

on:
  push:
    branches:
      - master
  pull_request:

permissions:
  contents: read

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0 # v7.0.0
        with:
          persist-credentials: false

      - name: Install pinned validators
        env:
          KUBECONFORM_VERSION: "0.8.0"
          KUBECONFORM_SHA256: "9bc2bffbf71f261128533edaf912153948b7ff238f9a531ae6d34466ec287883"
          ACTIONLINT_VERSION: "1.7.12"
          ACTIONLINT_SHA256: "8aca8db96f1b94770f1b0d72b6dddcb1ebb8123cb3712530b08cc387b349a3d8"
        run: |
          mkdir -p "$RUNNER_TEMP/bin"
          curl -fsSL --retry 3 \
            "https://github.com/yannh/kubeconform/releases/download/v${KUBECONFORM_VERSION}/kubeconform-linux-amd64.tar.gz" \
            -o "$RUNNER_TEMP/kubeconform.tar.gz"
          echo "${KUBECONFORM_SHA256}  $RUNNER_TEMP/kubeconform.tar.gz" | sha256sum -c -
          tar xzf "$RUNNER_TEMP/kubeconform.tar.gz" -C "$RUNNER_TEMP/bin" kubeconform

          curl -fsSL --retry 3 \
            "https://github.com/rhysd/actionlint/releases/download/v${ACTIONLINT_VERSION}/actionlint_${ACTIONLINT_VERSION}_linux_amd64.tar.gz" \
            -o "$RUNNER_TEMP/actionlint.tar.gz"
          echo "${ACTIONLINT_SHA256}  $RUNNER_TEMP/actionlint.tar.gz" | sha256sum -c -
          tar xzf "$RUNNER_TEMP/actionlint.tar.gz" -C "$RUNNER_TEMP/bin" actionlint
          echo "$RUNNER_TEMP/bin" >> "$GITHUB_PATH"

      - name: Validate canonical examples
        run: python3 tools/test_examples.py --require-tools

```

### 建立並推送到 Registry

實際專案中通常需要在 CI 中建立映像檔並推送到容器 Registry。以下示例展示了多階段建立 + 登入 + 推送的完整流程：

```yaml
name: Build and Push

on:
  push:
    branches: [main]

permissions:
  contents: read
  packages: write

jobs:
  build-push:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7

      - uses: docker/login-action@v4
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - uses: docker/setup-buildx-action@v4

      - uses: docker/build-push-action@v7
        with:
          context: .
          push: true
          tags: |
            ghcr.io/${{ github.repository }}:${{ github.sha }}
            ghcr.io/${{ github.repository }}:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max
          provenance: mode=max
          sbom: true
```

關鍵說明：

* `docker/login-action` 負責認證，支援 Docker Hub、GHCR、ECR 等主流 Registry。
* `cache-from` / `cache-to` 使用 GitHub Actions 原生快取（`type=gha`），無需額外設定即可加速增量建立。
* 標籤同時使用 commit hash 和 `latest`，兼顧版本追溯與部署便利。
* `provenance: mode=max` 和 `sbom: true` 會把建立來源證明和 SBOM 附加到推送的映像檔上；只做本地 `load: true` 的建立無法完整保留這些 attestation。

### 最佳實務

* 生產流水線要按完整 commit SHA 固定第三方 action；示例中使用 `@v4` / `@v6` 只是為了可讀性，仍屬於信任 tag 維護者的取捨，不能等同於不可變引用。
* 設定最小權限（例如 `contents: read`），需要寫入權限時再打開。
* 需要依賴快取時，優先使用官方支援的快取方案（例如針對語言包管理器的 cache 或 BuildKit cache）。
* 敏感憑證（Registry 密碼、Deploy Key 等）一律透過 `secrets` 注入，禁止硬編碼。
* 多平台建立可在 `build-push-action` 中新增 `platforms: linux/amd64,linux/arm64`。

如果你需要在某個步驟裡直接執行容器映像檔（而不是建立映像檔），可以使用 `docker://` 語法：

```yaml
- name: Run container step
  uses: docker://golang:alpine
  with:
    args: go version
```

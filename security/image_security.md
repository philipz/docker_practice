## 映像檔安全掃描與供應鏈安全

在 DevOps 流程中，容器映像檔安全已經成為不容忽視的關鍵環節。從開發、建立、儲存到部署，映像檔的整個生命週期都需要安全防護。本節深入討論映像檔漏洞掃描、軟體物料清單（SBOM）、映像檔簽名驗證等供應鏈安全實務。

### 容器映像檔漏洞掃描工具對比

#### Trivy - 輕量級通用掃描器

Trivy 是由 Aqua Security 開發的開源漏洞掃描器，以其輕量級、快速、準確而聞名，已成為業界標準。

**優點：**

- 零依賴，單個二進位檔案
- 掃描速度快（秒級）
- 支援映像檔、檔案系統、Git 倉庫多種掃描源
- 資料庫每日自動更新
- 支援多種輸出格式（JSON、表格、SBOM 等）

**安裝與基本使用：**

```bash
# 安裝 Trivy
curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh -o install-trivy.sh
less install-trivy.sh  # 先審閱腳本內容
sudo sh install-trivy.sh -b /usr/local/bin

# 掃描本地映像檔
trivy image nginx:latest

# 生成 JSON 格式報告
trivy image -f json -o report.json nginx:latest

# 掃描檔案系統
trivy fs /path/to/project

# 掃描 Git 倉庫
trivy repo https://github.com/aquasecurity/trivy
```
**在 CI/CD 中整合：**

```bash
# 設定嚴重程度過濾
trivy image --severity HIGH,CRITICAL \
  --exit-code 1 \
  myregistry.com/myapp:v1.0.0
```

#### Grype - 支援多種軟體包的掃描器

Grype 由 Anchore 開發，支援更廣泛的軟體包管理器和語言。

**優點：**

- 支援 Java、Python、Go、Ruby、JavaScript 等多種語言的依賴檢測
- 與 Syft（SBOM 生成器）配合效果好
- 可自訂漏洞資料庫源
- 支援離線掃描模式

**安裝與使用：**

```bash
# 安裝 Grype
curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh -o install-grype.sh
less install-grype.sh
sudo sh install-grype.sh -b /usr/local/bin

# 掃描映像檔
grype docker:nginx:latest

# 與 Syft 配合生成 SBOM
syft docker:nginx:latest -o json > sbom.json
grype sbom:sbom.json

# 掃描特定目錄
grype dir:/path/to/app
```

#### Snyk - 完整的安全平台

Snyk 提供了商業級的安全掃描服務，特別適合企業環境。

**特點：**

- 支援開源漏洞、許可證掃描和修復建議
- 與多個 Git 平台深度整合（GitHub、GitLab、Bitbucket）
- 提供修復建議和自動化修復 PR
- 支援 Kubernetes 部署後安全監控

**基本使用：**

```bash
# 安裝 Snyk CLI
npm install -g snyk

# 認證
snyk auth

# 掃描映像檔
snyk container test docker-archive://image.tar

# 監控倉庫
snyk monitor --docker
```
此外，Docker 官方提供的 **Docker Scout**（`docker scout` CLI）可以直接在 Docker Desktop 或命令行中對映像檔進行漏洞掃描和依賴分析，適合日常開發流程中快速檢查：

```bash
# 掃描本地映像檔
$ docker scout cves myapp:latest

# 查看映像檔的依賴和漏洞摘要
$ docker scout quickview myapp:latest
```

**工具對比表：**

| 特性 | Docker Scout | Trivy | Grype | Snyk |
|------|-------------|-------|-------|------|
| Docker 整合 | ✓（原生） | 需安裝 | 需安裝 | 需安裝 |
| 零依賴 | ✗ | ✓ | ✗ | ✗ |
| 離線模式 | ✗ | ✓ | ✓ | ✗ |
| 許可證掃描 | ✓ | ✓ | ✓ | ✓ |
| 自動修復建議 | ✓ | ✗ | ✗ | ✓ |
| 開源免費 | 部分 | ✓ | ✓ | 部分 |
| IDE 整合 | ✓ | ✓ | ✓ | ✓ |

### SBOM（軟體物料清單）生成與管理

SBOM（Software Bill of Materials）是一份詳細列表，記錄了軟體中使用的所有元件、依賴庫及其版本資訊。SBOM 在供應鏈安全中至關重要，特別是在發現新的安全漏洞時，能快速定位受影響的應用。

#### Syft - SBOM 生成工具

Syft 是 Anchore 推出的專業 SBOM 生成工具。

**安裝：**

```bash
curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh -o install-syft.sh
less install-syft.sh
sudo sh install-syft.sh -b /usr/local/bin
```
**生成 SBOM：**

```bash
# 從映像檔生成 SBOM（多種格式）
syft docker:nginx:latest -o json > sbom.json
syft docker:nginx:latest -o spdx > sbom.spdx
syft docker:nginx:latest -o cyclonedx > sbom.xml

# 從本地檔案系統生成
syft dir:/path/to/app -o json > sbom.json

# 從 OCI 映像檔檔案生成
syft oci-archive:image.tar -o json > sbom.json
```

#### CycloneDX 與 SPDX 格式

兩種主流的 SBOM 格式：

**CycloneDX 格式示例：**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<bom xmlns="http://cyclonedx.org/schema/bom/1.4" version="1">
  <components>
    <component type="library">
      <name>openssl</name>
      <version>1.1.1k</version>
      <purl>pkg:deb/debian/openssl@1.1.1k-1+deb11u5</purl>
    </component>
    <component type="library">
      <name>curl</name>
      <version>7.74.0-1.3+deb11u1</version>
      <purl>pkg:deb/debian/curl@7.74.0-1.3+deb11u1</purl>
    </component>
  </components>
</bom>
```
**SPDX 格式示例：**

```json
{
  "SPDXID": "SPDXRef-DOCUMENT",
  "spdxVersion": "SPDX-2.2",
  "creationInfo": {
    "created": "2024-03-01T12:00:00Z",
    "creators": ["Tool: syft"]
  },
  "packages": [
    {
      "SPDXID": "SPDXRef-Package-openssl",
      "name": "openssl",
      "versionInfo": "1.1.1k",
      "downloadLocation": "NOASSERTION"
    }
  ]
}
```

#### SBOM 的應用場景

**漏洞關聯：**

當新的 CVE 被發現時，可快速查詢受影響的應用：

```bash
# 使用 Grype 針對 SBOM 進行漏洞掃描
grype sbom:sbom.json --add-cpes-if-none
```
**合規性報告：**

將 SBOM 保存為建立產物，用於審計和合規性檢查。

**依賴升級決策：**

透過分析 SBOM 中的依賴版本，制定安全升級計畫。

### 映像檔簽名與驗證

映像檔簽名確保映像檔的來源可信且未被篡改。新專案通常優先評估 Cosign (Sigstore) 或 Notary Project 的 Notation；Docker Content Trust / Notary v1 屬於歷史路徑。

#### Cosign - 現代簽名解決方案

Cosign 是 Sigstore 專案的核心工具，支援無密鑰簽名，適合現代 CI/CD 流程。

**安裝：**

```bash
wget https://github.com/sigstore/cosign/releases/latest/download/cosign-linux-amd64
chmod +x cosign-linux-amd64
sudo mv cosign-linux-amd64 /usr/local/bin/cosign
```
**生成密鑰對（傳統方式）：**

```bash
cosign generate-key-pair

# 生成 cosign.key 和 cosign.pub
```
**簽名映像檔：**

```bash
# 先推送映像檔，再使用不可變 digest 簽名
IMAGE_DIGEST="myregistry.com/myapp@sha256:<digest>"
cosign sign --key cosign.key "$IMAGE_DIGEST"

# 系統會提示輸入私鑰密碼
```
**驗證簽名：**

```bash
# 使用公鑰驗證
cosign verify --key cosign.pub "$IMAGE_DIGEST"

# 輸出結果示例
# Verification successful!
# {
#   "critical": {
#     "identity": {...},
#     "image": {...},
#     "type": "cosign container image signature"
#   },
#   "optional": {...}
# }
```
**Keyless 簽名（推薦用於 CI/CD）：**

```bash
# 在 GitHub Actions 等 CI 中無需儲存密鑰
cosign sign --yes "$IMAGE_DIGEST"

# 驗證時檢查簽名證書中的 OIDC 身分宣告是否匹配預期 workflow 與 issuer
cosign verify "$IMAGE_DIGEST" \
  --certificate-identity https://github.com/myorg/myrepo/.github/workflows/build.yml@refs/heads/main \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com
```

#### Notary Project / Notation

Notation 是 Notary Project 的 OCI 簽名工具，適合希望採用 CNCF Notary Project 規範、或使用 registry/雲廠商原生整合的團隊。與 Cosign 類似，生產環境應圍繞不可變 digest 做簽名和策略校驗。

```bash
# 簽名已推送的映像檔 digest
notation sign myregistry.com/myapp@sha256:<digest>

# 驗證簽名
notation verify myregistry.com/myapp@sha256:<digest>
```

#### Docker Content Trust 與 Notary v1

> **注意：DCT 退役時間線**
>
> Docker 已宣布[退役 Content Trust](https://www.docker.com/blog/retiring-docker-content-trust/)，Docker Official Images 的部分 DCT 簽名證書自 2025 年 8 月起已陸續過期；根據 [Docker 官方退役說明](https://docs.docker.com/retired/)，Notary v1 服務 `notary.docker.io` 在 2026 年 7 月、8 月安排若干次 brownout（短時停服演練）之後，於 2026 年 12 月 8 日完全關閉。registry 服務商的具體節奏以其自身文件為準，不要把雲廠商特定日期直接當作 Docker 全域時間線。
>
> 新專案應優先使用上文介紹的 **Cosign (Sigstore)** 或 registry 原生簽名/證明能力；現有 DCT 使用者應先盤點依賴、驗證替代方案，再制定遷移計畫。

Docker Content Trust 使用 Notary v1 實作映像檔簽名，是 Docker 官方的傳統簽名解決方案，不建議新專案採用。**自 Docker Engine 29.0 起，Docker Content Trust 已從 Docker CLI 中移除**：`docker trust` 子命令不再內建（官方僅保留為可單獨建立的外掛程式），`DOCKER_CONTENT_TRUST` 環境變數不再生效，`docker push --disable-content-trust` 也僅作為已廢棄選項保留、不再有實際作用。下面的示例僅適用於 Docker Engine 28.x 及更早版本。

**歷史用法示例（不建議新專案採用）：**

```bash
# 在環境中啟用 DCT
export DOCKER_CONTENT_TRUST=1

# 此後所有 docker push/pull 都需要簽名
docker push myregistry.com/myapp:v1.0.0

# 如果映像檔未簽名，操作會被拒絕

# 禁用 DCT（僅用於特定操作）
docker push --disable-content-trust myregistry.com/myapp:v1.0.0
```
**簽名密鑰管理：**

```bash
# 首次推送時會提示建立 Delegation Key
# 密鑰儲存在 ~/.docker/trust/private/root_keys/ 和 ~/.docker/trust/private/tuf_keys/

# 查看 DCT/Notary 信任資料；RepoDigests 只是內容摘要，不等於簽名驗證
docker trust inspect --pretty myregistry.com/myapp:v1.0.0
```

### 供應鏈安全最佳實務

#### 1. 基礎映像檔安全

```dockerfile
# ❌ 不推薦：使用 latest 標籤
FROM ubuntu:latest
RUN apt-get update && apt-get install -y curl

# ✓ 推薦：固定基礎映像檔版本和摘要
FROM ubuntu:22.04@sha256:a6d2b38300ce017add71440577d5b0a90460d0e6e0e14...（完整 64 位元雜湊）
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*
```

#### 2. 建立時掃描

在 CI/CD 建立階段整合安全掃描，避免在 Dockerfile 裡從分支 URL 下載並執行遠端安裝腳本：

```bash
docker run --rm \
  -v "$PWD:/work" \
  -w /work \
  aquasec/trivy:latest \
  fs . --exit-code 1 --severity HIGH,CRITICAL
```

#### 3. 執行期映像檔掃描策略

```bash
# 映像檔建立完成後立即掃描
trivy image --severity HIGH,CRITICAL \
  --exit-code 1 \
  --timeout 30m \
  $IMAGE_NAME:$IMAGE_TAG

# 定期掃描已部署的映像檔
trivy image --scanners vuln,misconfig registry:5000/myapp:latest
```

#### 4. 映像檔倉庫安全設定

**Harbor（私有映像檔倉庫）的安全掃描：**

Harbor 的掃描器應在管理介面的 **Interrogation Services / Scanner** 中設定；推送自動掃描通常在專案級 **Configuration** 中啟用。不要把掃描策略誤寫成通用 `harbor.yml` 頂層欄位。實際部署時應按所用 Harbor 版本文檔設定 scanner、專案策略和漏洞阻斷閾值。

#### 5. 政策執行

在 Kubernetes 環境中使用 Admission Webhook 強制映像檔簽名和掃描：

```yaml
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingWebhookConfiguration
metadata:
  name: image-security-policy
webhooks:
- name: image-security.example.com
  clientConfig:
    service:
      name: image-security-webhook
      namespace: security
      path: "/validate"
  rules:
  - operations: ["CREATE", "UPDATE"]
    apiGroups: [""]
    apiVersions: ["v1"]
    resources: ["pods"]
  admissionReviewVersions: ["v1"]
  sideEffects: None
```

### CI/CD 中整合安全掃描

#### GitHub Actions 工作流示例

```yaml
name: Build and Scan Image

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build-scan:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
      security-events: write
      id-token: write

    steps:
    - name: Checkout code
      uses: actions/checkout@v7

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v4

    - name: Install Cosign
      if: github.event_name == 'push'
      # cosign-installer 沒有發布可移動的 v4 大版本標籤，只能引用完整版本號；
      # 安裝 Cosign v3+ 必須使用 v4 及以後的 installer，v3 系列只能安裝 Cosign 2.x。
      uses: sigstore/cosign-installer@v4.1.2

    - name: Login to Registry
      if: github.event_name == 'push'
      uses: docker/login-action@v4
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}

    - name: Build and push Docker image
      if: github.event_name == 'push'
      id: build-push
      uses: docker/build-push-action@v7
      with:
        context: .
        push: true
        tags: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
        provenance: mode=max
        sbom: true

    - name: Build Docker image for pull request scan
      if: github.event_name == 'pull_request'
      uses: docker/build-push-action@v7
      with:
        context: .
        push: false
        load: true
        tags: local/${{ env.IMAGE_NAME }}:pr

    - name: Run Trivy vulnerability scan
      # 安全提醒：2026 年 3 月 19 日 Trivy GitHub Actions 遭受供應鏈攻擊，
      # 76 個版本標籤被劫持。務必使用不可變的 commit SHA 引用，而非可變標籤。
      # 使用前請到 https://github.com/aquasecurity/trivy-action/releases 核實 SHA 對應正確版本。
      uses: aquasecurity/trivy-action@57a97c7e7821a5776cebc9bb87c984fa69cba8f1 # v0.35.0
      with:
        image-ref: ${{ github.event_name == 'push' && format('{0}/{1}@{2}', env.REGISTRY, env.IMAGE_NAME, steps.build-push.outputs.digest) || format('local/{0}:pr', env.IMAGE_NAME) }}
        format: 'sarif'
        output: 'trivy-results.sarif'
        severity: 'HIGH,CRITICAL'

    - name: Upload Trivy results to GitHub Security tab
      uses: github/codeql-action/upload-sarif@v3
      with:
        sarif_file: 'trivy-results.sarif'

    - name: Generate SBOM
      uses: anchore/sbom-action@v0
      with:
        image: ${{ github.event_name == 'push' && format('{0}/{1}@{2}', env.REGISTRY, env.IMAGE_NAME, steps.build-push.outputs.digest) || format('local/{0}:pr', env.IMAGE_NAME) }}
        format: cyclonedx-json
        output-file: sbom-cyclonedx.json

    - name: Upload SBOM
      uses: actions/upload-artifact@v7
      with:
        name: sbom
        path: sbom-cyclonedx.json

    - name: Sign image with Cosign
      if: github.event_name == 'push'
      run: |
        cosign sign --yes ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}@${{ steps.build-push.outputs.digest }}
```

#### GitLab CI 工作流示例

```yaml
stages:
  - build
  - scan
  - push
  - sign

variables:
  REGISTRY: registry.gitlab.com
  IMAGE_NAME: $REGISTRY/$CI_PROJECT_PATH

build:
  stage: build
  image: docker:<version>-cli@sha256:<docker-cli-digest>
  services:
    - name: docker:<version>-dind@sha256:<docker-dind-digest>
  script:
    - docker build -t $IMAGE_NAME:$CI_COMMIT_SHA .
    - docker save $IMAGE_NAME:$CI_COMMIT_SHA > image.tar

scan:trivy:
  stage: scan
  image: aquasec/trivy:<version>@sha256:<trivy-digest>
  script:
    - trivy image --severity HIGH,CRITICAL --exit-code 1 docker-archive://image.tar
  allow_failure: false

scan:grype:
  stage: scan
  image: anchore/grype:<version>@sha256:<grype-digest>
  script:
    - grype docker-archive://image.tar

generate:sbom:
  stage: scan
  image: anchore/syft:<version>@sha256:<syft-digest>
  script:
    - syft docker-archive://image.tar -o cyclonedx > sbom.xml
  artifacts:
    reports:
      cyclonedx: sbom.xml

# 如需讓 GitLab 安全面板擷取容器掃描結果，應輸出 GitLab 相容的 container_scanning 報告。

push:
  stage: push
  image: docker:<version>-cli@sha256:<docker-cli-digest>
  services:
    - name: docker:<version>-dind@sha256:<docker-dind-digest>
  script:
    - docker load < image.tar
    - echo "$REGISTRY_PASSWORD" | docker login --username "$REGISTRY_USER" --password-stdin "$REGISTRY"
    - docker push $IMAGE_NAME:$CI_COMMIT_SHA
    - DIGEST=$(docker buildx imagetools inspect "$IMAGE_NAME:$CI_COMMIT_SHA" --format '{{.Manifest.Digest}}')
    - echo "$IMAGE_NAME@$DIGEST" > image-digest.txt
  artifacts:
    paths:
      - image-digest.txt
  only:
    - main

sign:
  stage: sign
  image: gcr.io/projectsigstore/cosign:<version>@sha256:<cosign-digest>
  script:
    - cosign sign --key $COSIGN_KEY "$(cat image-digest.txt)"
  only:
    - main
```

### 常見問題與最佳實務

**Q: 掃描報告中有過時的 CVE，如何處理？**

A: 某些 CVE 可能已經被修復但資料庫未更新，可以：

- 手動驗證安全修補程式是否已應用
- 使用工具的忽略列表功能（如 Trivy 的 `.trivyignore`）
- 定期更新掃描工具和漏洞資料庫

**Q: 如何平衡映像檔大小和安全性？**

A:

- 使用多階段建立減少最終映像檔大小
- 使用精簡基礎映像檔（Alpine、Distroless）
- 定期更新依賴而不是一味求小
- 優先安全性，體積次之

**Q: 如何管理和輪換簽名密鑰？**

A:

- 在密鑰管理系統（如 HashiCorp Vault）中儲存密鑰
- 定期輪換密鑰（建議每 90 天）
- 使用 Keyless 簽名消除密鑰管理複雜性
- 保留密鑰輪換的審計日誌

## DevOps 完整工作流

本章將演示一個基於 Docker、Kubernetes 和 Jenkins/GitLab CI 的完整 DevOps 工作流。

### 工作流概覽

1. **Code**：開發人員提交程式碼到 GitLab。
2. **Build**：GitLab CI 觸發建立任務。
3. **Test**：執行單元測試和整合測試。
4. **Package**：建立 Docker 映像檔並推送到 Harbor/Registry。
5. **Deploy (Staging)**：自動部署到測試環境 Kubernetes 集群。
6. **Verify**：人工或自動化驗證。
7. **Release (Production)**：審批後自動部署到生產環境。

### 關鍵設定示例

本節透過一組最小可用的片段，展示典型 DevOps 流程中與 Docker 相關的關鍵設定。

#### 1. Dockerfile 多階段建立

使用 Docker 多階段建立可以有效減小映像檔體積。

```dockerfile
## Build stage

FROM golang:1.26 AS builder
WORKDIR /app
COPY . .
RUN go build -o main .

## Final stage

FROM alpine:3.21
WORKDIR /app
COPY --from=builder /app/main .
CMD ["./main"]
```

#### 2. GitLab CI 設定

GitLab CI（`.gitlab-ci.yml`）設定如下：

```yaml
stages:
  - test
  - build
  - deploy

unit_test:
  stage: test
  image: golang:1.26
  script:
    - go test ./...

build_image:
  stage: build
  image: docker:29
  services:
    - docker:29-dind
  script:
    - echo "$CI_REGISTRY_PASSWORD" | docker login -u "$CI_REGISTRY_USER" --password-stdin $CI_REGISTRY
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA

deploy_staging:
  stage: deploy
  image: dtzar/helm-kubectl
  script:
    - printf '%s' "$KUBE_CA_PEM" > kube-ca.crt
    - kubectl config set-cluster k8s --server=$KUBE_URL --certificate-authority=kube-ca.crt --embed-certs=true
    - kubectl config set-credentials admin --token=$KUBE_TOKEN
    - kubectl config set-context default --cluster=k8s --user=admin
    - kubectl config use-context default
    - kubectl set image deployment/myapp myapp=$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
      -n staging
  only:
    - develop
```

### 最佳實務

1. **不可變基礎設施**：一旦映像檔建立完成，在各個環境（Dev、Staging、Prod）中都應該使用同一個映像檔 tag（通常是 commit hash），而不是重新建立。
2. **設定分離**：使用 ConfigMap 和 Secret 管理環境特定的設定，不要打包進映像檔。
3. **應對 Docker Hub 限額 (Rate Limits)**：
   - Docker Hub 對匿名拉取實施了嚴格的限制（6 小時內約 100 次）。若在 CI/CD 中頻繁建立，極易觸發 `toomanyrequests` 錯誤。
   - **最佳策略**：
     - 在流水線開頭始終執行安全的身份認證（使用 PAT，而非密碼）。
     - 將常用的基礎映像檔快取到自建的 Harbor/Nexus，使用 Pull-Through Cache。
     - 開啟 Docker 建立引擎 (BuildKit) 的 inline 或 registry 快取功能，以降低全量拉取頻率。
4. **GitOps**：考慮引入 ArgoCD，將部署設定也作為程式碼儲存在 Git 中，實作 Git 驅動的部署同步。

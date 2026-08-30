## 14.8 Kubernetes 命令行 kubectl

[kubectl](https://github.com/kubernetes/kubernetes) 是 Kubernetes 自帶的客戶端，可以用它來直接操作 Kubernetes。

kubectl 的基本用法格式為：

```bash
kubectl [command] [resource] [name] [flags]
```

其中 `command` 是操作命令（如 get、apply、delete），`resource` 是資源型別（如 pod、deployment、service），`name` 是資源名稱（可選），`flags` 是各種選項引數。

### 14.8.1 get

顯示一個或多個資源。最常用的命令之一，用於查詢集群中的資源狀態。

```bash
# 查看所有 Pod
$ kubectl get pods

# 查看指定命名空間中的 Deployment
$ kubectl get deployment -n kube-system

# 查看所有資源
$ kubectl get all

# 使用更詳細的輸出格式
$ kubectl get pods -o wide

# 輸出為 YAML 格式
$ kubectl get pod my-pod -o yaml

# 根據標籤選擇資源
$ kubectl get pods -l app=nginx
```

### 14.8.2 describe

顯示資源的詳細資訊，包括事件、狀態、設定等。用於除錯和查看資源的完整資訊。

```bash
# 查看特定 Pod 的詳情
$ kubectl describe pod my-pod

# 查看 Node 的詳情
$ kubectl describe node node-1

# 查看 Deployment 的詳情
$ kubectl describe deployment nginx-deployment
```

### 14.8.3 apply

從檔案或標準輸入應用設定。這是宣告式資源管理的標準方式，可用於建立或更新資源。

```bash
# 應用 YAML 檔案
$ kubectl apply -f deployment.yaml

# 應用目錄中的所有 YAML 檔案
$ kubectl apply -f ./manifests/

# 從標準輸入應用設定
$ cat deployment.yaml | kubectl apply -f -
```

### 14.8.4 create

從檔案或標準輸入建立資源。與 apply 不同，create 僅用於建立新資源，如果資源已存在會報錯。

```bash
# 建立資源
$ kubectl create -f pod.yaml

# 從標準輸入建立
$ kubectl create -f - < deployment.yaml
```

### 14.8.5 delete

刪除一個或多個資源。支援按名稱、標籤、資源型別等多種方式刪除。

```bash
# 按名稱刪除
$ kubectl delete pod my-pod

# 刪除整個 Deployment（同時刪除其管理的 Pod）
$ kubectl delete deployment nginx-deployment

# 按標籤刪除
$ kubectl delete pods -l app=nginx

# 從檔案刪除
$ kubectl delete -f deployment.yaml
```

### 14.8.6 logs

查看 Pod 中容器的日誌。用於除錯應用和查看容器輸出。

```bash
# 查看 Pod 的日誌
$ kubectl logs my-pod

# 查看 Pod 中特定容器的日誌
$ kubectl logs my-pod -c container-name

# 實時跟蹤日誌（類似 tail -f）
$ kubectl logs -f my-pod

# 查看最近 100 行日誌
$ kubectl logs my-pod --tail=100

# 查看 Pod 啟動前的日誌（適用於已崩潰的容器）
$ kubectl logs my-pod --previous
```

### 14.8.7 exec

在執行中的容器內部執行命令。用於除錯、排查問題或執行應用內的操作。

```bash
# 進入容器的互動式 shell
$ kubectl exec -it my-pod -- /bin/sh

# 在容器中執行命令
$ kubectl exec my-pod -- ls -la /app

# 在 Pod 中的特定容器執行命令
$ kubectl exec -it my-pod -c container-name -- /bin/bash
```

### 14.8.8 port-forward

將本地埠號轉發到 Pod 的埠號。用於本地存取集群內的服務，無需暴露 Service。

```bash
# 將本地 8080 埠號轉發到 Pod 的 80 埠號
$ kubectl port-forward pod/my-pod 8080:80

# 使用隨機本地埠號
$ kubectl port-forward pod/my-pod :80

# 轉發到 Service
$ kubectl port-forward svc/my-service 8080:80
```

### 14.8.9 rollout

對 Deployment、DaemonSet、StatefulSet 等資源執行滾動更新、暫停、繼續或回滾操作。

```bash
# 查看滾動更新狀態
$ kubectl rollout status deployment/nginx-deployment

# 暫停滾動更新
$ kubectl rollout pause deployment/nginx-deployment

# 繼續滾動更新
$ kubectl rollout resume deployment/nginx-deployment

# 查看更新歷史
$ kubectl rollout history deployment/nginx-deployment

# 回滾到前一個版本
$ kubectl rollout undo deployment/nginx-deployment

# 回滾到特定版本
$ kubectl rollout undo deployment/nginx-deployment --to-revision=2
```

### 14.8.10 label

向資源加入、修改或刪除標籤。標籤用於組織和選擇資源。

```bash
# 為 Pod 加入標籤
$ kubectl label pod my-pod env=production

# 修改已有標籤
$ kubectl label pod my-pod env=staging --overwrite

# 刪除標籤
$ kubectl label pod my-pod env-

# 為多個資源加入標籤
$ kubectl label pods -l app=nginx version=v1
```

### 14.8.11 annotate

向資源加入或修改註解。註解用於儲存任意中繼資料，不用於資源選擇。

```bash
# 加入註解
$ kubectl annotate pod my-pod description="Production pod"

# 修改註解
$ kubectl annotate pod my-pod description="Staging pod" --overwrite

# 刪除註解
$ kubectl annotate pod my-pod description-
```

### 14.8.12 edit

直接編輯 Kubernetes 資源。編輯器由 `EDITOR` 環境變數指定。

```bash
# 編輯 Pod
$ kubectl edit pod my-pod

# 編輯 Deployment
$ kubectl edit deployment nginx-deployment
```

### 14.8.13 config

管理 kubectl 的設定檔案（通常位於 `~/.kube/config`）。

```bash
# 查看目前設定
$ kubectl config view

# 切換上下文
$ kubectl config use-context my-cluster

# 查看所有上下文
$ kubectl config get-contexts

# 設定預設命名空間
$ kubectl config set-context --current --namespace=my-namespace
```

### 14.8.14 cluster-info

顯示集群的連線資訊和元件狀態。

```bash
# 顯示集群資訊
$ kubectl cluster-info

# 顯示完整的集群狀態（注：componentstatuses 自 1.19 起已棄用，建議使用下方替代命令）
$ kubectl get componentstatuses
# 推薦替代：
$ kubectl get --raw='/readyz?verbose'
```

### 14.8.15 version

顯示 kubectl 客戶端和 Kubernetes API server 的版本資訊。

```bash
# 顯示版本
$ kubectl version

# 僅顯示客戶端版本
$ kubectl version --client

# 以 JSON 格式輸出
$ kubectl version --output=json
```

### 14.8.16 api-versions

列出 API server 支援的所有 API 版本，格式為「組/版本」。

```bash
$ kubectl api-versions
```

### 14.8.17 explain

解釋資源的欄位含義。用於了解 YAML 設定檔案中各欄位的作用。

```bash
# 查看 Pod 資源的欄位說明
$ kubectl explain pod

# 查看 Pod 下 spec 欄位的說明
$ kubectl explain pod.spec

# 查看具體欄位的詳細說明
$ kubectl explain pod.spec.containers
```

### 14.8.18 auth

檢查使用者權限，用於驗證 RBAC 設定。

```bash
# 檢查目前使用者是否有權限執行操作
$ kubectl auth can-i create pods

# 檢查特定使用者的權限
$ kubectl auth can-i create pods --as=other-user
```

### 14.8.19 help

顯示任何命令的幫助資訊。

```bash
# 顯示 kubectl 的一般幫助
$ kubectl help

# 顯示特定命令的幫助
$ kubectl get --help

# 顯示資源的 API 文件
$ kubectl explain deployment
```

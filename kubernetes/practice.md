## 13.5 實戰練習

本章透過部署一個 Nginx 網站並設定 Service，串聯前面學到的 Deployment、探針、資源配額和服務發現知識。

Deployment 與 Service 的[合併清單](../examples/validated/kubernetes/web.yaml)使用倉庫內固定的 Kubernetes 1.31 strict schema 做離線 `kubeconform` 校驗。下面的圍欄與該檔案由測試強制保持一致。

開始前請先準備好可用的 Kubernetes 集群和 `kubectl` 上下文。你可以先完成 [14.3 Docker Desktop](../kubernetes_setup/docker-desktop.md) 或 [14.4 Kind](../kubernetes_setup/kind.md)，並確認：

```bash
kubectl get nodes
```

### 13.5.1 目標

1. 部署一個包含 readiness probe 和資源請求/限制的 Nginx Deployment。
2. 建立一個 ClusterIP Service 暴露 Nginx。
3. 透過埠號轉發存取服務，並觀察一次滾動釋出。

### 13.5.2 儲存並應用合併清單

<!-- canonical-example: kubernetes -->
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 2
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
        - name: nginx
          image: nginx:1.28-alpine
          ports:
            - name: http
              containerPort: 80
          readinessProbe:
            httpGet:
              path: /
              port: http
          resources:
            requests:
              cpu: 50m
              memory: 32Mi
            limits:
              cpu: 200m
              memory: 128Mi
---
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  selector:
    app: nginx
  ports:
    - name: http
      port: 80
      targetPort: http
```

倉庫內執行時，可直接應用經過校驗的檔案：

```bash
kubectl apply -f examples/validated/kubernetes/web.yaml
kubectl get deployment/nginx-deployment service/nginx-service
```

Service 未指定 `type`，因此使用預設的 `ClusterIP`，不會依賴不同本地集群對 NodePort 的宿主機映射行為。

### 13.5.3 存取服務

```bash
kubectl port-forward service/nginx-service 8080:80
```

然後存取 `http://localhost:8080`。結束埠號轉發可按 `Ctrl+C`。

> Ingress 只有在集群中已安裝 Ingress controller 且設定了 IngressClass 時才會生效。目前練習只覆蓋 Service；Ingress/Gateway API 建議在完成第 14 章後再單獨練習。

### 13.5.4 觀察滾動釋出

修改 Pod 模板中的環境變數會觸發 Deployment 滾動釋出，而無需依賴另一個外部映像檔標籤：

```bash
kubectl set env deployment/nginx-deployment RELEASE_MARKER=demo-v2
kubectl rollout status deployment/nginx-deployment
```

### 13.5.5 清理資源

```bash
kubectl delete -f examples/validated/kubernetes/web.yaml
```

## VS Code

VS Code 的 [Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers)
可以把「開發環境」放進容器，同時保留 VS Code 的編輯、補全、除錯體驗。

本節提供一個最小可用示例：把任意專案（以 Go 為例）變成「打開即開發」的容器化環境。

### 前置條件

* 安裝 Docker Desktop（或 Linux 上的 Docker Engine）。
* VS Code 安裝擴展：Dev Containers（`ms-vscode-remote.remote-containers`）。

### 最小示例：.devcontainer/devcontainer.json

在專案根目錄建立 `.devcontainer/devcontainer.json`：

```json
{
  "name": "docker-practice-dev",
  "image": "golang:1.26",
  "workspaceFolder": "/work",
  "workspaceMount": "source=${localWorkspaceFolder},target=/work,type=bind",
  "customizations": {
    "vscode": {
      "extensions": [
        "golang.Go"
      ]
    }
  },
  "postCreateCommand": "go version"
}
```
然後在 VS Code 命令面板選擇：

* `Dev Containers: Reopen in Container`

VS Code 會拉取映像檔並啟動容器，隨後你就可以在容器內執行：

```bash
go test ./...
```

### 結合 Docker Compose（可選）

如果專案同時依賴資料庫/快取（例如 Postgres/Redis），可以使用 `dockerComposeFile`
把依賴一起拉起。

示例（`devcontainer.json` 片段）：

```json
{
  "name": "compose-dev",
  "dockerComposeFile": [
    "../docker-compose.yml"
  ],
  "service": "dev",
  "workspaceFolder": "/work"
}
```
注意：`service` 需要對應 compose 裡的服務名。

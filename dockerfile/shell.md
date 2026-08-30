## SHELL 指令

### 基本語法

```docker
SHELL ["executable", "parameters"]
```
`SHELL` 指令允許覆蓋 Docker 預設的 shell。

- **Linux 預設**：`["/bin/sh", "-c"]`
- **Windows 預設**：`["cmd", "/S", "/C"]`

該指令會影響後續的 `RUN`，`CMD`，`ENTRYPOINT` 指令（當它們使用 shell 格式時）。

---

### 為什麼要用 SHELL 指令

#### 1. 使用 bash 特性

預設的 `/bin/sh`（通常是 dash 或 alpine 的 ash）功能有限。如果你需要使用 bash 的特有功能（如陣列、`{}` 擴展、`pipefail` 等），可以切換 shell。

```docker
FROM ubuntu:24.04

## 切換到 bash

SHELL ["/bin/bash", "-c"]

## 現在可以使用 bash 特性了

RUN echo {a..z}
```

#### 2. 增強錯誤處理

預設情況下，管道命令 `cmd1 | cmd2` 只要 `cmd2` 成功，整個指令就視為成功。這可能掩蓋建立錯誤。

```docker
## ❌ 這裡的 wget 失敗了，但建立繼續（因為 tar 成功了）

RUN wget -O - https://invalid-url | tar xz
```
使用 `SHELL` 啟用 `pipefail`：

```docker
## ✅ 啟用 pipefail

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

## 如果 wget 失敗，整個 RUN 就會失敗

RUN wget -O - https://invalid-url | tar xz
```

#### 3. Windows 環境

在 Windows 容器中，經常需要在 `cmd` 和 `powershell` 之間切換。

```docker
FROM mcr.microsoft.com/windows/servercore:ltsc2022

## 預設是 cmd

RUN echo Default shell is cmd

## 切換到 powershell

SHELL ["powershell", "-command"]
RUN Write-Host "Hello from PowerShell"

## 切回 cmd

SHELL ["cmd", "/S", "/C"]
```
---

### 作用範圍

`SHELL` 指令可以出現多次，每次只影響其後的指令：

```docker
FROM ubuntu:24.04

## 使用預設 sh

RUN echo "Using sh"

SHELL ["/bin/bash", "-c"]

## 使用 bash

RUN echo "Using bash"

SHELL ["/bin/sh", "-c"]

## 回到 sh

RUN echo "Using sh again"
```
---

### 對其他指令的影響

`SHELL` 影響的是所有使用 **shell 格式** 的指令：

| 指令格式 | 是否受 SHELL 影響 |
|---------|-------------------|
| `RUN command` | ✅ 是 |
| `RUN ["exec", "param"]` | ❌ 否 |
| `CMD command` | ✅ 是 |
| `CMD ["exec", "param"]` | ❌ 否 |
| `ENTRYPOINT command` | ✅ 是 |
| `ENTRYPOINT ["exec", "param"]` | ❌ 否 |

---

### 最佳實踐

#### 1. 推薦開啟 pipefail

對於使用 bash 的映像檔，強烈建議開啟 `pipefail`，以確保建立過程中的錯誤能被即時擷取。

```docker
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
```

#### 2. 明確意圖

如果由於腳本需求必須更改 shell，最好在 Dockerfile 中顯式宣告，而不是依賴預設行為。

#### 3. 盡量保持一致

避免在 Dockerfile 中頻繁切換 SHELL，這會使建立過程難以理解和偵錯。盡量在頭部定義一次即可。

---

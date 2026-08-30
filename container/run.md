## 啟動容器

本節將詳細介紹 Docker 容器的啟動方式，包括新建啟動和重新啟動已停止的容器。

### 啟動方式概述

啟動容器有兩種方式：

- **新建並啟動**：基於映像檔建立新容器
- **重新啟動**：將已終止的容器重新執行

由於 Docker 容器非常輕量，實際使用中常常是隨時刪除和新建容器，而不是反覆重啟同一個容器。

### 新建並啟動

#### 基本語法

```bash
docker run [選項] 映像檔 [命令] [參數...]
```

#### 最簡單的例子

輸出「Hello World」後容器自動終止：

```bash
$ docker run ubuntu:24.04 /bin/echo 'Hello world'
Hello world
```
這與直接執行 `/bin/echo 'Hello world'` 幾乎沒有區別，但實際上已經啟動了一個完整的 Ubuntu 容器來執行這條命令。

> **版本說明**：範例使用 `ubuntu:24.04`，這是最新 LTS 版本。如需其他版本，可替換為 `ubuntu:22.04`、`ubuntu:20.04` 等。

#### 互動式容器

啟動一個可以互動的 bash 終端機：

```bash
$ docker run -it ubuntu:24.04 /bin/bash
root@af8bae53bdd3:/#
```
**參數說明**：

| 參數 | 作用 |
|------|------|
| `-i` | 保持標準輸入 (stdin) 打開，允許輸入 |
| `-t` | 分配虛擬終端機 (pseudo-TTY)，提供終端機介面 |
| `-it` | 兩者組合使用，獲得互動式終端機 |

在互動模式下可以執行命令：

```bash
root@af8bae53bdd3:/# pwd
/
root@af8bae53bdd3:/# ls
bin boot dev etc home lib lib64 media mnt opt proc root run sbin srv sys tmp usr var
root@af8bae53bdd3:/# exit  # 退出容器
```

### docker run 的完整流程

執行 `docker run` 時，Docker 在後臺完成以下操作：

```mermaid
flowchart TD
    Cmd["docker run ubuntu:24.04 /bin/echo 'Hello'"] --> Step1

    Step1{"1. 檢查本地是否有 ubuntu:24.04 映像檔"}
    Step1 -- 有 --> Step1_Yes["使用本地映像檔"]
    Step1 -- 無 --> Step1_No["從 Registry 下載"]

    Step1_Yes --> Step2
    Step1_No --> Step2

    Step2["2. 建立容器<br/>• 基於映像檔的唯讀層<br/>• 添加一層可讀寫層（容器儲存層）"] --> Step3
    Step3["3. 設定網路<br/>• 建立虛擬網卡<br/>• 分配 IP 位址<br/>• 連線到 Docker 網橋"] --> Step4
    Step4["4. 啟動容器，執行指定命令"] --> Step5
    Step5["5. 命令執行完畢，容器停止"]
```

### 常用啟動選項

#### 基礎選項

| 選項 | 說明 | 範例 |
|------|------|------|
| `-d` | 後臺執行 (detach)| `docker run -d nginx:latest` |
| `-it` | 互動式終端機 | `docker run -it ubuntu:24.04 bash` |
| `--name` | 指定容器名稱 | `docker run --name myapp nginx:latest` |
| `--rm` | 退出後自動刪除容器 | `docker run --rm ubuntu:24.04 echo hi` |

#### 埠號映射

```bash
## 將容器的 80 埠號映射到宿主主機的 8080 埠號

$ docker run -d -p 8080:80 nginx:latest

## 隨機映射埠號

$ docker run -d -P nginx:latest

## 只綁定到 localhost

$ docker run -d -p 127.0.0.1:8080:80 nginx:latest
```

#### 資料卷掛載

```bash
## 掛載命名卷

$ docker run -v mydata:/data nginx:latest

## 掛載宿主主機目錄

$ docker run -v /host/path:/container/path nginx:latest

## 唯讀掛載

$ docker run -v /host/path:/container/path:ro nginx:latest
```

#### 環境變數

```bash
## 設定單個環境變數

$ docker run -e MYSQL_ROOT_PASSWORD=secret mysql

## 從檔案載入環境變數

$ docker run --env-file .env myapp
```

#### 資源限制

```bash
## 限制記憶體

$ docker run -m 512m nginx:latest

## 限制 CPU

$ docker run --cpus=1.5 nginx:latest
```

### 啟動已終止容器

使用 `docker start` 重新啟動已停止的容器：

```bash
## 查看所有容器（包括已停止的）

$ docker ps -a
CONTAINER ID  IMAGE   STATUS                     NAMES
af8bae53bdd3  ubuntu  Exited (0) 2 minutes ago   myubuntu

## 重新啟動

$ docker start myubuntu

## 啟動並附加終端機

$ docker start -ai myubuntu
```

### 容器內程式的特點

容器內只執行指定的應用程式及其必需資源：

```bash
root@ba267838cc1b:/# ps
  PID TTY          TIME CMD
    1 ?        00:00:00 bash
   11 ?        00:00:00 ps
```
可見容器中僅執行了 `bash` 程式。這種特點使得 Docker 對資源的使用率極高。

> 💡 編者提示：容器內的 PID 1 程式很重要——它是容器的主程式，該程式退出則容器停止。詳見[常駐執行](daemon.md)章節。

### 常見問題

#### Q：容器啟動後立即退出

**原因**：主程式執行完畢或無法保持執行

```bash
## 這個容器會立即退出（echo 執行完就結束了）

$ docker run ubuntu:24.04 echo "hello"

## 解決：使用能持續執行的命令

$ docker run -d nginx:latest  # nginx 是持續執行的服務
```
詳細解釋見[常駐執行](daemon.md)。

#### Q：無法連線容器內的服務

**原因**：未正確映射埠號

```bash
## 錯誤：沒有 -p 參數，外部無法存取

$ docker run -d nginx:latest

## 正確：映射埠號

$ docker run -d -p 80:80 nginx:latest
```

#### Q：容器內修改的檔案遺失

**原因**：未使用資料卷，資料儲存在容器儲存層

```bash
## 使用資料卷持久化

$ docker run -v mydata:/app/data myapp
```
詳見[資料管理](../data_management/README.md)。

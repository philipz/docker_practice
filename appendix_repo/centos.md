## CentOS

### 基本資訊

[CentOS](https://en.wikipedia.org/wiki/CentOS) 是流行的 Linux 發行版，其軟體套件大多跟 RedHat 系列保持一致。

> ⚠️ **重要提示**：CentOS 8 已於 2021 年 12 月 31 日停止維護 (EOL)，CentOS 7 也已於 2024 年 6 月 30 日 **完全結束支援**。Docker Hub 上的 CentOS 官方映像檔 **已停止更新** 且存在未修復的安全漏洞。
>
> 2026 年了，對於任何新專案，**強烈建議** 使用以下生產級替代方案：
> - [Rocky Linux](https://hub.docker.com/r/rockylinux/rockylinux)：CentOS 原創始人發起的社群驅動專案，目前主流為 Rocky Linux 9。
> - [AlmaLinux](https://hub.docker.com/_/almalinux)：由 CloudLinux 支援的企業級發行版，提供長期支援。
> - [CentOS Stream](https://quay.io/repository/centos/centos)：RHEL 的上游開發分支，映像檔已遷移至 Quay.io（適合開發測試，不建議用於生產環境）。

該倉庫位於 [Docker Hub 的 CentOS 官方映像檔頁](https://hub.docker.com/_/centos)，提供了 CentOS 從 5 ~ 8 各個版本的映像檔（僅作為歷史歸檔，不再更新）。

### 使用方法

使用 Rocky Linux 9 替代（**推薦**）：

```bash
$ docker run --name rocky -it rockylinux/rockylinux:9 bash
```

使用舊版 CentOS 7（**僅用於維護舊專案，不推薦**）：

```bash
$ docker run --name centos -it centos:7 bash
```

### Dockerfile

請到 [CentOS 官方映像檔文件目錄](https://hub.docker.com/_/centos) 查看。

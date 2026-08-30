## 17.2 Fedora CoreOS 安裝

### 17.2.1 下載 ISO

在[下載頁面](https://fedoraproject.org/coreos/download/) `Bare Metal & Virtualized` 標籤頁下載 ISO。

### 17.2.2 編寫 Butane 設定

> **注意**：Fedora CoreOS 設定工具已從 `fcct` (Fedora CoreOS Config Transpiler) 更名為 **Butane**。新版本使用 `.bu` 副檔名和更新的 spec 版本。

```yaml
## example.bu

variant: fcos
version: 1.6.0
passwd:
  users:
    - name: core
      ssh_authorized_keys:
        - ssh-rsa AAAA...
```
將 `ssh-rsa AAAA...` 替換為自己的 SSH 公鑰（位於 `~/.ssh/id_rsa.pub`）。

### 17.2.3 轉換 Butane 設定為 Ignition

```bash
$ docker run -i --rm quay.io/coreos/butane:release --pretty --strict < example.bu > example.ign
```

### 17.2.4 掛載 ISO 啟動虛擬機並安裝

> 虛擬機需要分配 3GB 以上記憶體，否則會無法啟動。

在虛擬機終端執行以下命令安裝：

```bash
$ sudo coreos-installer install /dev/sda --ignition-file example.ign
```
安裝之後重新啟動即可使用。

### 17.2.5 使用

```bash
$ ssh core@虛擬機IP

$ podman --version
```

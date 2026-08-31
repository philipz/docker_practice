# 常見錯誤處理

| 錯誤資訊 / 現象 | 可能原因 | 解決方案 |
| :--- | :--- | :--- |
| `Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?` | Docker 服務未啟動 | Linux: `sudo systemctl start docker`<br>Mac/Win: 啟動 Docker Desktop |
| `permission denied while trying to connect to the Docker daemon socket` | 當前使用者無權存取 Docker socket | 臨時使用 `sudo docker ...`，或確認風險後執行 `sudo usermod -aG docker $USER` 並重新登入；`docker` 使用者群組等同授予 root 級權限，安全要求較高的環境優先評估 Rootless mode |
| `manifest for ... not found: manifest unknown` | 映像檔 tag 不存在 | 檢查 Docker Hub 該映像檔是否存在該 tag，或拼寫是否正確 |
| `connection refused` (pull image) | 網路不通或映像檔源無法存取 | 檢查網路，設定[映像檔加速器](../install/mirror.md) |
| `Bind for 0.0.0.0:8080 failed: port is already allocated` | 埠號被占用 | 檢查占用埠號的程式 (`lsof -i:8080`) 並殺掉，或換個埠號映射 (`-p 8081:80`) |
| `exec user process caused "exec format error"` | 架構不匹配（如在 x86 上跑 ARM 映像檔）| 使用 `docker buildx` 建立多架構映像檔，或拉取對應架構的映像檔 |
| `standard_init_linux.go:211: exec user process caused "no such file or directory"` | 找不到直譯器或相依庫 | 檢查 `ENTRYPOINT`/`CMD` 腳本開頭的 shebang (`#!/bin/sh` vs `#!/bin/bash`)，或確認二進位檔案是否相依缺失（Alpine 常見缺少 glibc）|
| `iptables: No chain/target/match by that name` | 防火牆規則缺失或衝突 | 重新啟動 Docker 服務重置 iptables 鏈: `sudo systemctl restart docker` |
| 容器內無法存取外網 | DNS 設定或轉發問題 | 檢查 `/etc/docker/daemon.json` 中的 DNS 設定 |

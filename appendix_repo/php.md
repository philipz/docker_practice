## PHP

### 基本資訊

[PHP](https://en.wikipedia.org/wiki/Php)（Hypertext Preprocessor 超文字預處理器的字母縮寫）是一種被廣泛應用的開放原始碼的多用途腳本語言，它可嵌入到 HTML 中，尤其適合 web 開發。

該倉庫位於 [Docker Hub 的 PHP 官方映像檔頁](https://hub.docker.com/_/php/)。具體可用版本以 Docker Hub 上的 tags 列表為準。

### 使用方法

下面的命令將執行一個已有的 PHP 腳本。

```bash
$ docker run -it --rm -v "$PWD":/app -w /app php:alpine php your-script.php
```

### Dockerfile

請到 [PHP 官方映像檔文件目錄](https://github.com/docker-library/docs/tree/master/php) 查看。

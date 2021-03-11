## 從映像檔產生 Dockerfile

CenturyLinkLabs 釋出 [dockerfile-from-image](https://github.com/CenturyLinkLabs/dockerfile-from-image) 工具，以逆向工程建立出 Dockerfile。
類似 `docker history` 指令，透過映像檔每一層的 metadata 來重建出那 Dockerfile ，即便沒有提供任何資訊。

### 使用方法

首先 `docker pull centurylink/dockerfile-from-image` 這已包好 Ruby script 的[映像檔](https://registry.hub.docker.com/u/centurylink/dockerfile-from-image/)，
接下來，執行下面命令，就可得到反推所產生的 Dockerfile.txt ：

```bash
docker run -v /var/run/docker.sock:/var/run/docker.sock \
    centurylink/dockerfile-from-image <IMAGE_TAG_OR_ID> > Dockerfile.txt
```

那 `<IMAGE_TAG_OR_ID>` 參數可以任何包含 tag 的映像檔名稱。

### 範例

以下是個示範，如何將官方 Ruby 的映像檔來產生出 Dockerfile。

```bash
$ docker pull ruby
Pulling repository ruby

$ docker run -v /run/docker.sock:/run/docker.sock centurylink/dockerfile-from-image
Usage: dockerfile-from-image.rb [options] <image_id>
    -f, --full-tree                  Generate Dockerfile for all parent layers
    -h, --help                       Show this message

$ docker run -v /run/docker.sock:/run/docker.sock centurylink/dockerfile-from-image ruby
FROM buildpack-deps:latest
RUN useradd -g users user
RUN apt-get update && apt-get install -y bison procps
RUN apt-get update && apt-get install -y ruby
ADD dir:03090a5fdc5feb8b4f1d6a69214c37b5f6d653f5185cddb6bf7fd71e6ded561c in /usr/src/ruby
WORKDIR /usr/src/ruby
RUN chown -R user:users .
USER user
RUN autoconf && ./configure --disable-install-doc
RUN make -j"$(nproc)"
RUN make check
USER root
RUN apt-get purge -y ruby
RUN make install
RUN echo 'gem: --no-rdoc --no-ri' >> /.gemrc
RUN gem install bundler
ONBUILD ADD . /usr/src/app
ONBUILD WORKDIR /usr/src/app
ONBUILD RUN [ ! -e Gemfile ] || bundle install --system
```

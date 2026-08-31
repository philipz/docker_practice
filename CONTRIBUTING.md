## 如何貢獻

領取或建立新的 [Issue](https://github.com/yeasy/docker_practice/issues)，如 [issue 235](https://github.com/yeasy/docker_practice/issues/235)，新增自己為 `Assignee`。

在 [GitHub](https://github.com/yeasy/docker_practice/fork) 上 `fork` 到自己的倉庫，如 `docker_user/docker_practice`，然後 `clone` 到本地，並設定使用者資訊。

```bash
$ git clone git@github.com:docker_user/docker_practice.git

$ cd docker_practice
```
修改程式碼後提交，並推送到自己的倉庫，注意修改提交訊息為對應 Issue 號和描述。

```bash
# Update the content

$ git commit -a -s

# In commit msg dialog, add content like "Fix issue #235: describe ur change"

$ git push
```
在 [GitHub](https://github.com/yeasy/docker_practice/pulls) 上提交 `Pull Request`，新增標籤，並邀請維護者進行 `Review`。

定期使用專案倉庫內容更新自己倉庫內容。

```bash
$ git remote add upstream https://github.com/yeasy/docker_practice

$ git fetch upstream

$ git rebase upstream/master

$ git push -f origin master
```

## 排版規範

本開源書籍遵循[中文排版指南](https://github.com/mzlogin/chinese-copywriting-guidelines)規範。

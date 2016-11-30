# 使用Docker部署

## 准备Docker

1. 安装Docker

    https://docker.github.io/engine/installation/linux/   
    不要漏了阅读 **Create a Docker group** 部分。
    
2. 安装Docker Compose

    https://docker.github.io/compose/install/  
    也可以使用 `pip install docker-compose` 安装。


## 下载本项目代码

```sh
git clone git@github.com:NetEaseGame/git-webhook.git
cd git-webhook
```
    
## 配置

配置 `app/config.py`

拷贝一份 config_docker_example.py 到同目录 config.py， 然后对应修改配置内容。只需配置一点:

- `GITHUB`: GitHub 登陆配置，可以到 [OAuth applications](https://github.com/settings/developers) 自行申请，登陆 Callback 地址为： `your_domain/github/callback`.
     
     
## 部署

```sh
docker-compose up
```

第一次部署可能需要几分钟或十几分钟，完成后执行 `make createdb` 初始化数据库。  
再访问 http://127.0.0.1:18340/ 即可。使用 GitHub 账号登陆。


## 添加WebHook

在工具中添加 Git 项目，获得 WebHook URL，并填写到 Github / GitLab / OscGit 的 WebHook 配置中。

**安装之后如何使用？**直接看你部署的 Web 应用文档吧，或者在[这里](http://webhook.hust.cc/#/doc/webhook)也可以看到。

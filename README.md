# Git WebHook

> 一个使用 Python Flask + SQLAchemy + Celery + Redis + React 开发的用于迅速搭建并使用  WebHook 进行自动化部署和运维系统，支持：**Github / GitLab / GitOsc**。

![GitHub](http://shields.hust.cc/Supported-GitHub-brightgreen.svg) ![GitLab](http://shields.hust.cc/Supported-GitLab-green.svg) ![GitOsc](http://shields.hust.cc/Supported-GitOsc-blue.svg)

 - 技术栈简单，**部署**容易；
 - 代码简洁易懂，**二次开发**毫无压力；
 - 支持 **Github / GitLab / GitOsc**；
 - 使用 SSH 方式，支持**多服务**配置；

Online DEMO Website: [http://webhook.hust.cc/](http://webhook.hust.cc/)，使用 gunicorn + gevent + ngxin 部署。


## 一、如何使用 ？

1. 下载本项目代码：

	```sh
	git clone git@github.com:NetEaseGame/git-webhook.git
	```

2. 安装 Python 依赖

	```sh
	pip install requirements.txt
	```

3. 配置 `config.py`

	拷贝一份 config_example.py 到同目录 config.py， 然后对应修改配置内容。主要需要配置三点：
	
	 - `DATABASE_URI`: 数据库地址，理论上可以使用**任何关系数据库**；推荐使用 sqlite 和 mysql （经过测试）；
	 - `CELERY REDIS`: Redis URI 配置，主要用于 Celery 后台任务；
	 - `GITHUB`: GitHub 登陆配置，可以到 [OAuth applications](https://github.com/settings/developers) 自行申请，登陆 Callback 地址为： `your_domain/github/callback`.

4. 初始化数据库结构
	
	```sh
	python scripts.py build_db
	```

5. 运行应用

	```sh
	python run_webhook.py
	```
	
	运行之后，打开 http://127.0.0.1:18340 即可访问。使用 GitHub 账号登陆。

6. 添加WebHook

	在工具中添加 Git 项目，获得 WebHook URL，并填写到 Github / GitLab / OscGit 的 WebHook 配置中。


## 三、效果预览

 - **首页**

![index.png](app/static/res/img/index.png)

 - **WebHook列表**

![webhook.png](app/static/res/img/webhook.png)

 - **服务器列表**

![server.png](app/static/res/img/server.png)

 - **WebHook 历史记录**

![history.png](app/static/res/img/history.png)


## 四、部署

代码使用 Flask 框架开发，线上部署使用 gunicorn + gevent + nginx 已经是比较成熟的方案了，本应用当然也可以使用这种方式部署。

主要的服务器依赖环境：

 - 数据库环境（自行选择，推荐 mysql 和 sqlite）；
 - Redis，利用 Celery 做后台任务；


## 五、贡献

项目使用 SSH 私钥的方式，直接登陆 Linux 服务器，执行部署或者运维的 Shell 命令，安全可靠，当然因为涉及到**私钥**，所以为了安全起见，建议在内网搭建使用（这些是我们的使用情景）。

**后端开发**使用：Python Flask + SQLAchemy + Celery + Redis，常规的技术栈；

**前端开发**使用 React + Webpack，并没有使用其他消息通信框架。

所以整体项目代码非常简单，大部分都能够修改和更新代码，并提交 Pull Request，目前系统 TODO 包括，我个人也将注意完善：


 - Celery 进程情况显示（当 Celery 进程没有执行的时候，在页面上提示，类似于 Sentry）；
 - 系统状态和统计（任务队列实时情况，WebHook 执行的统计图表）；
 - **发布为 pip 包，使得安装部署更加容易**；
 - Document 使用文档 & 帮助文档；


## LICENSE

MIT @hustcc
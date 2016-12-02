# CHANGELOG 修订历史

修改历史如下：


## v0.0.6 @2016-12-02

与之前的版本相比，增加：

 - SSH 登陆服务器支持账号密码登陆；
 - 发布到 Pypi 包，版本 0.0.6，使用 `pip install git-webhook` 即可安装；
 - 解决 SocketIO 以及 celery 的配置 bug；
 - **安装和启动方式**有了大量变化，简化许多；
 - 修改其他 bug ；


## v0.0.4 @2016-11-16

与之前的版本相比，增加：

 - 主要添加 **SocketIO** 支持，实时修改页面上的 WebHook 和 History 状态。
	1. 后台使用 flask-socketio 发送 webhook 和 history 两个 socket 状态；
	2. 前端使用 socketio + [onfire.js](https://github.com/hustcc/onfire.js) 分发和处理收到数据，并渲染到页面上；
 - 更新到此版本，请注意下做一下步骤：
	1. 在 Config.py 中添加 `SOCKET_MESSAGE_QUEUE` 配置，和 Celery 的 Redis 配置保持一致即可；
	2. 安装 Python 依赖：`flask-socketio`，如果需要使用 eventlet / gevent / gevent-websocket 部署，请自行安装；


## v0.0.3 @2016-11-11

与之前的版本相比，增加：

 - 增加 项目观察者角色（project Collaborators），Collaborator 具有以下权限 / 限制。
	1. 可见权限，包括 webhook 信息，history 信息（不能看到 server 信息）；
	2. 可手动执行权限（retry按钮）；
	3. 不能修改，删除 webhook 信息。
 - 更新到此版本，请注意运行 `python scripts.py rebuild_db` 生成新的数据结构，**不会丢失数据**。


## v0.0.2 @2016-11-11

与之前的版本相比，增加：

 - 在 WebHook 页面添加手动执行 hook shell 的功能，方便进行手动运维（鼠标 hover 到 WebHook 的状态那里，会出现一个按钮，点击即可直接开始执行该 WebHook 的 shell 脚本）。


## v0.0.1 @2016-11-05

开始的第一个版本，和之前未加入版本之前添加：

 - 加入版本号管理和控制；
 - 新增 hook 任务的 shell 执行时间长度；（**更新部署的时候，需要在 history 表新增字段 `update_time`，类型为 datetime，默认值为当前时间，不同数据库添加方式不同**）
 - 首页增加显示当前运行的版本号。

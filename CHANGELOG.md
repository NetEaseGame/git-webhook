# CHANGELOG 修订历史

修改历史如下


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

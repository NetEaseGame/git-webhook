# 开发指南

## 后端[Docker]

运行 `make dev` 启动所有需要的服务，然后就可以开工了。
可参考[Docker下使用镜像加速](http://www.imike.me/2016/04/20/Docker下使用镜像加速/)加快镜像下载速度。

### 添加server

使用`ssh/id_rsa`这个私钥，连接装在Docker里面的一个SSH服务器。


### 添加webhook

访问 http://localhost:10080/ ，这是装在Docker里面的Gogs。  
webhook地址中的IP改成`172.22.0.1`填入Gogs的项目设置中即可，
这个IP可以通过`docker network inspect gitwebhook_default`命令查看到。

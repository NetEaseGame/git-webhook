import React from 'react';
import { Link } from 'react-router';

import StringUtils from './utils/stringUtils.jsx';

const Document = React.createClass({
  gen_code: 'hustcc@onlinegame-14-121:~/.ssh$ ssh-keygen\n' + 
'Generating public/private rsa key pair.\n' + 
'Enter file in which to save the key (/home/hustcc/.ssh/id_rsa): id_rsa_forwebhook\n' + 
'id_rsa_forwebhook already exists.\n' + 
'Overwrite (y/n)? y\n' + 
'Enter passphrase (empty for no passphrase): \n' + 
'Enter same passphrase again: \n' + 
'Your identification has been saved in id_rsa_forwebhook.\n' + 
'Your public key has been saved in id_rsa_forwebhook.pub.\n' + 
'The key fingerprint is:\n' + 
'27:04:9f:0b:21:73:a7:2a:cd:4e:9e:43:2a:45:c2:29 hustcc@onlinegame-14-121\n' + 
'The key\'s randomart image is:\n' + 
'+--[ RSA 2048]----+\n' + 
'|    o + .        |\n' + 
'|. .  + * .       |\n' + 
'|Eo.   o +        |\n' + 
'|.o o . o .       |\n' + 
'|  o *   S .      |\n' + 
'| . B .   o       |\n' + 
'|. .              |\n' + 
'| .   .           |\n' + 
'|                 |\n' + 
'+-----------------+',
  add_key: '[hustcc@host ~]$ cd ~/.ssh\n' + 
'[hustcc@host .ssh]$ cat id_rsa_forwebhook.pub >> authorized_keys',

  getInitialState: function() {
    return {subject: 'qa'};
  },
  componentWillReceiveProps: function(nextProps) {
    this.setState({subject: nextProps.params.subject});
  },
  componentDidMount: function() {
    this.setState({subject: this.props.params.subject});
  },
  content: function(subject) {
    console.log(subject);
    if (subject === 'pkey')
      return (
        <div className="ui segment">
          <div className="ui medium header">如何在Linux上获取 Private Key？</div>
          <p>下面以账户 hustcc 登陆服务器 10.246.14.121 为例来介绍如何获得 SSH private key 。</p>
          <p>第一步是：<strong>生成密钥对</strong>。首先使用scrt登陆到 linux 中，并且 cd 到 /home/hustcc/.ssh/ 目录。运行 ssh-keygen 命令即可，过程如下：</p>
          <pre className="language-powershell" dangerouslySetInnerHTML={{__html: this.gen_code}} />
          <p>其中 passphrase 我没有输入，这样用 python 登陆的时候，就可以无密码登陆了。注意，是在你将要登陆的 linux 服务器上生成 key。</p>
          
          <p>第二步是：<strong>公钥添加到 authorized_keys 中</strong>。</p>
          <pre className="language-powershell" dangerouslySetInnerHTML={{__html: this.add_key}} />

          <p>所有步骤就完成了，然后获取 id_rsa_forwebhook 的内容填写到 Server 中 Private Key 那一栏即可。</p>
          <p className="red"><strong>由于 Private Key 的私密性和安全，请妥善保管自己的账号密码。</strong>。</p>
        </div>
      );
    if (subject === 'webhook') {
      return (
        <div className="ui segment">
          <div className="ui medium header">Git-WebHook 的简单原理？</div>
          <p>首先介绍一下<strong>什么是 Git 的 WebHook ？</strong>，以 GitHub 为例，在项目的 Setting 页面，可以看到一栏 WebHook 菜单，可以配置这个项目的 WebHook，也就是可以指定当项目发生某些情况的时候，去 POST 请求一个 Web Url 地址，同时携带当前项目的一些信息。</p>
          <p>同样的，任何 Git 服务都有这样的 WebHook 设置。我们利用 Git 的这个机制，可以在 Web Url 这里做拉取代码，自动部署，代码增量检查，CI 等等，同样，包括 Travis-ci 等很多 GitHub 第三方集成都是这样的一个原理。</p>
          <p className="green">本项目（Git-WebHool）就是基于这样的原理，做的一个 Web 应用，方便生成 WebHook Url 地址，方便填写 Hook 之后执行的 shell 脚本。</p>
          <div className="ui medium header">Git-WebHook 安装之后如何使用？</div>
          <p>第一步：<strong>本地部署本项目</strong>（如果是外网服务器，也可以使用我这边<a href="http://webhook.hust.cc" target="_blank">部署的服务</a> ），当然首选还是自己搭建部署，也是对自己服务器的安全着想。具体部署方式，参考项目 Readme 文件。</p>

          <p>第二步：<strong>添加服务器信息</strong>。当 Git 上项目有 PUSH 操作的时候，你需要在哪些机器人做操作，就需要那只哪些机器。具体需要配置，IP、PORT、用户名、Private Key（<Link to="/doc/pkey">如何生成？</Link>）这些信息，本项目使用 SSH 方式登录服务器执行相应的 Shell 命令。如下图所示：</p>
          <img className="ui fluid image" src="https://github.com/NetEaseGame/git-webhook/raw/master/app/static/res/img/server.png" />

          <p>第三步：<strong>添加 Git WebHook</strong>。主要填写 Git 项目的名字、需要 Hook 的分支名字，然后发生 PUSH 之后，需要在哪台服务器（第二步中配置的服务器中选择）执行 Shell 指令。如下图所示：</p>
          <img className="ui fluid image" src="https://github.com/NetEaseGame/git-webhook/raw/master/app/static/res/img/webhook.png" />
          <p className="green"><strong>最后一步：在 Git WebHook 右侧第一个按钮复制 WebHook Url 地址，并添加到 Git 项目中 Setting / WebHook 那一栏中即可生效。</strong>。</p>
        </div>
      );
    }
    return (
      <div className="ui segment">
          <h3 className="ui header">Open Source can get more ?</h3>
          <p>Here is document page.</p>
          <p>The background-end base on Flask, SQLAchemy, Celery, Redis.</p>
          <p>The front-end React, semantic-ui and other javascript library.</p>
          <p>Welcome to sumbit an issue or pr.</p>
          <a target="_blank" href="https://github.com/NetEaseGame/git-webhook" className="ui large button">Read More</a>
      </div>
    );
  },
  render: function() {
    return (
      <div className="ui grid">
        <div className="four wide column">
            <div className="ui purple segment pointer"><Link to='/doc/webhook'>1. Git-WebHook 的原理与使用 ?</Link></div>
            <div className="ui pink segment pointer"><Link to='/doc/pkey'>2. SSH Private Key 怎么获得 ?</Link></div>
            <div className="ui grey segment pointer"><Link to='/doc'>3. Q & A</Link></div>
        </div>
        <div className="twelve wide column">
          {
            this.content(this.state.subject)
          }
        </div>
      </div>
    );
  }
});

export default Document;
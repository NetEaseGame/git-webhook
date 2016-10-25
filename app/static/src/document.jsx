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
        TODO
        </div>
      );
    }
    return (
      <div className="ui segment">
          <h3 className="ui header">Open Source can get more ?</h3>
          <p>Here is document page.</p>
          <p>The background-end base on Flask, SQLAchemy, Celery, Redis.</p>
          <p>The front-end React, semantic-ui and other javascript library.</p>
          <a target="_blank" href="https://github.com/NetEaseGame/git-webhook" className="ui large button">Read More</a>
      </div>
    );
  },
  render: function() {
    return (
      <div className="ui grid">
        <div className="four wide column">
            <div className="ui purple segment pointer"><Link to='/doc/webhook'>1. Git-WebHook 的基本原理 ?</Link></div>
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
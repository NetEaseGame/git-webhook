import React from 'react';
import { Link } from 'react-router';

import TimeAgo from 'timeago-react';

import OnFireMixin from './mixins/onFireMixin.jsx';
import TipShowMixin from './mixins/tipShowMixin.jsx';
import RequestsMixin from './mixins/xhrRequestsMixin.jsx';

import StringUtils from './utils/stringUtils.jsx';

const WebHook = React.createClass({
  __ONFIRE__: 'WebHook',
  mixins: [RequestsMixin, OnFireMixin, TipShowMixin],  // 引入 mixin
  getInitialState: function() {
    return {
      showAddForm: false, 
      webhooks: [],
      servers: [],
      btnText: '添加新的 Git WebHook',
      editWebHook: {}
    };
  },
  currentEditIndex: -1,
  whenWebhookUpdate: function(webhook) {
    // websocket 传输过来的新的状态
    let webhooks = this.state.webhooks;
    for (let i = webhooks.length - 1; i >= 0; i--) {
      if (webhooks[i].id == webhook.id) {
        webhooks[i] = webhook;
        this.setState({webhooks: webhooks});
        break;
      }
    }
  },
  componentDidMount: function() {
    new Clipboard('.copy_btn'); // set copy button

    // load webhook
    this.get('/api/webhook/list', {}, function(r) {
      r = r.json();
      if (r.success) this.setState({webhooks: r.data});
      else this.showError('加载数据失败！');
    }.bind(this));

    // load server
    this.get('/api/server/list', {}, function(r) {
      r = r.json();
      if (r.success) this.setState({servers: r.data});
      else this.showError('加载数据失败！');
    }.bind(this));

    this.on('webhook-websocket', this.whenWebhookUpdate);
  },
  clickNewBtn: function(save) {
    if (save) {
      let updateOrAdd = this.refs.id.value;
      this.post('/api/webhook/new', {
        id: updateOrAdd,
        repo: this.refs.repo.value,
        branch: this.refs.branch.value,
        shell: this.refs.shell.value,
        server_id: this.refs.server_id.value
      }, function(r) {
        r = r.json();
        if (r.success) {
          this.refs.addForm.reset();

          let webhooks = this.state.webhooks;
          // update webhook
          if (updateOrAdd) webhooks[this.currentEditIndex] = r.data;
          // add webhook
          else webhooks.push(r.data);
          this.setState({webhooks: webhooks, editWebHook: {},showAddForm: false, btnText: '添加新的 Git WebHook'});
        }
        else this.showError(r.data);
      }.bind(this));
    }
    else {
      this.setState({showAddForm: true});
    }
  },
  clickCloseBtn: function() {
    this.refs.addForm.reset();
    this.setState({showAddForm: false, editWebHook:{}, btnText: '添加新的 Git WebHook'});
  },
  editWebHook: function(webhook, index) {
    if (this.refs.addForm) {
      this.refs.id.value = webhook.id;
      this.refs.repo.value = webhook.repo;
      this.refs.branch.value = webhook.branch;
      this.refs.shell.value = webhook.shell;
      this.refs.server_id.value = webhook.server_id;
    }
    this.setState({showAddForm: true, btnText: '确定保存 WebHook 信息', editWebHook: webhook});
    this.currentEditIndex = index;
  },
  deleteWebHook: function(webhook_id, index) {
    this.post('/api/webhook/delete', {
        webhook_id: webhook_id,
      }, function(r) {
        r = r.json();
        if (r.success) {
          let webhooks = this.state.webhooks;
          webhooks.splice(index, 1);
          this.setState({webhooks: webhooks, showAddForm: false});
        }
        else this.showError(r.data);
      }.bind(this));
  },
  retryBtnClick: function(webhook_id, index) {
    this.post('/api/webhook/retry', {
        webhook_id: webhook_id,
      }, function(r) {
        r = r.json();
        if (r.success) {
          let webhooks = this.state.webhooks;
          webhooks[index] = r.data;
          this.setState({webhooks: webhooks});
        }
        else this.showError(r.data);
      }.bind(this));
  },
  render: function() {
    return (
      <div className="ui tall stacked segment">
        <h3 className="ui dividing header right aligned">Git WebHook List</h3>
        <table className="ui very basic table">
          <thead>
            <tr>
              <th width="5%">#</th>
              <th width="20%">Repo</th>
              <th width="25%">Shell</th>
              <th width="15%">Server</th>
              <th width="10%">LastHook</th>
              <th width="10%">Status</th>
              <th width="15%">Operate</th>
            </tr>
          </thead>
          <tbody>
          {
            this.state.webhooks.map(function(webhook, i) {
              return (
                <tr key={i}>
                  <td title="Collaborator "><Link to={'/collaborator/' + webhook.id}><i className="ui users icon"></i></Link></td>
                  <td>
                    <Link to={'/history/' + webhook.id}> {webhook.repo + '@' + webhook.branch} </Link>
                  </td>
                  <td><pre className="language-powershell" dangerouslySetInnerHTML={{__html: webhook.shell}} /></td>
                  <td>{webhook.server.name}</td>
                  <td title={webhook.lastUpdate}><TimeAgo locale='zh_CN' datetime={webhook.lastUpdate} /></td>
                  <td className="hover">
                    <span className="hover_hidden">{StringUtils.statusToTag(webhook.status)}</span>
                    <span className="hover_show ui icon tiny button" onClick={this.retryBtnClick.bind(this, webhook.id, i)}>
                      <i className="icon refresh"></i>
                    </span>
                  </td>
                  <td>
                    <button className="mini ui icon button copy_btn" title="Copy WebHook to clipboard!" data-clipboard-text={location.protocol + '//' + location.host + '/api/git-webhook/' + webhook.key}><i className="ui icon copy"></i></button>
                    <button className="mini ui icon button" onClick={this.editWebHook.bind(this, webhook, i)}><i className="ui icon edit"></i></button>
                    <button className="mini ui icon button" onClick={this.deleteWebHook.bind(this, webhook.id, i)}><i className="ui icon delete"></i></button>
                  </td>
                </tr>
              )
            }.bind(this))
          }
          </tbody>
        </table>
        {
          this.state.showAddForm &&
          <form className="ui form" ref="addForm">
            <h3 className="ui dividing header left aligned">New WebHook</h3>
            <div className="three fields">
              <input ref="id" type="hidden" defaultValue={this.state.editWebHook.id} />
              <div className="field">
                <label>Git Repository</label>
                <input ref="repo" type="text" defaultValue={this.state.editWebHook.repo} placeholder="Repository Name" />
              </div>
              <div className="field">
                <label>Branch</label>
                <input ref="branch" type="text" defaultValue={this.state.editWebHook.branch} placeholder="Repository Branch" />
              </div>
              <div className="field">
                <label>Which Server <Link to="/server"><i className="ui icon add square"></i></Link></label>
                <select ref="server_id"  defaultValue={this.state.editWebHook.server_id}>
                  <option value="">Select Server</option>
                  {
                    this.state.servers.map(function(server, i) {
                      return (<option key={i} value={server.id}>{server.name + '@' + server.ip}</option>)
                    })
                  }
                </select>
              </div>
            </div>
            <div className="field">
              <label>Callback Shell Script</label>
              <textarea ref="shell" defaultValue={this.state.editWebHook.shell} rows="4"></textarea>
            </div>
          </form>
        }
        <div className="ui center aligned basic segment">
          <div className="ui center aligned basic segment">
            <div className="ui teal animated fade button mini" onClick={this.clickNewBtn.bind(this, this.state.showAddForm)}>
              <div className="visible content">{this.state.btnText}</div>
              <div className="hidden content">{this.state.btnText}</div>
            </div>
            { this.state.showAddForm &&
              <div className="ui red animated fade button mini" onClick={this.clickCloseBtn}>
                <div className="visible content">关闭表单</div>
                <div className="hidden content">关闭表单</div>
              </div>
            }
          </div>
        </div>
      </div>
    );
  }
});

export default WebHook;
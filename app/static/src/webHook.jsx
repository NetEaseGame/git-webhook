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
    };
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
  },
  clickNewBtn: function(save) {
    if (save) {
      this.post('/api/webhook/new', {
        repo: this.refs.repo.value,
        branch: this.refs.branch.value,
        shell: this.refs.shell.value,
        server_id: this.refs.server_id.value
      }, function(r) {
        r = r.json();
        if (r.success) {
          this.refs.addForm.reset();

          let webhooks = this.state.webhooks;
          webhooks.push(r.data);
          this.setState({webhooks: webhooks, showAddForm: false});
        }
        else this.showError(r.data);
      }.bind(this));
    }
    else {
      this.setState({showAddForm: true});
    }
  },
  editWebHook: function(webhook, index) {
    console.log(webhook, 'TODO');
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
  render: function() {
    return (
      <div className="ui tall stacked segment">
        <h3 className="ui dividing header right aligned">Git WebHook List</h3>
        <table className="ui very basic table">
          <thead>
            <tr>
              <th width="5%">#</th>
              <th width="15%">Repo</th>
              <th width="25%">Shell</th>
              <th width="15%">Server</th>
              <th width="10%">LastHook</th>
              <th width="15%">Status</th>
              <th width="15%">Operate</th>
            </tr>
          </thead>
          <tbody>
          {
            this.state.webhooks.map(function(webhook, i) {
              return (
                <tr key={i}>
                  <td>{webhook.id}</td>
                  <td><Link to={'/history/' + webhook.id}> {webhook.repo + '@' + webhook.branch} </Link></td>
                  <td dangerouslySetInnerHTML={{__html: "<pre>" + webhook.shell + "</pre>"}}></td>
                  <td>{webhook.server.name}</td>
                  <td title={webhook.lastUpdate}><TimeAgo locale='zh_CN' datetime={webhook.lastUpdate} /></td>
                  <td>{StringUtils.statusToTag(webhook.status)}</td>
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
              <div className="field">
                <label>Git Repository</label>
                <input ref="repo" type="text" placeholder="Repository Name" />
              </div>
              <div className="field">
                <label>Branch</label>
                <input ref="branch" type="text" placeholder="Repository Branch" />
              </div>
              <div className="field">
                <label>Which Server <Link to="/server"><i className="ui icon add square"></i></Link></label>
                <select ref="server_id">
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
              <textarea ref="shell" rows="4"></textarea>
            </div>
          </form>
        }
        <div className="ui center aligned basic segment">
          <div className="ui center aligned basic segment">
            <div className="ui teal animated fade button mini" onClick={this.clickNewBtn.bind(this, this.state.showAddForm)}>
              <div className="visible content">添加新的 Git WebHook</div>
              <div className="hidden content">添加新的 Git WebHook</div>
            </div>
          </div>
        </div>
      </div>
    );
  }
});

export default WebHook;
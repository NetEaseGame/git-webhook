import React from 'react';
import { Link } from 'react-router';

import TimeAgo from 'timeago-react';

import OnFireMixin from './mixins/onFireMixin.jsx';
import TipShowMixin from './mixins/tipShowMixin.jsx';
import RequestsMixin from './mixins/xhrRequestsMixin.jsx';


const Server = React.createClass({
  __ONFIRE__: 'Server',
  mixins: [RequestsMixin, OnFireMixin, TipShowMixin],  // 引入 mixin
  getInitialState: function() {
    return {
      showAddForm: false, 
      servers: []
    };
  },
  componentDidMount: function() {
    this.get('/api/server/list', {}, function(r) {
      r = r.json();
      if (r.success) this.setState({servers: r.data});
      else this.showError('加载数据失败！');
    }.bind(this));
  },
  clickNewBtn: function(save) {
    if (save) {
      this.post('/api/server/new', {
        name: this.refs.name.value,
        ip: this.refs.ip.value,
        port: this.refs.port.value,
        account: this.refs.account.value,
        pkey: this.refs.pkey.value
      }, function(r) {
        r = r.json();
        if (r.success) {
          this.refs.addForm.reset();

          let servers = this.state.servers;
          servers.push(r.data);
          this.setState({servers: servers, showAddForm: false});
        }
        else this.showError(r.data);
      }.bind(this));
    }
    else {
      this.setState({showAddForm: true});
    }
  },
  editServer: function(server, index) {
    console.log(server, 'TODO');
  },
  deleteServer: function(server_id, index) {
    this.post('/api/server/delete', {
        server_id: server_id,
      }, function(r) {
        r = r.json();
        if (r.success) {
          let servers = this.state.servers;
          servers.splice(index, 1);
          this.setState({servers: servers, showAddForm: false});
        }
        else this.showError(r.data);
      }.bind(this));
  },
  render: function() {
    return (
      <div className="ui tall stacked segment">
        <h3 className="ui dividing header right aligned">Server List</h3>
        <table className="ui very basic table">
          <thead>
            <tr>
              <th width="5%">#</th>
              <th width="15%">Name</th>
              <th width="20%">IP</th>
              <th width="8%">Port</th>
              <th width="17%">Account</th>
              <th width="10%">PKey</th>
              <th width="15%">Time</th>
              <th width="10%">Operate</th>
            </tr>
          </thead>
          <tbody>
          {
            this.state.servers.map(function(server, i) {
              return (
                <tr key={i}>
                  <td>{server.id}</td>
                  <td>{server.name}</td>
                  <td>{server.ip}</td>
                  <td>{server.port}</td>
                  <td>{server.account}</td>
                  <td>****</td>
                  <td title={server.add_time}><TimeAgo locale='zh_CN' datetime={server.add_time} /></td>
                  <td>
                    <button className="mini ui icon button" onClick={this.editServer.bind(this, server, i)}><i className="ui icon edit"></i></button>
                    <button className="mini ui icon button" onClick={this.deleteServer.bind(this, server.id, i)}><i className="ui icon delete"></i></button>
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
            <h3 className="ui dividing header left aligned">New Server</h3>
            <div className="four fields">
              <div className="field">
                <label>CName</label>
                <input ref="name" type="text" placeholder="Server Name" />
              </div>
              <div className="field">
                <label>Server IP</label>
                <input ref="ip" type="text" placeholder="Server IP" />
              </div>
              <div className="field">
                <label>Server SSH Port</label>
                <input ref="port" type="number" placeholder="Server Port" />
              </div>
              <div className="field">
                <label>Server SSH Account</label>
                <input ref="account" type="text" placeholder="Server Account" />
              </div>
            </div>
            <div className="field">
              <label>SSH Private Key <Link to="/doc/pkey"><i className="ui icon help"></i></Link></label>
              <textarea ref="pkey" rows="6"></textarea>
            </div>
          </form>
        }
        <div className="ui center aligned basic segment">
          <div className="ui center aligned basic segment">
            <div className="ui teal animated fade button mini" onClick={this.clickNewBtn.bind(this, this.state.showAddForm)}>
              <div className="visible content">添加新的 Server</div>
              <div className="hidden content">添加新的 Server</div>
            </div>
          </div>
        </div>
      </div>
    );
  }
});

export default Server;
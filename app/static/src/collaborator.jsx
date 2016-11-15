import React from 'react';
import { Link } from 'react-router';
import OnFireMixin from './mixins/onFireMixin.jsx';
import TipShowMixin from './mixins/tipShowMixin.jsx';
import RequestsMixin from './mixins/xhrRequestsMixin.jsx';
import TimeAgo from 'timeago-react';
import StringUtils from './utils/stringUtils.jsx';

const Collaborator = React.createClass({
  __ONFIRE__: 'Collaborator',
  mixins: [RequestsMixin, OnFireMixin, TipShowMixin],  // 引入 mixin
  getInitialState: function() {
    return {
      collaborators: [],
      showAddForm: false
    };
  },
  loadCollaborators: function() {
    this.get('/api/collaborator/list', {
      webhook_id: this.props.params.webhook_id
    }, function(r) {
      r = r.json();
      if (r.success) {
        this.setState({collaborators: r.data});
      }
      else this.showError('加载数据失败！');
    }.bind(this));
  },
  componentDidMount: function() {
    this.loadCollaborators();
  },
  clickNewBtn: function(save) {
    if (save) {
      this.post('/api/collaborator/new', {
        user_id: this.refs.user_id.value,
        webhook_id: this.props.params.webhook_id
      }, function(r) {
        r = r.json();
        if (r.success) {
          this.refs.addForm.reset();

          let collaborators = this.state.collaborators;
          collaborators.push(r.data);

          this.setState({collaborators: collaborators, showAddForm: false});
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
    this.setState({showAddForm: false});
  },
  deleteCollaborator: function(collaborator_id, index) {
    this.post('/api/collaborator/delete', {
        collaborator_id: collaborator_id,
      }, function(r) {
        r = r.json();
        if (r.success) {
          let collaborators = this.state.collaborators;
          collaborators.splice(index, 1);
          this.setState({collaborators: collaborators, showAddForm: false});
        }
        else this.showError(r.data);
      }.bind(this));
  },
  render: function() {
    return (
      <div className="ui tall stacked segment">
        <h3 className="ui dividing header right aligned">Collaborator List of WebHook #{this.props.params.webhook_id}</h3>
        <table className="ui very basic table">
          <thead>
            <tr>
              <th width="20%">#</th>
              <th width="25%">Name</th>
              <th width="25%">{'Location'}</th>
              <th width="15%">Last Login</th>
              <th width="15%">Add Time</th>
              <th width="10%">Operate</th>
            </tr>
          </thead>
          <tbody>
          {
            this.state.collaborators.map(function(collaborator, i) {
              return (
                <tr key={i}>
                  <td>
                    <img className="ui avatar image" src={collaborator.user.avatar || 'static/res/img/logo.png'} />
                    <span><a target="_blank" href={"https://github.com/" + collaborator.user_id}>{collaborator.user_id || ''}</a></span>
                  </td>
                  <td>
                    {collaborator.user.name || ''}
                  </td>
                  <td>{collaborator.user.location || ''}</td>
                  <td title={collaborator.user.last_login || new Date()}><TimeAgo locale='zh_CN' datetime={collaborator.user.last_login || new Date()} /></td>
                  <td title={collaborator.add_time}><TimeAgo locale='zh_CN' datetime={collaborator.add_time} /></td>
                  <td>
                    <button className="mini ui icon button" onClick={this.deleteCollaborator.bind(this, collaborator.id, i)}><i className="ui icon delete"></i></button>
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
            <h3 className="ui dividing header left aligned">New Collaborator</h3>
            <div className="ui form success">
              <div className="field">
                <label>GitHub User ID</label>
                <input ref="user_id" type="text" placeholder="GitHub User ID" />
              </div>
            </div>
          </form>
        }
        <div className="ui center aligned basic segment">
          <div className="ui center aligned basic segment">
            <div className="ui teal animated fade button mini" onClick={this.clickNewBtn.bind(this, this.state.showAddForm)}>
              <div className="visible content">添加新的 Collaborator</div>
              <div className="hidden content">添加新的 Collaborator</div>
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

export default Collaborator;

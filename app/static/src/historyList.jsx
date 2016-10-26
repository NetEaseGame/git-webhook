import React from 'react';
import { Link } from 'react-router';
import OnFireMixin from './mixins/onFireMixin.jsx';
import TipShowMixin from './mixins/tipShowMixin.jsx';
import RequestsMixin from './mixins/xhrRequestsMixin.jsx';

import TimeAgo from 'timeago-react';
import StringUtils from './utils/stringUtils.jsx';

const HistoryList = React.createClass({
  __ONFIRE__: 'HistoryList',
  mixins: [RequestsMixin, OnFireMixin, TipShowMixin],  // 引入 mixin
  currentPage: 1,
  contextTypes: {
    router: React.PropTypes.object.isRequired
  },
  getInitialState: function() {
    return {
      histories: [],
      has_prev: false,
      has_next: false
    };
  },
  loadHistories: function(page) {
    this.get('/api/history/list', {
      page: page,
      webhook_id: this.props.params.webhook_id
    }, function(r) {
      r = r.json();
      if (r.success) {
        this.currentPage = r.data.page;
        this.setState({
          histories: r.data.histories,
          has_prev: r.data.has_prev,
          has_next: r.data.has_next
        });

        this.context.router.push('/history/' + this.props.params.webhook_id + '/' + this.currentPage);
      }
      else this.showError('加载数据失败！');
    }.bind(this));
  },
  componentDidMount: function() {
    new Clipboard('.copy_btn'); // set copy button

    this.currentPage = this.props.params.page;
    this.loadHistories(this.currentPage);
  },
  clickPrev: function() {
    this.currentPage --;
    this.loadHistories(this.currentPage);
  },
  clickNext: function() {
    this.currentPage ++;
    this.loadHistories(this.currentPage);
  },
  consoleData: function(data) {
    console.log(JSON.parse(data));
    this.showInfo('复制到剪切板，在 Console 打印！');
  },
  render: function() {
    return (
      <div className="ui tall stacked segment">
        <h3 className="ui dividing header right aligned">History List of WebHook #{this.props.params.webhook_id}</h3>
        <div className="ui tiny buttons">
          <button onClick={this.clickPrev} className={this.state.has_prev && 'ui button' || 'ui button disabled'}>上一页</button>
          <div className="or"></div>
          <button onClick={this.clickNext} className={this.state.has_next && 'ui button' || 'ui button disabled'}>下一页</button>
        </div>
        <table className="ui very basic table">
          <thead>
            <tr>
              <th width="10%">#</th>
              <th width="20%">Pusher</th>
              <th width="40%">Shell Log</th>
              <th width="10%">Time</th>
              <th width="10%">Status</th>
              <th width="10%">Data</th>
            </tr>
          </thead>
          <tbody>
          {
            this.state.histories.map(function(history, i) {
              return (
                <tr key={i}>
                  <td>{history.id}</td>
                  <td>{history.push_user}</td>
                  <td><pre className="language-powershell" dangerouslySetInnerHTML={{__html: history.shell_log || 'No log.'}} /></td>
                  <td title={history.add_time}><TimeAgo locale='zh_CN' datetime={history.add_time} /></td>
                  <td>{StringUtils.statusToTag(history.status)}</td>
                  <td>
                    <button className="mini ui icon button copy_btn" 
                            title="Copy Push Data to clipboard!" 
                            data-clipboard-text={history.data}
                            onClick={this.consoleData.bind(this, history.data)}>
                      <i className="ui icon copy"></i> Copy Data
                    </button>
                  </td>
                </tr>
              )
            }.bind(this))
          }
          </tbody>
        </table>
        <div className="ui tiny buttons">
          <button onClick={this.clickPrev} className={this.state.has_prev && 'ui button' || 'ui button disabled'}>上一页</button>
          <div className="or"></div>
          <button onClick={this.clickNext} className={this.state.has_next && 'ui button' || 'ui button disabled'}>下一页</button>
        </div>
      </div>
    );
  }
});

export default HistoryList;
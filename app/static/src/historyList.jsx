import React from 'react';
import { Link } from 'react-router';
import OnFireMixin from './mixins/onFireMixin.jsx';
import TipShowMixin from './mixins/tipShowMixin.jsx';
import RequestsMixin from './mixins/xhrRequestsMixin.jsx';
import LogPreview from './component/logPreview.jsx';

import TimeAgo from 'timeago-react';
import StringUtils from './utils/stringUtils.jsx';
import hrn from 'hrn';

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
  whenHistoryUpdate: function(history) {
    if (history.webhook_id != this.props.params.webhook_id) {
      // 不匹配，不处理
      return;
    }
    let histories = this.state.histories;
    for (let i = histories.length - 1; i >= 0; i--) {
      if (histories[i].id == history.id) {
        histories[i] = history;
        this.setState({histories: histories});
        return;
      }
    }
    // 在 histories 中找不到，则直接添加
    // 添加 在数组最前面
    histories.unshift(history);
    // 去掉最后一个元素
    histories.pop();
    this.setState({histories: histories});
  },
  componentDidMount: function() {
    new Clipboard('.copy_btn'); // set copy button

    this.currentPage = this.props.params.page;
    this.loadHistories(this.currentPage);

    this.on('history-websocket', this.whenHistoryUpdate);
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
              <th width="18%">Pusher</th>
              <th width="35%">Shell Log</th>
              <th width="17%">Time</th>
              <th width="10%">Status</th>
              <th width="10%">Data</th>
            </tr>
          </thead>
          <tbody>
          {
            this.state.histories.map(function(history, i) {
              let diff_sec = (new Date(history.update_time || history.add_time) - new Date(history.add_time)) / 1000;
              if (diff_sec < 1) diff_sec = 1;
              return (
                <tr key={i}>
                  <td>{history.id}</td>
                  <td>{history.push_user}</td>
                  <td>
                    <LogPreview log={history.shell_log} />
                  </td>
                  <td title={history.add_time}>
                    <span title={diff_sec + ' sec'}>{ hrn(diff_sec, 1, [['s', 'm', 'h', 'd'], [1, 60, 60, 24]])}</span>
                    &nbsp; @ &nbsp; 
                    <TimeAgo locale='zh_CN' datetime={history.add_time} />
                  </td>
                  <td>{StringUtils.statusToTag(history.status)}</td>
                  <td>
                    <button className="mini ui icon button copy_btn" 
                            title="Copy Push Data to clipboard!" 
                            data-clipboard-text={history.data}
                            onClick={this.consoleData.bind(this, history.data)}>
                      <i className="ui icon copy"></i> Copy
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

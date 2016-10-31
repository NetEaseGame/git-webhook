import React from 'react';
import StringUtils from '../utils/stringUtils.jsx';
import pys from 'pys';

const LogPreview = React.createClass({
  propTypes: {
    log: React.PropTypes.string,
  },
  getInitialState: function() {
    return {showAll: false};
  },
  showToggle: function() {
    this.setState({showAll: !this.state.showAll})
  },
  render: function() {
    let html = this.props.log;
    let longLog = false;
    if (this.props.log && this.props.log.length >= 100) {
      longLog = true;
      if (! this.state.showAll) {
        html = pys(this.props.log)('0:100') + '...';
      }
    }
    html = html || 'No log.';
    return (
      <div className="ui segment">
        <pre className="language-powershell" dangerouslySetInnerHTML={{__html: html}} />
        { longLog &&
          <div className="ui bottom right attached label pointer" onClick={this.showToggle}> Show All / Lite</div>
        }
      </div>
    );
  }
});

export default LogPreview;
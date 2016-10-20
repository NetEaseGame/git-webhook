import React from 'react';
import OnFireMixin from '../mixins/onFireMixin.jsx';

const Alert = React.createClass({
  __ONFIRE__: 'Alert',
  mixins: [OnFireMixin],
  propTypes: {
  },
  getInitialState: function() {
    return {
      show: false, tip: '', type: 'info'  // error, warning, success, info
    };
  },
  componentWillReceiveProps: function(nextProps) {
  },
  componentDidMount: function() {
    this.on('show_alert', this.showAlert);
  },
  componentWillUnmount: function() {
    if (this.timer) {
      clearInterval(this.timer);
    }
  },
  showAlert: function(data){
    this.setState({show: true, tip: data.tip, type: data.type});

    if (this.timer) {
      clearInterval(this.timer);
    }
    this.timer = setTimeout(function(){
      this.setState({show: false});
    }.bind(this), 2000);

  },
  render() {
    let display = {"display": "none"};

    let colorDict = {
      'success': 'green',
      'warning': 'yellow',
      'error': 'red',
      'info': 'blue',
    };

    if (this.state.show) {
      display = {"display": "block"};
    }
    let className = 'ui ' + colorDict[this.state.type] + ' compact message';
    return (
      <div className={className} style={display} id="custom_alert">
        <p>{this.state.tip}</p>
      </div>
    );
  }
});

export default Alert;


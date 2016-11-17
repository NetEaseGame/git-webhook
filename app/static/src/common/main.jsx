import React from 'react';

import Header from './header.jsx';
import Footer from './footer.jsx';
import Alert from './alert.jsx';
import WebHook from '../webHook.jsx';
import Index from '../index.jsx';
import OnFireMixin from '../mixins/onFireMixin.jsx';

const MainComponent = React.createClass({
  socketio: null,
  __ONFIRE__: 'MainComponent',
  mixins: [OnFireMixin],  // 引入 mixin
  socketioCallback: function(type, data) {
    this.fire(type + '-websocket', JSON.parse(data));
  },
  componentDidMount: function() {
    this.socketio = io.connect(location.protocol + '//' + location.host);
    this.socketio.on('connect', function(d) {
      console.log(d);
    });

    ['webhook', 'history'].map(function(e) {
      this.socketio.on(e, this.socketioCallback.bind(this, e));
    }.bind(this));
  },
  componentWillUnmount: function() {
    if (this.socketio) this.socketio.disconnect();
    this.socketio = null;
  },
  // random bg
  getBgImgUrl: function() {
    return 'url(/static/res/img/bg' + new Date().getHours() % 5 + '.jpg)';
  },
  render: function() {
    let children = this.props.children;
    if (children) 
      return (
        <div className="ui main main-content" id="main_content" style={{backgroundImage: this.getBgImgUrl()}}>
          <Header />
          <div className="ui container content">
            { children }
          </div>
          <Footer />
          <Alert />
        </div>
      );
    return (<Index />);
  }
});

export default MainComponent;
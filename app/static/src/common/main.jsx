import React from 'react';

import Header from './header.jsx';
import Footer from './footer.jsx';
import Alert from './alert.jsx';
import WebHook from '../webHook.jsx';
import Index from '../index.jsx';

const MainComponent = React.createClass({
  // random bg
  getBgImgUrl: function() {
    return 'url(/static/res/img/bg' + new Date().getHours() % 5 + '.jpg)';
  },
  render: function() {
    let children = this.props.children || <Index />; 
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
  }
});

export default MainComponent;
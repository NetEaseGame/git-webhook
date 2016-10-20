import React from 'react';

import Header from './header.jsx';
import Footer from './footer.jsx';
import Alert from './alert.jsx';
// 首页
import IndexComponent from './index.jsx';

const MainComponent = React.createClass({
  getBgImgUrl: function() {
    return 'url(/static/res/img/bg' + new Date().getHours() % 5 + '.jpg)';
  },
  render: function() {
    let children = this.props.children; // 首页做好之后，去掉 || 之后的东西即可
    // 首页和内页风格大有不同
    if (children) {
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
    else {
      return (
        <IndexComponent />
      );
    }
  }
});

export default MainComponent;
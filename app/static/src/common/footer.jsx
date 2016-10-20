import React from 'react';

const Footer = React.createClass({
  propTypes: {
  },
  render: function() {
    return (
      <div className="ui inverted vertical footer segment">
        <div className="ui center aligned container">
          <div className="ui horizontal inverted small divided link list">
            <span>&copy; 2016 网易公司版权所有 &hearts; POPO群：<strong>xxxxxx</strong> &hearts;</span>
          </div>
        </div>
      </div>
    )
  }
});

export default Footer;
import React from 'react';

const Footer = React.createClass({
  render: function() {
    return (
      <div className="ui inverted vertical footer segment">
        <div className="ui center aligned container">
          <div className="ui horizontal inverted small divided link list">
            <span>&copy; 2016 &hearts;<a target="_blank" href="https://github.com/hustcc"> Hustcc </a>&hearts; 版权所有</span>
          </div>
        </div>
      </div>
    )
  }
});

export default Footer;
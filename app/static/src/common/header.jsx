import React from 'react';
import StringUtils from '../utils/stringUtils.jsx';
import { Link } from 'react-router';

const Header = React.createClass({
  componentDidMount: function() {
    $(this.refs.user_action).dropdown();
  },
  renderUserActionComp: function() {
    if (loginUser && loginUser.id) {
      return (
        <div className="ui pointing dropdown link item" ref="user_action">
          <span className="text">{loginUser.name}</span>
          <i className="dropdown icon"></i>
          <div className="menu">
            <a href="/logout" className="item"><i className="sign out icon"></i>Log out</a>
          </div>
        </div>
      )
    } 
    return (
      <a href="/login" className="item">登录</a>
    )
  },
  render: function() {
    return (
      <div className="ui fixed inverted menu">
        <div className="ui container">
          <Link to="/" className="header item">
            <img className="logo" width="32" height="32" src="static/res/img/logo.png" />
          </Link>
          <Link to="/" className="header item">Home</Link>
          <Link to="/webhook" className="header item">Git WebHook</Link>
          <Link to="/server" className="header item">Server</Link>
          <Link to="/doc" className="header item">Documents</Link>
          
          <div className="right menu">
            <a href="#" className="item">
              <img className="logo" width="32" height="32" src={loginUser.avatar} />
            </a>
            {this.renderUserActionComp()}
          </div>
        </div>
      </div>
    )
  }
});

export default Header;
import React from 'react';
import StringUtils from '../utils/stringUtils.jsx';
import { Link } from 'react-router';

const Header = React.createClass({
  propTypes: {},
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
            <a href="http://avatar.163-inc.com" target="_blank" className="item"><i className="user icon"></i>修改头像</a>
            <a href="/logout.html" className="item"><i className="sign out icon"></i>Log out</a>
          </div>
        </div>
      )
    } 
    return (
      <a href="/login.html" className="item">登录</a>
    )
  },
  render: function() {
    return (
      <div className="ui fixed inverted menu">
        <div className="ui container">
          <Link to="/" className="header item">
            <img className="logo" width="32" height="32" src="static/res/img/logo.png" />
          </Link>
          <Link to="/" className="header item">MTL Automation</Link>
          <Link to="/status" className="header item">系统状态</Link>
          <Link to="/document" className="header item">文档</Link>
          <div className="right menu">
            <a href="#" className="item">
              {StringUtils.avatarImg(loginUser.id, 32)}
            </a>
            {this.renderUserActionComp()}
          </div>
        </div>
      </div>
    )
  }
});

export default Header;
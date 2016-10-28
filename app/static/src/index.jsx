import React from 'react';
import { Link } from 'react-router';
import StringUtils from './utils/stringUtils.jsx';
require('../res/css/index.css');

const Index = React.createClass({
  render: function() {
    return (
      <div className="pusher">
        <div className="ui inverted vertical masthead center aligned segment">
          <div className="ui container">
            <div className="ui large secondary inverted pointing menu">
              <a className="active header item">Home</a>
              <a target="_blank" href="https://github.com/NetEaseGame/git-webhook" className="header item">Source on GitHub</a>
              <a target="_blank" href="https://github.com/hustcc" className="header item">Me</a>
              <Link to="/doc" className="header item">Documents</Link>
            </div>
          </div>

          <div className="ui text container">
            <h1 className="ui inverted header">
              Git WebHook
            </h1>
            <h2>GitHub / GitLab / Gogs / GitOsc are all supported.</h2>
            {
              loginUser && loginUser.id &&
                <Link to="/webhook" className="ui huge primary button">
                  <i className="dashboard icon"></i> 
                  DashBoard &nbsp;&nbsp;
                  <i className="dashboard icon"></i>
                </Link>
              ||
                <a href="/login" className="ui huge primary button">
                  <i className="github alternate icon"></i> 
                  &nbsp;&nbsp; Login Github &nbsp;&nbsp;
                  <i className="github alternate icon"></i>
                </a>
            }
          </div>
        </div>

        <div className="ui vertical stripe quote segment">
          <div className="ui equal width stackable internally celled grid">
            <div className="center aligned row">
              <div className="column">
                <h3>"Git WebHook to auto-deploy."</h3>
                <p>GitHub / GitLab / Gogs / GitOsc are supported.</p>
              </div>
              <div className="column">
                <h3>"Any hook has it's status."</h3>
                <p>
                  {
                    [1,2,3,4,5,6].map(function(status, i) {
                      return StringUtils.statusToTag(status);
                    })
                  }
                </p>
              </div>
            </div>
          </div>
        </div>

        <div className="ui vertical stripe segment">
          <div className="ui text container">
            <h3 className="ui header">Open Source can get more ?</h3>
            <p>The background-end base on Flask, SQLAchemy, Celery, Redis.</p>
            <p>The front-end React, semantic-ui and other javascript library.</p>
            <a target="_blank" href="https://github.com/NetEaseGame/git-webhook" className="ui large button">Read More</a>
          </div>
        </div>
      </div>
    );
  }
});

export default Index;
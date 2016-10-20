import React from 'react';
import { Link } from 'react-router';

const IndexComponent = React.createClass({
  render: function() {
    return (
      <div className="ui tall stacked segment">
        <div className="ui medium header">MTL Automation</div>
        <ol className="ui list">
          <li><strong><Link to="/">Index</Link></strong></li>
          <li><strong><Link to="/dashboard">DashBoard</Link></strong></li>
          <li><strong><Link to="/doc">Documents</Link></strong></li>
        </ol>
      </div>
    );
  }
});

export default IndexComponent;
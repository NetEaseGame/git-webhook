import React from 'react';
import { Link } from 'react-router';
import OnFireMixin from '../mixins/onFireMixin.jsx';

const Breadcrumb = React.createClass({
  __ONFIRE__: 'Breadcrumb',
  mixins: [OnFireMixin],  // 引入 mixin
  propTypes: {
    crumb: React.PropTypes.arrayOf(React.PropTypes.array)
  },
  getDefaultProps: function() {
    return {crumb: []};
  },
  componentWillMount: function() {
    this.setState({crumb: this.props.crumb});
    // 监控消息
    this.on('crumb', function(data) {
      this.setState({crumb: data});
    }.bind(this));
  },
  render: function() {
    const crumbSize = this.state.crumb.length;
    return (
      <div className="ui large breadcrumb">
        <Link className="section" to='/dashboard'>DashBoard</Link>
        {
          this.state.crumb.map(function(e, i) {
            let className = 'section';
            if (i == crumbSize - 1) {className = 'section active'}
            return (
              <span key={i}>
                <div className="divider"> / </div>
                <Link to={e[1]} className={className}>{e[0]}</Link>
              </span>
            )
          })
        }
      </div>
    );
  }
});

export default Breadcrumb;
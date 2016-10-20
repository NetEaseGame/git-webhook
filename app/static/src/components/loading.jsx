import React from 'react';

const Loading = React.createClass({
  propTypes: {
    loading: React.PropTypes.bool,
    tip: React.PropTypes.string,
  },
  componentDidUpdate: function(prevProps, prevState) {
    let className = "ui dimmer";
    if (this.props.loading) {
      className = "ui active dimmer";
    }
    this.refs.loading.className = className;
  },
  render: function() {
    return (
      <div className="" ref="loading">
        <div className="ui text loader">{this.props && 'loading...^_^!!'}</div>
      </div>
    );
  }
});

export default Loading;
import React from 'react';

const Paginate = React.createClass({
  propTypes: {
    total: React.PropTypes.number, // 总数据记录数
    page_size: React.PropTypes.number, // 总的数据页数
    current: React.PropTypes.number, // 当前所在的页数
    onClickPaginate: React.PropTypes.func, // 当前所在的页数
  },
  getInitialState: function() {
    return { total: this.props.total, page_size: this.props.page_size, current: this.props.current };
  },
  componentDidUpdate: function(prevProps, prevState) {
  },
  componentWillReceiveProps: function(nextProps) {
    this.setState(nextProps);
  },
  renderPaginate: function(page_num, p, i) {
    if (p >= 1 && p <= page_num) {
      let selected = false;
      let className = "ui compact label button";
      if (p == this.state.current) {
        selected = true;
        className = "ui compact label blue button";
      }
      return (
        <button key={i} disabled={selected} 
                className={className}
                onClick={this.onBtnClick.bind(this, p)}>{p}</button>
      )
    }
  },
  onBtnClick: function(page) {
    this.props.onClickPaginate(page);
  },
  render: function() {
    let left = true; // 左侧显示省略号
    let right = true; // 右侧显示省略号
    let page_num = parseInt((this.state.total - 1) / this.state.page_size) + 1
    if (this.state.current - 1 < 2) left = false;
    if (page_num - this.state.current < 2) right = false;

    let left_disabled = true;
    let right_disabled = true;
    if (this.state.current != 1) {
      left_disabled = false;
    }
    if (this.state.current != page_num && page_num != 0) {
      right_disabled = false;
    }

    let pages = new Array(this.state.current - 1, this.state.current, this.state.current + 1);

    return (
      <div className="ui buttons">
        <button disabled={left_disabled} 
                className="ui compact icon button"
                onClick={this.onBtnClick.bind(this, 1)}>
          <i className="angle double left icon"></i>
        </button>
        <button disabled={left_disabled} 
                className="ui compact icon button"
                onClick={this.onBtnClick.bind(this, this.state.current - 1)}>
          <i className="left angle icon"></i>
        </button>
        { left &&
          <button disabled="true" className="ui compact label button">...</button>
        }
        {
          pages.map(this.renderPaginate.bind(this, page_num))
        }
        
        { right &&
          <button disabled="true" className="ui compact label button">...</button>
        }
        <button disabled={right_disabled} 
                className="ui compact icon button"
                onClick={this.onBtnClick.bind(this, this.state.current + 1)}>
          <i className="right angle icon"></i>
        </button>
        <button disabled={right_disabled} 
                className="ui compact icon button"
                onClick={this.onBtnClick.bind(this, page_num)}>
          <i className="angle double right icon"></i>
        </button>
      </div>
    );
  }
});

export default Paginate;
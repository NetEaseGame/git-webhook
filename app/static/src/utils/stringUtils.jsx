import React from 'react';

let StringUtils = {
  statusToTag: function(status) {
    status = parseInt(status);
    let text, className;
    if (status == 1) {
      text = '等待';
      className = 'compact ui mini blue tag label';
    }
    else if (status == 2) {
      text = '执行';
      className = 'compact ui mini yellow tag label';
    }
    else if (status == 3) {
      text = '失败';
      className = 'compact ui mini red tag label';
    }
    else if (status == 4) {
      text = '成功';
      className = 'compact ui mini green tag label';
    }
    else if (status == 5) {
      text = '异常';
      className = 'compact ui mini red tag label';
    }
    else {
      text = '未知';
      className = 'compact ui mini grey tag label';
    }
    return (<span className={className}>{text}</span>);
  }
}

export default StringUtils;
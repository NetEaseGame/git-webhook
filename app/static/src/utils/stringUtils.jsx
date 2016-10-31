import React from 'react';
import pys from 'pys';

let StringUtils = {
  statusToTag: function(status) {
    status = parseInt(status);
    let text, color;
    if (status == 1) {
      text = '等待';
      color = 'blue';
    }
    else if (status == 2) {
      text = '执行';
      color = 'yellow';
    }
    else if (status == 3) {
      text = '失败';
      color = 'red';
    }
    else if (status == 4) {
      text = '成功';
      color = 'green';
    }
    else if (status == 5) {
      text = '异常';
      color = 'red';
    }
    else {
      text = '未知';
      color = 'grey';
    }
    return (<span className={'compact ui mini tag label ' + color}>{text}</span>);
  }
}

export default StringUtils;
import React from 'react';

let StringUtils = {
  isEmpty: function(input) {
    if (input == null || input == undefined) return true;

    let type = typeof input;
    if (type === 'string' && input == '') return true;
    if (type === 'object') {
      for (let key in input) {
        // 只要有一个元素，就不是空
        return false;
      }
      return true;
    }
    return false;
  },
  // 字符串为null
  isNone: function(str) {
    if (str == null || str == undefined) {
      return true;
    }
    return false;
  },
  startWith: function(str, needle) {
    if (isNone(str) || isNone(needle)) {
      return false;
    }
    if (str.indexOf(needle) === 0) {
      return true;
    }
    return false;
  }
}

export default StringUtils;
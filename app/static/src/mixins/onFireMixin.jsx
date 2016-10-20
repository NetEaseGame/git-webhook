import onfire from 'onfire.js';

let OnFireMixin = {
  bindingEvents: {}, // 缓存这个组件绑定的事件，用于在组建取消的时候结束八达岭
  // 绑定事件
  on: function(eventName, callback) {
    let eventObject = onfire.on(eventName, callback);

    // 如果为空，则设置为数组
    if (! this.bindingEvents[this.__ONFIRE__]) {
      this.bindingEvents[this.__ONFIRE__] = {};
    }
    this.bindingEvents[this.__ONFIRE__][eventObject[1]] = eventObject;

    return eventObject;
  },
  // 取消绑定事件
  un: function(eventObject) {
    if (this.bindingEvents[this.__ONFIRE__]) {
      delete this.bindingEvents[this.__ONFIRE__][eventObject[1]];
      return onfire.un(eventObject);
    }
    return true;
  },
  // 触发事件
  fire: function(eventName, data) {
    return onfire.fire(eventName, data);
  },

  componentDidMount: function() {
    // 校验有没有__ONFIRE__属性
    if (! this.__ONFIRE__) {
      throw new Error('Component should has attribute __ONFIRE__ if you want to use OnFireMixin.');
    }
  },
  // when unmont, un all the event
  componentWillUnmount: function() {
    if (this.bindingEvents[this.__ONFIRE__]) {
      for (let key in this.bindingEvents[this.__ONFIRE__]) {
        this.un(this.bindingEvents[this.__ONFIRE__][key]);
      }
    }
  }
}

export default OnFireMixin;
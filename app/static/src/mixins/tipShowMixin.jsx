import StringUtils from '../utils/stringUtils.jsx';

/*
一个用于提示的Mixin，如何使用？
1. 在component中引入本文件，得到 TipShowMixin 的变量
2. 在组件中添加： mixins: [TipShowMixin],
3. 在需要提示信息的地方加上ref="tip*",即使用以tip开头的任意字符串作为dom的ref
4. 同时设置这个ref的data-content="需要提示的字符串"
*/
let TipShowMixin = {
  renderTip: function() {
    for (let key in this.refs) {
      if (key.indexOf('tip') === 0 && (!StringUtils.isEmpty(this.refs[key].getAttribute('data-content')))) {
        // 以tip开头的dom组件，并且有data-content属性，全部都是需要提示的
        let position = this.refs[key].getAttribute('data-position');
        if(position != null && position != ''){
          $(this.refs[key]).popup({inline: true, hoverable: true, position : position});
        }else{
          $(this.refs[key]).popup({inline: true, hoverable: true, position : 'bottom left'});
        }
        
      }
    }
  },
  // 显示一些提示框
  componentDidMount: function() {
    this.renderTip();
  },

  showWarning: function(msg) {
  	this.fire('show_alert', {tip: msg, type: 'warning'});
  },
  showError: function(msg) {
  	this.fire('show_alert', {tip: msg, type: 'error'});
  },
  showSuccess: function(msg) {
  	this.fire('show_alert', {tip: msg, type: 'success'});
  },
  showInfo: function(msg) {
    this.fire('show_alert', {tip: msg, type: 'info'});
  }
}
export default TipShowMixin;
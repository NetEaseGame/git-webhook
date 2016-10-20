import timeagoJS from 'timeago.js';

let DateUtils = {
  timeago: function(date, local) {
    if (!local) local = 'zh_CN';
    return timeagoJS().format(date, local);
  },
  formatSec: function(sec) {
    sec = Number(sec).toFixed(1);
    if (sec < 60) {
      return sec + '秒'
    }
    else {
      sec = Number(sec / 60).toFixed(1);
      // 小于1小时
      if (sec < 60) {
        return sec + '分钟';
      }
      else {
        sec = Number(sec / 60).toFixed(1);
        // 小于24小时
        return sec + '小时';
      }
    }
  },
  formatDate: function(date, fmt) {
    if (!fmt) fmt = 'yyyy-MM-dd';
    var o = {
        "M+": date.getMonth() + 1, //月份 
        "d+": date.getDate(), //日 
        "h+": date.getHours(), //小时 
        "m+": date.getMinutes(), //分 
        "s+": date.getSeconds(), //秒 
        "q+": Math.floor((date.getMonth() + 3) / 3), //季度 
        "S": date.getMilliseconds() //毫秒 
    };
    if (/(y+)/.test(fmt)) fmt = fmt.replace(RegExp.$1, (date.getFullYear() + "").substr(4 - RegExp.$1.length));
    for (var k in o)
    if (new RegExp("(" + k + ")").test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
    return fmt;
  },
  parseDate: function(input) {
    if (input instanceof Date) {
      return input;
    } else if (!isNaN(input)) {
      return new Date(input);
    } else if (/^\d+$/.test(input)) {
      return new Date(parseInt(input, 10));
    } else {
      var s = (input || '').trim();
      s = s.replace(/\.\d+/, ''); // remove milliseconds
      s = s.replace(/-/, '/').replace(/-/, '/');
      s = s.replace(/T/, ' ').replace(/Z/, ' UTC');
      s = s.replace(/([\+\-]\d\d)\:?(\d\d)/, ' $1$2'); // -04:00 -> -0400
      return new Date(s);
    }
  },
   dateDiff: function(d1, d2) {
    if(!d1 || !d2) {
      return '未知';
    }
    d1 = this.parseDate(d1);
    d2 = this.parseDate(d2);
    let diff = (d1.getTime() - d2.getTime()) / 1000; // 相差的毫秒数
    return this.formatSec(diff);
  },
  week2String: function(week_index) {
    switch (week_index) {
      case 1:
        return '周一';
      case 2:
        return '周二';
      case 3:
        return '周三';
      case 4:
        return '周四';
      case 5:
        return '周五';
      case 6:
        return '周六';
    }
    return '周日';
  },
  string2Week: function(s) {
    switch (week_index) {
      case '周一':
        return 1;
      case '周二':
        return 2;
      case '周三':
        return 3;
      case '周四':
        return 4;
      case '周五':
        return 5;
      case '周六':
        return 6;
      default:
        return 0;
    }
    return 0;
  },
  hour2String: function(hour) {
    if(! hour) hour = 0;
    if (hour < 10) {
      hour = '0' + hour;
    }
    return hour + ':00';
  },
  string2Hour: function(s) {
    s = s.split(':')[0];
    return parseInt(s);
  },
  getWeekday: function(date) {
    var yyyy = date.split('-')[0];
    var mm = date.split('-')[1];
    var dd = date.split('-')[2];
    date = mm + '/' + dd +'/' + yyyy;
    var day = new Date(date);
    return this.week2String(day.getDay());
  }
}

export default DateUtils;
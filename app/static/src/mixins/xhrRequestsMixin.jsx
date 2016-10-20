import XHR from 'xhr.js';

let RequestsMixin = {
  xhrs: Array(),
  // get method
  get: function(url, params, success, failed) {
    let xhr = XHR();
    xhr.on('error', failed);
    xhr.on('fail', failed);

    this.xhrs.push(xhr);

    xhr.get(url, params, success);
  },
  // post method
  post: function(url, params, success, failed) {
    let xhr = XHR();
    xhr.on('error', failed);
    xhr.on('fail', failed);

    this.xhrs.push(xhr);

    xhr.post(url, params, success);
  },

  componentDidMount: function() {
  },
  // when unmont, abort all the request.
  componentWillUnmount: function() {
    this.xhrs.map(function(xhr) {
      xhr.abort();
      xhr = null;
    });
    this.xhrs = Array();
  }
}

export default RequestsMixin;
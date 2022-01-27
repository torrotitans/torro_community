export const setCookie = (name, value, time) => {
  var exp = new Date();
  exp.setTime(time || exp.getTime() + 60 * 60 * 1000);
  document.cookie =
    name + "=" + escape(value) + ";expires=" + exp.toGMTString();
};

export const getCookie = (name) => {
  var arr,
    reg = new RegExp("(^| )" + name + "=([^;]*)(;|$)");
  /* eslint-disable */
  return (arr = document.cookie.match(reg)) ? unescape(arr[2]) : null;
  /* eslint-disable */
};

export const delCookie = (name) => {
  var exp = new Date();
  exp.setTime(exp.getTime() - 1);
  var cval = getCookie(name);
  if (cval != null)
    document.cookie = name + "=" + cval + ";expires=" + exp.toGMTString();
};

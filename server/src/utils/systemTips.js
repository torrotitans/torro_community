/* third lib*/
import React from "react";
import ReactDOM from "react-dom";

/* material-ui */
import SystemTips from "@basics/SystemTips";

const ID = "system-tips";

export const closeTips = () => {
  const el = document.getElementById(ID);
  if (!el) {
    return;
  }
  ReactDOM.unmountComponentAtNode(el);
  setTimeout(() => {
    el.parentNode.removeChild(el);
  });
};

export const openTips = (options = {}) => {
  if (document.getElementById(ID)) {
    return;
  }

  const el = document.createElement("div");
  el.id = ID;
  ReactDOM.render(<SystemTips handleClose={closeTips} {...options} />, el);
  const parent = document.querySelector("#root");
  parent.insertBefore(el, parent.firstChild);
};

export default {
  openTips,
  closeTips,
};

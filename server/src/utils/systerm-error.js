/* third lib*/
import React from "react";
import ReactDOM from "react-dom";

/* material-ui */
import GlobalNotification from "@basics/GlobalNotification";

const ID = "system-error";

export const closeNotify = () => {
  const el = document.getElementById(ID);
  if (!el) {
    return;
  }
  ReactDOM.unmountComponentAtNode(el);
  setTimeout(() => {
    el.parentNode.removeChild(el);
  });
};

export const sendNotify = (options = {}) => {
  if (document.getElementById(ID)) {
    ReactDOM.render(
      <GlobalNotification handleClose={closeNotify} {...options} />,
      document.getElementById(ID)
    );
    return;
  }

  const el = document.createElement("div");
  el.id = ID;
  ReactDOM.render(
    <GlobalNotification handleClose={closeNotify} {...options} />,
    el
  );
  const parent = document.querySelector("#root");
  parent.insertBefore(el, parent.firstChild);
};

export default {
  sendNotify,
  closeNotify,
};

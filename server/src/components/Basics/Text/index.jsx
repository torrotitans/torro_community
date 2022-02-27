/* third lib */
import React from "react";
import cn from "classnames";

/* local components and methods */
import styles from "./styles.module.scss";
const Text = ({ type, title, className, children }) => {
  return (
    <span
      title={title}
      className={cn(className, styles[type], styles.fontFamily)}
    >
      {children}
    </span>
  );
};

Text.defaultProps = {
  type: "regular",
};

export default Text;

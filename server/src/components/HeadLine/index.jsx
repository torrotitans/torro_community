/* third lib */
import React from "react";

/* local components & methods */
import styles from "./styles.module.scss";

const HeadLine = ({ children }) => {
  return <h1 className={styles.headline}>{children}</h1>;
};

export default HeadLine;

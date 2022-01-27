import React from "react";
import styles from "./styles.module.scss";
const Frequently = () => {
  return (
    <div className={styles.frequently}>
      <div className={styles.frequentForm}>Add user to use case</div>
      <div className={styles.frequentForm}>Raise a new Jupyter notebook</div>
    </div>
  );
};

export default Frequently;

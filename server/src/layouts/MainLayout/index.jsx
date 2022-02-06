import React from "react";
import { Outlet } from "react-router-dom";
import styles from "./styles.module.scss";

const MainLayout = () => {
  return (
    <div className={styles.root}>
      <div className={styles.wrapper}>
        <div className={styles.contentContainer}>
          <div className={styles.content}>
            <Outlet />
          </div>
        </div>
      </div>
    </div>
  );
};

export default MainLayout;

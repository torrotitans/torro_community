/* third lib */
import React from "react";
import { Outlet } from "react-router-dom";

/* local components & methods */
import styles from "./styles.module.scss";
import withAuthentication from "src/hoc/withAuthentication";

const DashboardLayout = () => {
  return (
    <div className={styles.dashboardLayout}>
      <div className={styles.wrapper}>
        <div className={styles.content}>
          <Outlet />
        </div>
      </div>
    </div>
  );
};

export default withAuthentication(DashboardLayout);

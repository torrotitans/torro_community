/* third lib*/
import React, { useState, useCallback } from "react";
import styles from "./styles.module.scss";
import cn from "classnames";

/* material-ui */

/* local Component*/
// import Frequently from "./Frequently";
import RecordTable from "./RecordTable";
import Text from "@basics/Text";
// import { getQueryString } from "src/utils/url-util.js";

const DataUserView = () => {
  // const requestorView = getQueryString("requestor");
  const [currentTab, setCurrentTab] = useState(2);

  const tabList = [
    // { label: "Frequently used forms", value: 1 },
    { label: "Your Requests", value: 2 },
    { label: "Waiting Your Approval", value: 3 },
  ];

  const tabClickHandle = useCallback((value) => {
    setCurrentTab(value);
  }, []);

  const currentContent = useCallback(() => {
    switch (currentTab) {
      case 2:
        return <RecordTable />;
      case 3:
        return <RecordTable approved />;
      default:
      // return <Frequently />;
    }
  }, [currentTab]);

  return (
    <div className={styles.dataUserView}>
      <div className={styles.dataContent}>
        <div className={styles.tab}>
          {tabList.map((item) => {
            return (
              <div
                key={item.label}
                onClick={() => {
                  tabClickHandle(item.value);
                }}
                className={cn(styles.tabItem, {
                  [styles["active"]]: item.value === currentTab,
                })}
              >
                <Text type="subTitle">{item.label}</Text>
              </div>
            );
          })}
        </div>
        <div className={styles.tabContent}>{currentContent()}</div>
      </div>
    </div>
  );
};

export default DataUserView;

/* third lib*/
import React, { useMemo } from "react";
import styles from "./styles.module.scss";

const ProgressBar = ({ progress }) => {
  const progressPercent = useMemo(() => {
    let unit = 100 / progress.length;
    let count = 1;
    let countIndex = 0;
    progress.forEach((item, index) => {
      if (!!item.time) countIndex = index;
    });
    return unit * (count + countIndex);
  }, [progress]);

  return (
    <div className={styles.progressBar}>
      <div className={styles.flowDotList}>
        {progress.map((item, index) => {
          return (
            <div key={index} className={styles.flowItem}>
              <div className={styles.dot}>
                <div className={styles.progressItem}>
                  <div className={styles.progressName}>{item.label}</div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
      <div className={styles.progressLine}>
        <div className={styles.progressLineHolder}>
          <div
            className={styles.cover}
            style={{ height: progressPercent + "%" }}
          ></div>
        </div>
      </div>
    </div>
  );
};

export default ProgressBar;

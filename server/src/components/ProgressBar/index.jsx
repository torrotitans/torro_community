/* third lib*/
import React, { useMemo } from "react";
import styles from "./styles.module.scss";

const ProgressBar = ({ progress }) => {
  const progressPercent = useMemo(() => {
    let unit = 100 / progress.length;
    let count = 1;
    let countIndex = 0;
    progress.forEach((item, index) => {
      if (!!item.time) {
        if (index === progress.length - 1) {
          countIndex = progress.length - 1;
        } else {
          if (index === progress.length - 2) {
            countIndex = index;
          } else {
            countIndex = index + 1;
          }
        }
      }
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
                  <div title={item.label} className={styles.progressName}>
                    {item.label}
                  </div>
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

/* third lib*/
import React, { useMemo, useState } from "react";
import styles from "./styles.module.scss";
import { FormattedMessage as Intl } from "react-intl";
import Model from "@basics/Modal";

import Text from "@basics/Text";

const ProgressBar = ({ progress, stagesLog }) => {
  const [open, setOpen] = useState(false);

  const currentStepCount = useMemo(() => {
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
    return count + countIndex;
  }, [progress]);

  const progressPercent = useMemo(() => {
    let unit = 100 / progress.length;

    return unit * currentStepCount;
  }, [progress.length, currentStepCount]);

  return (
    <div className={styles.progressBar}>
      <div className={styles.flowDotList}>
        {progress.map((item, index) => {
          return (
            <div key={index} className={styles.flowItem}>
              <div className={styles.dot}>
                <div className={styles.progressItem}>
                  <div title={item.label} className={styles.progressName}>
                    <div className={styles.mainContent}>
                      {item.label}
                      {currentStepCount - 1 === index && (
                        <span
                          className={styles.viewLog}
                          onClick={() => {
                            setOpen(true);
                          }}
                        >
                          <Intl id="viewLog" />
                        </span>
                      )}
                    </div>
                    {item.adgroup && (
                      <div className={styles.subContent}>
                        <Intl id="adGroup" />
                        {item.adgroup}
                      </div>
                    )}
                    {item.operator && (
                      <div className={styles.subContent}>
                        <Intl id="approvedBy" />
                        {item.operator}
                      </div>
                    )}
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
      <Model
        open={open}
        handleClose={() => {
          setOpen(false);
        }}
      >
        <div className={styles.modalContent}>
          {stagesLog && (
            <div className={styles.logContent}>
              {stagesLog.map((item, index) => {
                return (
                  <div key={index} className={styles.stageLog}>
                    <div className={styles.stageTitile}>
                      <Text type="subTitle">{item.apiTaskName}</Text>
                    </div>
                    {item.logs && (
                      <div className={styles.stageLog}>{item.logs}</div>
                    )}
                    {!item.logs && (
                      <div className={styles.stageLog}>
                        <Intl id="noLogs" />
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </Model>
    </div>
  );
};

export default ProgressBar;

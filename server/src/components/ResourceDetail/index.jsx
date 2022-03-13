/* third lib*/
import React, { useCallback } from "react";
import { FormattedMessage as Intl } from "react-intl";

/* local components & methods */
import styles from "./styles.module.scss";
import { covertToCurrentTime } from "src/utils/timeFormat";
import { useGlobalContext } from "src/context";

const ResourceDetail = ({ tableData }) => {
  const { timeContext } = useGlobalContext();
  const covertTime = useCallback(
    (date) => {
      return covertToCurrentTime(date, timeContext.timeFormat);
    },
    [timeContext]
  );
  return (
    <div className={styles.resourceDetail}>
      <div className={styles.detailItem}>
        <div className={styles.detailLabel}>
          <Intl id="name" />
        </div>
        <div className={styles.detailValue}>
          {tableData.tableReference.tableId}
        </div>
      </div>
      <div className={styles.detailItem}>
        <div className={styles.detailLabel}>
          <Intl id="type" />
        </div>
        <div className={styles.detailValue}>{tableData.type}</div>
      </div>
      <div className={styles.detailItem}>
        <div className={styles.detailLabel}>
          <Intl id="location" />
        </div>
        <div className={styles.detailValue}>{tableData.location}</div>
      </div>
      <div className={styles.detailItem}>
        <div className={styles.detailLabel}>
          <Intl id="des" />
        </div>
        <div className={styles.detailValue}>{tableData.description}</div>
      </div>
      <div className={styles.detailItem}>
        <div className={styles.detailLabel}>
          <Intl id="createtime" />
        </div>
        <div className={styles.detailValue}>
          {covertTime(Number(tableData.creationTime))}
        </div>
      </div>
    </div>
  );
};

export default ResourceDetail;

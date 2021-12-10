/* third lib*/
import React, { useMemo } from "react";
import Scrollbar from "react-perfect-scrollbar";
import { FormattedMessage as Intl } from "react-intl";

/* local components & methods */
import styles from "./styles.module.scss";
import Text from "@comp/Text";
import FlowItemGroup from "./FlowItemGroup";
const WorkflowDesginPanel = ({ dropOptions }) => {
  const { type, data } = dropOptions;
  const haveOptions = useMemo(() => {
    return data && data.length > 0;
  }, [data]);
  return (
    <div className={styles.designerPanel}>
      <div className={styles.designerTitle}>
        <Text type="title">
          {type === "item" ? (
            <Intl id="workflowItems" />
          ) : (
            <Intl id="itemConditions" />
          )}
        </Text>
      </div>
      <Scrollbar>
        <div className={styles.workflowOptionsType}>
          <div className={styles.workflowItemList}>
            {haveOptions &&
              data.map((column, index) => {
                return <FlowItemGroup key={index} column={column} />;
              })}
          </div>
        </div>
      </Scrollbar>
    </div>
  );
};

export default WorkflowDesginPanel;

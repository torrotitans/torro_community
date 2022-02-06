/* third lib*/
import React, { Fragment, useCallback } from "react";
import cn from "classnames";
import { FormattedMessage as Intl } from "react-intl";

import AddCircleOutline from "@material-ui/icons/AddCircleOutline";

/* local components & methods */
import styles from "./styles.module.scss";
import FlowItem from "./FlowItem";
import ProcessArrow from "@assets/icons/ProcessArrow";

const StartButton = () => (
  <div className={cn(styles.startButton)}>
    <Intl id="start" />
    <span id="anchorStartBtn" className={styles.anchor_bottom}></span>
  </div>
);

const EndButton = () => (
  <div className={cn(styles.startButton, styles.end)}>
    <Intl id="end" />
    <span id="anchorStartBtn" className={styles.anchor_bottom}></span>
  </div>
);

const ProcessAnchor = ({ addPlaceHolder, showAdd }) => {
  return (
    <div className={styles.processAnchor}>
      <div className={styles.processIcon}>
        <ProcessArrow />
      </div>
      {showAdd && (
        <div
          onClick={addPlaceHolder}
          className={styles.addStageBtn}
          title="add Flow Item"
        >
          <AddCircleOutline />
        </div>
      )}
    </div>
  );
};

const PLACEHODER = "PLACEHODER";

const WorkflowRender = ({
  workflowData,
  onChange,
  onEdit,
  editFlow,
  editIndex,
  closeEdit,
  formFieldOptions,
}) => {
  const addHolderHandle = useCallback(
    (index) => {
      let tmpData = JSON.parse(JSON.stringify(workflowData));
      tmpData.splice(index + 1, 0, {
        group: PLACEHODER,
        label: <Intl id="dropwfItem" />,
        id: 0,
      });
      onChange(tmpData);
    },
    [onChange, workflowData]
  );

  const deleteHandle = useCallback(
    (index) => {
      let tmpData = JSON.parse(JSON.stringify(workflowData));
      let typeMap = tmpData.map((item) => item.group);
      if (typeMap.includes("PLACEHODER")) {
        tmpData.splice(tmpData.length - 1, 1);
      }
      tmpData.splice(index, 1);
      onChange(tmpData);
    },
    [onChange, workflowData]
  );

  return (
    <div className={styles.workflowRender}>
      <StartButton />

      <div className={styles.processIcon}>
        <ProcessArrow />
      </div>

      {workflowData.map((item, index) => {
        let preId = index === 0 ? "StartBtn" : workflowData[index - 1].id;
        let tmpEditMode = (editFlow && editIndex === index) || false;
        return (
          <Fragment key={index}>
            <FlowItem
              key={"contanier" + item.id}
              data={item}
              index={index}
              onEdit={onEdit}
              editFlow={tmpEditMode}
              closeEdit={closeEdit}
              onDelete={(index) => {
                deleteHandle(index);
              }}
              fromId={preId}
              formFieldOptions={formFieldOptions}
            />
            <ProcessAnchor
              addPlaceHolder={() => {
                addHolderHandle(index);
              }}
              data={item}
              showAdd={
                index === workflowData.length - 1 && item.group !== PLACEHODER
              }
            />
          </Fragment>
        );
      })}
      <EndButton />
    </div>
  );
};

export default WorkflowRender;

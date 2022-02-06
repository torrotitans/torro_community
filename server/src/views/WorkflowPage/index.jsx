/* third lib*/
import React, { useState, useEffect } from "react";

/* material-ui */

/* local components & methods */
import { getQueryString } from "src/utils/url-util.js";
import styles from "./styles.module.scss";
import Workflow from "@comp/Workflow";
import { getAllStages } from "@lib/api";
import { sendNotify } from "src/utils/systerm-error";

const WorkflowPage = () => {
  const workflowId = getQueryString("id");

  const [droppableItems, setDroppableItems] = useState(null);
  useEffect(() => {
    getAllStages({ workflow_id: workflowId })
      .then((res) => {
        let optionsList = res.data;
        setDroppableItems(optionsList);
      })
      .catch((e) => {
        sendNotify({ msg: e.message, status: 3, show: true });
      });
  }, [workflowId]);

  return (
    <div className={styles.WorkflowPage}>
      {droppableItems && (
        <Workflow flowId={workflowId} droppableItems={droppableItems} />
      )}
    </div>
  );
};

export default WorkflowPage;

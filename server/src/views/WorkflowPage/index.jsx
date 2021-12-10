/* third lib*/
import React, { useState, useEffect, useMemo } from "react";
import { FormattedMessage as Intl } from "react-intl";

/* material-ui */

/* local components & methods */
import { getQueryString } from "src/utils/url-util.js";
import styles from "./styles.module.scss";
import Workflow from "@comp/Workflow";
import { getAllStages } from "@lib/api";
import { sendNotify } from "src/utils/systerm-error";
import { useGlobalContext } from "src/context";

const WorkflowPage = () => {
  const { authContext } = useGlobalContext();
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
  }, []);

  return (
    <div className={styles.WorkflowPage}>
      {droppableItems && (
        <Workflow flowId={workflowId} droppableItems={droppableItems} />
      )}
    </div>
  );
};

export default WorkflowPage;

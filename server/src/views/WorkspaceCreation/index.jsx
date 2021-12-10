/* third lib*/
import React from "react";
import Scrollbar from "react-perfect-scrollbar";

/* material-ui */

/* local components & methods */
import styles from "./styles.module.scss";
import WorkspaceForm from "@comp/WorkspaceForm";

const WorkspaceCreation = () => {
  return (
    <div className={styles.workspaceCreation}>
      <Scrollbar>
        <WorkspaceForm addState={true} />
      </Scrollbar>
    </div>
  );
};

export default WorkspaceCreation;

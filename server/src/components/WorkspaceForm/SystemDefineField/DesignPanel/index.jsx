/* third lib*/
import React from "react";
import Scrollbar from "react-perfect-scrollbar";

/* local components & methods */
import styles from "./styles.module.scss";
import ModuleSelection from "./ModuleSelection";

const DesignPanel = ({ currentModule, onChange }) => {
  return (
    <div id="designPanel" className={styles.designerPanel}>
      {currentModule && (
        <Scrollbar>
          <ModuleSelection data={currentModule} onChange={onChange} />
        </Scrollbar>
      )}
    </div>
  );
};

export default DesignPanel;

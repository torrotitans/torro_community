/* third lib*/
import React, { useState } from "react";

/* material-ui */
import RemoveRedEye from "@material-ui/icons/RemoveRedEye";

/* local components & methods */
import OnboardDataDisplay from "@comp/OnboardDataDisplay";
import styles from "./styles.module.scss";
import Model from "@basics/Modal";

const ViewAccess = ({ data }) => {
  const [open, setOpen] = useState(false);

  return (
    <div className={styles.viewAccess}>
      <div className={styles.viewIcon}>
        <RemoveRedEye
          onClick={() => {
            setOpen(true);
          }}
        />
      </div>

      <Model
        open={open}
        handleClose={() => {
          setOpen(false);
        }}
      >
        <div className={styles.modalContent}>
          <OnboardDataDisplay tableList={data} />
        </div>
      </Model>
    </div>
  );
};

export default ViewAccess;

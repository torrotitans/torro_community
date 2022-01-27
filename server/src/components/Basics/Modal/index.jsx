/* third libs */
import React from "react";

/* material-ui */
import Fade from "@material-ui/core/Fade";
import Modal from "@material-ui/core/Modal";
import CloseIcon from "@material-ui/icons/Close";

/* local components & methods */
import styles from "./styles.module.scss";

const CustomModel = ({ children, name, open, handleClose }) => {
  return (
    <Modal
      open={open}
      onClose={handleClose}
      aria-labelledby={`${name}-modal-title`}
      aria-describedby={`${name}-modal-description`}
    >
      <Fade in={open}>
        <div className={styles.modelPaper}>
          {handleClose && (
            <CloseIcon className={styles.close} onClick={handleClose} />
          )}

          {children}
        </div>
      </Fade>
    </Modal>
  );
};

export default CustomModel;

/* third lib*/
import React, { useMemo, useEffect } from "react";

/* material-ui */
import Snackbar from "@material-ui/core/Snackbar";
import MuiAlert from "@material-ui/lab/Alert";

/* local components & methods */
import styles from "./styles.module.scss";

const statusMap = {
  0: { severity: "info", autoHideDuration: 6000 },
  1: { severity: "warning" },
  2: { severity: "success", autoHideDuration: 6000 },
  3: { severity: "error" },
};
function Alert(props) {
  return <MuiAlert elevation={6} variant="filled" {...props} />;
}

const GlobalNotification = ({ status, msg, show, handleClose }) => {
  const [open, setOpen] = React.useState(show);
  const severity = useMemo(() => {
    let tmpStatus = status || 1;

    return statusMap[tmpStatus].severity;
  }, [status]);

  const autoHideDuration = useMemo(() => {
    let tmpStatus = status || 1;

    return statusMap[tmpStatus].autoHideDuration;
  }, [status]);

  const onClose = (event, reason) => {
    if (reason === "clickaway") {
      return;
    }
    setOpen(false);
    handleClose();
  };

  useEffect(() => {
    setOpen(show);
  }, [show]);

  return (
    <div className={styles.globalNotification}>
      <Snackbar
        anchorOrigin={{ vertical: "top", horizontal: "center" }}
        open={open}
        autoHideDuration={autoHideDuration}
        onClose={onClose}
      >
        <Alert severity={severity} onClose={onClose}>
          {msg}
        </Alert>
      </Snackbar>
    </div>
  );
};

export default GlobalNotification;

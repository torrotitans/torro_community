/* third libs */
import React, { useMemo } from "react";
import { FormattedMessage as Intl } from "react-intl";
import cn from "classnames";

/* material-ui */
import Model from "@basics/Modal";
import Text from "@basics/Text";
import HeadLine from "@basics/HeadLine";
import Button from "@basics/Button";
import Loading from "@assets/icons/StatusIcon/Loading";
import Confirm from "@assets/icons/StatusIcon/Confirm";
import Success from "@assets/icons/StatusIcon/Success";
import ErrorIcon from "@assets/icons/StatusIcon/Error";

/* local components & methods */
import styles from "./styles.module.scss";
const statusMap = {
  0: { buttonText: "back", title: "plsWait", icon: Loading },
  1: { buttonText: "confirm", title: "almost", icon: Confirm },
  2: { buttonText: "continue", title: "allDone", icon: Success },
  3: { buttonText: "tryAgain", title: "ooops", icon: ErrorIcon },
  4: {
    buttonText: "stay",
    title: "loginExpired",
    icon: ErrorIcon,
    button2Text: "logout",
  },
};
const CallModal = ({
  status,
  children,
  content,
  open,
  buttonClickHandle,
  handleClose,
  buttonText,
  successCb,
}) => {
  const currentModelData = useMemo(() => {
    return statusMap[status];
  }, [status]);

  const Icon = useMemo(() => {
    return currentModelData.icon;
  }, [currentModelData]);

  const closeHandler = useMemo(() => {
    return status === 4 ? null : handleClose;
  }, [status, handleClose]);

  return (
    <Model open={open} handleClose={closeHandler}>
      <div className={cn(styles.confirmModel, styles["status" + status])}>
        <div className={styles.statusIcon}>
          <Icon />
        </div>
        <div className={styles.ModelContent}>
          <HeadLine>
            <Intl id={currentModelData.title} />
          </HeadLine>
          <div className={styles.content}>
            <Text type="large">{content}</Text>
          </div>
        </div>
        <div className={styles.extent}>{children}</div>
        <div className={styles.buttonGroup}>
          <Button
            onClick={() => {
              if (buttonClickHandle) {
                buttonClickHandle();
              } else {
                handleClose();
              }
            }}
          >
            <Text type="title">
              <Intl id={buttonText || currentModelData.buttonText} />
            </Text>
          </Button>
          {successCb && (
            <Button
              onClick={() => {
                successCb();
              }}
              className={styles.successCb}
            >
              <Text type="title">
                {currentModelData.button2Text ? (
                  currentModelData.button2Text
                ) : (
                  <Intl
                    id={
                      currentModelData.button2Text
                        ? currentModelData.button2Text
                        : "checkRequest"
                    }
                  />
                )}
              </Text>
            </Button>
          )}
        </div>
      </div>
    </Model>
  );
};

export default CallModal;

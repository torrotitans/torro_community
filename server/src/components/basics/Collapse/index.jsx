/* third lib*/
import React, { useState, useMemo } from "react";
import cn from "classnames";

/* material-ui */
import Collapse from "@material-ui/core/Collapse";
import AddIcon from "@material-ui/icons/Add";

/* local components & methods */
import styles from "./styles.module.scss";
import Text from "@comp/basics/Text";

const CollapseC = ({ children, title, disabled, column }) => {
  const [open, setOpen] = useState(false);
  const toggleHandle = () => {
    setOpen(!open);
  };
  const currentOpen = useMemo(() => {
    return open && !disabled;
  }, [open, disabled]);

  return (
    <div className={styles.collapse}>
      <div
        className={cn(
          styles.collapseLabel,
          { [styles["active"]]: currentOpen },
          { [styles["disabled"]]: disabled }
        )}
      >
        <Text type="subTitle">{title}</Text>
        <div className={styles.addIcon} onClick={toggleHandle}>
          <AddIcon />
        </div>
      </div>
      <Collapse in={currentOpen}>{children}</Collapse>
    </div>
  );
};

export default CollapseC;

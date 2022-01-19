/* third lib*/
import React, { useState, useMemo, useEffect } from "react";
import cn from "classnames";

/* material-ui */
import ClickAwayListener from "@material-ui/core/ClickAwayListener";

/* local components & methods */
import styles from "./styles.module.scss";
import TagDisplay from "@comp/TagDisplay";

const SystemTips = ({ style, show, handleClose, ...options }) => {
  const [openState, setOpenState] = useState(false);

  useEffect(() => {
    setTimeout(() => {
      setOpenState(true);
    }, 0);
  }, [show]);

  const TipsComponent = useMemo(() => {
    if (style === 1) {
      return <TagDisplay {...options} />;
    }
  }, [style, options]);

  return (
    <div className={styles.systemTips}>
      <ClickAwayListener onClickAway={handleClose}>
        <div
          id="designPanel"
          className={cn(styles.tipsPanel, {
            [styles["open"]]: openState,
          })}
        >
          {TipsComponent}
        </div>
      </ClickAwayListener>
    </div>
  );
};

export default SystemTips;

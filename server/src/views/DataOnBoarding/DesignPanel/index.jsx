/* third lib*/
import React, { useEffect, useState } from "react";
import cn from "classnames";
import ClickAwayListener from "@material-ui/core/ClickAwayListener";
import ScrollBar from "react-perfect-scrollbar";

/* local components & methods */
import styles from "./styles.module.scss";
import PolicyTagTree from "./PolicyTagTree";
import AddTag from "./AddTag";

const DesignPanel = ({
  open,
  handleClose,
  handleApply,
  type,
  tagTemplateList,
  checkedTagList,
}) => {
  const [openState, setOpenState] = useState(false);

  useEffect(() => {
    if (!open) {
      setOpenState(false);
      return;
    }
    setTimeout(() => {
      setOpenState(true);
    }, 0);
  }, [open]);

  if (!open) {
    return <></>;
  }

  return (
    <div className={styles.mask}>
      <ClickAwayListener onClickAway={handleClose}>
        <div
          id="designPanel"
          className={cn(styles.designerPanel, {
            [styles["open"]]: openState,
          })}
        >
          <ScrollBar>
            <div className={styles.innerContent}>
              {type === 0 && <PolicyTagTree handleApply={handleApply} />}
              {(type === 1 || type === 2) && (
                <AddTag
                  handleApply={handleApply}
                  type={type}
                  tagTemplateList={tagTemplateList}
                  checkedTagList={checkedTagList}
                />
              )}
            </div>
          </ScrollBar>
        </div>
      </ClickAwayListener>
    </div>
  );
};

export default DesignPanel;

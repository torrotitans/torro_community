/* third lib */
import React, { useCallback, useState } from "react";
import { FormattedMessage as Intl } from "react-intl";

/* material-ui */
import Paper from "@material-ui/core/Paper";
import Popper from "@material-ui/core/Popper";
import ClickAwayListener from "@material-ui/core/ClickAwayListener";
import ExpandMoreIcon from "@material-ui/icons/ExpandMore";

/* local components & methods */
import styles from "./styles.module.scss";
import DatePicker from "@basics/DatePicker";
import Select from "@basics/Select";
import Button from "@basics/Button";
import FilterIcon from "@assets/icons/FilterIcon";

const FilterPanel = ({
  id,
  options,
  handleApply,
  handleReset,
  condition,
  approved,
}) => {
  const [filterData, setFilterData] = useState({
    form_id: "",
    creator_id: "",
    from: "",
    to: "",
    ...condition,
  });
  const [open, setOpen] = React.useState(false);
  const anchorRef = React.useRef(null);

  const handleClick = (event) => {
    setOpen(!open);
  };

  const handleClose = useCallback((e) => {
    if (
      e &&
      e.target &&
      e.target.nodeName === "BODY" &&
      e.target.style.overflow === "hidden"
    ) {
      return;
    }
    setOpen(false);
  }, []);

  const handleResetClick = useCallback(
    (e) => {
      handleReset();
    },
    [handleReset]
  );

  return (
    <Paper id={id} ref={anchorRef} className={styles.filter}>
      <div onClick={handleClick} className={styles.input}>
        <FilterIcon />
        <ExpandMoreIcon />
      </div>
      <Popper
        placement="bottom"
        id="simple-menu"
        anchorEl={anchorRef.current}
        open={open}
      >
        <div className={styles.poppup}>
          <Paper className={styles.list}>
            <ClickAwayListener
              onClickAway={(e) => {
                handleClose(e);
              }}
            >
              <div className={styles.filterBox}>
                {approved && (
                  <div className={styles.filterItem}>
                    <div className={styles.label}>
                      <Intl id="requestor" />
                    </div>
                    <div className={styles.detail}>
                      <Select
                        value={filterData.creator_id}
                        options={options.creator}
                        onChange={(value) => {
                          setFilterData({
                            ...filterData,
                            creator_id: value,
                          });
                        }}
                      />
                    </div>
                  </div>
                )}
                <div className={styles.filterItem}>
                  <div className={styles.label}>
                    <Intl id="associatedForm" />
                  </div>
                  <div className={styles.detail}>
                    <Select
                      value={filterData.form_id}
                      options={options.formList}
                      onChange={(value) => {
                        setFilterData({
                          ...filterData,
                          form_id: value,
                        });
                      }}
                    />
                  </div>
                </div>
                <div className={styles.filterItem}>
                  <div className={styles.label}>Period</div>
                  <div className={styles.detail}>
                    <DatePicker
                      value={filterData.from}
                      onChange={(value) => {
                        setFilterData({
                          ...filterData,
                          from: value,
                        });
                      }}
                    />
                    <div className={styles.sep}>-</div>
                    <DatePicker
                      value={filterData.to}
                      onChange={(value) => {
                        setFilterData({
                          ...filterData,
                          to: value,
                        });
                      }}
                    />
                  </div>
                </div>
                <div className={styles.buttonRow}>
                  <div className={styles.clear}>
                    <Button
                      onClick={() => {
                        handleResetClick();
                      }}
                      size="small"
                    >
                      Reset
                    </Button>
                  </div>
                  <Button
                    size="small"
                    filled
                    onClick={() => {
                      handleApply(filterData);
                    }}
                  >
                    Apply
                  </Button>
                </div>
              </div>
            </ClickAwayListener>
          </Paper>
        </div>
      </Popper>
    </Paper>
  );
};

export default FilterPanel;

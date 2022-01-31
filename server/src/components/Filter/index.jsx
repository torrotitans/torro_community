/* third lib */
import React, { useEffect, useMemo, useState } from "react";

/* material-ui */
import Paper from "@material-ui/core/Paper";
import InputBase from "@material-ui/core/InputBase";
import MenuItem from "@material-ui/core/MenuItem";
import Popper from "@material-ui/core/Popper";
import ClickAwayListener from "@material-ui/core/ClickAwayListener";
import MenuList from "@material-ui/core/MenuList";

/* local components & methods */
import styles from "./styles.module.scss";
import FilterIcon from "@assets/icons/FilterIcon";
import { startsWith } from "lodash";

const Filter = ({ id, value, options, onChange }) => {
  const [current, setCurrent] = useState(value);
  const [inputVal, setInputVal] = useState("");

  const currentOption = useMemo(() => {
    let preList = [...options];
    if (inputVal) {
      preList = preList.filter((option) => {
        return startsWith(
          String(inputVal).toLowerCase(),
          String(option.label).toLowerCase()
        );
      });
    }
    return preList;
  }, [inputVal, options]);

  const handleInputChange = (event) => {
    setInputVal(event.target.value);
  };
  const [open, setOpen] = React.useState(false);
  const anchorRef = React.useRef(null);

  const handleClick = (event) => {
    setOpen(!open);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const selectHandle = (option) => {
    setInputVal(option.label);
    onChange(option.value);
    setOpen(false);
  };

  useEffect(() => {
    let currentOption = options.find((item) => item.value === value);
    setInputVal(currentOption ? currentOption.label : "");
    setCurrent(value);
  }, [value, options]);

  return (
    <Paper id={id} ref={anchorRef} className={styles.filter}>
      <InputBase
        id="outlined-select-currency"
        value={inputVal}
        onChange={handleInputChange}
        fullWidth
        placeholder={"Filter"}
        startAdornment={<FilterIcon />}
        onClick={handleClick}
        className={styles.input}
      />
      <Popper
        placement="bottom"
        id="simple-menu"
        anchorEl={anchorRef.current}
        open={open}
      >
        <div className={styles.poppup}>
          <Paper className={styles.list}>
            <ClickAwayListener onClickAway={handleClose}>
              <MenuList value={current}>
                {currentOption.map((option) => (
                  <MenuItem
                    onClick={() => {
                      selectHandle(option);
                    }}
                    key={option.value}
                    value={option.value}
                  >
                    {option.label}
                  </MenuItem>
                ))}
              </MenuList>
            </ClickAwayListener>
          </Paper>
        </div>
      </Popper>
    </Paper>
  );
};

export default Filter;

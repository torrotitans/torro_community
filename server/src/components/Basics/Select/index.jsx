/* third lib */
import React from "react";

/* material-ui */
import MenuItem from "@material-ui/core/MenuItem";
import Select from "@material-ui/core/Select";

/* local components and methods */
import styles from "./styles.module.scss";

const SelectC = ({
  value,
  options,
  onChange,
  inputProps,
  disableFullwidth,
  disabled,
  error,
  maxHeight,
}) => {
  return (
    <Select
      value={value}
      onChange={(e) => {
        onChange(e.target.value);
      }}
      error={error}
      variant="filled"
      inputProps={inputProps}
      disableUnderline
      disabled={disabled}
      displayEmpty
      fullWidth={!disableFullwidth}
      MenuProps={{
        anchorOrigin: {
          vertical: "bottom",
          horizontal: "left",
        },
        transformOrigin: {
          vertical: "top",
          horizontal: "left",
        },
        getContentAnchorEl: null,
        MenuListProps: {
          style: { maxHeight: maxHeight },
          className: styles.menuList,
        },
      }}
    >
      <MenuItem value="" disabled>
        <em>None</em>
      </MenuItem>
      {options &&
        options.length &&
        options.map((item, index) => {
          return (
            <MenuItem
              key={item.value + item.label + index}
              className={styles.menuItem}
              value={item.value}
            >
              {item.label}
            </MenuItem>
          );
        })}
    </Select>
  );
};

export default SelectC;

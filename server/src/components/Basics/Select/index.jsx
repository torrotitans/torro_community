/* third lib */
import React from "react";

/* material-ui */
import MenuItem from "@material-ui/core/MenuItem";
import Select from "@material-ui/core/Select";

const SelectC = ({
  value,
  options,
  onChange,
  inputProps,
  disableFullwidth,
  disabled,
  error,
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
      }}
    >
      <MenuItem value="" disabled>
        <em>None</em>
      </MenuItem>
      {options &&
        options.length &&
        options.map((item, index) => {
          return (
            <MenuItem key={item.value + item.label + index} value={item.value}>
              {item.label}
            </MenuItem>
          );
        })}
    </Select>
  );
};

export default SelectC;

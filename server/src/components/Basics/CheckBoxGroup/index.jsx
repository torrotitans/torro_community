/* third lib */
import React, { useState, useMemo } from "react";
import cn from "classnames";

/* material-ui */
import InputBase from "@material-ui/core/InputBase";
import MenuItem from "@material-ui/core/MenuItem";
import Select from "@material-ui/core/Select";
import Checkbox from "@material-ui/core/Checkbox";
import styles from "./styles.module.scss";
import SearchIcon from "@material-ui/icons/Search";
import { useCallback } from "react";

const CheckBoxGroup = ({
  value,
  options,
  onChange,
  inputProps,
  disableFullwidth,
  disabled,
  error,
}) => {
  const [filterVal, setFilterVal] = useState("");

  const currentOptions = useMemo(() => {
    return options.map((item) => {
      return { label: item.label, value: item.label };
    });
  }, [options]);

  const valueList = useMemo(() => {
    return value ? value.split(",") : [];
  }, [value]);

  const filterOptions = useMemo(() => {
    if (filterVal) {
      return currentOptions.filter((option) => {
        return new RegExp(
          filterVal.replace(/[()[\]{}?*+\\/]/g, "\\$&"),
          "i"
        ).test(option.label);
      });
    } else {
      return currentOptions;
    }
  }, [filterVal, currentOptions]);

  const closePopupHandle = useCallback((e) => {
    setFilterVal("");
  }, []);

  const stopPropagation = useCallback((e) => {
    e.stopPropagation();
  }, []);

  return (
    <Select
      value={valueList}
      onChange={(e) => {
        onChange(e.target.value.join(","));
      }}
      multiple
      renderValue={(selected) => selected.join(",")}
      error={error}
      variant="filled"
      inputProps={inputProps}
      onClose={closePopupHandle}
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
      <div className={styles.filterBox}>
        <SearchIcon />
        <InputBase
          className={styles.filterInput}
          value={filterVal}
          onKeyDown={stopPropagation}
          onClick={stopPropagation}
          onChange={(e) => {
            e.stopPropagation();
            setFilterVal(e.target.value);
          }}
          fullWidth
          placeholder="Search your option"
        />
      </div>

      {filterOptions &&
        filterOptions.length &&
        filterOptions.map((item, index) => {
          return (
            <MenuItem key={item.value + item.label + index} value={item.value}>
              <Checkbox
                className={cn(styles.checkbox, {
                  [styles["checked"]]: valueList.includes(item.value),
                })}
                checked={valueList.includes(item.value)}
              />
              {item.label}
            </MenuItem>
          );
        })}
    </Select>
  );
};

export default CheckBoxGroup;

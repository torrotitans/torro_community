// third lib
import React from "react";
import cn from "classnames";

/* material-ui */
import FormGroup from "@material-ui/core/FormGroup";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import Checkbox from "@material-ui/core/Checkbox";

/* local components & methods */
import styles from "./styles.module.scss";

const CheckBoxGroup = ({ value, options, onChange, disabled }) => {
  let valueStrList = value ? value.split(",") : [];
  let valueList = options.map((item) => {
    return valueStrList.includes(item.label) ? item.label : "";
  });

  return (
    <FormGroup>
      {options.map((item, index) => {
        const checked = valueList.includes(item.label);
        return (
          <FormControlLabel
            key={index}
            control={
              <Checkbox
                className={cn(styles.checkbox, {
                  [styles["checked"]]: checked,
                })}
                checked={checked}
                onChange={(e) => {
                  if (checked) {
                    valueList.splice(index, 1);
                  } else {
                    valueList.splice(index, 1, item.label);
                  }
                  onChange(valueList.filter((str) => str).join(","));
                }}
                name={item.label}
                disabled={disabled}
              />
            }
            label={item.label}
          />
        );
      })}
    </FormGroup>
  );
};

export default CheckBoxGroup;

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
  let valueList = value.split(",");
  return (
    <FormGroup>
      {options.map((item, index) => {
        const checked = valueList[index] === "true";
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
                  valueList[index] = String(e.target.checked);
                  onChange(valueList.join(","));
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

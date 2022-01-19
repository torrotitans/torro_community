// third lib
import React from "react";
import cn from "classnames";

/* material-ui */
import Radio from "@material-ui/core/Radio";
import RadioGroup from "@material-ui/core/RadioGroup";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import FormControl from "@material-ui/core/FormControl";

/* local components & methods */
import styles from "./styles.module.scss";

const CustRadioGroup = ({ value, options, onChange, disabled }) => {
  return (
    <FormControl className={styles.radioGroup}>
      <RadioGroup name="radio-buttons-group" className={styles.radioGroup}>
        {options.map((item, index) => {
          return (
            <FormControlLabel
              className={styles.radio}
              key={index}
              control={
                <Radio
                  className={cn(styles.radio, {
                    [styles["checked"]]: true,
                  })}
                  checked={value === item.label}
                  onChange={(e) => {
                    onChange(item.label);
                  }}
                  name={item.label}
                  disabled={disabled}
                />
              }
              label={item.label}
            />
          );
        })}
      </RadioGroup>
    </FormControl>
  );
};

export default CustRadioGroup;

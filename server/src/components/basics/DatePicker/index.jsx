/* third lib */
import React from "react";

/* material-ui */
import DateFnsUtils from "@date-io/date-fns";
import {
  MuiPickersUtilsProvider,
  KeyboardDatePicker,
} from "@material-ui/pickers";

/* local components & methods */
import styles from "./styles.module.scss";

const DatePicker = ({ value, id, name, onChange, disabled }) => {
  return (
    <div className={styles.datePickerBox}>
      <MuiPickersUtilsProvider utils={DateFnsUtils}>
        <KeyboardDatePicker
          className={styles.datePicker}
          name={name}
          format="MM/dd/yyyy"
          value={value || new Date()}
          onChange={(data) => onChange(data)}
          id={id}
          InputProps={{
            fullWidth: true,
            disabled: disabled,
            classes: {
              root: "MuiFilledInput-root",
              input: "MuiFilledInput-input",
              underline: "MuiFilledInput-underline",
            },
          }}
        />
      </MuiPickersUtilsProvider>
    </div>
  );
};

export default DatePicker;

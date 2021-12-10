/* third lib*/
import React, { useCallback } from "react";

/* material-ui */
import TextField from "@material-ui/core/TextField";
import styles from "./styles.module.scss";

const TextBox = ({
  id,
  name,
  onChange,
  value,
  type,
  placeholder,
  autoFocus,
  disabled,
  multiline,
  inputRef,
  maxLength,
  rows,
  error,
}) => {
  let textType = type || "text";

  return (
    <div className={styles.textBox}>
      <TextField
        id={id}
        name={name}
        value={value}
        inputProps={{ maxLength: maxLength }}
        onChange={(e) => {
          onChange(e.target.value);
        }}
        variant="filled"
        fullWidth
        placeholder={placeholder}
        type={textType}
        autoFocus={autoFocus}
        disabled={disabled}
        multiline={multiline}
        rows={rows}
        error={error}
        inputRef={inputRef}
      />
    </div>
  );
};

export default TextBox;

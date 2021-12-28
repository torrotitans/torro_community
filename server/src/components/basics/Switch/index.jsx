/* third lib */
import React from "react";
import cn from "classnames";

/* material-ui */
import Switch from "@material-ui/core/Switch";

/* local components & methods */
import styles from "./styles.module.scss";

const SwitchBtn = ({ name, value, onChange, disabled }) => {
  const checked = String(value) === "true";
  return (
    <div className={cn(styles.switch, { [styles["checked"]]: checked })}>
      <Switch
        checked={checked}
        onChange={(e) => {
          onChange(String(e.target.checked));
        }}
        name={name}
        inputProps={{ "aria-label": "checkbox" }}
        disabled={disabled}
      />
    </div>
  );
};

export default SwitchBtn;

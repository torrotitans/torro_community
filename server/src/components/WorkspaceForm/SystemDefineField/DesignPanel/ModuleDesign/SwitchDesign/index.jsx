/* third lib*/
import React from "react";
import { FormattedMessage as Intl } from "react-intl";

/* material-ui */
import Checkbox from "@material-ui/core/Checkbox";
import Input from "@material-ui/core/Input";

/* local components & methods */
import Text from "@basics/Text";
import styles from "../styles.module.scss";

const SwitchDesign = ({ data, onChange }) => {
  return (
    <div className={styles.ModuleEdit}>
      <div className={styles.title}>
        <Text type="subTitle">
          <Intl id="advanceOptions" />
        </Text>
      </div>
      <div className={styles.editItem}>
        <div className={styles.label}>
          <Text type="subTitle">
            <Intl id="label" />:
          </Text>
        </div>
        <Input
          className={styles.editInput}
          value={data.label}
          disableUnderline
          variant="outlined"
          onChange={(e) => {
            onChange({
              ...data,
              label: e.target.value,
            });
          }}
        />
      </div>
      <div className={styles.editItem}>
        <div className={styles.label}>
          <Text type="subTitle">
            <Intl id="default" />:
          </Text>
        </div>
        <Checkbox
          checked={data.default}
          onChange={() => {
            onChange({
              ...data,
              default: !data.default,
            });
          }}
        />
      </div>
    </div>
  );
};

export default SwitchDesign;

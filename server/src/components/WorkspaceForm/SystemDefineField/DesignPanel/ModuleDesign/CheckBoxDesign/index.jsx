/* third lib*/
import React from "react";
import { FormattedMessage as Intl } from "react-intl";
import cn from "classnames";

/* material-ui */
import Input from "@material-ui/core/Input";

/* local components & methods */
import Text from "@basics/Text";
import styles from "../styles.module.scss";
import KeyGroup from "@basics/KeyGroup";

const TextDesign = ({ data, onChange }) => {
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
      <div className={cn(styles.editItem, styles.columItem)}>
        <div className={styles.label}>
          <Text type="subTitle">
            <Intl id="checkboxItem" />:
          </Text>
        </div>

        <KeyGroup
          options={data.options}
          onChange={(options) => {
            onChange({
              ...data,
              options: options,
            });
          }}
        />
      </div>
    </div>
  );
};

export default TextDesign;

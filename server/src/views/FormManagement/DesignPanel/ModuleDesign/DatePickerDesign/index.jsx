/* third lib*/
import React from "react";
import { FormattedMessage as Intl } from "react-intl";

/* material-ui */
import Input from "@material-ui/core/Input";
import Checkbox from "@material-ui/core/Checkbox";

/* local components & methods */
import Text from "@basics/Text";
import styles from "../styles.module.scss";

const DatePickerDesign = ({ data, onChange, onlyLabel }) => {
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
      {!onlyLabel && (
        <>
          <div className={styles.editItem}>
            <div className={styles.label}>
              <Text type="subTitle">
                <Intl id="des" />:
              </Text>
            </div>
            <Input
              className={styles.editInput}
              value={data.des}
              disableUnderline
              variant="outlined"
              onChange={(e) => {
                onChange({
                  ...data,
                  des: e.target.value,
                });
              }}
            />
          </div>
          <div className={styles.editItem}>
            <div className={styles.label}>
              <Text type="subTitle">
                <Intl id="required" />:
              </Text>
            </div>
            <Checkbox
              checked={data.required}
              onChange={(e) => {
                onChange({
                  ...data,
                  required: !data.required,
                });
              }}
            />
          </div>
        </>
      )}
    </div>
  );
};

export default DatePickerDesign;

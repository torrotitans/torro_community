/* third lib*/
import React from "react";
import { FormattedMessage as Intl } from "react-intl";
import cn from "classnames";

/* material-ui */
import Input from "@material-ui/core/Input";
import Checkbox from "@material-ui/core/Checkbox";

/* local components & methods */
import Text from "@basics/Text";
import styles from "../styles.module.scss";
import Select from "@basics/Select";
const ruleOptions = [
  { label: "Default", value: 0 },
  { label: "Amount", value: 1 },
  { label: "Email", value: 2 },
  { label: "Phone", value: 3 },
];

const TextDesign = ({ data, onChange, systemCopy }) => {
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
      {!systemCopy && (
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
          <div className={styles.editItem}>
            <div className={styles.label}>
              <Text type="subTitle">
                <Intl id="itemWidth" />:
              </Text>
            </div>
            <Input
              className={styles.editInput}
              value={data.width === undefined ? 33 : data.width}
              disableUnderline
              variant="outlined"
              inputProps={{ type: "number" }}
              onChange={(e) => {
                let value = e.target.value;
                if (value <= 100) {
                  onChange({
                    ...data,
                    width: value,
                  });
                }
              }}
            />
          </div>
          <div className={styles.editItem}>
            <div className={styles.label}>
              <Text type="subTitle">
                <Intl id="maxLength" />:
              </Text>
            </div>
            <Input
              className={styles.editInput}
              value={data.maxLength}
              disableUnderline
              variant="outlined"
              inputProps={{ type: "number" }}
              onChange={(e) => {
                let value = e.target.value;
                if (value.length > 3) {
                  value = value.slice(0, 3);
                }
                onChange({
                  ...data,
                  maxLength: value,
                });
              }}
            />
          </div>
          <div className={styles.editItem}>
            <div className={styles.label}>
              <Text type="subTitle">
                <Intl id="placeholder" />:
              </Text>
            </div>
            <Input
              className={styles.editInput}
              value={data.placeholder}
              disableUnderline
              variant="outlined"
              onChange={(e) => {
                onChange({
                  ...data,
                  placeholder: e.target.value,
                });
              }}
            />
          </div>
          <div className={styles.editItem}>
            <div className={styles.label}>
              <Text type="subTitle">
                <Intl id="defaultvalue" />:
              </Text>
            </div>
            <Input
              className={styles.editInput}
              value={data.default}
              disableUnderline
              variant="outlined"
              onChange={(e) => {
                onChange({
                  ...data,
                  default: e.target.value,
                });
              }}
            />
          </div>
          <div className={cn(styles.editItem, styles.columItem)}>
            <div className={styles.label}>
              <Text type="subTitle">
                <Intl id="options" />:
              </Text>
            </div>
            <Select
              value={data.rule}
              options={ruleOptions}
              onChange={(value) => {}}
            />
          </div>
        </>
      )}
    </div>
  );
};

export default TextDesign;

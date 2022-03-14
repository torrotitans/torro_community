/* third lib*/
import React from "react";
import { FormattedMessage as Intl } from "react-intl";

/* material-ui */
import Checkbox from "@material-ui/core/Checkbox";

/* local components & methods */
import Text from "@basics/Text";
import styles from "../styles.module.scss";
import Input from "@material-ui/core/Input";

const UploadDesign = ({ data, onChange, onlyLabel }) => {
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
                <Intl id="multiple" />:
              </Text>
            </div>
            <Checkbox
              checked={data.multiple || false}
              onChange={() => {
                onChange({
                  ...data,
                  multiple: !data.multiple,
                });
              }}
            />
          </div>
        </>
      )}
    </div>
  );
};

export default UploadDesign;

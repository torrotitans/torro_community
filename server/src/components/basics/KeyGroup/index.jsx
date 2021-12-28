/* third lib*/
import React, { useMemo } from "react";

/* material-ui */
import RemoveCircleOutlineIcon from "@material-ui/icons/RemoveCircleOutline";
import AddCircleOutlineIcon from "@material-ui/icons/AddCircleOutline";
import Input from "@material-ui/core/Input";

/* local components & methods */
import styles from "./styles.module.scss";

const KeyGroup = ({ options, onChange }) => {
  let maxId = useMemo(() => {
    return options.length + 1;
  }, [options]);

  const optionsChange = (value, index, label) => {
    let tmpOptions = JSON.parse(JSON.stringify(options));
    tmpOptions[index].label = value;
    onChange(tmpOptions);
  };

  const addItem = (index) => {
    let tmpOptions = JSON.parse(JSON.stringify(options));
    tmpOptions.splice(index + 1, 0, {
      label: "Options" + maxId,
    });
    onChange(tmpOptions);
  };

  const deleteItem = (index) => {
    let tmpOptions = JSON.parse(JSON.stringify(options));
    tmpOptions.splice(index, 1);
    onChange(tmpOptions);
  };
  return (
    <div className={styles.keypairGroup}>
      {options.map((item, index) => {
        return (
          <div key={index} className={styles.keypairItem}>
            <Input
              className={styles.editInput}
              value={item.label}
              disableUnderline
              variant="outlined"
              onChange={(e) => {
                optionsChange(e.target.value, index, true);
              }}
            />

            <div className={styles.operaction}>
              {options.length > 1 && (
                <div
                  className={styles.icon}
                  onClick={() => {
                    deleteItem(index);
                  }}
                >
                  <RemoveCircleOutlineIcon />
                </div>
              )}
              <div
                className={styles.icon}
                onClick={() => {
                  addItem(index);
                }}
              >
                <AddCircleOutlineIcon />
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default KeyGroup;

/* third lib*/
import React, { useEffect, useMemo, useState } from "react";
import cn from "classnames";

/* material-ui */
import CloseIcon from "@material-ui/icons/Close";

/* local components & methods */
import styles from "./styles.module.scss";
import TextBox from "@comp/basics/TextBox";
import Select from "@comp/basics/Select";
import Ueditor from "./Ueditor";
import Schema from "./Schema";
import CommonConditionHolder from "../CommonConditionHolder";
import CheckBoxGroup from "@comp/basics/CheckBoxGroup";
import DatePicker from "@comp/basics/DatePicker";
import Switch from "@comp/basics/Switch";
import Text from "@comp/basics/Text";

const conditionTypeList = [
  { label: "=", value: "0" },
  { label: "!=", value: "1" },
  { label: ">=", value: "2" },
  { label: "<=", value: "3" },
];

const FormCondition = ({
  index,
  item,
  onChange,
  currentData,
  options,
  formFieldOptions,
}) => {
  return (
    <>
      <div className={styles.conditionLabel}>{item.label}</div>
      <div className={styles.conditionType}>
        <Select
          value={item.conditionType}
          options={conditionTypeList}
          onChange={(value) => {
            let tmpData = {
              ...currentData,
            };
            tmpData.condition[index].conditionType = value;
            onChange(tmpData);
          }}
        />
      </div>
      <div className={styles.conditionValue}>
        {item.style === 1 && (
          <CheckBoxGroup
            value={item.value}
            options={item.options}
            onChange={(value) => {
              let tmpData = {
                ...currentData,
              };
              tmpData.condition[index].value = value;
              onChange(tmpData);
            }}
          />
        )}
        {item.style === 2 && (
          <Select
            value={item.value}
            options={options}
            onChange={(value) => {
              let tmpData = {
                ...currentData,
              };
              tmpData.condition[index].value = value;
              onChange(tmpData);
            }}
          ></Select>
        )}
        {item.style === 3 && (
          <TextBox
            id={item.id}
            name={item.label}
            value={item.value}
            placeholder={item.placeholder}
            onChange={(value) => {
              let tmpData = {
                ...currentData,
              };
              tmpData.condition[index].value = value;
              onChange(tmpData);
            }}
          />
        )}

        {item.style === 5 && (
          <Switch
            value={item.value}
            onChange={(value) => {
              let tmpData = {
                ...currentData,
              };
              tmpData.condition[index].value = value;
              onChange(tmpData);
            }}
          />
        )}

        {item.style === 6 && (
          <DatePicker
            value={item.value}
            onChange={(value) => {
              let tmpData = {
                ...currentData,
              };
              tmpData.condition[index].value = value;
              onChange(tmpData);
            }}
          />
        )}
      </div>
    </>
  );
};

const ApprovalCondition = ({
  index,
  item,
  onChange,
  currentData,
  options,
  formFieldOptions,
}) => {
  return (
    <>
      <div className={styles.conditionLabel}>
        <Text type="regular">Approver{index + 1}:</Text>
      </div>

      <div className={styles.conditionValue}>
        <Text type="regular">{item.label}</Text>
      </div>
    </>
  );
};

const CommonCondition = ({
  index,
  item,
  onChange,
  currentData,
  options,
  formFieldOptions,
}) => {
  return (
    <>
      <div className={styles.conditionLabel} title={item.des}>
        {item.label}:
      </div>
      <div className={styles.conditionValue}>
        {item.style === 1 && (
          <TextBox
            id={item.id}
            name={item.label}
            value={item.value}
            placeholder={item.placeholder || ""}
            onChange={(value) => {
              let tmpData = {
                ...currentData,
              };
              tmpData.condition[index].value = value;
              onChange(tmpData);
            }}
          />
        )}
        {item.style === 2 && (
          <Select
            value={item.value}
            options={options}
            onChange={(value) => {
              let tmpData = {
                ...currentData,
              };
              tmpData.condition[index].value = value;
              onChange(tmpData);
            }}
          />
        )}
        {item.style === 3 && (
          <Ueditor
            value={item.value}
            options={formFieldOptions}
            onChange={(value) => {
              let tmpData = {
                ...currentData,
              };
              tmpData.condition[index].value = value;
              onChange(tmpData);
            }}
          />
        )}

        {item.style === 4 && (
          <Schema
            value={item.value}
            options={options}
            onChange={(value) => {
              let tmpData = {
                ...currentData,
              };
              tmpData.condition[index].value = value;
              onChange(tmpData);
            }}
          />
        )}

        {item.style === 5 && (
          <Select
            value={item.value}
            options={formFieldOptions}
            onChange={(value) => {
              let tmpData = {
                ...currentData,
              };
              tmpData.condition[index].value = value;
              onChange(tmpData);
            }}
          />
        )}
      </div>
    </>
  );
};

const ConditionItem = ({
  currentData,
  onChange,
  formFieldOptions,
  editFlow,
  flowIndex,
}) => {
  const Condition = useMemo(() => {
    switch (currentData.flowType) {
      case "Trigger":
        return FormCondition;
      case "Approval":
        return ApprovalCondition;
      case "GoogleCloud":
        return CommonCondition;
      case "System":
        return CommonCondition;
      default:
        return () => {
          return <></>;
        };
    }
  }, [currentData]);

  const enableCc = useMemo(() => {
    return (
      currentData.flowType === "Trigger" || currentData.flowType === "Approval"
    );
  }, [currentData.flowType]);

  const ccTitle = useMemo(() => {
    return currentData.flowType === "Approval" ? "Drop approver here" : null;
  }, [currentData.flowType]);

  return (
    <>
      {currentData.condition && (
        <div>
          <div className={styles.contentTitle}>Condition:</div>
          <div className={styles.childItemList}>
            {currentData.condition.map((item, index) => {
              let options = item.options || [];
              return (
                <div className={styles.conditionItem} key={index}>
                  <Condition
                    index={index}
                    item={item}
                    onChange={(data) => {
                      onChange(data);
                    }}
                    currentData={currentData}
                    options={options}
                    formFieldOptions={formFieldOptions}
                  />
                  {enableCc && (
                    <div className={styles.deleteIcon}>
                      <CloseIcon
                        onClick={() => {
                          let tmpData = {
                            ...currentData,
                          };
                          tmpData.condition.splice(index, 1);
                          onChange(tmpData);
                        }}
                      />
                    </div>
                  )}
                </div>
              );
            })}
          </div>
          {enableCc && (
            <CommonConditionHolder
              droppable={editFlow}
              index={flowIndex}
              title={ccTitle}
            />
          )}
        </div>
      )}
    </>
  );
};

export default ConditionItem;

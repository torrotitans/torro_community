/* third lib*/
import React, { useEffect, useMemo, useState } from "react";
import cn from "classnames";
import { FormattedMessage as Intl } from "react-intl";

/* local components & methods */
import Collapse from "@comp/basics/Collapse";
import Text from "@comp/basics/Text";
import styles from "./styles.module.scss";
import CheckBoxIcon from "src/icons/moduleIcon/CheckBoxIcon";
import DropdownIcon from "src/icons/moduleIcon/DropdownIcon";
import TextIcon from "src/icons/moduleIcon/TextIcon";
import UploadIcon from "src/icons/moduleIcon/UploadIcon";
import ToggleIcon from "src/icons/moduleIcon/ToggleIcon";
import DatePickerIcon from "src/icons/moduleIcon/DatePickerIcon";

/* moduleDesigb */
import CheckBoxDesign from "../ModuleDesign/CheckBoxDesign";
import DropdownDesign from "../ModuleDesign/DropdownDesign";
import TextDesign from "../ModuleDesign/TextDesign";
import UploadDesign from "../ModuleDesign/UploadDesign";
import SwitchDesign from "../ModuleDesign/SwitchDesign";
import DatePickerDesign from "../ModuleDesign/DatePickerDesign";

const ModuleTemplate = ({ templateData, setTemplate }) => {
  let systemList = templateData.systemList;

  return (
    <>
      <div
        className={styles.defaultTemplate}
        onClick={() => {
          setTemplate(templateData.default);
        }}
      >
        <Text type="subTitle">
          <Intl id="restoreField" />
        </Text>
      </div>

      {systemList && systemList.length > 0 && (
        <Collapse title={<Intl id="sysField" />}>
          {systemList.map((item, index) => {
            return (
              <div
                key={index}
                className={styles.templateItem}
                onClick={() => {
                  setTemplate(item);
                }}
              >
                {item.label}
              </div>
            );
          })}
        </Collapse>
      )}
    </>
  );
};

const ModuleSelection = ({ data, template, onChange, tagTemplate }) => {
  const curModuleStyle = useMemo(() => {
    return data.style;
  }, [data]);

  const moduleTypeList = useMemo(() => {
    return tagTemplate
      ? [{ style: 3, icon: TextIcon, cls: "text" }]
      : [
          { style: 1, icon: CheckBoxIcon, cls: "checkbox", temp: "text" },
          { style: 2, icon: DropdownIcon, cls: "dropdown" },
          { style: 3, icon: TextIcon, cls: "text" },
          { style: 4, icon: UploadIcon, cls: "upload" },
          { style: 5, icon: ToggleIcon, cls: "switch" },
          { style: 6, icon: DatePickerIcon, cls: "datepicker" },
        ];
  }, [tagTemplate]);

  const currentTemplate = useMemo(() => {
    return (
      template.find((item) => {
        return Number(item.style) === Number(curModuleStyle);
      }) || null
    );
  }, [curModuleStyle, template]);

  const ModuleEdit = useMemo(() => {
    let style = Number(curModuleStyle);
    switch (style) {
      case 1:
        return CheckBoxDesign;
      case 2:
        return DropdownDesign;
      case 3:
        return TextDesign;
      case 4:
        return UploadDesign;
      case 5:
        return SwitchDesign;
      case 6:
        return DatePickerDesign;
      default:
    }
  }, [curModuleStyle]);

  const handleClick = (style) => {
    const defaultTemplate = template.find((item) => {
      return Number(item.style) === Number(style);
    }).default;
    onChange(defaultTemplate, true);
  };

  if (!template) {
    return <></>;
  }

  return (
    <>
      <div className={styles.designerTitle}>
        <Text type="title">Fields Tool</Text>
      </div>
      <div className={styles.ModuleType}>
        {moduleTypeList.map((item) => {
          let Icon = item.icon;
          return (
            <div
              key={item.style}
              className={cn(styles.moduleIcon, styles[item.cls], {
                [styles["active"]]: item.style === curModuleStyle,
              })}
              onClick={() => {
                handleClick(item.style);
              }}
            >
              <Icon className={styles[item.cls]} />
            </div>
          );
        })}
      </div>
      <div className={styles.title}>
        <Text type="subTitle">
          <Intl id="template" />
        </Text>
      </div>
      {currentTemplate && (
        <div className={styles.workflowOptionsType}>
          <div className={styles.workflowItemList}>
            <ModuleTemplate
              templateData={currentTemplate}
              setTemplate={(data) => {
                onChange(data, true);
              }}
            />
          </div>
          {data.edit === 1 && <ModuleEdit data={data} onChange={onChange} />}
        </div>
      )}
    </>
  );
};

export default ModuleSelection;

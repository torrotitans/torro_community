/* third lib*/
import React, { useEffect, useMemo, useState } from "react";
import { FormattedMessage as Intl } from "react-intl";
import { useForm } from "react-hook-form";
import Scrollbar from "react-perfect-scrollbar";
import cn from "classnames";

/* material-ui */
import ArrowBackIcon from "@material-ui/icons/ArrowBack";

/* local components & methods */

import Button from "@basics/Button";
import FormItem from "@comp/FormItem";
import CheckBoxIcon from "@assets/icons/moduleIcon/CheckBoxIcon";
import DropdownIcon from "@assets/icons/moduleIcon/DropdownIcon";
import TextIcon from "@assets/icons/moduleIcon/TextIcon";
import UploadIcon from "@assets/icons/moduleIcon/UploadIcon";
import ToggleIcon from "@assets/icons/moduleIcon/ToggleIcon";
import DatePickerIcon from "@assets/icons/moduleIcon/DatePickerIcon";
import styles from "./styles.module.scss";
import {} from "@lib/api";
import DesignPanel from "./DesignPanel";
import Text from "@basics/Text";
import HeadLine from "@basics/HeadLine";

const moduleTypeList = [
  { style: 1, icon: CheckBoxIcon, cls: "checkbox", temp: "text" },
  { style: 2, icon: DropdownIcon, cls: "dropdown" },
  { style: 3, icon: TextIcon, cls: "text" },
  { style: 4, icon: UploadIcon, cls: "upload" },
  { style: 5, icon: ToggleIcon, cls: "switch" },
  { style: 6, icon: DatePickerIcon, cls: "datepicker" },
];

const styleMap = {
  1: "Checkbox",
  2: "Dropdown",
  3: "Text",
  4: "Upload",
  5: "Toggle",
  6: "Datepicker",
};

const SystemDefineField = ({
  cancelHandle,
  fieldTemplate,
  systemDefineField,
  onChange,
}) => {
  const { control } = useForm(); // initialise the hook
  const [defineData, setDefineData] = useState(systemDefineField);
  const [editData, setEditData] = useState(null);
  const [currentStyle, setCurrentStyle] = useState(1);

  const LatestId = useMemo(() => {
    let maxId = 0;
    Object.keys(defineData).forEach((key) => {
      let fieldList = defineData[key];
      fieldList.forEach((item) => {
        let idI = Number(item.id.replace("s", ""));
        if (idI > maxId) maxId = idI;
      });
    });
    return maxId + 1;
  }, [defineData]);

  const fieldTemplateMap = useMemo(() => {
    let map = {};
    fieldTemplate.forEach((item) => {
      map[item.style] = {
        ...item.default,
        id: `s${LatestId}`,
        label: `System field${LatestId}`,
      };
    });
    return map;
  }, [fieldTemplate, LatestId]);

  const currentModule = useMemo(() => {
    if (!editData) {
      return null;
    }
    return defineData[editData.style][editData.index];
  }, [editData, defineData]);

  const deleteHandle = (index) => {
    let tmpData = JSON.parse(JSON.stringify(defineData));
    tmpData[currentStyle].splice(index, 1);
    setDefineData(tmpData);
  };

  const renderFormItem = (items) => {
    return items.map((item, index) => {
      return (
        <FormItem
          key={index}
          data={item}
          index={index}
          onChange={() => {}}
          onDelete={() => {
            deleteHandle(index);
          }}
          editState={
            editData
              ? editData.index === index && editData.style === item.style
              : false
          }
          onEdit={(key) => {
            if (key) {
              setEditData({
                style: item.style,
                index: index,
              });
            } else {
              setEditData(null);
            }
          }}
          enableEdit={true}
          control={control}
        />
      );
    });
  };

  const currentList = useMemo(() => {
    return defineData[currentStyle];
  }, [defineData, currentStyle]);

  const clickAwayHandle = (e) => {
    setEditData(null);
  };

  useEffect(() => {
    setDefineData({
      1: [],
      2: [],
      3: [],
      4: [],
      5: [],
      6: [],
      ...systemDefineField,
    });
  }, [systemDefineField]);

  return (
    <div className={styles.systemDefineField}>
      <div className={styles.content} onClick={clickAwayHandle}>
        <Scrollbar>
          <div className={styles.defineView}>
            <div
              className={styles.onBack}
              onClick={() => {
                cancelHandle();
              }}
            >
              <ArrowBackIcon />
              <Text type="subTitle">
                <Intl id="back" />
              </Text>
            </div>
            <div className={styles.ModuleType}>
              {moduleTypeList.map((item) => {
                let Icon = item.icon;
                return (
                  <div
                    key={item.style}
                    className={cn(styles.moduleIcon, styles[item.cls], {
                      [styles["active"]]: item.style === currentStyle,
                    })}
                    onClick={() => {
                      setCurrentStyle(item.style);
                    }}
                  >
                    <Icon className={styles[item.cls]} />
                  </div>
                );
              })}
            </div>
            <div className={styles.itemList}>
              <div className={styles.itemType}>
                <div className={styles.itemTypeTitle}>
                  <HeadLine>{styleMap[currentStyle]}</HeadLine>
                  <div
                    className={styles.addFields}
                    onClick={(e) => {
                      let tmp = { ...defineData };
                      tmp[currentStyle].push(fieldTemplateMap[currentStyle]);
                      setDefineData(tmp);
                    }}
                  >
                    <Intl id="addField" />
                  </div>
                </div>
                {currentList && (
                  <div className={styles.itemList}>
                    <div className={styles.items}>
                      {renderFormItem(currentList)}
                    </div>
                  </div>
                )}
              </div>
            </div>
            <div className={styles.buttonWrapper}>
              <Button
                className={styles.button}
                variant="contained"
                onClick={() => {
                  onChange(defineData);
                }}
              >
                <Intl id="save" />
              </Button>
            </div>
          </div>
        </Scrollbar>
      </div>
      <DesignPanel
        id="designPanel"
        currentModule={currentModule}
        onChange={(data) => {
          let tmp = { ...defineData };
          tmp[editData.style][editData.index] = data;
          setDefineData(tmp);
        }}
      />
    </div>
  );
};

export default SystemDefineField;

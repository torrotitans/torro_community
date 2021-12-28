/* third lib*/
import React, { useEffect, useMemo, useState } from "react";
import cn from "classnames";
import { FormattedMessage as Intl } from "react-intl";

/* local components & methods */
import Text from "@comp/basics/Text";
import styles from "./styles.module.scss";

/* moduleDesigb */
import CheckBoxDesign from "../ModuleDesign/CheckBoxDesign";
import DropdownDesign from "../ModuleDesign/DropdownDesign";
import TextDesign from "../ModuleDesign/TextDesign";
import UploadDesign from "../ModuleDesign/UploadDesign";
import SwitchDesign from "../ModuleDesign/SwitchDesign";
import DatePickerDesign from "../ModuleDesign/DatePickerDesign";

const ModuleSelection = ({ data, onChange }) => {
  const curModuleStyle = useMemo(() => {
    return data.style;
  }, [data]);

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

  return (
    <>
      <div className={styles.designerTitle}>
        <Text type="title">Fields Tool</Text>
      </div>
      <div className={styles.moduleEdit}>
        <ModuleEdit data={data} onChange={onChange} />
      </div>
    </>
  );
};

export default ModuleSelection;

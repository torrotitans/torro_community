/* third lib*/
import React, { useEffect, useState, useCallback, useMemo } from "react";
import { FormattedMessage as Intl } from "react-intl";
import { useForm } from "react-hook-form";
import cn from "classnames";

/* material-ui */
import RemoveRedEye from "@material-ui/icons/RemoveRedEye";

/* local components & methods */
import FormItem from "@comp/FormItem";
import PolicyTags from "@comp/PolicyTags";
import styles from "./styles.module.scss";
import Model from "@comp/Model";

const Form = ({ formId, data }) => {
  const { handleSubmit, control, register } = useForm(); // initialise the hook
  const renderFormItem = (items, disabled) => {
    return items.map((item, index) => {
      return (
        <FormItem
          key={index}
          data={item}
          index={index}
          control={control}
          register={register}
          disabled={disabled}
          fullWidth={formId != 101}
        />
      );
    });
  };
  return (
    <form id={`currentForm${formId}`} className={styles.form}>
      <div className={styles.formOptions}>{renderFormItem(data)}</div>
    </form>
  );
};

const PolicyTree = ({ formId, data }) => {
  return <PolicyTags value={data} onChange={(data) => {}} displayView />;
};

const SpecialField = ({ formId, fieldLabel, data }) => {
  const [open, setOpen] = useState(false);

  const FieldDisplay = useMemo(() => {
    if (fieldLabel === "fieldList") {
      return Form;
    }
    if (formId == 3) {
      return PolicyTree;
    }
  }, [formId, fieldLabel]);

  return (
    <>
      <div className={styles.viewIcon}>
        <RemoveRedEye
          onClick={() => {
            setOpen(true);
          }}
        />
      </div>

      <Model
        open={open}
        handleClose={() => {
          setOpen(false);
        }}
      >
        <div className={styles.mask}></div>
        <FieldDisplay formId={formId} data={data} />
      </Model>
    </>
  );
};

export default SpecialField;

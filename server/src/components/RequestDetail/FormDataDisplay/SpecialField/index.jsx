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
import TableTagDisplay from "@comp/TableTagDisplay";
import OnboardDataDisplay from "@comp/OnboardDataDisplay";
import styles from "./styles.module.scss";
import Model from "@comp/basics/Modal";
import UsecaseInfo from "@comp/UsecaseInfo";

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
          fullWidth={![101, 102, 103].includes(formId)}
        />
      );
    });
  };
  return (
    <>
      <div className={styles.mask}></div>
      <form id={`currentForm${formId}`} className={styles.form}>
        <div className={styles.formOptions}>{renderFormItem(data)}</div>
      </form>
    </>
  );
};

const PolicyTree = ({ formId, data }) => {
  return <PolicyTags value={data} onChange={(data) => {}} displayView />;
};

const TableTags = ({ data }) => {
  return (
    <div>
      {data.map((tag, index) => {
        return <TableTagDisplay key={index} tagData={tag} />;
      })}
    </div>
  );
};

const TableDisplay = ({ data }) => {
  return <OnboardDataDisplay tableList={data} />;
};

const UseCase = ({ data }) => {
  return <UsecaseInfo tableList={data} usecaseId={366} />;
};

const SpecialField = ({ formId, fieldLabel, data, type }) => {
  const [open, setOpen] = useState(false);

  const FieldDisplay = useMemo(() => {
    if (type === "usecase") {
      return UseCase;
    }
    if (fieldLabel === "fieldList") {
      return Form;
    }
    if (formId === 3) {
      return PolicyTree;
    }
    if (formId === 107 || formId === 108) {
      if (fieldLabel === "Table Tags") {
        return TableTags;
      }
      if (fieldLabel === "Fields") {
        return TableDisplay;
      }
    }
  }, [formId, fieldLabel, type]);

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
        <div className={styles.modalContent}>
          <FieldDisplay formId={formId} data={data} />
        </div>
      </Model>
    </>
  );
};

export default SpecialField;

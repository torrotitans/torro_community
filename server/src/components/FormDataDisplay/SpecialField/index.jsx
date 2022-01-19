/* third lib*/
import React, { useEffect, useState, useMemo } from "react";
import { useForm } from "react-hook-form";

/* material-ui */
import RemoveRedEye from "@material-ui/icons/RemoveRedEye";

/* local components & methods */
import FormItem from "@comp/FormItem";
import PolicyTags from "@comp/PolicyTags";
import TableTagDisplay from "@comp/TableTag";
import OnboardDataDisplay from "@comp/OnboardDataDisplay";
import styles from "./styles.module.scss";
import Model from "@basics/Modal";
import UsecaseInfo from "@comp/UsecaseInfo";
import { getUseCaseList } from "@lib/api";
import { sendNotify } from "src/utils/systerm-error";

const Form = ({ formId, data }) => {
  const { control, register } = useForm(); // initialise the hook
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
  const [useCaseId, setUsecaseId] = useState();
  useEffect(() => {
    getUseCaseList()
      .then((res) => {
        if (res.data) {
          res.data.forEach((item) => {
            if (item.usecase_name === data) {
              setUsecaseId(item.id);
            }
          });
        }
      })
      .catch((e) => {
        sendNotify({ msg: e.message, status: 3, show: true });
      });
  }, [data]);

  if (!useCaseId) {
    return <></>;
  }
  return <UsecaseInfo tableList={data} usecaseId={useCaseId} />;
};

const SpecialField = ({ formId, data, special }) => {
  const [open, setOpen] = useState(false);

  const FieldDisplay = useMemo(() => {
    switch (special?.comp) {
      case "UseCase":
        return UseCase;
      case "Form":
        return Form;
      case "PolicyTree":
        return PolicyTree;
      case "TableTags":
        return TableTags;
      case "TableDisplay":
        return TableDisplay;

      default:
        break;
    }
  }, [special]);

  return (
    <div className={styles.specialField}>
      {special.showValue && <div className={styles.specialStr}>{data}</div>}
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
    </div>
  );
};

export default SpecialField;

/* third lib*/
import React, { useEffect, useState, useCallback } from "react";
import { FormattedMessage as Intl } from "react-intl";
import { useForm } from "react-hook-form";
import Scrollbar from "react-perfect-scrollbar";

/* local components & methods */
import HeadLine from "@comp/HeadLine";
import FormItem from "@comp/FormItem";
import Button from "@comp/Button";
import styles from "./styles.module.scss";
import { getWsList, getFormItem, wsPut, raiseFormRequest } from "@lib/api";
import Loading from "src/icons/Loading";
import { sendNotify } from "src/utils/systerm-error";
import CallModal from "@comp/CallModal";
import { SUCCESS } from "src/lib/data/callStatus";

const UseCaseCreation = () => {
  const { handleSubmit, control, register } = useForm(); // initialise the hook
  const [formData, setFormData] = useState(null);
  const [formLoading, setFormLoading] = useState(true);

  const [submitData, setSubmitData] = useState(null);
  const [modalData, setModalData] = useState({
    open: false,
    status: 0,
    content: "",
  });

  const buttonClickHandle = useCallback(() => {
    let apiCall = raiseFormRequest;
    let postData = submitData;
    return;
    switch (modalData.status) {
      case 1:
      case 3:
        setModalData({
          ...modalData,
          status: 0,
          content: <Intl id="loadNpatience" />,
        });
        apiCall(postData)
          .then((res) => {
            if (res.code === SUCCESS) {
              setModalData({
                open: true,
                status: 2,
                content: <Intl id="wsIsAdd" />,
              });
            }
          })
          .catch(() => {
            setModalData({
              ...modalData,
              status: 3,
              content: <Intl id="checkInput" />,
            });
          });
        break;
      default:
        setModalData({ ...modalData, open: false });
        break;
    }
  }, [modalData, submitData]);

  const submitHandle = useCallback((data) => {
    setModalData({
      open: true,
      status: 1,
      content: <Intl id="confirmAddWS" />,
    });
    setSubmitData({
      ...data,
    });
  }, []);

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
        />
      );
    });
  };

  useEffect(() => {
    setFormLoading(true);
    getFormItem({
      id: 2,
    })
      .then((res) => {
        if (res.code === 200) {
          let data = res.data;
          let tempFieldList = data.fieldList.map((item) => {
            if (item.style === 6) {
              item.default = new Date();
            }
            return item;
          });
          setFormData({
            ...data,
            fieldList: tempFieldList,
          });
          setFormLoading(false);
        }
      })
      .catch((e) => {
        sendNotify({ msg: e.message, status: 3, show: true });
      });
  }, []);

  return (
    <div className={styles.useCaseCreation}>
      <div className={styles.formView}>
        <Scrollbar>
          {formLoading && <Loading />}
          {!formLoading && formData && (
            <div className={styles.formControl}>
              <HeadLine>
                <Intl id="createUc" />
              </HeadLine>
              <form
                className={styles.form}
                id={`currentForm${formData.id}`}
                onSubmit={handleSubmit(submitHandle)}
              >
                <div className={styles.formOptions}>
                  {renderFormItem(formData.fieldList)}
                </div>
                <div className={styles.buttonWrapper}>
                  <Button
                    className={styles.button}
                    type="submit"
                    variant="contained"
                  >
                    <Intl id="submit" />
                  </Button>
                </div>
              </form>
              <CallModal
                open={modalData.open}
                content={modalData.content}
                status={modalData.status}
                buttonClickHandle={() => {
                  if (!modalData.cb) {
                    buttonClickHandle();
                  } else {
                    modalData.cb();
                  }
                }}
                handleClose={() => {
                  setModalData({ ...modalData, open: false });
                }}
              />
            </div>
          )}
        </Scrollbar>
      </div>
    </div>
  );
};

export default UseCaseCreation;

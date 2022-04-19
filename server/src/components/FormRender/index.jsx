/* third lib*/
import React, { useEffect, useState, useCallback } from "react";
import { FormattedMessage as Intl } from "react-intl";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";
import ScrollBar from "react-perfect-scrollbar";

/* local components & methods */
import FormItem from "@comp/FormItem";
import Button from "@basics/Button";
import HeadLine from "@basics/HeadLine";
import Text from "@basics/Text";
import styles from "./styles.module.scss";
import {
  getFormItem,
  raiseFormRequest,
  updateFormRequest,
  getUcResource,
} from "@lib/api";
import Loading from "@assets/icons/Loading";
import { sendNotify } from "src/utils/systerm-error";
import CallModal from "@basics/CallModal";
import { SUCCESS } from "src/lib/data/callStatus";
import { useMemo } from "react";

const UC_FORM_ID = "2";
const specialForm = [{ id: 2, torroDefField: ["s1", "u2", "u3", "u8", "u11"] }];
const UC_PROP_MAP = {
  u2: "owner_group",
  u3: "team_group",
  u8: "service_account",
  u11: "label",
};

const UC_PROP = ["u2", "u3", "u8", "u11"];

const FormRender = ({ formId, onBack, defaultData }) => {
  const navigate = useNavigate();
  const { handleSubmit, control, register, setValue } = useForm(); // initialise the hook
  const [formData, setFormData] = useState(null);
  const [formLoading, setFormLoading] = useState(true);
  const [submitData, setSubmitData] = useState(null);
  const [ucDef, setUcDef] = useState({});
  const [modalData, setModalData] = useState({
    open: false,
    status: 0,
    content: "",
  });

  const ucForm = useMemo(() => {
    return formId === UC_FORM_ID;
  }, [formId]);

  const specialField = useMemo(() => {
    if (!formData) {
      return [];
    }
    let tmp = [];
    specialForm.forEach((item) => {
      if (item.id === formData.id) tmp = item.torroDefField || [];
    });

    return tmp;
  }, [formData]);

  const buttonClickHandle = useCallback(() => {
    let apiCall = defaultData ? updateFormRequest : raiseFormRequest;
    let postData = submitData;

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
                content: <Intl id="newRequestSubmit" />,
                successCb: () => {
                  navigate(`/app/requestDetail?id=${res.data.id}`);
                },
              });
            }
          })
          .catch((e) => {
            setModalData({
              ...modalData,
              status: 3,
              content: e.message,
            });
          });
        break;
      default:
        setModalData({ ...modalData, open: false });
        break;
    }
  }, [modalData, submitData, defaultData, navigate]);

  const submitHandle = useCallback(
    (data, d, f) => {
      setModalData({
        open: true,
        status: 1,
        content: <Intl id="confirmRaise" />,
      });
      let files = {};
      Object.keys(data).forEach((key) => {
        if (data[key] instanceof Array && data[key][0] instanceof File) {
          data[key].forEach((item, index) => {
            files[key + "-" + (index + 1)] = item;
          });
          data[key] = [];
        }
      });
      if (ucForm) {
        UC_PROP.forEach((key) => {
          data[key] = ucDef[key][data[key]];
        });
      }
      setSubmitData({
        ...files,
        form_id: formId,
        form_field_values_dict: data,
      });
    },
    [formId, setSubmitData, ucForm, ucDef]
  );

  const renderFormItem = useCallback(
    (items, disabled) => {
      return items.map((item, index) => {
        return (
          <FormItem
            key={index}
            data={item}
            index={index}
            control={control}
            register={register}
            disabled={disabled}
            changeCb={(e) => {
              if (ucForm && UC_PROP.includes(item.id)) {
                UC_PROP.forEach((key) => {
                  setValue(key, e);
                });
              }
            }}
            specialField={specialField}
          />
        );
      });
    },
    [control, register, setValue, ucForm, specialField]
  );

  const initUcDef = useCallback((tempFieldList, formData) => {
    getUcResource()
      .then((res2) => {
        if (res2.data) {
          let tmpUcDef = {};
          Object.keys(UC_PROP_MAP).forEach((key) => {
            tmpUcDef[key] = [];
          });
          res2.data.forEach((item, index) => {
            Object.keys(UC_PROP_MAP).forEach((key) => {
              tmpUcDef[key].push(item.resource[UC_PROP_MAP[key]]);
            });
          });
          setUcDef(tmpUcDef);
          tempFieldList = tempFieldList.map((item) => {
            if (UC_PROP.includes(item.id)) {
              item.style = 2;
              item.options = tmpUcDef[item.id].map((val, index) => ({
                label: val,
                value: index,
              }));
            }
            return item;
          });
          setFormData({
            ...formData,
            fieldList: tempFieldList,
          });
          setFormLoading(false);
        }
      })
      .catch((e) => {
        sendNotify({ msg: e.message, status: 3, show: true });
      });
  }, []);

  useEffect(() => {
    setFormLoading(true);
    getFormItem({
      id: formId,
    })
      .then((res) => {
        if (res.code === 200) {
          let data = res.data;
          let tempFieldList = data.fieldList.map((item) => {
            if (defaultData && defaultData[item.id]) {
              item.default = defaultData[item.id];
            }
            return item;
          });

          if (ucForm) {
            initUcDef(tempFieldList, data);
            return;
          }
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
  }, [formId, defaultData, initUcDef, ucForm]);

  return (
    <div className={styles.formRender}>
      <ScrollBar>
        <div className={styles.formControl}>
          {formLoading && <Loading />}
          {!formLoading && formData && (
            <>
              <div className={styles.formTitle}>
                <HeadLine>{formData.title}</HeadLine>
              </div>
              <div className={styles.formDes}>
                <Text>{formData.des}</Text>
              </div>
              <form
                className={styles.form}
                onSubmit={handleSubmit(submitHandle)}
              >
                <div className={styles.formOptions}>
                  {renderFormItem(formData.fieldList)}
                </div>
                <div className={styles.buttonWrapper}>
                  {onBack && (
                    <Button
                      onClick={() => {
                        onBack();
                      }}
                      className={styles.button}
                      variant="contained"
                    >
                      <Intl id="cancel" />
                    </Button>
                  )}
                  <Button
                    className={styles.button}
                    type="submit"
                    variant="contained"
                  >
                    <Intl id="submit" />
                  </Button>
                </div>
              </form>
            </>
          )}
          <CallModal
            open={modalData.open}
            content={modalData.content}
            status={modalData.status}
            successCb={modalData.successCb}
            buttonClickHandle={buttonClickHandle}
            handleClose={() => {
              setModalData({ ...modalData, open: false });
            }}
          />
        </div>
      </ScrollBar>
    </div>
  );
};

export default FormRender;

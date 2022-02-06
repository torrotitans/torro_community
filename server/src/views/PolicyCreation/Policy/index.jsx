/* third lib*/
import React, { useEffect, useState, useCallback } from "react";
import { FormattedMessage as Intl } from "react-intl";
import { useForm } from "react-hook-form";
import Scrollbar from "react-perfect-scrollbar";

/* material-ui */
import FormLabel from "@material-ui/core/FormLabel";

/* local components & methods */
import HeadLine from "@basics/HeadLine";
import FormItem from "@comp/FormItem";
import Button from "@basics/Button";
import Text from "@basics/Text";
import styles from "./styles.module.scss";
import { wsPut, wsPost, getPolicyDetail, getPolicyForm } from "@lib/api";
import Loading from "@assets/icons/Loading";
import CallModal from "@basics/CallModal";
import { SUCCESS } from "src/lib/data/callStatus";
import { sendNotify } from "src/utils/systerm-error";
import PolicyTags from "../PolicyTags";

const Policy = ({ currentId, onBack }) => {
  const { handleSubmit, control, register } = useForm(); // initialise the hook
  const [formData, setFormData] = useState(null);
  const [formLoading, setFormLoading] = useState(true);

  const [currentData, setCurrentData] = useState(null);
  const [policTags, setPolicTags] = useState([]);
  const [submitData, setSubmitData] = useState(null);
  const [policyId, setPolicyId] = useState(currentId);
  const [modalData, setModalData] = useState({
    open: false,
    status: 0,
    content: "",
  });

  const buttonClickHandle = useCallback(() => {
    let apiCall = policyId ? wsPut : wsPost;
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
                content: policyId ? (
                  <Intl id="wsUpdated" />
                ) : (
                  <Intl id="wsIsAdd" />
                ),
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
  }, [modalData, submitData, policyId]);

  const submitHandle = useCallback(
    (data) => {
      setModalData({
        open: true,
        status: 1,
        content: policyId ? (
          <Intl id="confirmUpdatePolicy" />
        ) : (
          <Intl id="confirmAddPolicy" />
        ),
      });
      setSubmitData({
        ...currentData,
        ...data,
        policy_tags: policTags,
      });
    },
    [policTags, currentData, policyId]
  );

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
    setPolicyId(currentId);
    getPolicyForm()
      .then((res) => {
        if (res.data) {
          let policyForm = res.data;
          getPolicyDetail({ id: currentId }).then((res) => {
            let data = res.data;
            let tmp = JSON.parse(JSON.stringify(policyForm));
            let tmpFieldList = tmp.fieldList.map((item) => {
              if (item.id && data[item.id]) {
                item.default = data[item.id];
              }
              return item;
            });
            setPolicTags(data.policy_tags);
            setFormData({
              ...tmp,
              fieldList: tmpFieldList,
              title: data.ws_name,
              des: data.ws_des,
            });
            setCurrentData(data);
            setFormLoading(false);
          });
        }
      })
      .catch((e) => {
        sendNotify({ msg: e.message, status: 3, show: true });
      });
  }, [currentId]);

  return (
    <div className={styles.policy}>
      <div className={styles.formView}>
        <Scrollbar>
          {formLoading && <Loading />}
          {!formLoading && formData && (
            <div className={styles.formControl}>
              <HeadLine>
                {policyId ? (
                  <Intl id="createPolicy" />
                ) : (
                  <Intl id="createPolicy" />
                )}
              </HeadLine>
              <form
                className={styles.form}
                id={`currentForm${formData.id}`}
                onSubmit={handleSubmit(submitHandle)}
              >
                <div className={styles.formOptions}>
                  {renderFormItem(formData.fieldList)}
                </div>
                <div className={styles.formItemLine}>
                  <div className={styles.formItemTitle}>
                    <FormLabel className={styles.fieldTitle}>
                      <Text type="subTitle">
                        <Intl id="policyTagStru" />
                      </Text>
                    </FormLabel>
                  </div>
                  <PolicyTags
                    policTags={policTags}
                    onChange={(data) => {
                      setPolicTags(data);
                    }}
                  />
                </div>
                <div className={styles.buttonWrapper}>
                  <Button
                    onClick={() => {
                      onBack();
                    }}
                    className={styles.button}
                    variant="contained"
                  >
                    <Intl id="back" />
                  </Button>
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

export default Policy;

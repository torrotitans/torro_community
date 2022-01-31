/*third lib*/
import React, { useCallback, useEffect } from "react";
import { useForm } from "react-hook-form";
import { FormattedMessage as Intl } from "react-intl";
import { useNavigate } from "react-router-dom";
import Scrollbar from "react-perfect-scrollbar";

/*local components && methods*/
import withAuthentication from "src/hoc/withAuthentication";
import Button from "@basics/Button";
import Torro from "@assets/icons/Torrotext";
import styles from "./styles.module.scss";
import { getOrgForm, OrgSetup } from "@lib/api";
import { useGlobalContext } from "src/context";
import HeadLine from "@basics/HeadLine";
import decode from "src/utils/encode.js";
import Text from "@basics/Text";
import { sendNotify } from "src/utils/systerm-error";
import { useState } from "react";
import FormItem from "@comp/FormItem";
import Loading from "@assets/icons/Loading";

const OrgSetting = () => {
  const { handleSubmit, control, register } = useForm(); // initialise the hook
  const { Encrypt } = decode;
  const { setAuth, authContext } = useGlobalContext();
  const [formData, setFormData] = useState(null);
  const [formLoading, setFormLoading] = useState(true);

  let navigate = useNavigate();

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

  const submitHandle = useCallback(
    (data) => {
      data.admin_pwd = Encrypt(data.admin_pwd);
      data.use_ssl = data.use_ssl === "false" ? false : true;
      OrgSetup(data)
        .then((res) => {
          if (res.data) {
            setAuth({
              ...authContext,
              init: false,
            });
            navigate("/login", {
              replace: true,
            });
          }
        })
        .catch((e) => {
          sendNotify({ msg: e.message, status: 3, show: true });
        });
    },
    [Encrypt, authContext, navigate, setAuth]
  );

  useEffect(() => {
    getOrgForm()
      .then((res) => {
        if (res.data) {
          setFormData(res.data);
          setFormLoading(false);
        }
      })
      .catch((e) => {
        sendNotify({ msg: e.message, status: 3, show: true });
      });
  }, []);

  return (
    <div className={styles.orgSettingPage}>
      <Scrollbar>
        {formLoading && <Loading />}
        {!formLoading && formData && (
          <div className={styles.pageBox}>
            <div className={styles.logo}>
              <Torro />
            </div>
            <div className={styles.title}>
              <HeadLine>{formData.title}</HeadLine>
              <div className={styles.formDes}>
                <Text>{formData.des}</Text>
              </div>
            </div>
            <div className={styles.formControl}>
              <form
                className={styles.form}
                id={`currentForm${formData.id}`}
                onSubmit={handleSubmit(submitHandle)}
              >
                <div className={styles.formOptions}>
                  {renderFormItem(formData.fieldList)}
                </div>

                <div className={styles.buttonWrapper}>
                  <Button className={styles.button} type="submit" filled>
                    <Intl id="setup" />
                  </Button>
                </div>
              </form>
            </div>
          </div>
        )}
      </Scrollbar>
    </div>
  );
};
export default withAuthentication(OrgSetting);

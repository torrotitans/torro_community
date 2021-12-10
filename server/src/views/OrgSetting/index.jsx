/*third lib*/
import React, { useCallback } from "react";
import { useForm } from "react-hook-form";
import { FormattedMessage as Intl } from "react-intl";
import { useNavigate } from "react-router-dom";

/*local components && methods*/
import withAuthentication from "src/hoc/withAuthentication";
import UserInput from "@comp/UserComp/UserInput";
import UserFileUpload from "@comp/UserComp/UserFileUpload";
import Button from "@comp/Button";
import Torro from "src/icons/Torrotext";
import styles from "./styles.module.scss";
import { OrgSetup } from "@lib/api";
import { useGlobalContext } from "src/context";
import HeadLine from "@comp/HeadLine";
import decode from "src/utils/encode.js";
import Text from "@comp/Text";

const OrgSetting = () => {
  const { handleSubmit, reset, control, register } = useForm(); // initialise the hook
  const { Encrypt } = decode;
  const { setAuth, authContext } = useGlobalContext();
  let navigate = useNavigate();

  const submitHandle = useCallback(
    (data) => {
      data.admin_pwd = Encrypt(data.admin_pwd);
      data.use_sll = Boolean(data.use_sll);
      OrgSetup(data).then((res) => {
        if (res.data) {
          setAuth({
            ...authContext,
            init: false,
          });
          navigate("/login", {
            replace: true,
          });
        }
      });
    },
    [Encrypt, authContext, navigate, setAuth]
  );

  return (
    <div className={styles.orgSettingPage}>
      <div className={styles.pageBox}>
        <div className={styles.logo}>
          <Torro />
        </div>
        <div className={styles.title}>
          <HeadLine>
            <Intl id="projectSetup" />
          </HeadLine>
          <div className={styles.formDes}>
            <Text>
              <Intl id="setupDes" />
            </Text>
          </div>
        </div>
        <form
          className={styles.settingForm}
          onSubmit={handleSubmit(submitHandle)}
        >
          <div className={styles.formContent}>
            <div className={styles.formItem}>
              <UserInput
                label={<Intl id="host" />}
                id="host"
                name="host"
                autoFocus
                control={control}
              />
            </div>
            <div className={styles.formItem}>
              <UserInput
                label={<Intl id="port" />}
                id="port"
                name="port"
                autoFocus
                control={control}
              />
            </div>
            <div className={styles.formItem}>
              <UserFileUpload
                ref={register}
                label={<Intl id="cer_path" />}
                id="cer_path"
                type="file"
                name="cer_path"
                control={control}
              />
            </div>
            <div className={styles.formItem}>
              <UserInput
                label={<Intl id="use_sll" />}
                id="use_sll"
                name="use_sll"
                autoFocus
                control={control}
              />
            </div>
            <div className={styles.formItem}>
              <UserInput
                label={<Intl id="admin" />}
                id="admin"
                name="admin"
                autoFocus
                control={control}
              />
            </div>
            <div className={styles.formItem}>
              <UserInput
                label={<Intl id="admin_pwd" />}
                type="password"
                id="admin_pwd"
                name="admin_pwd"
                control={control}
              />
            </div>
            <div className={styles.formItem}>
              <UserInput
                label={<Intl id="admin_group" />}
                id="admin_group"
                name="admin_group"
                autoFocus
                control={control}
              />
            </div>
            <div className={styles.formItem}>
              <UserInput
                label={<Intl id="base_group" />}
                id="base_group"
                name="base_group"
                autoFocus
                control={control}
              />
            </div>
            <div className={styles.formItem}>
              <UserInput
                label={<Intl id="org_name" />}
                id="org_name"
                name="org_name"
                autoFocus
                control={control}
              />
            </div>
            <div className={styles.formItem}>
              <UserInput
                label={<Intl id="des" />}
                id="des"
                name="des"
                autoFocus
                control={control}
              />
            </div>
            <div className={styles.formItem}>
              <UserInput
                label={<Intl id="search_base" />}
                id="search_base"
                name="search_base"
                autoFocus
                control={control}
              />
            </div>
          </div>
          <div className={styles.buttonGroup}>
            <Button className={styles.button} type="submit" filled>
              <Intl id="setup" />
            </Button>
            <Button onClick={reset} className={styles.button}>
              <Intl id="reset" />
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
};
export default withAuthentication(OrgSetting);

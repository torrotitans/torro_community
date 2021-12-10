/*third lib*/
import React, { useCallback, useState } from "react";
import { useForm } from "react-hook-form";
import { FormattedMessage as Intl } from "react-intl";
import { useNavigate } from "react-router-dom";
import cn from "classnames";

/*local components && methods*/
import withAuthentication from "src/hoc/withAuthentication";
import UserInput from "@comp/UserComp/UserInput";
import Button from "@comp/Button";
import Torro from "src/icons/Torrotext";
import styles from "./styles.module.scss";
import { LoginCall } from "@lib/api";
import { useGlobalContext } from "src/context";
import decode from "src/utils/encode.js";
import CallModal from "@comp/CallModal";

const LoginPage = () => {
  const { handleSubmit, reset, control } = useForm(); // initialise the hook
  const { Encrypt } = decode;
  const { setAuth, authContext } = useGlobalContext();
  const [logining, setLogining] = useState(false);
  let navigate = useNavigate();
  const [modalData, setModalData] = useState({
    open: false,
    status: 0,
    content: "",
    cb: null,
  });

  const submitHandle = useCallback(
    (data) => {
      if (logining) return;
      data.login_password = Encrypt(data.login_password);
      setLogining(true);
      LoginCall(data)
        .then((res) => {
          if (res.msg === "[ORG_SETTING]") {
            let tmpAuth = {
              ...authContext,
              init: true,
            };
            setAuth(tmpAuth);
            navigate("/orgSetting", {
              replace: true,
            });
          }

          if (res.msg === "request successfully" && res.data) {
            let data = res.data;
            let tmpAuth = {
              ...authContext,
              userName: data.ACCOUNT_NAME,
              userId: data.ID,
              accountId: data.ACCOUNT_ID,
              roleList: data.role_list,
              role: "",
              wsList: data.workspace_list,
              wsId: data.workspace_id,
              ad_group_list: data.ad_group_list,
            };

            if (data.role_list.length > 1) {
              setAuth(tmpAuth);
              navigate("/roleSelect", { replace: true });
            } else {
              tmpAuth = {
                ...tmpAuth,
                role: data.role_list[0],
              };
              setAuth(tmpAuth);
              navigate("/", { replace: true });
            }
          }
        })
        .catch((e) => {
          setLogining(false);
          setModalData({
            ...modalData,
            open: true,
            status: 3,
            content: <Intl id="goesWrong" />,
            buttonText: "close",
            cb: null,
          });
        });
    },
    [authContext, Encrypt, navigate, setAuth, modalData, logining]
  );

  return (
    <div className={styles.loginPage}>
      <div className={styles.loginBox}>
        <div className={styles.logo}>
          <Torro />
        </div>
        <form
          className={styles.loginForm}
          onSubmit={handleSubmit(submitHandle)}
        >
          <div className={styles.formItem}>
            <UserInput
              label={<Intl id="userName" />}
              id="login_name"
              name="login_name"
              autoFocus
              control={control}
            />
          </div>
          <div className={styles.formItem}>
            <UserInput
              label={<Intl id="pwd" />}
              type="password"
              id="login_password"
              name="login_password"
              control={control}
            />
          </div>
          {logining ? (
            <Button className={cn(styles.button, styles.disabled)} filled>
              <Intl id="logining" />
            </Button>
          ) : (
            <Button className={styles.button} type="submit" filled>
              <Intl id="login" />
            </Button>
          )}
          <Button onClick={reset} className={styles.button}>
            <Intl id="reset" />
          </Button>
        </form>
      </div>
      <CallModal
        open={modalData.open}
        content={modalData.content}
        status={modalData.status}
        buttonText={modalData.buttonText}
        buttonClickHandle={() => {
          if (!modalData.cb) {
            setModalData({ ...modalData, open: false, cb: null });
          } else {
            modalData.cb();
          }
        }}
        handleClose={() => {
          setModalData({ ...modalData, open: false, cb: null });
        }}
      />
    </div>
  );
};

export default withAuthentication(LoginPage);

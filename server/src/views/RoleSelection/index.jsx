/* third lib*/
import React from "react";
import { useNavigate } from "react-router-dom";
import { FormattedMessage as Intl } from "react-intl";

/* local components & methods */
import Torro from "@assets/icons/Torro";
import { default as dataUser } from "@assets/roleBtn/dataUser.svg";
import { default as dataGovernor } from "@assets/roleBtn/dataGovernor.svg";
import { default as itAdmin } from "@assets/roleBtn/itAdmin.svg";
import styles from "./styles.module.scss";
import { useGlobalContext } from "src/context";
import { USER, GOVERNOR, IT } from "src/lib/data/roleType.js";
import withAuthentication from "src/hoc/withAuthentication";
import { updateLogin } from "@lib/api";
import { sendNotify } from "src/utils/systerm-error";
import { useMemo } from "react";

const RoleSelection = () => {
  const { setAuth, authContext } = useGlobalContext();

  let navigate = useNavigate();

  const selectRoleHandle = (role) => {
    updateLogin({ role_name: role })
      .then((res) => {
        if (res.data) {
          setAuth({
            ...authContext,
            role: role,
          });
          navigate("/app/dashboard");
        }
      })
      .catch((e) => {
        sendNotify({
          msg: e.message,
          status: 3,
          show: true,
        });
      });
  };

  /* temp logic start */
  const roleList = useMemo(() => {
    const realRoles = ["USER", "IT", "GOVERNOR"];
    if (authContext.roleList.length > 0) {
      return authContext.roleList.filter((role) => realRoles.includes(role));
    } else {
      return [];
    }
  }, [authContext.roleList]);
  /* temp logic end*/

  return (
    <div className={styles.roleSelection}>
      <Torro className={styles.logo} />
      <div className={styles.messageBox}>
        <div className={styles.userName}>Hi, {authContext.userName}.</div>
        <div className={styles.message}>
          <Intl id="plsSelectRole" />
        </div>
      </div>
      <div className={styles.roleGroup}>
        {roleList.map((item) => {
          let tmpSrc;
          switch (item) {
            case USER:
              tmpSrc = dataUser;
              break;
            case GOVERNOR:
              tmpSrc = dataGovernor;
              break;
            case IT:
              tmpSrc = itAdmin;
              break;
            default:
              tmpSrc = dataUser;
          }
          return (
            <img
              onClick={() => {
                selectRoleHandle(item);
              }}
              key={item}
              className={styles.btn}
              src={tmpSrc}
              alt=""
            />
          );
        })}
      </div>
    </div>
  );
};

export default withAuthentication(RoleSelection);

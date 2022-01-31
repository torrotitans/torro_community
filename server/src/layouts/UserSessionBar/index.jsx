/* third lib*/
import React, { useState, useCallback, useMemo } from "react";
import ClickAwayListener from "@material-ui/core/ClickAwayListener";
import { useNavigate } from "react-router-dom";

/* material-ui */
import MenuIcon from "@material-ui/icons/Menu";
import NotificationsIcon from "@material-ui/icons/Notifications";
import AccountCircleIcon from "@material-ui/icons/AccountCircle";

/* local components & methods */
import styles from "./styles.module.scss";
import { useGlobalContext } from "src/context";
import { USER, GOVERNOR, IT, ADMIN } from "src/lib/data/roleType.js";
import LANGUAGE from "src/lib/data/languageType";
import Model from "@basics/Modal";
import DoubleSquare from "@assets/icons/DoubleSquare";
import DoubleCircle from "@assets/icons/DoubleCircle";
import DoubleTriangle from "@assets/icons/DoubleTriangle";
import LeftNav from "src/components/LeftNav";
import Text from "@basics/Text";
import Torro from "@assets/icons/Torrotext";
import Select from "@basics/Select";
import { sendNotify } from "src/utils/systerm-error";
import { updateLogin } from "@lib/api";
import { useEffect } from "react";

const UserTag = ({ role }) => {
  const { setAuth, authContext } = useGlobalContext();
  let navigate = useNavigate();

  const navigateToRoleSelect = useCallback(() => {
    if (authContext.roleList.length > 1) {
      setAuth({
        ...authContext,
        role: "",
      });
      navigate("/roleSelect", {
        replace: true,
      });
    }
  }, [setAuth, authContext, navigate]);

  return (
    <div className={styles.userTag} onClick={navigateToRoleSelect}>
      {role === IT && (
        <>
          <DoubleTriangle className={styles.svgIcon} />
          <div className={styles.iconLabel}>IT ADMIN</div>
        </>
      )}
      {role === GOVERNOR && (
        <>
          <DoubleCircle className={styles.svgIcon} />
          <div className={styles.iconLabel}>DATA GOVERNOR</div>
        </>
      )}
      {role === USER && (
        <>
          <DoubleSquare className={styles.svgIcon} />
          <div className={styles.iconLabel}>DATA USER</div>
        </>
      )}
    </div>
  );
};

const UserSessionBar = () => {
  const {
    authContext,
    setAuth,
    languageContext,
    setLanguage,
  } = useGlobalContext();
  const [notifyNum, setNotifyNum] = useState(1);
  const [openModel, setOpenModel] = useState(false);

  const [showNav, setShowNav] = useState(false);

  const handleClose = () => {
    setShowNav(false);
  };

  const notifyClickHandle = () => {
    setOpenModel(true);
  };
  const closeHandle = () => {
    setOpenModel(false);
  };

  const isLogin = useMemo(() => {
    return authContext.userId && authContext.userId !== "null";
  }, [authContext]);

  const haveRole = useMemo(() => {
    return !!authContext.role && authContext.role !== "null";
  }, [authContext]);

  const serviceAdmin = useMemo(() => {
    return authContext.serviceAdmin;
  }, [authContext]);

  const handleWsChange = useCallback(
    (value) => {
      let postData = {
        workspace_id: value,
        role_name: authContext.role !== ADMIN ? "" : ADMIN,
      };
      updateLogin(postData)
        .then((res) => {
          if (res.data) {
            setAuth({
              ...authContext,
              role: res.data.role_name,
              roleList: res.data.role_list,
              wsId: Number(res.data.workspace_id),
              wsList: res.data.workspace_list,
            });
            setTimeout(() => {
              window.location.reload();
            }, 0);
          }
        })
        .catch((e) => {
          sendNotify({ msg: e.message, status: 3, show: true });
        });
    },
    [setAuth, authContext]
  );

  const haveWs = useMemo(() => {
    return authContext.wsList.length > 0 && authContext.wsId;
  }, [authContext]);

  const displayNav = useMemo(() => {
    return isLogin && (haveRole || serviceAdmin) && haveWs;
  }, [isLogin, haveRole, serviceAdmin, haveWs]);

  useEffect(() => {
    setNotifyNum(1);
  }, []);

  return (
    <ClickAwayListener onClickAway={handleClose}>
      <div className={styles.UserSessionBar}>
        <div className={styles.UserSessionContent}>
          <div className={styles.leftBox}>
            {displayNav && (
              <div
                className={styles.menu}
                onClick={() => {
                  setShowNav(true);
                }}
              >
                <MenuIcon />
              </div>
            )}
            <div className={styles.logo}>
              <Torro />
            </div>
            {authContext.wsList.length > 0 && authContext.wsId && (
              <div className={styles.optionsBox}>
                <Select
                  value={authContext.wsId}
                  options={authContext.wsList}
                  disableFullwidth={true}
                  onChange={(value) => {
                    handleWsChange(value);
                  }}
                />
              </div>
            )}
          </div>
          <div className={styles.userBox}>
            <div className={styles.userInfo}>
              <div className={styles.rightBox}>
                <div className={styles.optionsBox}>
                  <Select
                    value={languageContext.lang}
                    options={LANGUAGE}
                    disableFullwidth={true}
                    onChange={(value) => {
                      setLanguage({
                        ...languageContext,
                        lang: value,
                      });
                    }}
                  />
                </div>
                {isLogin && (
                  <>
                    <div
                      className={styles.toolIcon}
                      onClick={notifyClickHandle}
                    >
                      <NotificationsIcon className={styles.svgIcon} />
                      {notifyNum > 0 && (
                        <div className={styles.notificaNum}>{notifyNum}</div>
                      )}
                    </div>
                    {authContext.role && (
                      <div className={styles.toolIcon}>
                        <UserTag role={authContext.role} />
                      </div>
                    )}

                    <div className={styles.toolIcon}>
                      <AccountCircleIcon className={styles.svgIcon} />
                    </div>
                    <div className={styles.userName}>
                      <Text>{authContext.userName}</Text>
                    </div>
                  </>
                )}
              </div>
            </div>
          </div>
          <Model open={openModel} handleClose={closeHandle}>
            <div>11</div>
          </Model>
        </div>

        {displayNav && <LeftNav open={showNav} closeHandle={handleClose} />}
      </div>
    </ClickAwayListener>
  );
};

export default UserSessionBar;

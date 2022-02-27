/* third lib*/
import React, {
  useState,
  useCallback,
  useMemo,
  useEffect,
  useRef,
} from "react";
import ClickAwayListener from "@material-ui/core/ClickAwayListener";
import { useNavigate } from "react-router-dom";
import { FormattedMessage as Intl } from "react-intl";

/* material-ui */
import MenuIcon from "@material-ui/icons/Menu";
import ExitToAppIcon from "@material-ui/icons/ExitToApp";
import NotificationsIcon from "@material-ui/icons/Notifications";
import AccountCircleIcon from "@material-ui/icons/AccountCircle";
import Popper from "@material-ui/core/Popper";
import Typography from "@material-ui/core/Typography";

/* local components & methods */
import styles from "./styles.module.scss";
import { useGlobalContext } from "src/context";
import { USER, GOVERNOR, IT, ADMIN } from "src/lib/data/roleType.js";
// import LANGUAGE from "src/lib/data/languageType";
import Model from "@basics/Modal";
import NotifyTable from "./NotifyTable";
import DoubleSquare from "@assets/icons/DoubleSquare";
import DoubleCircle from "@assets/icons/DoubleCircle";
import DoubleTriangle from "@assets/icons/DoubleTriangle";
import LeftNav from "src/components/LeftNav";
import Text from "@basics/Text";
import Torro from "@assets/icons/Torrotext";
import CallModal from "@basics/CallModal";
import Select from "@basics/Select";
import { sendNotify } from "src/utils/systerm-error";
import { updateLogin, getNotify, readNotify } from "@lib/api";

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
      {role === ADMIN && (
        <div className={styles.iconLabel}>
          <Intl id="serviceAdmin" />
        </div>
      )}
      {role === IT && (
        <>
          <DoubleTriangle className={styles.svgIcon} />
          <div className={styles.iconLabel}>
            <Intl id="it" />
          </div>
        </>
      )}
      {role === GOVERNOR && (
        <>
          <DoubleCircle className={styles.svgIcon} />
          <div className={styles.iconLabel}>
            <Intl id="dg" />
          </div>
        </>
      )}
      {role === USER && (
        <>
          <DoubleSquare className={styles.svgIcon} />
          <div className={styles.iconLabel}>
            <Intl id="du" />
          </div>
        </>
      )}
    </div>
  );
};

const UserSessionBar = () => {
  const {
    authContext,
    setAuth,
    // languageContext,
    // setLanguage,
  } = useGlobalContext();
  const navigate = useNavigate();
  const bellRef = useRef();

  const [notify, setNotify] = useState([]);
  const [openModel, setOpenModel] = useState(false);
  const [showNav, setShowNav] = useState(false);
  const [anchorEl, setAnchorEl] = React.useState(null);
  const [notifyHash, setNotifyHash] = useState();

  const open = Boolean(anchorEl);
  const id = open ? "simple-Popper" : undefined;

  const [modalData, setModalData] = useState({
    open: false,
    status: 0,
    content: "",
  });

  const isLogin = useMemo(() => {
    return authContext.userId && authContext.userId !== "null";
  }, [authContext]);

  const haveRole = useMemo(() => {
    return !!authContext.role && authContext.role !== "null";
  }, [authContext]);

  const isServiceAdmin = useMemo(() => {
    return authContext.role === ADMIN;
  }, [authContext]);

  const haveWs = useMemo(() => {
    return authContext.wsList.length > 0 && authContext.wsId;
  }, [authContext]);

  const displayNav = useMemo(() => {
    return isLogin && (haveRole || isServiceAdmin) && haveWs;
  }, [isLogin, haveRole, isServiceAdmin, haveWs]);

  const unRead = useMemo(() => {
    return notify.filter((item) => !item.is_read);
  }, [notify]);

  const handleClose = useCallback(() => {
    setShowNav(false);
  }, []);

  const notifyClickHandle = useCallback(() => {
    setOpenModel(true);
    setAnchorEl(false);
  }, []);

  const closeHandle = useCallback(() => {
    setOpenModel(false);
  }, []);

  // workspace change
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
          sendNotify({
            msg: e.message,
            status: 3,
            show: true,
          });
        });
    },
    [setAuth, authContext]
  );

  // signOut
  const signOut = useCallback(() => {
    setAuth({
      userName: "",
      userId: "",
      accountId: "",
      roleList: [],
      role: "",
      init: false,
      wsList: [],
      wsId: "",
      ad_group_list: [],
    });
  }, [setAuth]);

  const exitHandle = useCallback(() => {
    setModalData({
      open: true,
      status: 1,
      content: <Intl id="confirmLogout" />,
      cb: signOut,
    });
  }, [signOut]);

  const setUnRead = useCallback(
    (id) => {
      setNotify(
        notify.map((item) => {
          if (item.id === id) {
            item.is_read = 1;
          }
          return item;
        })
      );
    },
    [notify]
  );

  const readAll = useCallback(() => {
    let unReadIdList = unRead.map((item) => item.id);
    readNotify({ nodify_id: unReadIdList, is_read: 1 })
      .then((res) => {
        if (res.code === 200) {
          setNotify(
            notify.map((not) => {
              if (unReadIdList.includes(not.id)) {
                not.is_read = 1;
              }
              return not;
            })
          );
        }
      })
      .catch((e) => {
        sendNotify({
          msg: e.message,
          status: 3,
          show: true,
        });
      });
  }, [unRead, notify]);

  // System notify
  const viewRequest = useCallback(
    (requestId, id) => {
      closeHandle();
      setUnRead(id);
      readNotify({ nodify_id: id, is_read: 1 })
        .then((res) => {})
        .catch((e) => {
          sendNotify({
            msg: e.message,
            status: 3,
            show: true,
          });
        });
      navigate(`/app/approvalFlow?id=${requestId}`);
    },
    [navigate, closeHandle, setUnRead]
  );

  useEffect(() => {
    let loop;
    if (authContext.userId && authContext.role) {
      getNotify()
        .then((res) => {
          if (res.data) {
            setNotify(res.data);
          }
        })
        .catch((e) => {
          sendNotify({
            msg: e.message,
            status: 3,
            show: true,
          });
        });
      loop = setInterval(() => {
        setNotifyHash(Math.floor(Math.random() * 100000));
      }, 5000);
    }

    return () => {
      clearInterval(loop);
      loop = null;
    };
    /* eslint-disable */
  }, [authContext]);
  /* eslint-disable */

  useEffect(() => {
    if (authContext.userId && authContext.role && notifyHash) {
      getNotify()
        .then((res) => {
          if (res.data) {
            setNotify(res.data);
            let unReadList = res.data.filter((item) => !item.is_read);
            if (unReadList.length > unRead.length && notifyHash) {
              setAnchorEl(bellRef.current);
            }
          }
        })
        .catch((e) => {
          sendNotify({
            msg: e.message,
            status: 3,
            show: true,
          });
        });
    }
  }, [notifyHash]);

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
                {/* <div className={styles.optionsBox}>
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
                </div> */}
                {isLogin && (
                  <>
                    <div
                      className={styles.toolIcon}
                      onClick={notifyClickHandle}
                      ref={bellRef}
                    >
                      <NotificationsIcon className={styles.svgIcon} />
                      {unRead.length > 0 && (
                        <div className={styles.notificaNum}></div>
                      )}
                      <div>
                        <Popper
                          id={id}
                          open={open}
                          anchorEl={anchorEl}
                          onClose={() => {
                            setAnchorEl(null);
                          }}
                          placement="bottom"
                        >
                          <Typography className={styles.newNotify}>
                            <Text type="subTitle">
                              <Intl id="gotNewRequest" />
                            </Text>
                          </Typography>
                        </Popper>
                      </div>
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
                    <div className={styles.toolIcon} title="Exit">
                      <ExitToAppIcon
                        onClick={exitHandle}
                        className={styles.svgIcon}
                      />
                    </div>
                  </>
                )}
              </div>
            </div>
          </div>
          <Model open={openModel} handleClose={closeHandle}>
            <NotifyTable
              notify={notify}
              viewRequest={viewRequest}
              unRead={unRead}
              readAll={readAll}
            />
          </Model>
          <CallModal
            open={modalData.open}
            content={modalData.content}
            status={modalData.status}
            handleClose={() => {
              setModalData({
                ...modalData,
                open: false,
              });
            }}
            buttonClickHandle={modalData.cb}
          />
        </div>

        {displayNav && <LeftNav open={showNav} closeHandle={handleClose} />}
      </div>
    </ClickAwayListener>
  );
};

export default UserSessionBar;

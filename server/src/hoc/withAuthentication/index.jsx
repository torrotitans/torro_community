/* third lib */
import React, { useEffect, useState } from "react";
import { Navigate } from "react-router-dom";

/* local components & methods */
import { useGlobalContext } from "src/context";
import UserSessionBar from "src/layouts/UserSessionBar";
import CallModal from "@basics/CallModal";
import { refreshToken } from "@lib/api";

const withAuthentication = (VerificationPage) => (props) => {
  const { authContext, setAuth } = useGlobalContext();
  let firstInit = String(authContext.init) === "true";
  let isLoggedIn = authContext.userId && authContext.userId !== "null";
  let haveRole = !!authContext.role && authContext.role !== "null";
  let haveWs = authContext.wsList && authContext.wsList.length > 0;
  let isServiceAdmin = authContext.roleList.includes("admin");

  const [modalData, setModalData] = useState({
    open: false,
    status: 0,
    content: "",
    cb: null,
  });

  console.log(authContext);

  useEffect(() => {
    if (!!authContext.expTime) {
      let loginTimer = setInterval(() => {
        let currTime = new Date().getTime();
        if (currTime > authContext.expTime) {
          setModalData({
            open: true,
            status: 5,
            content: "time expired",
            cb: () => {
              setAuth(
                {
                  userName: "",
                  userId: "",
                  accountId: "",
                  roleList: [],
                  role: "",
                  init: false,
                  wsList: [],
                  wsId: "",
                  ad_group_list: [],
                  expTime: 0,
                },
                "logout"
              );
            },
          });
          clearInterval(loginTimer);
          loginTimer = null;
        } else if (currTime > authContext.expTime - 5 * 60 * 1000) {
          let time = Math.floor(authContext.expTime - currTime);
          let minute = Math.floor((time / 1000 / 60) % 60);
          let second = Math.floor((time / 1000) % 60);
          setModalData({
            open: true,
            status: 4,
            content: `You can keep the login status within ${minute}:${second}`,
            cb: () => {
              refreshToken()
                .then(() => {
                  setAuth(authContext, "refreshToken");
                  setModalData({
                    open: false,
                    status: 4,
                    content: `You can keep the login status within ${minute}:${second}`,
                  });
                  clearInterval(loginTimer);
                  loginTimer = null;
                })
                .catch((e) => {
                  clearInterval(loginTimer);
                  loginTimer = null;
                });
            },
            successCb: () => {
              setAuth(
                {
                  userName: "",
                  userId: "",
                  accountId: "",
                  roleList: [],
                  role: "",
                  init: false,
                  wsList: [],
                  wsId: "",
                  ad_group_list: [],
                  expTime: 0,
                },
                "logout"
              );
              clearInterval(loginTimer);
              loginTimer = null;
            },
          });
        }
      }, 1000);
      return () => {
        clearInterval(loginTimer);
        loginTimer = null;
      };
    }
  }, [authContext, setAuth]);

  if (window.location.pathname.indexOf("/orgSetting") !== -1 && !firstInit) {
    return <Navigate to="/login" />;
  }
  if (window.location.pathname.indexOf("/orgSetting") === -1 && firstInit) {
    return <Navigate to="/orgSetting" />;
  }
  if (
    window.location.pathname.indexOf("/login") === -1 &&
    !isLoggedIn &&
    !firstInit
  ) {
    return <Navigate to="/login" />;
  }

  if (isLoggedIn) {
    // no workspace protection
    if (!haveWs) {
      if (
        window.location.pathname.indexOf("/app/workspaceCreation") === -1 &&
        isServiceAdmin
      ) {
        return <Navigate to="/app/workspaceCreation" />;
      }
      if (
        window.location.pathname.indexOf("/noWorkspace") === -1 &&
        !isServiceAdmin
      ) {
        return <Navigate to="/noWorkspace" />;
      }
    } else {
      // Not Admin role need to have role to login dashboard.
      if (
        window.location.pathname.indexOf("/roleSelect") === -1 &&
        !haveRole &&
        !isServiceAdmin
      ) {
        return <Navigate to="/roleSelect" />;
      }

      // User auth keep alive.
      if (
        (haveRole || isServiceAdmin) &&
        window.location.pathname.indexOf("/login") !== -1 &&
        window.location.pathname.indexOf("/roleSelect") === -1
      ) {
        return <Navigate to="/app/dashboard" />;
      }
    }
  }

  return (
    <>
      <UserSessionBar />
      <VerificationPage {...props} />

      <CallModal
        open={modalData.open}
        content={modalData.content}
        status={modalData.status}
        successCb={modalData.successCb}
        buttonClickHandle={modalData.cb}
        handleClose={() => {
          setModalData({ ...modalData, open: false, cb: null });
        }}
      ></CallModal>
    </>
  );
};

export default withAuthentication;

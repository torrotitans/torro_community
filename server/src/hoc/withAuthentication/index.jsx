/* third lib */
import React from "react";
import { Navigate } from "react-router-dom";

/* local components & methods */
import { useGlobalContext } from "src/context";
import UserSessionBar from "src/layouts/UserSessionBar";

const withAuthentication = (VerificationPage) => (props) => {
  const { authContext } = useGlobalContext();
  let firstInit = String(authContext.init) === "true";
  let isLoggedIn = authContext.userId && authContext.userId !== "null";
  let haveRole = !!authContext.role && authContext.role !== "null";
  let haveWs = authContext.wsList && authContext.wsList.length > 0;
  let isServiceAdmin = authContext.roleList.includes("admin");

  console.log(authContext);

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
    </>
  );
};

export default withAuthentication;

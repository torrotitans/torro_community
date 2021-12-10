/* third lib */
import React from "react";
import { Navigate } from "react-router-dom";

/* local components & methods */
import { useGlobalContext } from "src/context";
import UserSessionBar from "src/layouts/UserSessionBar";

const withAuthentication = (VerificationPage) => (props) => {
  const { authContext, languageContext } = useGlobalContext();
  let firstInit = String(authContext.init) === "true";
  let isLoggedIn = authContext.userId && authContext.userId !== "null";
  let haveRole = !!authContext.role && authContext.role !== "null";
  let haveWs = authContext.wsList && authContext.wsList.length > 0;

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
    if (window.location.pathname.indexOf("/noWorkspace") === -1 && !haveWs) {
      return <Navigate to="/noWorkspace" />;
    } else {
      if (window.location.pathname.indexOf("/roleSelect") === -1 && !haveRole) {
        return <Navigate to="/roleSelect" />;
      }
      if (haveWs && window.location.pathname.indexOf("/noWorkspace") != -1) {
        return <Navigate to="/app/dashboard" />;
      }
      if (
        haveRole &&
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

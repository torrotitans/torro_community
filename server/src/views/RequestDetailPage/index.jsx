/* third lib*/
import React from "react";
import { getQueryString } from "src/utils/url-util.js";
import RequestDetail from "@comp/RequestDetail";

const RequestDetailPage = () => {
  const recordId = getQueryString("id");
  const approved = getQueryString("approved");
  return <RequestDetail recordId={recordId} approvedView={approved} />;
};

export default RequestDetailPage;

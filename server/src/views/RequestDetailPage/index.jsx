/* third lib*/
import React from "react";
import { getQueryString } from "src/utils/url-util.js";
import RequestDetail from "@comp/RequestDetail";
import RequestDetailList from "@comp/RequestDetailList";

const RequestDetailPage = ({ approved }) => {
  const recordId = getQueryString("id");
  const recordList = getQueryString("idList");

  if (recordId) {
    return <RequestDetail recordId={recordId} approvedView={approved} />;
  } else if (recordList) {
    return <RequestDetailList idListStr={recordList} approvedView={approved} />;
  }
};

export default RequestDetailPage;

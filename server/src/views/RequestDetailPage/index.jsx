/* third lib*/
import React from "react";
import { getQueryString } from "src/utils/url-util.js";
import RequestDetail from "@comp/RequestDetail";
import RequestDetailList from "@comp/RequestDetailList";

const RequestDetailPage = () => {
  const recordId = getQueryString("id");
  const approved = getQueryString("approved");
  const recordList = getQueryString("idList");
  if (recordId) {
    return <RequestDetail recordId={recordId} approvedView={approved} />;
  } else if (recordList) {
    let idList = recordList.split("|");
    return <RequestDetailList recordList={idList} approvedView={approved} />;
  }
};

export default RequestDetailPage;

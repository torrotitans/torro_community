/* third lib*/
import React from "react";
import { getQueryString } from "src/utils/url-util.js";
import FormRender from "@comp/FormRender";

const FormPage = () => {
  const formId = getQueryString("id");
  return <FormRender formId={formId} />;
};

export default FormPage;

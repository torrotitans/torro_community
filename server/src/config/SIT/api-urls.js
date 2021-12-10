import { DELETE, GET, POST, PUT } from "@lib/data/api-types";

const API_URL = "http://localhost:3000/";

const config = {
  login: {
    // url: `${API_URL}/stub/userData.json`,
    url: "http://34.96.134.183/api/login",
    method: POST,
  },
  loginPut: {
    url: "http://34.96.134.183/api/login",
    method: PUT,
  },
  orgPost: {
    url: "http://34.96.134.183/api/orgSetting",
    // url: "http://127.0.0.1:5000/orgSetting",
    method: POST,
  },
  postFormRequest: {
    url: "http://34.96.134.183/api/inputFormData",
    method: POST,
  },
  putFormRequest: {
    url: "http://34.96.134.183/api/inputFormData",
    method: PUT,
  },
  requestDataGet: {
    // url: `${API_URL}/stub/requestDataGet.json`,
    url: "http://34.96.134.183/api/getInputFormInfo",
    method: POST,
  },
  requestDetailGet: {
    url: "http://34.96.134.183/api/getInputFormDetails",
    method: POST,
  },
  fieldTemplateGet: {
    url: `${API_URL}/stub/fieldTemplate.json`,
    method: GET,
  },
  formListGet: {
    // url: `${API_URL}/stub/formItem.json`,
    url: "http://34.96.134.183/api/getFormList",
    method: GET,
  },
  formItemGet: {
    // url: `${API_URL}/stub/formTemplate.json`,
    url: "http://34.96.134.183/api/getFormData",
    method: POST,
  },

  formDataPost: {
    // url: `${API_URL}/stub/postData.json`,
    url: "http://34.96.134.183/api/postFormData",
    method: PUT,
  },

  formAddPost: {
    // url: `${API_URL}/stub/addFormData.json`,
    url: "http://34.96.134.183/api/postFormData",
    method: POST,
  },

  formDelete: {
    // url: `${API_URL}/stub/addFormData.json`,
    url: "http://34.96.134.183/api/postFormData",
    method: DELETE,
  },

  flowDataGet: {
    url: `${API_URL}/stub/flowData.json`,
    method: GET,
  },

  approverLevelGet: {
    url: `${API_URL}/stub/approverLevel.json`,
    method: GET,
  },

  defaultDropItemGet: {
    url: `${API_URL}/stub/defaultDropItem.json`,
    method: GET,
  },

  workFlowDataGet: {
    url: "http://34.96.134.183/api/getDetailsWorkflowDataById",
    method: POST,
  },
  workFlowFormDataGet: {
    url: "http://34.96.134.183/api/getBaseWorkflowListByFormId",
    method: GET,
  },

  workFlowDataPut: {
    url: "http://34.96.134.183/api/postWorkflowData",
    method: PUT,
  },

  workFlowDataPost: {
    url: "http://34.96.134.183/api/postWorkflowData",
    method: POST,
  },

  workFlowDataDelete: {
    url: "http://34.96.134.183/api/postWorkflowData",
    method: DELETE,
  },

  ConsoleGet: {
    // url: "http://localhost:5000/commandrun",
    url: "http://34.96.134.183/api/debug",
    method: POST,
  },
};
export default config;

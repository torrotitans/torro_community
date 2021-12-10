import { DELETE, GET, POST, PUT } from "@lib/data/api-types";

const API_URL = "";

const config = {
  login: {
    // url: `${API_URL}/stub/userData.json`,
    url: "http://34.92.243.193/api/login",
    method: POST,
  },
  loginPut: {
    url: "http://34.92.243.193/api/login",
    method: PUT,
  },
  filterOptionGet: {
    // url: `${API_URL}/stub/requestor.json`,
    url: "http://34.92.243.193/api/getDashboardOptions",
    method: GET,
  },

  orgPost: {
    url: "http://34.92.243.193/api/orgSetting",
    // url: "http://127.0.0.1:5000/orgSetting",
    method: POST,
  },
  postFormRequest: {
    url: "http://34.92.243.193/api/inputFormData",
    method: POST,
  },
  putFormRequest: {
    url: "http://34.92.243.193/api/inputFormData",
    method: PUT,
  },
  deleteFormRequest: {
    url: "http://34.92.243.193/api/inputFormData",
    method: DELETE,
  },

  postRequestStatus: {
    url: "http://34.92.243.193/api/changeStatus",
    method: POST,
  },
  requestDataGet: {
    // url: `${API_URL}/stub/requestDataGet.json`,
    url: "http://34.92.243.193/api/getInputFormInfo",
    method: POST,
  },
  requestDetailGet: {
    // url: `${API_URL}/stub/InputformDetail.json`,
    url: "http://34.92.243.193/api/getInputFormDetails",
    method: POST,
  },

  commentPost: {
    url: "http://34.92.243.193/api/inputFormComment",
    method: POST,
  },

  commentDelete: {
    url: "http://34.92.243.193/api/inputFormComment",
    method: DELETE,
  },

  fieldTemplateGet: {
    // url: `${API_URL}/stub/fieldTemplate.json`,
    url: "http://34.92.243.193/api/getFieldTemplate",
    method: GET,
  },
  workspaceGet: {
    // url: `${API_URL}/stub/workspaceGet.json`,
    url: "http://34.92.243.193/api/workspaceSetting",
    method: GET,
  },
  workspaceDetailGet: {
    // url: `${API_URL}/stub/workspaceGet.json`,
    url: "http://34.92.243.193/api/workspaceInfo",
    method: POST,
  },
  workspacePut: {
    // url: `${API_URL}/stub/wsPut.json`,
    url: "http://34.92.243.193/api/workspaceSetting",
    method: PUT,
  },
  workspacePost: {
    // url: `${API_URL}/stub/wsPut.json`,
    url: "http://34.92.243.193/api/workspaceSetting",
    method: POST,
  },
  workspaceDelete: {
    // url: `${API_URL}/stub/workspaceGet.json`,
    url: "http://34.92.243.193/api/workspaceSetting",
    method: DELETE,
  },
  useCaseGet: {
    url: "http://34.92.243.193/api/usecaseInfo",
    method: GET,
  },
  useCasePost: {
    url: "http://34.92.243.193/api/usecaseInfo",
    method: POST,
  },

  formListGet: {
    // url: `${API_URL}/stub/formItem.json`,
    url: "http://34.92.243.193/api/getFormList",
    method: GET,
  },
  formItemGet: {
    // url: `${API_URL}/stub/tmpGetFormData.json`,
    url: "http://34.92.243.193/api/getFormData",
    method: POST,
  },

  formDataPost: {
    // url: `${API_URL}/stub/postData.json`,
    url: "http://34.92.243.193/api/postFormData",
    method: PUT,
  },

  formAddPost: {
    // url: `${API_URL}/stub/addFormData.json`,
    url: "http://34.92.243.193/api/postFormData",
    method: POST,
  },

  formDelete: {
    // url: `${API_URL}/stub/addFormData.json`,
    url: "http://34.92.243.193/api/postFormData",
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

  allStageGet: {
    // url: `${API_URL}/stub/allStages.json`,
    url: `http://34.92.243.193/api/getAllStages`,
    method: POST,
  },

  workFlowDataGet: {
    url: "http://34.92.243.193/api/getDetailsWorkflowDataById",
    method: POST,
  },
  workFlowFormDataGet: {
    url: "http://34.92.243.193/api/getBaseWorkflowListByFormId",
    method: GET,
  },

  workFlowDataPut: {
    url: "http://34.92.243.193/api/postWorkflowData",
    method: PUT,
  },

  workFlowDataPost: {
    url: "http://34.92.243.193/api/postWorkflowData",
    method: POST,
  },

  workFlowDataDelete: {
    url: "http://34.92.243.193/api/postWorkflowData",
    method: DELETE,
  },

  ConsoleGet: {
    // url: "http://localhost:5000/commandrun",
    url: "http://34.92.243.193/api/debug",
    method: POST,
  },

  lookupResource: {
    // url: `${API_URL}/stub/bq_table_schema.json`,
    url: "http://34.92.243.193/api/tableSchema",
    method: PUT,
  },

  tableSchemaGet: {
    // url: `${API_URL}/stub/bq_table_schema.json`,
    url: "http://34.92.243.193/api/tableSchema",
    method: POST,
  },

  policyTagGet: {
    url: `${API_URL}/stub/policy_tags.json`,
    // url: "http://34.92.243.193/api/debug",
    method: GET,
  },

  policysGet: {
    // url: `${API_URL}/stub/policys.json`,
    url: "http://34.92.243.193/api/getPolicyTagsList",
    method: GET,
  },

  tableDataGet: {
    url: `${API_URL}/stub/tableData.json`,
    // url: "http://34.92.243.193/api/getPolicyTagsList",
    method: GET,
  },
  policyDetailGet: {
    url: `${API_URL}/stub/policyDetail.json`,
    // url: "http://34.92.243.193/api/debug",
    method: GET,
  },

  governersTagGet: {
    // url: `${API_URL}/stub/TagList.json`,
    url: "http://34.92.243.193/api/getTagTemplateList",
    method: GET,
  },
};

export default config;

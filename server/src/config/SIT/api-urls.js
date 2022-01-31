import { DELETE, GET, POST, PUT } from "@lib/data/api-types";

/* eslint-disable no-undef */
const BASE_API_URL = process?.env?.REACT_APP_API_URL || "http://35.220.239.54";
/* eslint-disable no-new */

const config = {
  login: {
    url: `${BASE_API_URL}/api/login`,
    method: POST,
  },
  loginPut: {
    url: `${BASE_API_URL}/api/login`,
    method: PUT,
  },
  filterOptionGet: {
    url: `${BASE_API_URL}/api/getDashboardOptions`,
    method: GET,
  },
  orgPost: {
    url: `${BASE_API_URL}/api/orgSetting`,
    method: POST,
  },
  postFormRequest: {
    url: `${BASE_API_URL}/api/inputFormData`,
    method: POST,
  },
  postFormRequestList: {
    url: `${BASE_API_URL}/api/inputFormDataList`,
    method: POST,
  },
  putFormRequest: {
    url: `${BASE_API_URL}/api/inputFormData`,
    method: PUT,
  },
  deleteFormRequest: {
    url: `${BASE_API_URL}/api/inputFormData`,
    method: DELETE,
  },

  postRequestStatus: {
    url: `${BASE_API_URL}/api/changeStatus`,
    method: POST,
  },

  postRequestStatusList: {
    url: `${BASE_API_URL}/api/changeStatusList`,
    method: POST,
  },

  requestDataGet: {
    url: `${BASE_API_URL}/api/getInputFormInfo`,
    method: POST,
  },
  requestDetailGet: {
    url: `${BASE_API_URL}/api/getInputFormDetails`,
    method: POST,
  },

  requestDetailListGet: {
    url: `${BASE_API_URL}/api/getInputFormDetailsList`,
    method: POST,
  },

  commentPost: {
    url: `${BASE_API_URL}/api/inputFormComment`,
    method: POST,
  },

  commentDelete: {
    url: `${BASE_API_URL}/api/inputFormComment`,
    method: DELETE,
  },

  fieldTemplateGet: {
    url: `${BASE_API_URL}/api/getFieldTemplate`,
    method: GET,
  },
  workspaceGet: {
    url: `${BASE_API_URL}/api/workspaceSetting`,
    method: GET,
  },
  workspaceDetailGet: {
    url: `${BASE_API_URL}/api/workspaceInfo`,
    method: POST,
  },
  workspacePut: {
    url: `${BASE_API_URL}/api/workspaceSetting`,
    method: PUT,
  },
  workspacePost: {
    url: `${BASE_API_URL}/api/workspaceSetting`,
    method: POST,
  },
  workspaceDelete: {
    url: `${BASE_API_URL}/api/workspaceSetting`,
    method: DELETE,
  },
  useCaseGet: {
    url: `${BASE_API_URL}/api/usecaseInfo`,
    method: GET,
  },
  useCasePost: {
    url: `${BASE_API_URL}/api/usecaseInfo`,
    method: POST,
  },

  formListGet: {
    url: `${BASE_API_URL}/api/getFormList/1`,
    method: GET,
  },
  formItemGet: {
    url: `${BASE_API_URL}/api/getFormData`,
    method: POST,
  },

  formItemListGet: {
    url: `${BASE_API_URL}/api/getFormDataList`,
    method: POST,
  },

  formDataPost: {
    url: `${BASE_API_URL}/api/postFormData`,
    method: PUT,
  },

  formAddPost: {
    url: `${BASE_API_URL}/api/postFormData`,
    method: POST,
  },

  formDelete: {
    url: `${BASE_API_URL}/api/postFormData`,
    method: DELETE,
  },

  flowDataGet: {
    url: `/stub/flowData.json`,
    method: GET,
  },

  approverLevelGet: {
    url: `/stub/approverLevel.json`,
    method: GET,
  },

  allStageGet: {
    url: `${BASE_API_URL}/api/getAllStages`,
    method: POST,
  },

  workFlowDataGet: {
    url: `${BASE_API_URL}/api/getDetailsWorkflowDataById`,
    method: POST,
  },
  workFlowFormDataGet: {
    url: `${BASE_API_URL}/api/getBaseWorkflowListByFormId`,
    method: GET,
  },

  workFlowDataPut: {
    url: `${BASE_API_URL}/api/postWorkflowData`,
    method: PUT,
  },

  workFlowDataPost: {
    url: `${BASE_API_URL}/api/postWorkflowData`,
    method: POST,
  },

  workFlowDataDelete: {
    url: `${BASE_API_URL}/api/postWorkflowData`,
    method: DELETE,
  },

  ConsoleGet: {
    url: `${BASE_API_URL}/api/debug`,
    method: POST,
  },

  lookupResource: {
    url: `${BASE_API_URL}/api/tableSchema`,
    method: PUT,
  },

  tableSchemaGet: {
    url: `${BASE_API_URL}/api/tableSchema`,
    method: POST,
  },

  policyTagGet: {
    url: `/stub/policy_tags.json`,
    method: GET,
  },

  policysGet: {
    url: `${BASE_API_URL}/api/getPolicyTagsList`,
    method: GET,
  },

  tableDataGet: {
    url: `/stub/tableData.json`,
    method: GET,
  },
  policyDetailGet: {
    url: `/stub/policyDetail.json`,
    method: GET,
  },

  governersTagGet: {
    url: `${BASE_API_URL}/api/getTagTemplateList`,
    method: GET,
  },

  /* static data */
  onBoardDataForm: {
    url: `${BASE_API_URL}/api/torroConfig/en.form.dataOnBoardForm`,
    method: GET,
  },

  fieldDisplayConfig: {
    url: `${BASE_API_URL}/api/torroConfig/en.form.specialRenderItem`,
    method: GET,
  },

  useCaseMemberConfig: {
    url: `${BASE_API_URL}/api/torroConfig/en.form.ucMemberConfig`,
    method: GET,
  },

  requiredTableTag: {
    url: `${BASE_API_URL}/api/torroConfig/en.form.requireTableTagId`,
    method: GET,
  },

  orgFormGet: {
    url: `${BASE_API_URL}/api/torroConfig/en.form.orgSettingForm`,
    method: GET,
  },
};

export default config;

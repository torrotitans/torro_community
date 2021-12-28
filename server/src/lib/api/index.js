import api from "src/config/api-urls";
import { DELETE, POST, PUT } from "@lib/data/api-types";
import { isObject } from "formik";

let API_CONFIG = api;

const appendQueryStr = (url, param) => {
  return `${url}${
    url.endsWith("?") ? "" : url.includes("?") ? "&" : "?"
  }${Object.entries(param)
    .reduce(
      (params, [key, val]) => [
        ...params,
        `${encodeURIComponent(key)}=${encodeURIComponent(val)}`,
      ],
      []
    )
    .join("&")}`;
};

const handleObjectToFormData = (data, ss) => {
  let _data = data;

  if (_data instanceof FormData) {
    return _data;
  }

  if (isObject(data)) {
    const formData = new FormData();
    Object.keys(data).map((key) => {
      if (typeof data[key] === "object") {
        if (data[key] instanceof File) {
          formData.append(key, data[key], data[key].name);
        } else if (data[key] instanceof FileList) {
          formData.append(key, data[key][0], data[key][0].name);
        } else {
          formData.append(key, JSON.stringify(data[key]));
        }
      } else {
        formData.append(key, data[key]);
      }
    });
    _data = formData;
  } else {
    _data = JSON.stringify(data, null, 2);
  }
  return _data;
};

const handleResponse = async (response) => {
  const body = response.json ? await response.json() : {};
  const statusCode = response.status.toString().split("");
  let technicalError = statusCode[0] === "5";

  const res = {
    errorInfo: body.errorInfo,
    status: response.status,
    technicalError,
  };
  if (response.ok) {
    if (res.errorInfo) {
      return res;
    }

    if (body.code && body.code !== 200) {
      throw new Error(body.msg);
    }
    return body;
  } else {
    if (res.errorInfo) {
      return res;
    } else {
      throw response;
    }
  }
};

const callApi = (method, url, param) => {
  const canHaveBody = method === POST || method === PUT || method === DELETE;
  const postUrl = canHaveBody
    ? url
    : (param && appendQueryStr(url, param)) || url;
  const isFormData = param instanceof FormData;
  const body = canHaveBody
    ? isFormData
      ? param
      : handleObjectToFormData(param)
    : null;

  return fetch(postUrl, {
    body,
    method,
    credentials: "include",
  });
};
export const LoginCall = async (param) => {
  let {
    login: { url, method },
  } = API_CONFIG;

  return await handleResponse(await callApi(method, url, param));
};

export const updateLogin = async (param) => {
  let {
    loginPut: { url, method },
  } = API_CONFIG;

  return await handleResponse(await callApi(method, url, param));
};

export const OrgSetup = async (param) => {
  let {
    orgPost: { url, method },
  } = API_CONFIG;

  return await handleResponse(await callApi(method, url, param));
};

export const getRequestData = async (param) => {
  let {
    requestDataGet: { url, method },
  } = API_CONFIG;

  return await handleResponse(await callApi(method, url, param));
};

export const getFilterOptions = async (param) => {
  let {
    filterOptionGet: { url, method },
  } = API_CONFIG;

  return await handleResponse(await callApi(method, url, param));
};

export const getRequestDetail = async (param) => {
  let {
    requestDetailGet: { url, method },
  } = API_CONFIG;

  return await handleResponse(await callApi(method, url, param));
};

export const postComment = async (param) => {
  let {
    commentPost: { url, method },
  } = API_CONFIG;

  return await handleResponse(await callApi(method, url, param));
};

export const deleteComment = async (param) => {
  let {
    commentDelete: { url, method },
  } = API_CONFIG;

  return await handleResponse(await callApi(method, url, param));
};

export const getFormList = async (param) => {
  let {
    formListGet: { url, method },
  } = API_CONFIG;

  return await handleResponse(await callApi(method, url, param));
};

export const getFieldTemplate = async (param) => {
  let {
    fieldTemplateGet: { url, method },
  } = API_CONFIG;

  return await handleResponse(await callApi(method, url, param));
};

export const getFormItem = async (param) => {
  let {
    formItemGet: { url, method },
  } = API_CONFIG;

  return await handleResponse(await callApi(method, url, param));
};

export const postFormData = async (param) => {
  let {
    formDataPost: { url, method },
  } = API_CONFIG;

  return await handleResponse(await callApi(method, url, param));
};

export const addFormData = async (param) => {
  let {
    formAddPost: { url, method },
  } = API_CONFIG;

  return await handleResponse(await callApi(method, url, param));
};

export const getAllStages = async (param) => {
  let {
    allStageGet: { url, method },
  } = API_CONFIG;

  return await handleResponse(await callApi(method, url, param));
};

export const getFlowData = async (param) => {
  let {
    flowDataGet: { url, method },
  } = API_CONFIG;

  return await handleResponse(await callApi(method, url, null));
};

export const deleteFormData = async (param) => {
  let {
    formDelete: { url, method },
  } = API_CONFIG;

  return await handleResponse(await callApi(method, url, param));
};

export const getWorkflowData = async (param) => {
  let {
    workFlowDataGet: { url, method },
  } = API_CONFIG;

  return await handleResponse(await callApi(method, url, param));
};

export const getFormWorkflowData = async (param) => {
  let {
    workFlowFormDataGet: { url, method },
  } = API_CONFIG;

  return await handleResponse(await callApi(method, url, param));
};

export const postWorkflowData = async (param) => {
  let {
    workFlowDataPost: { url, method },
  } = API_CONFIG;

  return await handleResponse(await callApi(method, url, param));
};

export const saveWorkflowData = async (param) => {
  let {
    workFlowDataPut: { url, method },
  } = API_CONFIG;

  return await handleResponse(await callApi(method, url, param));
};

export const deleteWorkflowData = async (param) => {
  let {
    workFlowDataDelete: { url, method },
  } = API_CONFIG;

  return await handleResponse(await callApi(method, url, param));
};

export const getConsole = async (param) => {
  let {
    ConsoleGet: { url, method },
  } = API_CONFIG;

  return await handleResponse(await callApi(method, url, param));
};

export const raiseFormRequest = async (param) => {
  let {
    postFormRequest: { url, method },
  } = API_CONFIG;

  return await handleResponse(await callApi(method, url, param));
};

export const updateFormRequest = async (param) => {
  let {
    putFormRequest: { url, method },
  } = API_CONFIG;

  return await handleResponse(await callApi(method, url, param));
};

export const deleteFormRequest = async (param) => {
  let {
    deleteFormRequest: { url, method },
  } = API_CONFIG;

  return await handleResponse(await callApi(method, url, param));
};

export const changeStatus = async (param) => {
  let {
    postRequestStatus: { url, method },
  } = API_CONFIG;

  return await handleResponse(await callApi(method, url, param));
};

export const getWsList = async (param) => {
  let {
    workspaceGet: { url, method },
  } = API_CONFIG;

  return await handleResponse(await callApi(method, url, param));
};

export const wsPut = async (param) => {
  let {
    workspacePut: { url, method },
  } = API_CONFIG;

  return await handleResponse(await callApi(method, url, param));
};

export const wsPost = async (param) => {
  let {
    workspacePost: { url, method },
  } = API_CONFIG;

  return await handleResponse(await callApi(method, url, param));
};

export const wsDelete = async (param) => {
  let {
    workspaceDelete: { url, method },
  } = API_CONFIG;

  return await handleResponse(await callApi(method, url, param));
};

export const getWsDetail = async (param) => {
  let {
    workspaceDetailGet: { url, method },
  } = API_CONFIG;

  return await handleResponse(await callApi(method, url, param));
};

export const getUseCaseList = async () => {
  let {
    useCaseGet: { url, method },
  } = API_CONFIG;

  return await handleResponse(await callApi(method, url));
};

export const getUseCaseDetail = async (param) => {
  let {
    useCasePost: { url, method },
  } = API_CONFIG;

  return await handleResponse(await callApi(method, url, param));
};

export const lookupResource = async (param) => {
  let {
    lookupResource: { url, method },
  } = API_CONFIG;

  return await handleResponse(await callApi(method, url, param));
};

export const getTableSchema = async (param) => {
  let {
    tableSchemaGet: { url, method },
  } = API_CONFIG;

  return await handleResponse(await callApi(method, url, param));
};

export const getPolicayTag = async (param) => {
  let {
    policyTagGet: { url, method },
  } = API_CONFIG;

  return await handleResponse(await callApi(method, url, param));
};

export const getPolicys = async (param) => {
  let {
    policysGet: { url, method },
  } = API_CONFIG;

  return await handleResponse(await callApi(method, url, param));
};

export const getPolicyDetail = async (param) => {
  let {
    policyDetailGet: { url, method },
  } = API_CONFIG;

  return await handleResponse(await callApi(method, url, param));
};

export const getTableData = async (param) => {
  let {
    tableDataGet: { url, method },
  } = API_CONFIG;

  return await handleResponse(await callApi(method, url, param));
};

export const getTags = async (param) => {
  let {
    governersTagGet: { url, method },
  } = API_CONFIG;

  return await handleResponse(await callApi(method, url, param));
};

/* ============== static data call =====================*/

export const getOnBoardDataForm = async (param) => {
  let {
    onBoardDataForm: { url, method },
  } = API_CONFIG;

  return await handleResponse(await callApi(method, url, param));
};

/* ============== static data end =====================*/

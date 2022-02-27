import React, { useContext, createContext, useReducer } from "react";
import { setCookie, getCookie } from "src/utils/cookie-helper";
import decode from "src/utils/encode.js";
const globalData = {};
const GlobalContext = createContext(globalData);
const { Encrypt, Decrypt } = decode;

const Identity = (() => {
  let Idata = {
    userName: "",
    userId: "",
    accountId: "",
    roleList: [],
    role: "",
    init: false,
    wsList: [],
    wsId: "",
    ad_group_list: [],
    userCN: "",
  };
  try {
    if (!getCookie("TORRO_AUTH")) {
      throw new Error("Login expired.");
    }
    let decodeData = Decrypt(getCookie("TORRO_AUTH"));
    Idata = JSON.parse(decodeData);
  } catch (error) {
    new Error("Login expired.");
  }
  return Idata;
})();

const GlobalContextProvider = (props) => {
  const [authContext, authContextDispatch] = useReducer(
    (state, actions) => {
      let newState = state;
      newState = {
        ...state,
        init: actions.payload.init,
        userName: actions.payload.userName,
        userId: actions.payload.userId,
        userCN: actions.payload.userCN,
        roleList: actions.payload.roleList,
        role: actions.payload.role,
        wsList: actions.payload.wsList,
        wsId: actions.payload.wsId,
        accountId: actions.payload.accountId,
        ad_group_list: actions.payload.ad_group_list,
      };
      let sessionToken = JSON.stringify(newState);
      let encodeToken = Encrypt(sessionToken);
      setCookie("TORRO_AUTH", encodeToken);
      return newState;
    },
    {
      init: Identity.init,
      userName: Identity.userName,
      userId: Identity.userId,
      roleList: Identity.roleList,
      role: Identity.role,
      wsList: Identity.wsList,
      wsId: Identity.wsId,
      accountId: Identity.accountId,
      ad_group_list: Identity.ad_group_list,
      userCN: Identity.userCN,
    }
  );

  const [languageContext, languageContextDispatch] = useReducer(
    (state, actions) => {
      let newState = state;
      newState = {
        ...state,
        lang: actions.payload.lang,
      };
      setCookie("TORRO_LANG", actions.payload.lang);
      return newState;
    },
    {
      lang: getCookie("TORRO_LANG") || "en",
    }
  );

  const [formListContext, formListContextDispatch] = useReducer(
    (state, actions) => {
      let newState = state;
      newState = {
        ...state,
        list: actions.payload,
        userList: actions.payload.filter((item) => item.hide === 0),
        managementList: actions.payload.filter(
          (item) => item.hide === 0 || item.id === 2
        ),
      };
      return newState;
    },
    {
      list: [],
      userList: [],
    }
  );

  const [torroConfigContext, torroConfigDispatch] = useReducer(
    (state, actions) => {
      let newState = state;
      newState = {
        ...state,
        ...actions.payload,
      };
      return newState;
    },
    {}
  );

  const [wsContext, wsContextDispatch] = useReducer(
    (state, actions) => {
      let newState = state;
      newState = {
        ...state,
        wsList: actions.payload.wsList,
        wsId: actions.payload.wsId,
      };
      return newState;
    },
    {
      wsList: [
        {
          value: 356,
          label: "New workspace",
        },
        {
          value: 361,
          label: "New workspace1",
        },
        {
          value: 362,
          label: "Torro",
        },
        {
          value: 364,
          label: "New workspace2",
        },
      ],
      wsId: 362,
    }
  );

  const setAuth = (role) => {
    authContextDispatch({
      type: "",
      payload: role,
    });
  };

  const setLanguage = (lang) => {
    languageContextDispatch({
      type: "",
      payload: lang,
    });
  };

  const setFormContext = (list) => {
    formListContextDispatch({
      type: "",
      payload: list,
    });
  };

  const setWsContext = (data) => {
    wsContextDispatch({
      type: "",
      payload: data,
    });
  };

  const setTorroConfig = (data) => {
    torroConfigDispatch({
      type: "",
      payload: data,
    });
  };

  const value = {
    authContext,
    setAuth,
    languageContext,
    setLanguage,
    formListContext,
    setFormContext,
    wsContext,
    setWsContext,
    torroConfigContext,
    setTorroConfig,
  };

  return (
    <GlobalContext.Provider value={value}>
      {props.children}
    </GlobalContext.Provider>
  );
};

const useGlobalContext = () => useContext(GlobalContext);

export { GlobalContextProvider, useGlobalContext };

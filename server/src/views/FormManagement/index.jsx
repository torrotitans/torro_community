/* third lib*/
import React, { useCallback, useEffect, useMemo, useState } from "react";
import { FormattedMessage as Intl } from "react-intl";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";

/* material-ui */
import AddIcon from "@material-ui/icons/Add";

/* local components & methods */
import Loading from "@assets/icons/Loading";
import Button from "@basics/Button";
import TextEdit from "@basics/TextEdit";
import FormItem from "@comp/FormItem";
import styles from "./styles.module.scss";
import CallModal from "@basics/CallModal";
import { getQueryString } from "src/utils/url-util.js";
import {
  getFormItem,
  postFormData,
  addFormData,
  deleteFormData,
  getUcResource,
} from "@lib/api";
import DesignPanel from "./DesignPanel";
import { sendNotify } from "src/utils/systerm-error";
import { SUCCESS } from "src/lib/data/callStatus";
import { useGlobalContext } from "src/context";

const defaultIndex = -1;
const specialForm = [{ id: 2, torroDefField: ["s1", "u2", "u3", "u8", "u11"] }];
const UC_FORM_ID = "2";
const UC_PROP_MAP = {
  u2: "owner_group",
  u3: "team_group",
  u8: "service_account",
  u11: "label",
};

const UC_PROP = ["u2", "u3", "u8", "u11"];

const FormManagement = ({ tagTemplate }) => {
  const { formListContext } = useGlobalContext();

  const { control } = useForm(); // initialise the hook
  const [formData, setFormData] = useState(null);
  const [formId, setFormId] = useState(getQueryString("formId") || null);
  const [editModuleIndex, setEditModuleIndex] = useState(-1);
  const [formLoading, setFormLoading] = useState(true);
  const navigate = useNavigate();

  const [modalData, setModalData] = useState({
    open: false,
    status: 0,
    content: "",
    cb: null,
  });

  const formList = useMemo(() => {
    return formListContext?.managementList || [];
  }, [formListContext]);

  const ucForm = useMemo(() => {
    return String(formId) === UC_FORM_ID;
  }, [formId]);

  const currentModule = useMemo(() => {
    return editModuleIndex !== defaultIndex
      ? formData.fieldList[editModuleIndex]
      : null;
  }, [editModuleIndex, formData]);

  const maxFieldId = useMemo(() => {
    let maxId = 0;
    if (formData) {
      formData.fieldList.forEach((item) => {
        if (item.id && item.id.indexOf("u") !== -1) {
          let tmpId = item.id.replace("u", "");
          if (Number(tmpId) > maxId) {
            maxId = Number(tmpId);
          }
        }
      });
    }

    return maxId;
  }, [formData]);

  const saveFormData = useCallback(() => {
    let apiCall = formData.id === "ADD" ? addFormData : postFormData;
    let postData = {
      title: formData.title,
      fieldList: formData.fieldList,
      des: formData.des,
    };
    if (formData.id && formData.id !== "ADD") {
      postData.id = formData.id;
    }
    if (tagTemplate) {
      postData.tag_template = true;
    }
    setModalData({
      ...modalData,
      status: 0,
      content: <Intl id="loadNpatience" />,
      cb: null,
    });
    apiCall(postData)
      .then((res) => {
        if (res.code === SUCCESS) {
          setModalData({
            ...modalData,
            status: 2,
            content:
              formData.id === "ADD"
                ? "New form is submitted."
                : "This form is submitted.",
            successCb: () => {
              navigate(`/app/requestDetail?id=${res.data.id}`);
            },
            cb: () => {
              navigate(`/app/dashboard`);
            },
          });
        }
      })
      .catch(() => {
        setModalData({
          ...modalData,
          status: 3,
          content: <Intl id="checkInput" />,
          cb: null,
        });
      });
  }, [modalData, formData, tagTemplate, navigate]);

  const addForm = () => {
    let tmpFormData = {
      id: "ADD",
      title: "Form Name",
      fields_num: 0,
      fieldList: [],
      des: "Form des",
    };
    setFormData(tmpFormData);
  };

  const deleteFieldHandle = (index) => {
    let tempList = JSON.parse(JSON.stringify(formData.fieldList));
    tempList.splice(index, 1);
    setFormData({
      ...formData,
      fieldList: tempList,
    });
  };

  const handleDataChange = (data, defaultTemplate) => {
    if (defaultTemplate) {
      if (
        currentModule.id.startsWith("s") ||
        currentModule.id.startsWith("d")
      ) {
        formData.fieldList[editModuleIndex] = {
          ...data,
          id: "u" + (maxFieldId + 1),
        };
      } else {
        formData.fieldList[editModuleIndex] = {
          ...data,
          id: currentModule.id,
        };
      }
    } else {
      formData.fieldList[editModuleIndex] = data;
    }
    setFormData({ ...formData });
  };

  const addField = (data) => {
    let tempList = JSON.parse(JSON.stringify(formData.fieldList));
    tempList.push(data);
    setFormData({
      ...formData,
      fieldList: tempList,
    });
  };

  const deleteForm = (id, index) => {
    setModalData({
      open: true,
      status: 1,
      content: <Intl id="confirmDeleteForm" />,
      cb: () => {
        setModalData({
          open: false,
          status: 0,
          content: <Intl id="submitting" />,
          cb: null,
        });
        deleteFormData({ id: id }).then((res) => {
          if (res.code === SUCCESS) {
            setModalData({
              open: true,
              status: 2,
              content: <Intl id="formDeleted" />,
              cb: () => {
                setModalData({
                  status: 2,
                  open: false,
                  content: <Intl id="formDeleted" />,
                  cb: null,
                });
              },
            });
          }
        });
      },
    });
  };

  const upHandle = useCallback(
    (index) => {
      let tempList = JSON.parse(JSON.stringify(formData.fieldList));
      let currentIndex = index - 1;
      let currItem = tempList.splice(index, 1)[0];
      tempList.splice(currentIndex, 0, currItem);
      setFormData({
        ...formData,
        fieldList: tempList,
      });
    },
    [formData]
  );
  const downHandle = useCallback(
    (index) => {
      let tempList = JSON.parse(JSON.stringify(formData.fieldList));
      let currentIndex = index + 1;
      let currItem = tempList.splice(index, 1)[0];
      tempList.splice(currentIndex, 0, currItem);
      setFormData({
        ...formData,
        fieldList: tempList,
      });
    },
    [formData]
  );

  const copySystemFieldHandle = useCallback(
    (item) => {
      let tempList = JSON.parse(JSON.stringify(formData.fieldList));
      tempList.push({
        ...item,
        point_id: item.id,
        id: "u" + (maxFieldId + 1),
      });
      setFormData({
        ...formData,
        fieldList: tempList,
      });
    },
    [formData, maxFieldId]
  );

  const specialField = useMemo(() => {
    if (!formData) {
      return [];
    }
    let tmp = [];
    specialForm.forEach((item) => {
      if (item.id === formData.id) tmp = item.torroDefField || [];
    });

    return tmp;
  }, [formData]);

  console.log(formData);

  const renderFormItem = (items) => {
    let itemLen = items.length;

    return items.map((item, index) => {
      return (
        <FormItem
          enableEdit={!specialField.includes(item.id)}
          key={index}
          data={item}
          index={index}
          onChange={() => {}}
          editState={editModuleIndex === index}
          onDelete={() => {
            deleteFieldHandle(index);
          }}
          onEdit={(key) => {
            if (key) {
              setEditModuleIndex(index);
            } else {
              setEditModuleIndex(defaultIndex);
            }
          }}
          onCopy={
            item.id.startsWith("s") || item.id.startsWith("d")
              ? () => {
                  copySystemFieldHandle(item);
                }
              : null
          }
          onUp={
            index === 0
              ? null
              : () => {
                  upHandle(index);
                }
          }
          onDown={
            index === itemLen - 1
              ? null
              : () => {
                  downHandle(index);
                }
          }
          control={control}
          systemTag={
            item.id.startsWith("s") ||
            item.id.startsWith("d") ||
            specialField.includes(item.id)
          }
        />
      );
    });
  };

  const existIdList = useMemo(() => {
    if (!formData) {
      return [];
    }
    return formData.fieldList.map((item) => item.id);
  }, [formData]);

  const clickAwayHandle = (e) => {
    setEditModuleIndex(defaultIndex);
  };
  const initUcDef = useCallback((tempFieldList, formData) => {
    getUcResource()
      .then((res2) => {
        if (res2.data) {
          let tmpUcDef = {};
          Object.keys(UC_PROP_MAP).forEach((key) => {
            tmpUcDef[key] = [];
          });
          res2.data.forEach((item, index) => {
            Object.keys(UC_PROP_MAP).forEach((key) => {
              tmpUcDef[key].push(item.resource[UC_PROP_MAP[key]]);
            });
          });
          tempFieldList = tempFieldList.map((item) => {
            if (UC_PROP.includes(item.id)) {
              item.style = 2;
              item.options = tmpUcDef[item.id].map((val, index) => ({
                label: val,
                value: index,
              }));
            }
            return item;
          });
          setFormData({
            ...formData,
            fieldList: tempFieldList,
          });
          setFormLoading(false);
        }
      })
      .catch((e) => {
        sendNotify({ msg: e.message, status: 3, show: true });
      });
  }, []);

  const getFormData = useCallback(
    (id) => {
      setFormLoading(true);
      getFormItem({ id: id })
        .then((res) => {
          if (res.code === SUCCESS) {
            let data = res.data;
            if (ucForm) {
              initUcDef(data.fieldList, data);
              return;
            }
            setFormLoading(false);
            setFormData({
              ...res.data,
            });
          }
        })
        .catch((e) => {
          sendNotify({ msg: e.message, status: 3, show: true });
        });
    },
    [initUcDef, ucForm]
  );

  useEffect(() => {
    if (!formId) {
      setFormData({
        id: "ADD",
        title: tagTemplate ? "Tag template name" : "Form Name",
        fields_num: 0,
        fieldList: [],
        des: tagTemplate ? "Tag template description" : "Form Description",
      });
      setFormLoading(false);
      return;
    }
    getFormData(formId);
  }, [formId, tagTemplate, getFormData]);

  return (
    <div className={styles.formManagement}>
      <div className={styles.formControl} onClick={clickAwayHandle}>
        {formLoading && <Loading />}
        {!formLoading && formData && (
          <div className={styles.currentForm}>
            <div className={styles.formTitle}>
              <TextEdit
                value={formData.title}
                onChange={(title) => {
                  setFormData({
                    ...formData,
                    title: title,
                  });
                }}
              />
            </div>

            <div className={styles.formDes}>
              <TextEdit
                value={formData.des}
                onChange={(des) => {
                  setFormData({
                    ...formData,
                    des: des,
                  });
                }}
              />
            </div>
            <div className={styles.form}>
              <form id={`currentForm${formData.id}`}>
                <div className={styles.formOptions}>
                  {renderFormItem(formData.fieldList)}
                </div>
                <div
                  className={styles.addFields}
                  onClick={(e) => {
                    e.stopPropagation();
                    const data = {
                      default: "",
                      des: "",
                      edit: 1,
                      id: "u" + (maxFieldId + 1),
                      point_id: "",
                      label: "Text",
                      options: [],
                      placeholder: "",
                      style: 3,
                      required: true,
                      maxLength: 25,
                      rule: 0,
                    };
                    addField(data);
                    setEditModuleIndex(formData.fieldList.length);
                  }}
                >
                  <AddIcon />
                  <Intl id="addField" />
                </div>
              </form>
              <div className={styles.buttonWrapper}>
                <Button
                  className={styles.button}
                  variant="contained"
                  onClick={() => {
                    setModalData({
                      open: true,
                      status: 1,
                      content:
                        formData.id === "ADD"
                          ? "Do you confirm to add a new form?"
                          : "Please confirm to submit this form.",
                      cb: null,
                    });
                  }}
                >
                  <Intl id="save" />
                </Button>
              </div>
            </div>
          </div>
        )}
      </div>
      <DesignPanel
        id="designPanel"
        formList={formList}
        currentForm={formData}
        currentModule={currentModule}
        existIdList={existIdList}
        onChange={handleDataChange}
        tagTemplate={tagTemplate}
        formChange={(id) => {
          const tempData = formList.find((item) => {
            return item.id === id;
          });
          setFormId(tempData.id);
        }}
        addForm={addForm}
        deleteForm={deleteForm}
      />
      <CallModal
        open={modalData.open}
        content={modalData.content}
        status={modalData.status}
        successCb={modalData.successCb}
        buttonClickHandle={() => {
          if (!modalData.cb) {
            switch (modalData.status) {
              case 0:
              case 2:
                setModalData({ ...modalData, open: false, cb: null });
                break;
              case 1:
              case 3:
                saveFormData();
                break;
              default:
                break;
            }
          } else {
            modalData.cb();
          }
        }}
        handleClose={() => {
          setModalData({ ...modalData, open: false, cb: null });
        }}
      />
    </div>
  );
};

export default FormManagement;

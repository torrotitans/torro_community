/* third lib*/
import React, {
  useEffect,
  useState,
  useCallback,
  useMemo,
  useRef,
} from "react";
import { FormattedMessage as Intl } from "react-intl";
import { useForm } from "react-hook-form";
import Scrollbar from "react-perfect-scrollbar";
import { useNavigate } from "react-router-dom";
import XLSX from "xlsx";

/* material-ui */
import FormLabel from "@material-ui/core/FormLabel";

/* local components & methods */
import { useGlobalContext } from "src/context";
import HeadLine from "@basics/HeadLine";
import FormItem from "@comp/FormItem";
import Button from "@basics/Button";
import Text from "@basics/Text";
import styles from "./styles.module.scss";
import {
  getFieldTemplate,
  wsPut,
  wsPost,
  getWsDetail,
  getWorkspaceForm,
} from "@lib/api";
import { STATIC_TEMPLATE } from "@lib/data/staticTemplate";
import Loading from "@assets/icons/Loading";
import { sendNotify } from "src/utils/systerm-error";
import CallModal from "@basics/CallModal";
import { SUCCESS } from "src/lib/data/callStatus";
import SystemDefineField from "./SystemDefineField";
import RegionDesign from "./RegionDesign";
import GroupListTable from "./GroupListTable";

const FILENAME = "AD group list template.xlsx";

const Workspace = ({ currentId, onBack, addState }) => {
  const { handleSubmit, control, register } = useForm(); // initialise the hook
  const { setAuth, authContext } = useGlobalContext();
  const navigate = useNavigate();
  const fileRef = useRef();

  const [formData, setFormData] = useState(null);
  const [formLoading, setFormLoading] = useState(true);
  const [adList, setAdList] = useState([
    ["Use case Owner Group", "Use case Team Group", "Admin Service Account"],
  ]);

  const [step, setStep] = useState(0);
  const [currentWs, setCurrentWs] = useState(null);
  const [regions, setRegions] = useState([]);
  const [fieldTemplate, setFieldTemplate] = useState([]);
  const [submitData, setSubmitData] = useState(null);
  const [wsId, setWsId] = useState(currentId);
  const [modalData, setModalData] = useState({
    open: false,
    status: 0,
    content: "",
  });

  const currentField = useMemo(() => {
    if (currentWs && currentWs.system) {
      let tmp = "";
      const formItemMap = {
        1: "Checkbox",
        2: "Dropdown",
        3: "Textbox",
        4: "Upload",
        5: "Toggle",
        6: "Datepicker",
      };

      Object.keys(currentWs.system).forEach((key) => {
        tmp += `${currentWs.system[key].length} ${formItemMap[key]} `;
      });
      return tmp;
    } else {
      return "";
    }
  }, [currentWs]);

  const addRegion = () => {
    let tmp = [...regions];
    tmp.push({
      region: "",
      group: "",
      workflow: "",
      countryList: [],
    });
    setRegions(tmp);
  };

  const downLoadTemplate = useCallback(() => {
    let ws_name = "Sheet1";
    let wb = XLSX.utils.book_new();
    let ws = XLSX.utils.aoa_to_sheet(adList);

    ws["!cols"] = [{ width: 30 }, { width: 30 }, { width: 30 }];

    XLSX.utils.book_append_sheet(wb, ws, ws_name);
    XLSX.writeFile(wb, FILENAME);
  }, [adList]);

  const uploadFile = useCallback(() => {
    fileRef.current.click();
  }, []);

  const clearFile = useCallback((e) => {
    e.target.value = null;
  }, []);

  const uploadExcel = useCallback((e) => {
    var X = XLSX;
    var to_json = function to_json(workbook) {
      var result = {};
      workbook.SheetNames.forEach(function(sheetName) {
        var roa = X.utils.sheet_to_json(workbook.Sheets[sheetName], {
          header: 1,
        });
        if (roa.length) result[sheetName] = roa;
      });
      return result;
    };

    let f = e.target.files[0];
    let reader = new FileReader();
    reader.onload = function(e) {
      var data = e.target.result;
      let d = to_json(X.read(data, { type: "array" }));
      setAdList(d["Sheet1"]);
    };
    reader.readAsArrayBuffer(f);
  }, []);

  const buttonClickHandle = useCallback(() => {
    let apiCall = addState ? wsPost : wsPut;
    let postData = submitData;
    switch (modalData.status) {
      case 1:
      case 3:
        setModalData({
          ...modalData,
          status: 0,
          content: <Intl id="loadNpatience" />,
        });
        apiCall(postData)
          .then((res) => {
            if (res.code === SUCCESS) {
              setModalData({
                open: true,
                status: 2,
                content: wsId ? <Intl id="wsUpdated" /> : <Intl id="wsIsAdd" />,
                cb: () => {
                  if (addState) {
                    setAuth({
                      ...authContext,
                      role: res.data.role_name,
                      roleList: res.data.role_list,
                      wsId: Number(res.data.workspace_id),
                      wsList: res.data.workspace_list,
                    });
                    navigate("/app/dashboard");
                  } else {
                    window.location.reload();
                  }
                },
              });
            }
          })
          .catch(() => {
            setModalData({
              ...modalData,
              status: 3,
              content: <Intl id="checkInput" />,
            });
          });
        break;
      default:
        setModalData({ ...modalData, open: false });
        break;
    }
  }, [modalData, submitData, wsId, addState, authContext, setAuth, navigate]);

  const checkRegionEmptyVal = useCallback((regions) => {
    let validate = true;
    regions.forEach((regionItem) => {
      if (!regionItem.region || !regionItem.workflow) {
        validate = false;
      }

      regionItem.countryList.forEach((countryItem) => {
        if (!countryItem.country || !countryItem.workflow) {
          validate = false;
        }
      });
    });

    return validate;
  }, []);

  const submitHandle = useCallback(
    (data) => {
      if (!checkRegionEmptyVal(regions)) {
        sendNotify({
          msg:
            "Each region or country need to fill in name and workflow value.",
          status: 3,
          show: true,
        });
        return;
      }
      setModalData({
        open: true,
        status: 1,
        content: wsId ? (
          <Intl id="confirmUpdateWs" />
        ) : (
          <Intl id="confirmAddWS" />
        ),
      });

      let groupData = adList.filter((d, index) => index !== 0);
      let groupMap = {
        ownerGroupList: [],
        teamGroupList: [],
        accontList: [],
      };
      groupData.forEach((item) => {
        groupMap.ownerGroupList.push(item[0]);
        groupMap.teamGroupList.push(item[1]);
        groupMap.accontList.push(item[2]);
      });
      setSubmitData({
        ...currentWs,
        ...data,
        regions: regions,
        groupArr: groupMap,
      });
      console.log({
        ...currentWs,
        ...data,
        regions: regions,
        groupArr: groupMap,
      });
    },
    [regions, currentWs, wsId, adList, checkRegionEmptyVal]
  );

  const renderFormItem = (items, disabled) => {
    return items.map((item, index) => {
      return (
        <FormItem
          key={index}
          data={item}
          index={index}
          control={control}
          register={register}
          disabled={disabled}
        />
      );
    });
  };

  useEffect(() => {
    getFieldTemplate()
      .then((res) => {
        if (res) {
          let dynamic = res.data.dynamic;
          let system = res.data.system;
          setFieldTemplate(
            STATIC_TEMPLATE.map((item, index) => {
              let style = index + 1;
              return {
                ...item,
                systemList: [...dynamic[style], ...system[style]],
              };
            })
          );
        }
      })
      .catch((e) => {
        setFieldTemplate(STATIC_TEMPLATE);
        sendNotify({ msg: e.message, status: 3, show: true });
      });
  }, []);

  useEffect(() => {
    getWorkspaceForm()
      .then((res) => {
        if (res.data) {
          let workspaceData = res.data;
          if (addState) {
            setFormData(workspaceData);
            setCurrentWs({
              it_group: "",
              dg_group: "",
              ws_name: "",
              ws_des: "",
              ws_owner_group: "",
              ws_team_group: "",
              cycle: "",
              approval: "",
              regions: [],
              system: {
                1: [],
                2: [],
                3: [],
                4: [],
                5: [],
                6: [],
              },
            });
            setFormLoading(false);
            return;
          }
          setWsId(currentId);
          getWsDetail({ id: currentId })
            .then((res) => {
              let data = res.data;
              let tmp = JSON.parse(JSON.stringify(workspaceData));
              let tmpFieldList = tmp.fieldList.map((item) => {
                if (item.id && data[item.id]) {
                  item.default = data[item.id];
                }
                return item;
              });

              data.system =
                JSON.stringify(data.system) === "{}"
                  ? {
                      1: [],
                      2: [],
                      3: [],
                      4: [],
                      5: [],
                      6: [],
                    }
                  : data.system;
              setRegions(data.regions);
              setFormData({
                ...tmp,
                fieldList: tmpFieldList,
                title: data.ws_name,
                des: data.ws_des,
              });
              setCurrentWs(data);
              setFormLoading(false);
            })
            .catch((e) => {
              sendNotify({ msg: e.message, status: 3, show: true });
            });
        }
      })
      .catch((e) => {
        sendNotify({ msg: e.message, status: 3, show: true });
      });
  }, [currentId, addState]);

  return (
    <>
      {step === 0 && (
        <div className={styles.workspaceForm}>
          <div className={styles.formView}>
            <Scrollbar>
              {formLoading && <Loading />}
              {!formLoading && formData && (
                <div className={styles.formControl}>
                  <HeadLine>
                    {wsId ? <Intl id="updateWs" /> : <Intl id="createWs" />}
                  </HeadLine>
                  <form
                    className={styles.form}
                    id={`currentForm${formData.id}`}
                    onSubmit={handleSubmit(submitHandle)}
                  >
                    <div className={styles.formOptions}>
                      {renderFormItem(formData.fieldList)}
                    </div>

                    <div className={styles.formItemLine}>
                      <div className={styles.formItemTitle}>
                        <FormLabel className={styles.fieldTitle}>
                          <Text type="subTitle">
                            <Intl id="defaultAd" />
                          </Text>
                        </FormLabel>
                        <div className={styles.excelBtnGroup}>
                          <div
                            className={styles.operationBtn}
                            onClick={downLoadTemplate}
                          >
                            <Intl id="downLoadExcel" />
                          </div>
                          <div
                            className={styles.operationBtn}
                            onClick={uploadFile}
                          >
                            {currentId ? (
                              <Intl id="addNewAD" />
                            ) : (
                              <Intl id="uploadExcel" />
                            )}

                            <input
                              className={styles.uploadBtn}
                              type="file"
                              name="xlfile"
                              id="xlf"
                              ref={fileRef}
                              accept=".csv, application/vnd.ms-excel, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                              onChange={uploadExcel}
                              onClick={clearFile}
                            ></input>
                          </div>
                        </div>
                      </div>

                      <GroupListTable
                        data={adList}
                        onChange={(data) => {
                          setAdList(data);
                        }}
                      />
                    </div>
                    <div className={styles.formItemLine}>
                      <div className={styles.formItemTitle}>
                        <FormLabel className={styles.fieldTitle}>
                          <Text type="subTitle">
                            <Intl id="regionStructure" />
                          </Text>
                        </FormLabel>
                        <div
                          className={styles.operationBtn}
                          onClick={(e) => {
                            addRegion();
                          }}
                        >
                          <Intl id="addRegion" />
                        </div>
                      </div>

                      <RegionDesign
                        regions={regions}
                        onChange={(data) => {
                          setRegions(data);
                        }}
                      />
                    </div>

                    <div className={styles.formItemLine}>
                      <div className={styles.formItemTitle}>
                        <FormLabel className={styles.fieldTitle}>
                          <Text type="subTitle">
                            <Intl id="systemField" />
                          </Text>
                        </FormLabel>
                        <div
                          className={styles.operationBtn}
                          onClick={(e) => {
                            setStep(1);
                          }}
                        >
                          <Intl id="updateSystemField" />
                        </div>
                      </div>
                      <div className={styles.systemField}>
                        <div className={styles.currentField}>
                          {currentField}
                        </div>
                      </div>
                    </div>

                    <div className={styles.buttonWrapper}>
                      {onBack && (
                        <Button
                          onClick={() => {
                            onBack();
                          }}
                          className={styles.button}
                          variant="contained"
                        >
                          <Intl id="back" />
                        </Button>
                      )}
                      <Button
                        className={styles.button}
                        type="submit"
                        variant="contained"
                      >
                        <Intl id="submit" />
                      </Button>
                    </div>
                  </form>
                </div>
              )}
            </Scrollbar>
          </div>
        </div>
      )}
      {step === 1 && (
        <SystemDefineField
          fieldTemplate={fieldTemplate}
          systemDefineField={currentWs.system}
          onChange={(data) => {
            setCurrentWs({
              ...currentWs,
              system: data,
            });
            setStep(0);
          }}
          cancelHandle={() => {
            setStep(0);
          }}
        />
      )}
      <CallModal
        open={modalData.open}
        content={modalData.content}
        status={modalData.status}
        buttonClickHandle={() => {
          if (!modalData.cb) {
            buttonClickHandle();
          } else {
            modalData.cb();
          }
        }}
        handleClose={() => {
          setModalData({ ...modalData, open: false });
        }}
      />
    </>
  );
};

export default Workspace;

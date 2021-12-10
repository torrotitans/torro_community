/* third lib*/
import React, { useEffect, useState, useCallback, useMemo } from "react";
import { FormattedMessage as Intl } from "react-intl";
import { useForm } from "react-hook-form";
import Scrollbar from "react-perfect-scrollbar";

/* material-ui */
import FormLabel from "@material-ui/core/FormLabel";

/* local components & methods */
import HeadLine from "@comp/HeadLine";
import FormItem from "@comp/FormItem";
import Button from "@comp/Button";
import Text from "@comp/Text";
import styles from "./styles.module.scss";
import { getFieldTemplate, wsPut, wsPost, getWsDetail } from "@lib/api";
import Loading from "src/icons/Loading";
import { sendNotify } from "src/utils/systerm-error";
import CallModal from "@comp/CallModal";
import { SUCCESS } from "src/lib/data/callStatus";
import SystemDefineField from "./SystemDefineField";
import RegionDesign from "./RegionDesign";

const workspaceData = {
  des: "Create workspace",
  fieldList: [
    {
      default: "",
      des: "IT admin AD group",
      edit: 1,
      id: "it_group",
      label: "IT admin AD group",
      options: [],
      placeholder: "IT admin AD group",
      style: 3,
    },
    {
      default: "",
      des: "Data Governance AD Group",
      edit: 1,
      id: "dg_group",
      label: "Data Governance AD Group",
      options: [],
      placeholder: "Data Governance AD Group",
      style: 3,
    },
    {
      default: "",
      des: "Workspace Name",
      edit: 1,
      id: "ws_name",
      label: "Workspace Name",
      options: [],
      placeholder: "Workspace Name",
      style: 3,
    },
    {
      default: "",
      des: "Workspace Description",
      edit: 1,
      id: "ws_des",
      label: "Workspace Description",
      options: [],
      placeholder: "Workspace Description",
      style: 3,
    },
    {
      default: "",
      des: "WS head AD group",
      edit: 1,
      id: "ws_head_group",
      label: "WS head AD group",
      options: [],
      placeholder: "WS head AD group",
      style: 3,
    },
    {
      default: "",
      des: "WS Team AD group",
      edit: 1,
      id: "ws_team_group",
      label: "WS Team AD group",
      options: [],
      placeholder: "WS Team AD group",
      style: 3,
    },
    {
      default: "",
      des: "User recertification cycle",
      edit: 1,
      id: "cycle",
      label: "User recertification cycle",
      options: [
        { label: "Monthly", value: "Monthly" },
        { label: "Quarterly", value: "Quarterly" },
        { label: "Semi Annually", value: "Semi Annually" },
        { label: "Annually", value: "Annually" },
      ],
      placeholder: "",
      style: 2,
    },
    {
      default: "",
      des: "Use case approval flow",
      edit: 1,
      id: "approval",
      label: "Use case approval flow",
      options: [
        {
          label: "Need workspace IT approval",
        },
        {
          label: "Need workspace Head approval",
        },
      ],
      placeholder: "",
      style: 1,
    },
  ],
  fields_num: 6,
  id: 372,
  title: "Create workspace",
  u_max_id: 0,
};

const Workspace = ({ currentId, onBack, addState }) => {
  const { handleSubmit, control, register } = useForm(); // initialise the hook
  const [formData, setFormData] = useState(null);
  const [formLoading, setFormLoading] = useState(true);

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
  }, [modalData, submitData, wsId, addState]);

  const submitHandle = useCallback(
    (data) => {
      setModalData({
        open: true,
        status: 1,
        content: wsId ? (
          <Intl id="confirmUpdateWs" />
        ) : (
          <Intl id="confirmAddWS" />
        ),
      });
      setSubmitData({
        ...currentWs,
        ...data,
        regions: regions,
      });
    },
    [regions, currentWs, wsId]
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
    getFieldTemplate().then((res) => {
      if (res) {
        let dynamic = res.data.dynamic;
        let system = res.data.system;
        setFieldTemplate([
          {
            style: 1,
            default: {
              style: 1,
              label: "CheckBox",
              default: "true,false",
              options: [{ label: "true" }, { label: "false" }],
            },
            systemList: [...dynamic[1], ...system[1]],
          },
          {
            style: 2,
            default: {
              style: 2,
              label: "Dropdown",
              default: "Option1",
              options: [
                { label: "Option1", value: "Option1" },
                { label: "Option2", value: "Option2" },
              ],
            },
            systemList: [...dynamic[2], ...system[2]],
          },
          {
            style: 3,
            default: {
              style: 3,
              label: "Text",
              placeholder: "",
              default: "",
            },
            systemList: [...dynamic[3], ...system[3]],
          },
          {
            style: 4,
            default: {
              style: 4,
              label: "Upload",
              placeholder: "",
              default: "",
              multiple: false,
            },
            systemList: [...dynamic[4], ...system[4]],
          },
          {
            style: 5,
            default: {
              style: 5,
              label: "Switch",
              default: true,
              placeholder: "",
            },
            systemList: [...dynamic[5], ...system[5]],
          },
          {
            style: 6,
            default: {
              style: 6,
              label: "DatePicker",
              placeholder: "",
              default: "",
            },
            systemList: [...dynamic[6], ...system[6]],
          },
        ]);
      }
    });
  }, []);

  useEffect(() => {
    if (addState) {
      setFormData(workspaceData);
      setCurrentWs({
        it_group: "",
        dg_group: "",
        ws_name: "",
        ws_des: "",
        ws_head_group: "",
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
                            <Intl id="regionStructure" />
                          </Text>
                        </FormLabel>
                        <div
                          className={styles.addRegionBtn}
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
                          className={styles.addRegionBtn}
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

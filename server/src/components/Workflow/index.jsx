/* third lib*/
import React, { useState, useMemo, useEffect, useCallback } from "react";
import { FormattedMessage as Intl } from "react-intl";
import Scrollbar from "react-perfect-scrollbar";

/* local components & methods */
import styles from "./styles.module.scss";
import Loading from "@assets/icons/Loading";
import Button from "@basics/Button";
import TextEdit from "@basics/TextEdit";
import { DragDropContext } from "react-beautiful-dnd";
import CallModal from "@basics/CallModal";
import { getWorkflowData, saveWorkflowData, getFormItem } from "@lib/api";
import { SUCCESS } from "src/lib/data/callStatus";
import { sendNotify } from "src/utils/systerm-error";
import WorkflowRender from "./WorkflowRender";
import WorkflowDesginPanel from "./WorkflowDesginPanel";

const Workflow = ({ flowId, droppableItems }) => {
  const [workflowData, setWorkflowData] = useState(null);
  const [formFields, setFormFields] = useState([]);
  const [flowLoading, setFlowLoading] = useState(true);
  const [editIndex, setEditIndex] = useState(null);
  const [conditionItems, setConditionItems] = useState([]);
  const [modalData, setModalData] = useState({
    open: false,
    status: 0,
    content: "",
    cb: null,
  });

  const validateCheck = useCallback((workflowData) => {
    let checkData = {
      validate: true,
      msg: "",
    };
    let flowTypeStep = workflowData.stages.map((item) => item.flowType);
    if (!flowTypeStep.includes("Approval")) {
      checkData.validate = false;
      checkData.msg = "Approval process is require in each workflow.";
    } else {
      let stages = workflowData.stages;
      stages.forEach((item) => {
        item.condition.forEach((con) => {
          if (!con.value && item.flowType !== "Approval") {
            checkData.validate = false;
            checkData.msg = `${item.label} has condition value is Empty`;
          }
        });
      });
    }
    return checkData;
  }, []);

  const submitHandle = () => {
    let checked = validateCheck(workflowData);
    if (!checked.validate) {
      sendNotify({
        msg: checked.msg,
        status: 3,
        show: true,
      });
      return;
    }
    setModalData({
      open: true,
      status: 1,
      content: "Do you confirm to save the workflow?",
      cb: () => {
        setModalData({
          ...modalData,
          status: 0,
          content: "Submitting. and appreciate your patience.",
          cb: null,
        });
        saveWorkflowData({
          ...workflowData,
          create_by: "45120695",
          modify_by: "45120695",
        })
          .then((res) => {
            if (res.code === SUCCESS) {
              setModalData({
                open: true,
                status: 2,
                content: "workflow has been saved",
                cb: () => {
                  setModalData({
                    open: false,
                    status: 2,
                    content: "workflow has been saved",
                    cb: null,
                  });
                },
              });
            }
          })
          .catch((e) => {
            setModalData({
              open: true,
              status: 3,
              content: e.message,
              cb: () => {
                setModalData({
                  open: false,
                  content: e.message,
                  cb: null,
                  status: 3,
                });
              },
            });
          });
      },
    });
  };

  const flow = useMemo(() => {
    return workflowData ? workflowData.stages : [];
  }, [workflowData]);

  const editFlow = useMemo(() => {
    if (editIndex !== null) {
      return flow[editIndex];
    } else {
      return null;
    }
  }, [editIndex, flow]);

  const flowIdList = useMemo(() => {
    if (editFlow) {
      return editFlow.condition.map((item) => {
        return item.id;
      });
    }
    return flow.map((item) => {
      return item.id;
    });
  }, [flow, editFlow]);

  const dropOptions = useMemo(() => {
    let tmpList;
    if (editFlow) {
      let tmpConditions = conditionItems
        ? conditionItems.filter((condition) => {
            return !flowIdList.includes(condition.id);
          })
        : [];
      return { type: "condition", data: tmpConditions };
    } else {
      tmpList = JSON.parse(JSON.stringify(droppableItems));
      // not unique item splice have dropped item from optionsList
      tmpList = tmpList.filter((item) => item.group !== "Approval");
      tmpList.forEach((item) => {
        item.itemList = item.itemList.filter((condition) => {
          return !flowIdList.includes(condition.id);
        });
      });
      return { type: "item", data: tmpList };
    }
  }, [flowIdList, editFlow, droppableItems, conditionItems]);

  const dropOptionMap = useMemo(() => {
    let mapData = {};
    dropOptions.data.forEach((item, index) => {
      mapData[item.group] = { seq: index, data: item };
    });
    return mapData;
  }, [dropOptions]);

  const commonConditionMap = useMemo(() => {
    let mapData = {};
    droppableItems.forEach((item, index) => {
      mapData[item.group] = item.commonConditions || [];
    });
    return mapData;
  }, [droppableItems]);

  const formFieldOptions = useMemo(() => {
    return formFields.map((item) => ({ label: item.label, value: item.id }));
  }, [formFields]);

  const onDragEnd = (result) => {
    // dropped outside the list
    if (!result.destination) {
      return;
    }
    const { source, destination, draggableId } = result;
    let droppableId = destination.droppableId;
    let isCondition = false;

    const tmpData = draggableId.split("_");
    const itemType = tmpData[0];

    if (droppableId.includes("condition")) {
      droppableId = droppableId.replace("condition", "");
      isCondition = true;
    }

    const destinationIndex = Number(droppableId.replace("droppable", ""));

    const itemIndex = source.index;
    let data = dropOptionMap[itemType].data.itemList[itemIndex];
    let tempFlow = JSON.parse(JSON.stringify(flow));
    if (isCondition) {
      tempFlow[destinationIndex].condition.push(data);
    } else {
      tempFlow.splice(destinationIndex, 1, data);
    }
    setWorkflowData({ ...workflowData, stages: tempFlow });
  };

  useEffect(() => {
    setFlowLoading(true);
    getWorkflowData({ id: flowId })
      .then((res) => {
        if (res.code === SUCCESS) {
          let wfData = res.data;
          getFormItem({ id: wfData.form_id })
            .then((res2) => {
              if (res2.code === SUCCESS) {
                let tmpItemList = res2.data.fieldList;
                setFormFields(tmpItemList);
                setWorkflowData(wfData);
                setFlowLoading(false);
              }
            })
            .catch((e) => {
              sendNotify({ msg: e.message, status: 3, show: true });
            });
        }
      })
      .catch((e) => {
        sendNotify({
          msg: "Faild to get workflow data.",
          status: 3,
          show: true,
        });
      });
  }, [flowId]);

  const getChildOptions = (data) => {
    if (data.flowType === "Trigger") {
      let tmpItemList = formFields.map((item) => ({
        id: item.id,
        style: item.style,
        options: item.options,
        label: item.label,
        placeholder: item.placeholder,
        value: item.default || "",
        conditionType: "0",
      }));
      setConditionItems([
        {
          label: "Form Fields",
          group: "FormField",
          itemList: tmpItemList,
        },
      ]);
    }

    if (data.flowType === "Approval") {
      let condtions = commonConditionMap[data.flowType];
      setConditionItems([
        {
          label: "Approval Level",
          group: "ApprovalLevel",
          itemList: condtions,
        },
      ]);
    }
  };

  return (
    <div className={styles.workflow}>
      <DragDropContext onDragEnd={onDragEnd}>
        <div className={styles.workflowview}>
          {flowLoading && <Loading />}
          {!flowLoading && (
            <>
              <div className={styles.nameEditBar}>
                <div className={styles.textEditor}>
                  <TextEdit
                    value={workflowData.workflow_name}
                    onChange={(name) => {
                      setWorkflowData({
                        ...workflowData,
                        workflow_name: name,
                      });
                    }}
                  />
                </div>
                <div className={styles.buttonGroup}>
                  <Button
                    onClick={() => {
                      window.history.back();
                    }}
                    className={styles.button}
                  >
                    <Intl id="back" />
                  </Button>

                  <Button
                    onClick={submitHandle}
                    filled
                    className={styles.button}
                  >
                    <Intl id="save" />
                  </Button>
                </div>
              </div>
              <div className={styles.workflowPanel}>
                <div className={styles.flowContainer}>
                  <Scrollbar className={styles.flowContainerScrollbar}>
                    <WorkflowRender
                      editFlow={editFlow}
                      closeEdit={(data) => {
                        let tmpFlow = JSON.parse(JSON.stringify(flow));
                        tmpFlow[editIndex] = data;
                        setWorkflowData({ ...workflowData, stages: tmpFlow });
                        setConditionItems(null);
                      }}
                      editIndex={editIndex}
                      onEdit={(index, data) => {
                        setConditionItems(null);
                        setEditIndex(index);
                        if (index !== null) {
                          getChildOptions(data);
                        }
                      }}
                      formFieldOptions={formFieldOptions}
                      workflowData={flow}
                      onChange={(data) => {
                        setWorkflowData({ ...workflowData, stages: data });
                      }}
                    />
                  </Scrollbar>
                </div>
              </div>
            </>
          )}
        </div>
        <WorkflowDesginPanel dropOptions={dropOptions} />
      </DragDropContext>
      <CallModal
        open={modalData.open}
        content={modalData.content}
        status={modalData.status}
        buttonClickHandle={modalData.cb}
        handleClose={() => {
          setModalData({ ...modalData, open: false, cb: null });
        }}
      />
    </div>
  );
};

export default Workflow;

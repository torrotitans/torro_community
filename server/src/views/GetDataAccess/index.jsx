/* third lib*/
import React, { useState, useEffect, useMemo, useCallback } from "react";
import { FormattedMessage as Intl } from "react-intl";
import { useForm, useWatch } from "react-hook-form";
import ScrollBar from "react-perfect-scrollbar";
import { useNavigate } from "react-router-dom";

/* material-ui */
import List from "@material-ui/core/List";
import ListItem from "@material-ui/core/ListItem";
import ListItemText from "@material-ui/core/ListItemText";
import Delete from "@material-ui/icons/Delete";

/* local components & methods */
import styles from "./styles.module.scss";
import FormItem from "@comp/FormItem";
import HeadLine from "@basics/HeadLine";
import Text from "@basics/Text";
import CallModal from "@basics/CallModal";
import Loading from "@assets/icons/Loading";
import Button from "@basics/Button";
import ResourceDetail from "@comp/ResourceDetail";
import {
  getUseCaseList,
  getOnBoardDataForm,
  getTableSchema,
  getPolicys,
  getTags,
  raiseFormRequestList,
} from "@lib/api";
import { sendNotify } from "src/utils/systerm-error";
import TableTagDisplay from "@comp/TableTag";
import Select from "@basics/Select";
import TableSchema from "./TableSchema";

const GET_ACCESS_FORM_ID = 108;

const GetDataAccess = () => {
  const { handleSubmit, control, register } = useForm(); // initialise the hook
  const navigate = useNavigate();
  const resourceType = useWatch({
    control,
    name: "resourceType",
    defaultValue: "GCP",
  });

  const [formLoading, setFormLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState();
  const [tableData, setTableData] = useState(null);
  const [policys, setPolicys] = useState([]);
  const [cartList, setCartList] = useState([]);
  const [tagTemplateList, setTagTempalteList] = useState([]);
  const [submitData, setSubmitData] = useState(null);
  const [onBoardDataForm, setOnBoardDataForm] = useState(null);
  const [useCaseList, setUseCaseList] = useState([]);
  const [selectedUc, setSelectedUc] = useState("");
  const [selectedList, setSelectedList] = useState([]);

  const tableForm = useMemo(() => {
    if (!onBoardDataForm) {
      return [];
    }
    return resourceType === "GCP" ? onBoardDataForm.gcp : onBoardDataForm.hive;
  }, [resourceType, onBoardDataForm]);

  const [modalData, setModalData] = useState({
    open: false,
    status: 0,
    content: "",
    cb: null,
  });
  const tableList = useMemo(() => {
    return tableData?.schema?.fields;
  }, [tableData]);

  const submitHandle = (data) => {
    setSearchQuery(data);
  };

  const buttonClickHandle = useCallback(() => {
    switch (modalData.status) {
      case 1:
      case 3:
        setModalData({
          ...modalData,
          status: 0,
          content: <Intl id="loadNpatience" />,
        });

        raiseFormRequestList(submitData)
          .then((res) => {
            setModalData({
              open: true,
              status: 2,
              content: <Intl id="newRequestSubmit" />,
              successCb: () => {
                setModalData({
                  open: true,
                  status: 2,
                  content: <Intl id="newRequestSubmit" />,
                  successCb: () => {
                    navigate(`/app/dashboard?requestor=true`);
                  },
                });
              },
            });
          })
          .catch((e) => {
            sendNotify({ msg: e.message, status: 3, show: true });
          })
          .catch((e) => {
            setModalData({
              ...modalData,
              status: 3,
              content: e.message,
            });
          });
        break;
      default:
        setModalData({ ...modalData, open: false });
        break;
    }
  }, [modalData, submitData, navigate]);

  const orderHandle = useCallback(() => {
    if (cartList.length > 0) {
      setModalData({
        open: true,
        status: 1,
        content: <Intl id="confirmOnboard" />,
      });

      let requestList = cartList.map((item) => {
        let selectedList = item.selectedList;
        let tmp = [...item.schema.fields];
        let list = [];
        const removeNotSelected = (data, parentIndex) => {
          for (let i = data.length - 1; i >= 0; i--) {
            let item = data[i];
            let index = i;
            let currIndex = parentIndex ? `${parentIndex}.${index}` : index;
            if (item.type === "RECORD") {
              removeNotSelected(item.fields, currIndex);
            } else {
              let policTagId = item?.policyTags?.names[0] || "";
              if (policTagId && !selectedList.includes(policTagId)) {
                let indexArr =
                  typeof currIndex === "string"
                    ? currIndex.split(".")
                    : [currIndex];
                let objPointer = null;
                list.push(currIndex);

                indexArr.forEach((tmpIndex, arrIndex) => {
                  if (!objPointer) {
                    objPointer = tmp[tmpIndex];
                    if (arrIndex === indexArr.length - 1) {
                      tmp.splice(index, 1);
                    }
                  } else if (arrIndex === indexArr.length - 1) {
                    objPointer.fields.splice(tmpIndex, 1);
                  } else {
                    objPointer = objPointer.fields[tmpIndex];
                  }
                });
              }
            }
          }
        };
        removeNotSelected(item.schema.fields);
        return {
          form_id: GET_ACCESS_FORM_ID,
          form_field_values_dict: {
            u1: item?.tableReference.projectId,
            d15: selectedUc,
            u3: item?.location,
            u4: item?.tableReference.datasetId,
            u5: item?.tableReference.tableId,
            u6: tmp,
          },
        };
      });

      setSubmitData({
        data: requestList,
      });
    }
  }, [selectedUc, cartList]);

  const closeModal = () => {
    setModalData({ ...modalData, open: false, cb: null });
  };

  const policyMap = useMemo(() => {
    let map = {};
    if (policys.length > 0) {
      policys.forEach((item) => {
        if (item.policy_tags_dict) {
          map = {
            ...map,
            ...item.policy_tags_dict,
          };
        }
      });
    }
    return map;
  }, [policys]);

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

  const addCartHandle = useCallback(
    (selectedList) => {
      if (tableData.seq != null) {
        let tmp = [...cartList];
        tmp.splice(tableData.seq, 1, {
          ...tableData,
          selectedList: selectedList,
        });
        setCartList(tmp);
      } else {
        let exist;
        cartList.forEach((item) => {
          if (
            item?.tableReference.projectId ===
              tableData?.tableReference.projectId &&
            item?.tableReference.datasetId ===
              tableData?.tableReference.datasetId &&
            item?.tableReference.tableId === tableData?.tableReference.tableId
          ) {
            exist = true;
          }
        });
        if (exist) {
          sendNotify({
            msg: "Have exist data resouce in cart list",
            status: 3,
            show: true,
          });
          return;
        }
        setCartList([
          ...cartList,
          {
            ...tableData,
            seq: cartList.length,
            selectedList: selectedList,
          },
        ]);
      }

      setTableData(null);
      setSelectedList([]);
    },
    [tableData, cartList]
  );

  const removeCartItem = useCallback(
    (seq) => {
      let tmp = [...cartList];
      tmp.splice(seq, 1);
      setCartList(tmp);
    },
    [cartList]
  );

  const showBackItem = useCallback((item) => {
    setTableData(item);
    setSelectedList(item.selectedList);
  }, []);

  useEffect(() => {
    if (searchQuery) {
      let postData = { ...searchQuery };
      setFormLoading(true);
      getTableSchema(postData)
        .then((res) => {
          setTableData(res.data);
          setFormLoading(false);
          setSelectedList([]);
        })
        .catch((e) => {
          sendNotify({ msg: e.message, status: 3, show: true });
        });
    }
  }, [searchQuery]);

  useEffect(() => {
    getPolicys()
      .then((res) => {
        setPolicys(res.data);
      })
      .catch((e) => {
        sendNotify({
          msg: "Get Policy tags error.",
          status: 3,
          show: true,
        });
      });
  }, []);

  useEffect(() => {
    getTags()
      .then((res) => {
        setTagTempalteList(res.data);
      })
      .catch((e) => {
        sendNotify({
          msg: "Get Policy tags error.",
          status: 3,
          show: true,
        });
      });
  }, []);

  useEffect(() => {
    getOnBoardDataForm()
      .then((res) => {
        if (res.data) {
          setOnBoardDataForm(res.data);
        }
      })
      .catch((e) => {
        sendNotify({
          msg: "Get Policy tags error.",
          status: 3,
          show: true,
        });
      });
  }, []);

  useEffect(() => {
    getUseCaseList().then((res) => {
      if (res.data) {
        setUseCaseList(
          res.data.map((item) => {
            return { label: item.usecase_name, value: item.usecase_name };
          })
        );
      }
    }, []);
  }, []);

  return (
    <div className={styles.dataDiscover}>
      <div className={styles.dataContainer}>
        <div className={styles.dataLeftPanel}>
          <ScrollBar>
            <div className={styles.leftPanelContainer}>
              <div className={styles.title}>
                <HeadLine>
                  <Intl id="getDataAccess" />
                </HeadLine>
              </div>
              <form
                className={styles.tableSearch}
                id="tableSearch"
                onSubmit={handleSubmit(submitHandle)}
              >
                <div className={styles.formOptions}>
                  {renderFormItem(tableForm)}
                </div>
                <div className={styles.buttonWrapper}>
                  <Button
                    className={styles.button}
                    type="submit"
                    variant="contained"
                  >
                    <Intl id="search" />
                  </Button>
                </div>
              </form>
              {formLoading && <Loading></Loading>}
              {!formLoading && tableList && (
                <>
                  <div className={styles.secondTitle}>
                    <Text type="title">
                      <Intl id="resourceDetail" />
                    </Text>
                  </div>
                  <ResourceDetail tableData={tableData} />
                  {tableData.tags && tableData.tags.length > 0 && (
                    <div>
                      <div className={styles.secondTitle}>
                        <Text type="title">Tags ({tableData.tags.length})</Text>
                      </div>
                      <div className={styles.tableTagList}>
                        {tableData.tags.map((tag, index) => {
                          return <TableTagDisplay key={index} tagData={tag} />;
                        })}
                      </div>
                    </div>
                  )}
                  <TableSchema
                    tableData={tableData}
                    tagTemplateList={tagTemplateList}
                    policyMap={policyMap}
                    addCartHandle={addCartHandle}
                    alreadySelected={selectedList}
                  />
                </>
              )}
            </div>
          </ScrollBar>
        </div>
        <div className={styles.dataRightPanel}>
          <div className={styles.rightPanelContent}>
            <div className={styles.rightPanelTitle}>
              <Text type="title">
                <Intl id="dataAccessCart" />
              </Text>
            </div>
            <div className={styles.cartView}>
              <ScrollBar>
                <div className={styles.cartContent}>
                  {cartList.length > 0 && (
                    <>
                      <div className={styles.cartItemList}>
                        <List>
                          {cartList.map((row, index) => (
                            <ListItem className={styles.cartItem} key={index}>
                              <div
                                className={styles.cartItemDetail}
                                onClick={() => {
                                  showBackItem(row);
                                }}
                              >
                                <ListItemText>
                                  {row.tableReference.tableId}
                                </ListItemText>
                                <ListItemText
                                  className={styles.columnLengh}
                                >{`${row.schema.fields.length} columns`}</ListItemText>
                              </div>
                              <Delete
                                onClick={() => {
                                  removeCartItem(index);
                                }}
                              />
                            </ListItem>
                          ))}
                        </List>
                      </div>
                      <div className={styles.selectUseCase}>
                        <Text type="subTitle">
                          <Intl id="selectedUc" />
                        </Text>
                      </div>
                      <Select
                        value={selectedUc}
                        options={useCaseList}
                        onChange={(value) => {
                          setSelectedUc(value);
                        }}
                      />
                    </>
                  )}
                </div>
              </ScrollBar>
            </div>
            <div className={styles.orderNow}>
              <Button
                filled
                onClick={orderHandle}
                disabled={cartList.length < 1}
                size="small"
              >
                <Intl id="submit" />
              </Button>
            </div>
          </div>
        </div>
      </div>

      <CallModal
        open={modalData.open}
        content={modalData.content}
        status={modalData.status}
        buttonClickHandle={buttonClickHandle}
        handleClose={closeModal}
        successCb={modalData.successCb}
      />
    </div>
  );
};

export default GetDataAccess;

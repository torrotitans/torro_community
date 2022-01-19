/* third lib*/
import React, { useState, useEffect, useMemo, useCallback } from "react";
import { FormattedMessage as Intl } from "react-intl";
import { useForm, useWatch } from "react-hook-form";
import ScrollBar from "react-perfect-scrollbar";

/* material-ui */
import Paper from "@material-ui/core/Paper";
import TablePagination from "@material-ui/core/TablePagination";
import Checkbox from "@material-ui/core/Checkbox";
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
import {
  getUseCaseList,
  getOnBoardDataForm,
  getTableSchema,
  getPolicys,
  getTags,
  raiseFormRequestList,
} from "@lib/api";
import { sendNotify } from "src/utils/systerm-error";
import { openTips } from "src/utils/systemTips";
import {
  Table,
  TableBody,
  TableContainer,
  TableHead,
  TableRow,
  TableCell,
} from "@basics/Table";
import TableTagDisplay from "@comp/TableTag";
import Select from "@basics/Select";

const GET_ACCESS_FORM_ID = 108;

const GetDataAccess = () => {
  const { handleSubmit, control, register } = useForm(); // initialise the hook
  const resourceType = useWatch({
    control,
    name: "resourceType",
    defaultValue: "GCP",
  });

  const [formLoading, setFormLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState();
  const [tableData, setTableData] = useState(null);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [policys, setPolicys] = useState([]);
  const [selectedList, setSelectedList] = useState([]);
  const [cartList, setCartList] = useState([]);
  const [tagTemplateList, setTagTempalteList] = useState([]);
  const [submitData, setSubmitData] = useState(null);
  const [onBoardDataForm, setOnBoardDataForm] = useState(null);
  const [useCaseList, setUseCaseList] = useState([]);
  const [selectedUc, setSelectedUc] = useState("");

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

  const filterTableList = useMemo(() => {
    if (!tableList) {
      return [];
    }
    let tmpList = tableList;
    return tmpList.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage);
  }, [tableList, page, rowsPerPage]);

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

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
            console.log(res);
            setModalData({
              open: true,
              status: 2,
              content: <Intl id="newRequestSubmit" />,
              successCb: () => {
                setModalData({
                  open: false,
                  status: 2,
                  content: <Intl id="newRequestSubmit" />,
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
  }, [modalData, submitData]);

  const orderHandle = useCallback(() => {
    if (cartList.length > 0) {
      setModalData({
        open: true,
        status: 1,
        content: <Intl id="confirmOnboard" />,
      });

      let requestList = cartList.map((item) => {
        return {
          form_id: GET_ACCESS_FORM_ID,
          form_field_values_dict: {
            u1: item?.tableReference.projectId,
            d15: selectedUc,
            u3: item?.location,
            u4: item?.tableReference.datasetId,
            u5: item?.tableReference.tableId,
            u6: item?.selectedColumns,
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

  const policMap = useMemo(() => {
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

  const tagTemplateMap = useMemo(() => {
    let map = {};
    tagTemplateList.forEach((item) => {
      map[item.tag_template_form_id] = item.display_name;
    });
    return map;
  }, [tagTemplateList]);

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

  const isSelectedAll = useMemo(() => {
    if (!selectedList || !tableList) {
      return false;
    }
    return selectedList.length === tableList.length;
  }, [selectedList, tableList]);

  const onSelectAllClick = useCallback(() => {
    if (isSelectedAll) {
      setSelectedList([]);
    } else {
      let tmp = tableList.map((item, index) => {
        return index;
      });
      setSelectedList(tmp);
    }
  }, [tableList, isSelectedAll]);

  const isSelected = useCallback(
    (index) => {
      let calcIndex = page * rowsPerPage + index;
      return selectedList.includes(calcIndex);
    },
    [selectedList, page, rowsPerPage]
  );

  const onSelect = useCallback(
    (index) => {
      let calcIndex = page * rowsPerPage + index;
      if (!selectedList.includes(calcIndex)) {
        let tmp = [...selectedList, calcIndex];
        setSelectedList(tmp);
      } else {
        let currentIndex = selectedList.indexOf(calcIndex);
        let tmp = [...selectedList];
        tmp.splice(currentIndex, 1);
        setSelectedList(tmp);
      }
    },
    [selectedList, page, rowsPerPage]
  );

  const enableAddTagBtn = useMemo(() => {
    return selectedList.length > 0;
  }, [selectedList]);

  const addCartHandle = useCallback(() => {
    if (!enableAddTagBtn) {
      return;
    }
    let columns = tableData.schema.fields.filter((item, index) => {
      return selectedList.includes(index);
    });
    if (tableData.seq != null) {
      let tmp = [...cartList];
      tmp.splice(tableData.seq, 1, {
        ...tableData,
        selectedColumns: columns,
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
          selectedColumns: columns,
          seq: cartList.length,
        },
      ]);
    }

    setTableData(null);
    setSelectedList([]);
  }, [selectedList, enableAddTagBtn, tableData, cartList]);

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
    let selectedField = item.selectedColumns.map((item) => item.name);
    let selectedIndex = [];
    item.schema.fields.forEach((item, index) => {
      if (selectedField.includes(item.name)) {
        selectedIndex.push(index);
      }
    });
    setSelectedList(selectedIndex);
  }, []);

  useEffect(() => {
    if (searchQuery) {
      let postData = { ...searchQuery };
      setFormLoading(true);
      getTableSchema(postData)
        .then((res) => {
          setTableData(res.data);
          setFormLoading(false);
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
                  <div className={styles.resourceDetail}>
                    <div className={styles.detailItem}>
                      <div className={styles.detailLabel}>Name</div>
                      <div className={styles.detailValue}>
                        {tableData.tableReference.tableId}
                      </div>
                    </div>
                    <div className={styles.detailItem}>
                      <div className={styles.detailLabel}>Type</div>
                      <div className={styles.detailValue}>{tableData.type}</div>
                    </div>
                    <div className={styles.detailItem}>
                      <div className={styles.detailLabel}>Location</div>
                      <div className={styles.detailValue}>
                        {tableData.location}
                      </div>
                    </div>
                    <div className={styles.detailItem}>
                      <div className={styles.detailLabel}>Description</div>
                      <div className={styles.detailValue}>
                        {tableData.description}
                      </div>
                    </div>
                    <div className={styles.detailItem}>
                      <div className={styles.detailLabel}>CreationTime</div>
                      <div className={styles.detailValue}>
                        {tableData.creationTime}
                      </div>
                    </div>
                  </div>
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
                  <div className={styles.filter}>
                    <Button
                      filled
                      onClick={addCartHandle}
                      disabled={!enableAddTagBtn}
                    >
                      <Intl id="addToCart" />
                    </Button>
                  </div>
                  <TableContainer component={Paper}>
                    <Table aria-label="simple table">
                      <TableHead>
                        <TableRow>
                          <TableCell align="center">
                            <div className={styles.selectAll}>
                              <Checkbox
                                color="primary"
                                checked={isSelectedAll}
                                onChange={onSelectAllClick}
                              />
                            </div>
                          </TableCell>
                          <TableCell align="center">
                            <Text type="subTitle">
                              <Intl id="fieldName" />
                            </Text>
                          </TableCell>
                          <TableCell align="center">
                            <Text type="subTitle">
                              <Intl id="type" />
                            </Text>
                          </TableCell>
                          <TableCell align="center">
                            <Text type="subTitle">
                              <Intl id="mode" />
                            </Text>
                          </TableCell>
                          <TableCell align="center">
                            <Text type="subTitle">
                              <Intl id="ColumnTags" />
                            </Text>
                          </TableCell>
                          <TableCell align="center">
                            <Text type="subTitle">
                              <Intl id="policyTagOr" />
                            </Text>
                          </TableCell>
                          <TableCell align="center" width="25%">
                            <Text type="subTitle">
                              <Intl id="description" />
                            </Text>
                          </TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {filterTableList.map((row, rowIndex) => (
                          <TableRow key={rowIndex}>
                            <TableCell align="center">
                              <Checkbox
                                color="primary"
                                checked={isSelected(rowIndex)}
                                onChange={() => {
                                  onSelect(rowIndex);
                                }}
                              />
                            </TableCell>
                            <TableCell align="center">{row.name}</TableCell>
                            <TableCell align="center">{row.type}</TableCell>
                            <TableCell align="center">{row.mode}</TableCell>
                            <TableCell align="center">
                              {row.tags &&
                                row.tags.map((item, index) => {
                                  return (
                                    <div key={index}>
                                      {tagTemplateMap[
                                        item.tag_template_form_id
                                      ] && (
                                        <div
                                          className={styles.policyTag}
                                          key={index}
                                          onClick={() => {
                                            openTips({
                                              style: 1,
                                              tagData: item,
                                            });
                                          }}
                                        >
                                          <span className={styles.policyName}>
                                            {
                                              tagTemplateMap[
                                                item.tag_template_form_id
                                              ]
                                            }
                                          </span>
                                        </div>
                                      )}
                                    </div>
                                  );
                                })}
                            </TableCell>
                            <TableCell align="center">
                              {row.policyTags &&
                                row.policyTags.names.map((item, index) => {
                                  return (
                                    <div key={index}>
                                      {policMap[item] && (
                                        <div
                                          className={styles.policyTag}
                                          key={index}
                                        >
                                          <span className={styles.policyName}>
                                            {
                                              policMap[item]
                                                .taxonomy_display_name
                                            }{" "}
                                            :
                                          </span>
                                          <span
                                            className={styles.policytagname}
                                          >
                                            {policMap[item].display_name}
                                          </span>
                                        </div>
                                      )}
                                    </div>
                                  );
                                })}
                            </TableCell>
                            <TableCell align="center">
                              {row.description}
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </TableContainer>
                  <TablePagination
                    rowsPerPageOptions={[5, 10, 25]}
                    component="div"
                    count={tableList.length}
                    rowsPerPage={rowsPerPage}
                    page={page}
                    onChangePage={handleChangePage}
                    onChangeRowsPerPage={handleChangeRowsPerPage}
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
                                >{`${row.selectedColumns.length} columns`}</ListItemText>
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
      />
    </div>
  );
};

export default GetDataAccess;

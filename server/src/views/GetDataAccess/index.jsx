/* third lib*/
import React, { useState, useEffect, useMemo, useCallback } from "react";
import { FormattedMessage as Intl } from "react-intl";
import { useForm, useWatch } from "react-hook-form";
import ScrollBar from "react-perfect-scrollbar";
import cn from "classnames";

/* material-ui */
import Paper from "@material-ui/core/Paper";
import TablePagination from "@material-ui/core/TablePagination";
import Checkbox from "@material-ui/core/Checkbox";
import List from "@material-ui/core/List";
import ListItem from "@material-ui/core/ListItem";
import ListItemText from "@material-ui/core/ListItemText";

/* local components & methods */
import styles from "./styles.module.scss";
import FormItem from "@comp/FormItem";
import HeadLine from "@comp/HeadLine";
import Text from "@comp/Text";
import CallModal from "@comp/CallModal";
import Loading from "src/icons/Loading";
import { getTableSchema, getPolicys, getTags } from "@lib/api";
import Button from "@comp/Button";
import { sendNotify } from "src/utils/systerm-error";
import {
  Table,
  TableBody,
  TableContainer,
  TableHead,
  TableRow,
  TableCell,
} from "@comp/Table";

const GetDataAccess = () => {
  const { handleSubmit, control, register, reset } = useForm(); // initialise the hook
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

  const tableForm = useMemo(() => {
    let gcrFlag = resourceType === "GCP";

    return [
      {
        default: "Use case1",
        des: "staff name",
        edit: 1,
        id: "u2",
        label: "Use case name",
        options: [
          {
            label: "Use case1",
            value: "Use case1",
          },
          {
            label: "Use case2",
            value: "Use case2",
          },
        ],
        placeholder: "placeholder",
        style: 2,
      },
      {
        default: "GCP",
        des: "Resource type",
        edit: 1,
        id: "resourceType",
        label: "Resource type",
        options: [{ label: "GCP" }, { label: "Hive" }],
        placeholder: "Resource type",
        style: 8,
        required: true,
      },
      {
        default: "",
        des: gcrFlag ? "GCP Project" : "Service name",
        edit: 1,
        id: "projectId",
        label: gcrFlag ? "GCP Project" : "Service name",
        options: [],
        placeholder: gcrFlag ? "GCP Project" : "Service name",
        style: 3,
        required: true,
      },
      {
        default: "",
        des: gcrFlag ? "Dataset" : "Database",
        edit: 1,
        id: "datasetName",
        label: gcrFlag ? "Dataset" : "Database",
        options: [],
        placeholder: gcrFlag ? "Dataset" : "Database",
        style: 3,
        required: true,
      },
      {
        default: "",
        des: "Table",
        edit: 1,
        id: "tableName",
        label: "Table",
        options: [],
        placeholder: "Table",
        style: 3,
        required: true,
      },
    ];
  }, [resourceType]);

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
    setCartList([
      ...cartList,
      { requestName: tableData.tableReference.tableId, columns: columns },
    ]);
  }, [selectedList, enableAddTagBtn, tableData, cartList]);

  useEffect(() => {
    if (searchQuery) {
      setFormLoading(true);
      getTableSchema(searchQuery)
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

  return (
    <div className={styles.dataDiscover}>
      <div className={styles.dataContainer}>
        <div className={styles.dataLeftPanel}>
          <ScrollBar>
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
                                          {policMap[item].taxonomy_display_name}{" "}
                                          :
                                        </span>
                                        <span className={styles.policytagname}>
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
                  <div className={styles.cartItemList}>
                    <List>
                      {cartList.map((row, index) => (
                        <ListItem className={styles.cartItem} key={index}>
                          <ListItemText>{row.requestName}</ListItemText>
                          <ListItemText>{`${row.columns.length} columns`}</ListItemText>
                        </ListItem>
                      ))}
                    </List>
                  </div>
                </div>
              </ScrollBar>
            </div>
            <div className={styles.orderNow}>
              <Button filled onClick={() => {}}>
                <Intl id="orderNow" />
              </Button>
            </div>
          </div>
        </div>
      </div>

      <CallModal
        open={modalData.open}
        content={modalData.content}
        status={modalData.status}
        buttonClickHandle={modalData.cb}
        handleClose={closeModal}
      />
    </div>
  );
};

export default GetDataAccess;

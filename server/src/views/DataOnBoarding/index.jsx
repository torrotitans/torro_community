/* third lib*/
import React, { useState, useEffect, useMemo, useCallback } from "react";
import { FormattedMessage as Intl } from "react-intl";
import { useForm, useWatch } from "react-hook-form";
import ScrollBar from "react-perfect-scrollbar";

/* material-ui */
import Paper from "@material-ui/core/Paper";
import TablePagination from "@material-ui/core/TablePagination";
import Checkbox from "@material-ui/core/Checkbox";
import Delete from "@material-ui/icons/Close";

/* local components & methods */
import styles from "./styles.module.scss";
/* local components & methods */
import FormItem from "@comp/FormItem";
import HeadLine from "@comp/HeadLine";
import Text from "@comp/Text";
import CallModal from "@comp/CallModal";
import Loading from "src/icons/Loading";
import DesignPanel from "./DesignPanel";
import TableTagDisplay from "./TableTagDisplay";
import { getTableSchema, getTags, getPolicys } from "@lib/api";
import { SUCCESS } from "src/lib/data/callStatus";
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

const DataOnBoarding = () => {
  const { handleSubmit, control, register, formState } = useForm(); // initialise the hook
  const resourceType = useWatch({
    control,
    name: "resourceType",
    defaultValue: "GCP",
  });

  const [policys, setPolicys] = useState([]);
  const [formLoading, setFormLoading] = useState(false);
  const [addState, setAddState] = useState(false);
  const [searchQuery, setSearchQuery] = useState();
  const [tableData, setTableData] = useState(null);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [selectedList, setSelectedList] = useState([]);
  const [type, setType] = useState(0);
  const [tagTemplateList, setTagTempalteList] = useState([]);

  const [modalData, setModalData] = useState({
    open: false,
    status: 0,
    content: "",
    cb: null,
  });

  const tableForm = useMemo(() => {
    let gcrFlag = resourceType === "GCP";

    return [
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

  const tableList = useMemo(() => {
    return tableData?.schema?.fields;
  }, [tableData]);

  const tagTemplateMap = useMemo(() => {
    let map = {};
    tagTemplateList.forEach((item) => {
      map[item.tag_template_form_id] = item.display_name;
    });
    return map;
  }, [tagTemplateList]);

  const filterTableList = useMemo(() => {
    if (!tableList) {
      return [];
    }
    let tmpList = tableList;
    return tmpList.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage);
  }, [tableList, page, rowsPerPage]);

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

  const closeModal = () => {
    setModalData({ ...modalData, open: false, cb: null });
  };

  const handleClose = (e) => {
    if (
      e &&
      e.target &&
      e.target.nodeName === "BODY" &&
      e.target.style.overflow === "hidden"
    ) {
      return;
    }
    setAddState(false);
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

  const selectedItem = useMemo(() => {
    if (!tableList) {
      return [];
    }
    return tableList.filter((item, index) => {
      return selectedList.includes(index);
    });
  }, [selectedList, tableList]);

  const handleApply = useCallback(
    (data, type) => {
      if (type === "POLICY") {
        let tmp = [...tableList];
        selectedList.forEach((item, index) => {
          tmp[item].policyTags = { names: data };
        });
        let tmpData = JSON.parse(JSON.stringify(tableData));
        tmpData.schema.fields = tmp;
        setTableData(tmpData);
        setAddState(false);
        setSelectedList([]);
      } else if (type === "TABLETAG") {
        let tmpData = JSON.parse(JSON.stringify(tableData));
        if (!tmpData.tags) {
          tmpData.tags = [];
        }
        tmpData.tags.push(data);
        setTableData(tmpData);
      } else if (type === "COLUMNTAGS") {
        let tmp = [...tableList];
        selectedList.forEach((item, index) => {
          if (!tmp[item].tags) {
            tmp[item].tags = [];
          }
          tmp[item].tags.push(data);
        });
        let tmpData = JSON.parse(JSON.stringify(tableData));
        tmpData.schema.fields = tmp;
        setTableData(tmpData);
        setAddState(false);
        setSelectedList([]);
      }
    },
    [selectedList, tableList, tableData]
  );

  const handleDeletePolicyTag = useCallback(
    (tag, recordIndex) => {
      let tmp = [...tableList];
      let calcIndex = page * rowsPerPage + recordIndex;
      let tagList = tmp[calcIndex].policyTags.names;
      let tagIndex = tagList.indexOf(tag);
      tagList.splice(tagIndex, 1);
      tmp[calcIndex].policyTags.names = tagList;

      let tmpData = JSON.parse(JSON.stringify(tableData));
      tmpData.schema.fields = tmp;
      setTableData(tmpData);
    },
    [tableData, tableList, page, rowsPerPage]
  );

  const handleDeleteTag = useCallback(
    (tag, recordIndex) => {
      let tmp = [...tableList];
      let calcIndex = page * rowsPerPage + recordIndex;
      let tagList = tmp[calcIndex].tags;
      let tagIndex = tagList.indexOf(tag);
      tagList.splice(tagIndex, 1);
      tmp[calcIndex].tags = tagList;
      let tmpData = JSON.parse(JSON.stringify(tableData));
      tmpData.schema.fields = tmp;
      setTableData(tmpData);
    },
    [tableData, tableList, page, rowsPerPage]
  );

  useEffect(() => {
    if (searchQuery) {
      setFormLoading(true);
      getTableSchema(searchQuery)
        .then((res) => {
          if (res.data) {
            setTableData(res.data);
            setFormLoading(false);
          }
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
    <div className={styles.dataOnboarding}>
      <ScrollBar>
        <div className={styles.dataContainer}>
          <div className={styles.title}>
            <HeadLine>
              <Intl id="dataOnboarding" />
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
          {!formLoading && tableData && (
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
                  <div className={styles.detailValue}>{tableData.location}</div>
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
                <TableTagDisplay tags={tableData.tags} />
              )}
              <div className={styles.filter}>
                <Button
                  filled
                  onClick={() => {
                    setType(1);
                    setAddState(true);
                  }}
                >
                  <Intl id="addTableTag" />
                </Button>
                <Button
                  filled
                  onClick={() => {
                    if (enableAddTagBtn) {
                      setType(2);
                      setAddState(true);
                    }
                  }}
                  disabled={!enableAddTagBtn}
                >
                  <Intl id="addColumnTag" />
                </Button>
                <Button
                  filled
                  onClick={() => {
                    if (enableAddTagBtn) {
                      setType(0);
                      setAddState(true);
                    }
                  }}
                  disabled={!enableAddTagBtn}
                >
                  <Intl id="addPolicyTag" />
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
                                      <span className={styles.delete}>
                                        <Delete
                                          onClick={() => {
                                            handleDeleteTag(item, rowIndex);
                                          }}
                                        />
                                      </span>
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
                                      <span className={styles.delete}>
                                        <Delete
                                          onClick={() => {
                                            handleDeletePolicyTag(
                                              item,
                                              rowIndex
                                            );
                                          }}
                                        />
                                      </span>
                                      <span className={styles.policyName}>
                                        {policMap[item].taxonomy_display_name} :
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
                        <TableCell align="center">{row.description}</TableCell>
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
        {addState && (
          <DesignPanel
            open={addState}
            handleClose={handleClose}
            handleApply={handleApply}
            tagTemplateList={tagTemplateList}
            type={type}
          />
        )}
        <CallModal
          open={modalData.open}
          content={modalData.content}
          status={modalData.status}
          buttonClickHandle={modalData.cb}
          handleClose={closeModal}
        />
      </ScrollBar>
    </div>
  );
};

export default DataOnBoarding;

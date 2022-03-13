/* third lib*/
import React, { useState, useEffect, useMemo, useCallback } from "react";
import { FormattedMessage as Intl } from "react-intl";
import { useForm, useWatch } from "react-hook-form";
import ScrollBar from "react-perfect-scrollbar";
import { useNavigate } from "react-router-dom";

/* material-ui */
import Paper from "@material-ui/core/Paper";
import TablePagination from "@material-ui/core/TablePagination";
import Checkbox from "@material-ui/core/Checkbox";
import Delete from "@material-ui/icons/Close";

/* local components & methods */
import styles from "./styles.module.scss";
/* local components & methods */
import FormItem from "@comp/FormItem";
import HeadLine from "@basics/HeadLine";
import Text from "@basics/Text";
import CallModal from "@basics/CallModal";
import Loading from "@assets/icons/Loading";
import DesignPanel from "./DesignPanel";
import TableTagDisplay from "@comp/TableTag";
import ResourceDetail from "@comp/ResourceDetail";
import {
  getOnBoardDataForm,
  getRequiredTableTag,
  getTableSchema,
  getTags,
  getPolicys,
  raiseFormRequest,
} from "@lib/api";
import { SUCCESS } from "src/lib/data/callStatus";
import Button from "@basics/Button";
import { sendNotify } from "src/utils/systerm-error";

import {
  Table,
  TableBody,
  TableContainer,
  TableHead,
  TableRow,
  TableCell,
} from "@basics/Table";

const DataOnBoarding = () => {
  const { handleSubmit, control, register } = useForm(); // initialise the hook
  const navigate = useNavigate();
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
  const [submitData, setSubmitData] = useState(null);
  const [onBoardDataForm, setOnBoardDataForm] = useState(null);
  const [requiredTableTag, setRequiredTableTag] = useState([]);

  const [modalData, setModalData] = useState({
    open: false,
    status: 0,
    content: "",
    cb: null,
  });

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

  const tableForm = useMemo(() => {
    if (!onBoardDataForm) {
      return [];
    }
    return resourceType === "GCP" ? onBoardDataForm.gcp : onBoardDataForm.hive;
  }, [resourceType, onBoardDataForm]);

  const tableList = useMemo(() => {
    return tableData?.schema?.fields;
  }, [tableData]);

  const tableTags = useMemo(() => {
    return tableData?.tags || [];
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

  const isSelectedAll = useMemo(() => {
    if (!selectedList || !tableList) {
      return false;
    }
    return selectedList.length === tableList.length;
  }, [selectedList, tableList]);

  const enableAddTagBtn = useMemo(() => {
    return selectedList.length > 0;
  }, [selectedList]);

  const checkedTagList = useMemo(() => {
    if (type === 1) {
      return tableTags;
    }
    if (tableList && type === 2 && selectedList.length === 1) {
      return tableList[selectedList[0]].tags;
    }

    return [];
  }, [selectedList, tableList, type, tableTags]);

  const haveTableTag = useMemo(() => {
    return tableData?.tags.length > 0;
  }, [tableData]);

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
        tmpData.tags = data;
        setAddState(false);
        setTableData(tmpData);
      } else if (type === "COLUMNTAGS") {
        let tmp = [...tableList];
        selectedList.forEach((item, index) => {
          if (!tmp[item].tags) {
            tmp[item].tags = [];
          }
          tmp[item].tags = data;
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
      let tmp = JSON.parse(JSON.stringify(tableList));
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

  const buttonClickHandle = useCallback(() => {
    let apiCall = raiseFormRequest;
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
                content: <Intl id="newRequestSubmit" />,
                successCb: () => {
                  navigate(`/app/requestDetail?id=${res.data.id}`);
                },
              });
            }
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

  const onBoardHandle = useCallback(
    (data) => {
      let avaliable = true;

      tableData.tags.forEach((item) => {
        if (!item.data) {
          sendNotify({
            msg: "Table tag have empty value, please check your input.",
            status: 3,
            show: true,
          });
          avaliable = false;
        }
      });

      if (avaliable) {
        setModalData({
          open: true,
          status: 1,
          content: <Intl id="confirmOnboard" />,
        });
        setSubmitData({
          form_id: "107",
          form_field_values_dict: {
            u1: tableData?.tableReference.projectId,
            u2: tableData?.location,
            u3: tableData?.tableReference.datasetId,
            u4: tableData?.tableReference.tableId,
            u5: tableData?.schema?.fields,
            u6: tableData?.tags,
          },
        });
      }
    },
    [tableData]
  );

  useEffect(() => {
    if (searchQuery) {
      setFormLoading(true);
      getTableSchema(searchQuery)
        .then((res) => {
          if (res.data) {
            let tmpData = res.data;

            /* deal with require Table Tag */
            tmpData.tags = tmpData?.tags || [];
            let tagFormIdList = [];
            let concatList = [];

            tmpData.tags = tmpData.tags.map((item) => {
              tagFormIdList.push(item.tag_template_form_id);
              if (requiredTableTag.includes(item.tag_template_form_id)) {
                return { ...item, required: true };
              } else {
                return item;
              }
            });

            requiredTableTag.forEach((id) => {
              if (!tagFormIdList.includes(id)) {
                concatList.push({
                  tag_template_form_id: id,
                  data: null,
                  required: true,
                });
              }
            });
            tmpData.tags = concatList.concat(tmpData.tags);
            setTableData(tmpData);
            setFormLoading(false);
          }
        })
        .catch((e) => {
          sendNotify({ msg: e.message, status: 3, show: true });
        });
    }
  }, [searchQuery, requiredTableTag]);

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
    getRequiredTableTag()
      .then((res) => {
        if (res.data) {
          setRequiredTableTag(res.data);
        }
      })
      .catch((e) => {
        sendNotify({
          msg: "System error",
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
              <ResourceDetail tableData={tableData} />
              {tableTags && tableTags.length > 0 && (
                <div>
                  <div className={styles.secondTitle}>
                    <Text type="title">Tags ({tableTags.length})</Text>
                  </div>
                  <div className={styles.tableTagList}>
                    {tableTags.map((tag, index) => {
                      return <TableTagDisplay key={index} tagData={tag} />;
                    })}
                  </div>
                </div>
              )}
              <div className={styles.filter}>
                <Button
                  filled
                  onClick={() => {
                    setType(1);
                    setAddState(true);
                  }}
                >
                  {!haveTableTag ? (
                    <Intl id="addTableTag" />
                  ) : (
                    <Intl id="modifyTableTag" />
                  )}
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
                                      className={styles.columnTag}
                                      key={index}
                                      onClick={(e) => {
                                        e.stopPropagation();
                                        let calcIndex =
                                          page * rowsPerPage + rowIndex;
                                        setSelectedList([calcIndex]);
                                        setType(2);
                                        setAddState(true);
                                      }}
                                    >
                                      <span className={styles.delete}>
                                        <Delete
                                          onClick={(e) => {
                                            e.stopPropagation();
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

              <div className={styles.buttonWrapper}>
                <Button
                  className={styles.button}
                  onClick={onBoardHandle}
                  variant="contained"
                >
                  <Intl id="submit" />
                </Button>
              </div>
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
            checkedTagList={checkedTagList}
          />
        )}
        <CallModal
          open={modalData.open}
          content={modalData.content}
          status={modalData.status}
          successCb={modalData.successCb}
          buttonClickHandle={buttonClickHandle}
          handleClose={closeModal}
        />
      </ScrollBar>
    </div>
  );
};

export default DataOnBoarding;

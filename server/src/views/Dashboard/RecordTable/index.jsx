// third lib
import React, { useState, useEffect, useMemo } from "react";
import { FormattedMessage as Intl } from "react-intl";
import Scrollbar from "react-perfect-scrollbar";
import cn from "classnames";
import { useNavigate } from "react-router-dom";

/* material-ui */
import VisibilityIcon from "@material-ui/icons/Visibility";
import Paper from "@material-ui/core/Paper";
import TablePagination from "@material-ui/core/TablePagination";
import Checkbox from "@material-ui/core/Checkbox";

/* local components & methods */
import styles from "./styles.module.scss";
import Text from "@basics/Text";
import Loading from "@assets/icons/Loading";
import Search from "@basics/Search";
import Filter from "@comp/FilterPanel";
import {
  Table,
  TableBody,
  TableContainer,
  TableHead,
  TableRow,
  TableCell,
} from "@basics/Table";
import { getRequestData, getFilterOptions } from "@lib/api";
import { sendNotify } from "src/utils/systerm-error";
import { useCallback } from "react";
import Button from "@basics/Button";
import { useGlobalContext } from "src/context";
import { covertToHKTime } from "src/utils/timeFormat";

const tabList = [
  { label: "Pending requests", value: [[0, "="]], style: "pending" },
  { label: "Rejected requests", value: [[1, "="]], style: "reject" },
  {
    label: "Approved requests",
    value: [[3, "="], [4, "="], "OR"],
    style: "approved",
  },
  {
    label: "Close requests",
    value: [[2, "="], [5, "="], [6, "="], "OR"],
    style: "close",
  },
];

const RecordTable = ({ approved }) => {
  const { authContext, formListContext } = useGlobalContext();
  const navigate = useNavigate();

  const [formLoading, setFormLoading] = useState(true);
  const [tableList, setTableList] = useState([]);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);

  const [status, setStatus] = useState([[0, "="]]);
  const [tabIndex, setTabIndex] = useState(0);
  const [ticketId, setTicketId] = useState();
  const [filterOptions, setFilterOption] = useState({
    requestor: [],
    form: [],
  });
  const [selectedList, setSelectedList] = useState([]);
  const [condition, setCondition] = useState({});

  const formList = useMemo(() => {
    return formListContext.list;
  }, [formListContext]);

  const formIdMap = useMemo(() => {
    let map = {};
    formList.forEach((item) => {
      map[item.id] = item.title;
    });
    return map;
  }, [formList]);

  const filterTableList = useMemo(() => {
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

  const filterRecord = useCallback(
    (data, sta) => {
      setFormLoading(true);
      let postData = {};
      if (approved) {
        postData.approverView = true;
      }

      // filterCondition
      let con = data ? data : condition;
      if (con.form_id) postData.form_id = [[con.form_id, "="]];
      if (con.creator_id) postData.creator_id = [[con.creator_id, "="]];
      if (con.from || con.to) {
        postData.create_time = [];
        if (con.from) {
          postData.create_time.push([con.from, ">"]);
        }
        if (con.to) {
          postData.create_time.push([con.to, "<"]);
        }
        if (con.from && con.to) {
          postData.create_time.push("AND");
        }
      }

      // filter by status
      let currentStatus = sta ? sta : status;
      postData.form_status = currentStatus;

      // filter by ticket Id
      if (ticketId) {
        postData.id = [[ticketId, "="]];
      }

      getRequestData(postData)
        .then((res) => {
          setTableList(res.data);
          setFormLoading(false);
        })
        .catch((e) => {
          sendNotify({ msg: e.message, status: 3, show: true });
        });
    },
    [condition, approved, status, ticketId]
  );

  const tabClickHandle = useCallback(
    (value, index) => {
      setStatus(value);
      setTabIndex(index);
      setTicketId("");
      setCondition({});
      filterRecord({}, value);
    },
    [filterRecord]
  );

  const handleApply = useCallback(
    (data) => {
      setCondition(data);
      filterRecord(data);
    },
    [filterRecord]
  );

  const handleReset = useCallback(() => {
    setCondition({});
    filterRecord({});
  }, [filterRecord]);

  const handleSearch = useCallback(() => {
    filterRecord();
  }, [filterRecord]);

  const isSelectedAll = useMemo(() => {
    if (!selectedList || !tableList) {
      return false;
    }
    return selectedList.length > 0 && selectedList.length === tableList.length;
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

  useEffect(() => {
    let postData = {
      form_status: [[0, "="]],
    };
    if (approved) {
      postData.approverView = true;
    }
    setFormLoading(true);
    Promise.all([getFilterOptions(), getRequestData(postData)])
      .then((res) => {
        let res1 = res[0];
        let res2 = res[1];
        if (res1.data && res2.data) {
          setFilterOption(res1.data.data);
          setTableList(res2.data);
          setFormLoading(false);
        }
      })
      .catch((e) => {
        sendNotify({ msg: e.message, status: 3, show: true });
      });
  }, [approved, authContext.userId]);

  return (
    <div className={styles.tableContainer}>
      <div className={styles.statusTab}>
        {tabList.map((item, index) => {
          return (
            <Button
              key={item.label}
              onClick={() => {
                tabClickHandle(item.value, index);
                setPage(0);
                setSelectedList([]);
              }}
              className={cn(styles.statusTabItem, {
                [styles["active"]]: index === tabIndex,
                [styles[item.style]]: true,
              })}
              size="small"
            >
              <Text>{item.label}</Text>
            </Button>
          );
        })}
      </div>
      <div className={styles.tableData}>
        <Scrollbar>
          {formLoading && <Loading></Loading>}
          {!formLoading && (
            <div className={styles.tableContent}>
              <div className={styles.toolBar}>
                <div className={styles.filterBox}>
                  <div className={styles.filterItem}>
                    <Search
                      value={ticketId}
                      placeholder="Seach by ticket ID"
                      onChange={(value) => {
                        setTicketId(value);
                      }}
                      handleSearch={handleSearch}
                    />
                  </div>
                  <div className={styles.filterItem}>
                    <Filter
                      options={filterOptions}
                      handleApply={handleApply}
                      approved={approved}
                      condition={condition}
                      handleReset={handleReset}
                    />
                  </div>
                </div>
              </div>

              <div className={cn(styles.table, styles["table" + tabIndex])}>
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
                              className={styles.checkbox}
                            />
                          </div>
                        </TableCell>
                        <TableCell align="center">
                          <Text type="subTitle">
                            <Intl id="requestId" />
                          </Text>
                        </TableCell>
                        <TableCell align="center">
                          <Text type="subTitle">
                            <Intl id="useCase" />
                          </Text>
                        </TableCell>
                        {approved && (
                          <TableCell align="center">
                            <Text type="subTitle">
                              <Intl id="requestor" />
                            </Text>
                          </TableCell>
                        )}
                        <TableCell align="center">
                          <Text type="subTitle">
                            <Intl id="associatedForm" />
                          </Text>
                        </TableCell>
                        <TableCell align="center">
                          <Text type="subTitle">
                            <Intl id="createtime" />
                          </Text>
                        </TableCell>
                        <TableCell align="center">
                          <Text type="subTitle">
                            <Intl id="operation" />
                          </Text>
                        </TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {filterTableList.map((row, index) => (
                        <TableRow key={index}>
                          <TableCell align="center">
                            <Checkbox
                              color="primary"
                              checked={isSelected(index)}
                              className={styles.checkbox}
                              onChange={() => {
                                onSelect(index);
                              }}
                            />
                          </TableCell>
                          <TableCell align="center">{row.id}</TableCell>
                          <TableCell align="center">
                            {row["Use case"] || "-"}
                          </TableCell>
                          {approved && (
                            <TableCell align="center">
                              {row.creator_id}
                            </TableCell>
                          )}
                          <TableCell align="center">
                            {formIdMap[row.form_id] || "Unknown"}
                          </TableCell>
                          <TableCell align="center">
                            {covertToHKTime(row.create_time)}
                          </TableCell>
                          <TableCell align="center">
                            <div className={styles.operation}>
                              <VisibilityIcon
                                onClick={() => {
                                  if (approved) {
                                    navigate(`/app/approvalFlow?id=${row.id}`);
                                  } else {
                                    navigate(`/app/requestDetail?id=${row.id}`);
                                  }
                                }}
                              />
                            </div>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              </div>
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
                  onClick={() => {
                    if (selectedList.length < 1) {
                      return;
                    }
                    let selectedIdList = selectedList.map((selectedIndex) => {
                      return tableList[selectedIndex].id;
                    });

                    if (approved) {
                      navigate(
                        `/app/approvalFlow?idList=${selectedIdList.join("|")}`
                      );
                    } else {
                      navigate(
                        `/app/requestDetail?idList=${selectedIdList.join("|")}`
                      );
                    }
                  }}
                  variant="contained"
                  disabled={selectedList.length < 1}
                >
                  <Intl id="previewAll" />
                </Button>
              </div>
            </div>
          )}
        </Scrollbar>
      </div>
    </div>
  );
};

export default RecordTable;

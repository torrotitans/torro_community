/* third lib*/
import React, { useState, useEffect, useMemo } from "react";
import { FormattedMessage as Intl } from "react-intl";
import { useNavigate } from "react-router-dom";

/* material-ui */
import Delete from "@material-ui/icons/Delete";
import EditIcon from "@material-ui/icons/Edit";
import Paper from "@material-ui/core/Paper";
import TablePagination from "@material-ui/core/TablePagination";

/* local components & methods */
import {
  Table,
  TableBody,
  TableContainer,
  TableHead,
  TableRow,
  TableCell,
} from "@basics/Table";
import Select from "@basics/Select";
import styles from "./styles.module.scss";
import HeadLine from "@basics/HeadLine";
import Text from "@basics/Text";
import CallModal from "@basics/CallModal";
import Model from "@basics/Modal";
import Filter from "@comp/Filter";
import Loading from "@assets/icons/Loading";
import {
  getFormWorkflowData,
  postWorkflowData,
  deleteWorkflowData,
} from "@lib/api";
import { SUCCESS } from "src/lib/data/callStatus";
import Button from "@basics/Button";
import { sendNotify } from "src/utils/systerm-error";
import { useGlobalContext } from "src/context";
import { covertToHKTime } from "src/utils/timeFormat";
const TRIGGER = "Trigger";

const WorkflowManagement = () => {
  const { authContext, formListContext } = useGlobalContext();
  const navigate = useNavigate();

  const [formLoading, setFormLoading] = useState(true);
  const [tableList, setTableList] = useState([]);
  const [addModal, setAddModal] = useState(false);
  const [selectedForm, setSelectedForm] = useState("");
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [filterVal, setFilterVal] = useState("");

  const [modalData, setModalData] = useState({
    open: false,
    status: 0,
    content: "",
    cb: null,
  });

  const formList = useMemo(() => {
    return formListContext.userList;
  }, [formListContext]);

  const selectOpetion = useMemo(() => {
    return formList.map((item) => {
      return {
        label: item.title,
        value: item.id,
      };
    });
  }, [formList]);

  const filterTableList = useMemo(() => {
    let tmpList;
    if (filterVal) {
      tmpList = tableList.filter((item) => item.form_id === filterVal);
    } else {
      tmpList = tableList;
    }
    return tmpList.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage);
  }, [tableList, page, rowsPerPage, filterVal]);

  const addNewWorkFlow = (item, seq) => {
    setAddModal(false);
    setModalData({
      open: true,
      status: 1,
      content: <Intl id="confirmNewWorkflow" />,
      cb: () => {
        setModalData({
          open: true,
          status: 0,
          content: <Intl id="submitting" />,
          cb: null,
        });
        postWorkflowData({
          form_id: item.id,
          workflow_name: "new workFlow",
          created_time: "",
          updated_time: "",
          create_by: authContext.userId,
          modify_by: "",
          stages: [
            {
              apiTaskName: "",
              id: 100,
              label: `Form | ${item.title}`,
              flowType: TRIGGER,
              condition: [],
            },
            {
              apiTaskName: "",
              condition: [],
              flowType: "Approval",
              id: 101,
              label: "Approval Process",
            },
          ],
        })
          .then((res) => {
            if (res.code === SUCCESS) {
              let tmpList = [...tableList];
              tmpList.push({ ...res.data, formName: item.title });
              setTableList(tmpList);
              setModalData({
                open: true,
                status: 2,
                content: <Intl id="workflowCreated" />,
                cb: () => {
                  closeModal();
                  navigate(`/app/workflow?id=${res.data.id}`);
                },
              });
            }
          })
          .catch((e) => {
            setModalData({
              open: true,
              status: 3,
              content: e.message,
              cb: closeModal,
            });
          });
      },
    });
  };
  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const closeModal = () => {
    setModalData({ ...modalData, open: false, cb: null });
  };

  useEffect(() => {
    Promise.all([getFormWorkflowData()])
      .then((res) => {
        let res1 = res[0];

        let tmpMap = {};
        formList.forEach((item) => {
          tmpMap[item.id] = {
            name: item.title,
            createTime: item.create_time,
          };
        });

        setTableList(
          res1.data.map((item) => {
            return {
              ...item,
              formName: (tmpMap[item.form_id] && tmpMap[item.form_id].name) || (
                <Intl id="workflowCreated" />
              ),
            };
          })
        );
        setFormLoading(false);
      })
      .catch((e) => {
        sendNotify({ msg: e.message, status: 3, show: true });
      });
  }, [formList]);

  return (
    <div className={styles.workflowManagement}>
      {formLoading && <Loading></Loading>}
      {!formLoading && (
        <>
          <div className={styles.workflowContainer}>
            <div className={styles.title}>
              <HeadLine>
                <Intl id="workflowManagement" />
              </HeadLine>
            </div>
            <div className={styles.filter}>
              <Button
                filled
                onClick={() => {
                  setAddModal(true);
                }}
              >
                <Intl id="addWorkflow" />
              </Button>
              <Filter
                id="filter"
                value={filterVal}
                options={selectOpetion}
                onChange={(val) => {
                  setFilterVal(val);
                }}
              />
            </div>
            <TableContainer component={Paper}>
              <Table aria-label="simple table">
                <TableHead>
                  <TableRow>
                    <TableCell align="center">
                      <Text type="subTitle">
                        <Intl id="workflowId" />
                      </Text>
                    </TableCell>
                    <TableCell align="center">
                      <Text type="subTitle">
                        <Intl id="workflowName" />
                      </Text>
                    </TableCell>
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
                        {row.id}
                        {row.available === 0 && (
                          <span className={styles.expired}>
                            (<Intl id="expired" />)
                          </span>
                        )}
                      </TableCell>
                      <TableCell align="center">{row.workflow_name}</TableCell>
                      <TableCell align="center">{row.formName}</TableCell>
                      <TableCell align="center">
                        {covertToHKTime(row.create_time)}
                      </TableCell>
                      <TableCell align="center">
                        <div className={styles.operation}>
                          <EditIcon
                            onClick={() => {
                              navigate(`/app/workflow?id=${row.id}`);
                            }}
                          />

                          <Delete
                            onClick={(e) => {
                              setModalData({
                                open: true,
                                status: 1,
                                content: <Intl id="workflowRemove" />,
                                cb: () => {
                                  setModalData({
                                    open: true,
                                    status: 0,
                                    content: <Intl id="submitting" />,
                                    cb: null,
                                  });
                                  deleteWorkflowData({
                                    id: row.id,
                                    stage_hash: row.stage_hash,
                                  })
                                    .then((res) => {
                                      if (res.code === SUCCESS) {
                                        setModalData({
                                          open: true,
                                          status: 2,
                                          content: <Intl id="workflowDelete" />,
                                          cb: () => {
                                            setModalData({
                                              content: "",
                                              status: 2,
                                              open: false,
                                              cb: null,
                                            });
                                          },
                                        });
                                        let tmpList = [...tableList];
                                        tmpList.splice(index, 1);
                                        setTableList(tmpList);
                                      }
                                    })
                                    .catch((e) => {
                                      setModalData({
                                        open: true,
                                        status: 3,
                                        content: e.message,
                                        cb: (e) => {
                                          setModalData({
                                            content: e.message,
                                            status: 3,
                                            open: false,
                                            cb: null,
                                          });
                                        },
                                      });
                                    });
                                },
                              });
                            }}
                          />
                        </div>
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
          </div>

          <CallModal
            open={modalData.open}
            content={modalData.content}
            status={modalData.status}
            buttonClickHandle={modalData.cb}
            handleClose={closeModal}
          />
          <Model
            open={addModal}
            handleClose={() => {
              setAddModal(false);
            }}
          >
            <div className={styles.addModal}>
              <div className={styles.modalTips}>
                <Text type="subTitle">
                  <Intl id="plsSelectForm" />
                </Text>
              </div>
              <Select
                value={selectedForm}
                options={selectOpetion}
                onChange={(value) => {
                  setSelectedForm(value);
                }}
              />
              <div className={styles.button}>
                <Button
                  size="small"
                  filled
                  onClick={() => {
                    let currentForm = formList.find((item) => {
                      return item.id === selectedForm;
                    });
                    addNewWorkFlow(currentForm);
                  }}
                >
                  <Intl id="add" />
                </Button>
              </div>
            </div>
          </Model>
        </>
      )}
    </div>
  );
};

export default WorkflowManagement;

/* third lib*/
import React, { useState, useEffect, useCallback, useMemo } from "react";
import { FormattedMessage as Intl } from "react-intl";
import Scrollbar from "react-perfect-scrollbar";
import { useForm } from "react-hook-form";

/* material-ui */
import Delete from "@material-ui/icons/Delete";
import EditIcon from "@material-ui/icons/Edit";
import VisibilityIcon from "@material-ui/icons/Visibility";
import Paper from "@material-ui/core/Paper";
import TablePagination from "@material-ui/core/TablePagination";

/* local components & methods */
import styles from "./styles.module.scss";
import {
  Table,
  TableBody,
  TableContainer,
  TableHead,
  TableRow,
  TableCell,
} from "@basics/Table";
import HeadLine from "@basics/HeadLine";
import Text from "@basics/Text";
import CallModal from "@basics/CallModal";
import Loading from "@assets/icons/Loading";
import WorkspaceForm from "@comp/WorkspaceForm";
import {
  wsDelete,
  deleteFormRequest,
  getUseCaseList,
  getUseCaseDetail,
  getWsDetail,
} from "@lib/api";
import { SUCCESS } from "src/lib/data/callStatus";
import Button from "@basics/Button";
import { sendNotify } from "src/utils/systerm-error";
import { useGlobalContext } from "src/context";
import FormRender from "@comp/FormRender";
import FormItem from "@comp/FormItem";
import UsecaseInfo from "@comp/UsecaseInfo";
import { GOVERNOR, IT, ADMIN } from "src/lib/data/roleType.js";
import { covertToHKTime } from "src/utils/timeFormat";
import GroupListTable from "@comp/GroupListTable";

const USE_CASE_FORM_ID = 2;

const WorkspaceManage = () => {
  const { setAuth, authContext } = useGlobalContext();
  const { control, register } = useForm(); // initialise the hook

  const [wsData, setWsData] = useState();
  const [formLoading, setFormLoading] = useState(true);
  const [addState, setAddState] = useState(false);
  const [step, setStep] = useState(0);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);

  const [ucDefaultData, setUcDefaultData] = useState(null);
  const [viewUcId, setViewUcId] = useState(null);
  const [modalData, setModalData] = useState({
    open: false,
    status: 0,
    content: "",
    cb: null,
  });

  const disableEditWs = useMemo(() => {
    return ![ADMIN, GOVERNOR, IT].includes(authContext.role);
  }, [authContext.role]);

  const isServiceAdmin = useMemo(() => {
    return authContext.role === ADMIN;
  }, [authContext]);

  const useCaseList = useMemo(() => {
    if (!wsData) {
      return [];
    }
    let tmpList = wsData.ucList;
    return tmpList.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage);
  }, [wsData, page, rowsPerPage]);

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

  const handleWsDelete = useCallback(() => {
    if (!isServiceAdmin) {
      return;
    }
    setModalData({
      open: true,
      status: 1,
      content: <Intl id="confirmDeleteWs" />,
      cb: () => {
        setModalData({
          open: true,
          status: 0,
          content: <Intl id="submitting" />,
          cb: null,
        });
        wsDelete({
          id: wsData.id,
        })
          .then((res) => {
            if (res.code === SUCCESS) {
              setModalData({
                open: true,
                status: 2,
                content: <Intl id="wsDeleted" />,
                cb: () => {
                  setAuth({
                    ...authContext,
                    role: res.data.role_name,
                    roleList: res.data.role_list,
                    wsId: Number(res.data.workspace_id),
                    wsList: res.data.workspace_list,
                  });
                  window.location.reload();
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
  }, [wsData, authContext, setAuth, isServiceAdmin]);

  const handleWsEdit = useCallback(() => {
    if (disableEditWs) {
      return;
    }
    setStep(1);
  }, [disableEditWs]);

  const handleUcClick = useCallback((uc, ucIndex) => {
    getUseCaseDetail({ id: uc.id })
      .then((res) => {
        let ucData = res.data;
        let defaultData = {
          form_id: USE_CASE_FORM_ID,
          id: res.id,
          s1: ucData.region_country,
          u2: ucData.uc_owner_group,
          u3: ucData.uc_team_group,
          u4: ucData.validity_date,
          u5: ucData.usecase_name,
          u6: ucData.uc_des,
          u7: ucData.service_account,
          u8: ucData.budget,
          u9: ucData.resources_access_list,
          u10: ucData.allow_cross_region,
        };
        setUcDefaultData(defaultData);
        setStep(2);
      })
      .catch((e) => {
        sendNotify({ msg: e.message, status: 3, show: true });
      });
  }, []);

  const handleUcDelete = useCallback((ucId, ucIndex, row, rowIndex) => {
    setModalData({
      open: true,
      status: 1,
      content: <Intl id="confirmDeleteUc" />,
      cb: () => {
        setModalData({
          open: true,
          status: 0,
          content: <Intl id="submitting" />,
          cb: null,
        });
        deleteFormRequest({
          form_id: USE_CASE_FORM_ID,
          id: ucId,
        })
          .then((res) => {
            if (res.code === SUCCESS) {
              setModalData({
                open: true,
                status: 2,
                content: <Intl id="ucDeleted" />,
                cb: () => {
                  setModalData({
                    content: "",
                    status: 2,
                    open: false,
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
  }, []);

  const handleViewClick = useCallback((uc, ucIndex) => {
    setViewUcId(uc.id);
    setStep(3);
  }, []);

  const dynamicField = useMemo(() => {
    let fieldList = [];
    if (wsData && wsData.dynamic) {
      Object.keys(wsData.dynamic).forEach((key) => {
        fieldList = fieldList.concat(
          wsData.dynamic[key].filter((item) => item.label !== "Team")
        );

        /* real logic
        fieldList = fieldList.concat(wsData.dynamic[key]);
        */
      });
    }

    return fieldList;
  }, [wsData]);

  const systemField = useMemo(() => {
    if (wsData && wsData.system) {
      let tmp = "";
      const formItemMap = {
        1: "Checkbox",
        2: "Dropdown",
        3: "Textbox",
        4: "Upload",
        5: "Toggle",
        6: "Datepicker",
      };

      Object.keys(wsData.system).forEach((key) => {
        tmp += `${wsData.system[key].length} ${formItemMap[key]} `;
      });
      return tmp;
    } else {
      return "";
    }
  }, [wsData]);

  useEffect(() => {
    if (step === 0) {
      Promise.all([getUseCaseList(), getWsDetail({ id: authContext.wsId })])
        .then((res) => {
          let res1 = res[0];
          let res2 = res[1];
          if (res1.data && res2.data) {
            let ucList = res1.data.filter(
              (item) => item.workspace_id === authContext.wsId
            );
            setWsData({
              ...res2.data,
              ucList: ucList,
            });
            setFormLoading(false);
          }
        })
        .catch((e) => {
          sendNotify({ msg: e.message, status: 3, show: true });
        });
    }
  }, [step, authContext]);

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

  return (
    <div className={styles.workspaceCreation}>
      <Scrollbar>
        {formLoading && <Loading></Loading>}
        {!formLoading && (
          <>
            {step === 0 && (
              <div className={styles.wsContainer}>
                <div className={styles.title}>
                  <HeadLine>
                    <Intl id="wsMan" />
                  </HeadLine>
                </div>
                <div className={styles.wsDetailBox}>
                  <div className={styles.secondTitle}>
                    <Text type="title">
                      <Intl id="wsDetail" />
                    </Text>
                  </div>
                  <div className={styles.detailBox}>
                    <div className={styles.detailItem}>
                      <div className={styles.detailLabel}>
                        <Text type="subTitle">
                          <Intl id="workspaceName" />
                        </Text>
                      </div>
                      <div className={styles.detailValue}>{wsData.ws_name}</div>
                    </div>
                    <div className={styles.detailItem}>
                      <div className={styles.detailLabel}>
                        <Text type="subTitle">
                          <Intl id="wsAD" />
                        </Text>
                      </div>
                      <div className={styles.detailValue}>
                        {wsData.ws_owner_group}
                      </div>
                    </div>
                    <div className={styles.detailItem}>
                      <div className={styles.detailLabel}>
                        <Text type="subTitle">
                          <Intl id="itAD" />
                        </Text>
                      </div>
                      <div className={styles.detailValue}>
                        {wsData.it_group}
                      </div>
                    </div>

                    <div className={styles.detailItem}>
                      <div className={styles.detailLabel}>
                        <Text type="subTitle">
                          <Intl id="dataGovernorAd" />
                        </Text>
                      </div>
                      <div className={styles.detailValue}>
                        {wsData.dg_group}
                      </div>
                    </div>
                    <div className={styles.detailItem}>
                      <div className={styles.detailLabel}>
                        <Text type="subTitle">
                          <Intl id="wsTeamAD" />
                        </Text>
                      </div>
                      <div className={styles.detailValue}>
                        {wsData.ws_team_group}
                      </div>
                    </div>
                    <div className={styles.detailItem}>
                      <div className={styles.detailLabel}>
                        <Text type="subTitle">
                          <Intl id="wsDes" />
                        </Text>
                      </div>
                      <div className={styles.detailValue}>{wsData.ws_des}</div>
                    </div>
                    <div className={styles.detailItem}>
                      <div className={styles.detailLabel}>
                        <Text type="subTitle">
                          <Intl id="userCycle" />
                        </Text>
                      </div>
                      <div className={styles.detailValue}>{wsData.cycle}</div>
                    </div>
                    <div className={styles.detailItem}>
                      <div className={styles.detailLabel}>
                        <Text type="subTitle">
                          <Intl id="ucFlow" />
                        </Text>
                      </div>
                      <div className={styles.detailValue}>
                        {wsData.approval}
                      </div>
                    </div>
                  </div>
                  <div className={styles.fullLineField}>
                    <div className={styles.secondTitle}>
                      <Text type="title">
                        <Intl id="defaultAd" />
                      </Text>
                    </div>
                    <div className={styles.formOptions}>
                      <GroupListTable data={wsData.groupArr} editable={false} />
                    </div>
                  </div>
                  <div className={styles.fullLineField}>
                    <div className={styles.secondTitle}>
                      <Text type="title">
                        <Intl id="dynamicApprover" />
                      </Text>
                    </div>
                    <div className={styles.formOptions}>
                      {renderFormItem(dynamicField)}
                    </div>
                  </div>
                  <div className={styles.fullLineField}>
                    <div className={styles.secondTitle}>
                      <Text type="title">
                        <Intl id="systemField" />
                      </Text>
                    </div>
                    <div className={styles.detailValue}>{systemField}</div>
                  </div>
                </div>

                <div className={styles.wsDetailBox}>
                  <div className={styles.secondTitle}>
                    <Text type="title">
                      <Intl id="ucList" />
                    </Text>
                  </div>
                  {useCaseList && useCaseList.length > 0 && (
                    <>
                      <TableContainer component={Paper}>
                        <Table>
                          <TableHead>
                            <TableRow>
                              <TableCell width="20%" align="center">
                                <Text type="subTitle">
                                  <Intl id="ucId" />
                                </Text>
                              </TableCell>
                              <TableCell width="20%" align="center">
                                <Text type="subTitle">
                                  <Intl id="ucName" />
                                </Text>
                              </TableCell>
                              <TableCell width="20%" align="center">
                                <Text type="subTitle">
                                  <Intl id="usOwnerGroup" />
                                </Text>
                              </TableCell>
                              <TableCell width="20%" align="center">
                                <Text type="subTitle">
                                  <Intl id="ValidityDate" />
                                </Text>
                              </TableCell>
                              <TableCell width="20%" align="center">
                                <Text type="subTitle">
                                  <Intl id="operation" />
                                </Text>
                              </TableCell>
                            </TableRow>
                          </TableHead>
                          <TableBody>
                            {useCaseList.map((uc, ucIndex) => (
                              <TableRow key={ucIndex}>
                                <TableCell align="center">
                                  <Text>{uc.id}</Text>
                                </TableCell>
                                <TableCell align="center">
                                  <Text>{uc.uc_owner_group}</Text>
                                </TableCell>
                                <TableCell align="center">
                                  <Text>{uc.uc_owner_group}</Text>
                                </TableCell>
                                <TableCell align="center">
                                  <Text>
                                    {covertToHKTime(uc.validity_date)}
                                  </Text>
                                </TableCell>
                                <TableCell align="center">
                                  <div className={styles.operation}>
                                    <VisibilityIcon
                                      onClick={() => {
                                        handleViewClick(uc, ucIndex);
                                      }}
                                    />
                                    <EditIcon
                                      onClick={() => {
                                        handleUcClick(uc, ucIndex);
                                      }}
                                    />
                                    <Delete
                                      onClick={(e) => {
                                        handleUcDelete(uc.id, ucIndex);
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
                        count={wsData.ucList.length}
                        rowsPerPage={rowsPerPage}
                        page={page}
                        onChangePage={handleChangePage}
                        onChangeRowsPerPage={handleChangeRowsPerPage}
                      />
                    </>
                  )}
                </div>
                {!disableEditWs && (
                  <div className={styles.buttonWrapper}>
                    {isServiceAdmin && (
                      <Button
                        onClick={() => {
                          handleWsDelete();
                        }}
                        className={styles.button}
                        variant="contained"
                      >
                        <Intl id="delete" />
                      </Button>
                    )}
                    <Button
                      onClick={() => {
                        handleWsEdit();
                      }}
                      className={styles.button}
                      variant="contained"
                    >
                      <Intl id="edit" />
                    </Button>
                  </div>
                )}
              </div>
            )}
            {step === 1 && (
              <WorkspaceForm
                onBack={() => {
                  setStep(0);
                  setAddState(false);
                }}
                currentId={authContext.wsId}
                addState={addState}
              />
            )}

            {step === 2 && (
              <FormRender
                formId={USE_CASE_FORM_ID}
                onBack={() => {
                  setStep(0);
                  setUcDefaultData(null);
                }}
                defaultData={ucDefaultData}
              />
            )}

            {step === 3 && (
              <UsecaseInfo
                onBack={() => {
                  setStep(0);
                  setUcDefaultData(null);
                }}
                usecaseId={viewUcId}
              />
            )}

            <CallModal
              open={modalData.open}
              content={modalData.content}
              status={modalData.status}
              buttonClickHandle={modalData.cb}
              handleClose={closeModal}
            />
          </>
        )}
      </Scrollbar>
    </div>
  );
};

export default WorkspaceManage;

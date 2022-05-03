// third lib
import React, { useState, useEffect, useCallback, useMemo } from "react";
import { FormattedMessage as Intl } from "react-intl";
import ScrollBar from "react-perfect-scrollbar";
import cn from "classnames";

/* material-ui */
import List from "@material-ui/core/List";
import ListItem from "@material-ui/core/ListItem";
import ListItemSecondaryAction from "@material-ui/core/ListItemSecondaryAction";
import ListItemText from "@material-ui/core/ListItemText";
import ArrowBackIcon from "@material-ui/icons/ArrowBack";
import ThumbDownAltIcon from "@material-ui/icons/ThumbDownAlt";
import ThumbUpAltIcon from "@material-ui/icons/ThumbUpAlt";
import Checkbox from "@material-ui/core/Checkbox";
import MarkUnreadChatAltIcon from "@assets/icons/MarkUnreadChatAlt";

/* local components & methods */
import FormDataDisplay from "../FormDataDisplay";
import Button from "@basics/Button";
import styles from "./styles.module.scss";
import Loading from "@assets/icons/Loading";
import HeadLine from "@basics/HeadLine";
import {
  changeStatusList,
  getRequestDetailList,
  getFormDataList,
} from "@lib/api";
import { sendNotify } from "src/utils/systerm-error";
import Text from "@basics/Text";
import CallModal from "@basics/CallModal";

const RequestDetailList = ({ idListStr, approvedView }) => {
  const [formLoading, setFormLoading] = useState(true);
  const [requestList, setRequestList] = useState([]);
  const [currentData, setCurrentData] = useState();
  const [selectedList, setSelectedList] = useState([]);
  const [modalData, setModalData] = useState({
    open: false,
    status: 0,
    content: "",
  });
  const [submitData, setSubmitData] = useState();

  const disableBtn = useMemo(() => {
    return selectedList.length === 0;
  }, [selectedList]);

  const recordList = useMemo(() => {
    let idList = idListStr.split("|");
    return idList;
  }, [idListStr]);

  const isSelected = useCallback(
    (index) => {
      return selectedList.includes(index);
    },
    [selectedList]
  );

  const onSelect = useCallback(
    (index) => {
      if (!selectedList.includes(index)) {
        let tmp = [...selectedList, index];
        setSelectedList(tmp);
      } else {
        let currentIndex = selectedList.indexOf(index);
        let tmp = [...selectedList];
        tmp.splice(currentIndex, 1);
        setSelectedList(tmp);
      }
    },
    [selectedList]
  );

  const buttonClickHandle = useCallback(() => {
    let successTips;
    successTips =
      submitData.action === 1
        ? "Selected Request have been rejected"
        : "Selected have been approved";

    switch (modalData.status) {
      case 1:
      case 3:
        setModalData({
          ...modalData,
          status: 0,
          content: <Intl id="loadNpatience" />,
        });

        changeStatusList(submitData.data)
          .then((res) => {
            if (res.code === 200) {
              setModalData({
                open: true,
                status: 2,
                content: successTips,
              });
              window.location.reload();
            }
          })
          .catch(() => {
            setModalData({
              ...modalData,
              status: 3,
              content: <Intl id="goesWrong" />,
            });
          });
        break;
      default:
        setModalData({ ...modalData, open: false });
        break;
    }
  }, [modalData, submitData]);

  const submitHandle = useCallback(
    (action) => {
      setModalData({
        open: true,
        status: 1,
        content:
          action === 1
            ? "Do you confirm to reject selected request?"
            : "Do you confirm to approve selected request?",
      });
      let selected = requestList.filter((request) => {
        return selectedList.includes(request.seq);
      });

      let selectedData = selected.map((item) => ({
        id: item.record.id,
        form_status: action,
        form_id: item.form.id,
        comment: "",
      }));

      setSubmitData({
        action: action,
        data: { data: selectedData },
      });
    },
    [requestList, selectedList]
  );

  useEffect(() => {
    getRequestDetailList({ idList: recordList })
      .then((recordData) => {
        setFormLoading(true);
        if (recordData.data) {
          let record = recordData.data;
          let formIdList = record.map((item) => {
            let latestRecord = item[0];
            return latestRecord.form_id;
          });

          getFormDataList({ idList: formIdList })
            .then((formData) => {
              if (formData.data) {
                let tmp = formData.data.map((form, index) => {
                  return {
                    form: form,
                    record: record[index][0],
                    seq: index,
                    status: record[index][0].form_status,
                    checked: index === 0,
                  };
                });
                setRequestList(tmp);
                setCurrentData(tmp[0]);
                setFormLoading(false);
              }
            })
            .catch((e) => {
              sendNotify({ msg: e.message, status: 3, show: true });
            });
        }
      })
      .catch((e) => {
        sendNotify({ msg: e.message, status: 3, show: true });
      });
  }, [recordList]);

  return (
    <div className={styles.requestDetail}>
      {formLoading && <Loading></Loading>}

      {!formLoading && (
        <div className={styles.detailContent}>
          <div className={styles.form}>
            <ScrollBar>
              <div className={styles.mainContent}>
                <div
                  className={styles.onBack}
                  onClick={() => {
                    window.history.back();
                  }}
                >
                  <ArrowBackIcon />
                  <Text type="subTitle">
                    <Intl id="back" />
                  </Text>
                </div>
                {currentData && (
                  <FormDataDisplay
                    formId={currentData.form.id}
                    formTemplate={currentData.form}
                    recordId={currentData.record.id}
                    approvedView={approvedView}
                    defaultData={currentData.record}
                    enableReOpen={false}
                    isLatestRecord={true}
                  />
                )}
              </div>
            </ScrollBar>
          </div>

          <div className={styles.requestList}>
            <ScrollBar>
              <div className={styles.requestContent}>
                <HeadLine>
                  <Intl id="requestList" />
                </HeadLine>
                <div className={styles.requestTable}>
                  <List>
                    {requestList.map((request, index) => (
                      <ListItem
                        key={index}
                        className={cn(styles.requestItem, {
                          [styles["active"]]: currentData.seq === index,
                        })}
                        onClick={() => {
                          setCurrentData(request);
                          setRequestList(
                            requestList.map((item, currIndex) => {
                              if (index === currIndex) {
                                item.checked = true;
                              }
                              return item;
                            })
                          );
                        }}
                      >
                        <ListItemText>{request.record.id}</ListItemText>
                        <ListItemText>
                          <div className={styles.timeStamp}>
                            {request.form.title}
                          </div>
                        </ListItemText>
                        <ListItemSecondaryAction className={styles.svg}>
                          {!approvedView && <MarkUnreadChatAltIcon />}
                          {approvedView && (
                            <>
                              {(request.status === 4 ||
                                request.status === 2) && <ThumbUpAltIcon />}
                              {request.status === 1 && <ThumbDownAltIcon />}
                              {request.status === 0 && !request.checked && (
                                <MarkUnreadChatAltIcon />
                              )}
                              {request.status === 0 && request.checked && (
                                <Checkbox
                                  className={styles.checkbox}
                                  color="primary"
                                  checked={isSelected(index)}
                                  onChange={() => {
                                    onSelect(index);
                                  }}
                                />
                              )}
                            </>
                          )}
                        </ListItemSecondaryAction>
                      </ListItem>
                    ))}
                  </List>
                </div>

                {approvedView && (
                  <div className={styles.buttonWrapper}>
                    <Button
                      className={styles.button}
                      onClick={() => {
                        if (disableBtn) {
                          return;
                        }
                        submitHandle(4);
                      }}
                      variant="contained"
                      disabled={disableBtn}
                    >
                      <Intl id="approveAll" />
                    </Button>
                    <Button
                      className={styles.button}
                      onClick={() => {
                        if (disableBtn) {
                          return;
                        }
                        submitHandle(1);
                      }}
                      variant="contained"
                      disabled={disableBtn}
                    >
                      <Intl id="rejectAll" />
                    </Button>
                  </div>
                )}
              </div>
            </ScrollBar>
          </div>
        </div>
      )}

      <CallModal
        open={modalData.open}
        content={modalData.content}
        status={modalData.status}
        buttonClickHandle={buttonClickHandle}
        handleClose={() => {
          setModalData({ ...modalData, open: false });
        }}
      />
    </div>
  );
};

export default RequestDetailList;

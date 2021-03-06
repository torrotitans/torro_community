// third lib
import React, { useState, useEffect, useCallback, useMemo } from "react";
import { FormattedMessage as Intl } from "react-intl";
import ScrollBar from "react-perfect-scrollbar";
import cn from "classnames";

/* material-ui */
import List from "@material-ui/core/List";
import ListItem from "@material-ui/core/ListItem";
import TodayIcon from "@material-ui/icons/Today";
import LaunchIcon from "@material-ui/icons/Launch";
import ArrowBackIcon from "@material-ui/icons/ArrowBack";

/* local components & methods */
import FormDataDisplay from "../FormDataDisplay";
import styles from "./styles.module.scss";
import Loading from "@assets/icons/Loading";
import { getRequestDetail, getFormItem } from "@lib/api";
import { sendNotify } from "src/utils/systerm-error";
import Text from "@basics/Text";
import CallModal from "@basics/CallModal";
import { covertToCurrentTime } from "src/utils/timeFormat";
import { useGlobalContext } from "src/context";

const RequestDetail = ({ recordId, approvedView }) => {
  const { timeContext } = useGlobalContext();

  const [formLoading, setFormLoading] = useState(true);
  const [tableList, setTableList] = useState([]);
  const [formData, setFormData] = useState();
  const [changeData, setChangeData] = useState();
  const [editView, setEditView] = useState(false);
  const [isApprover, setIsApprover] = useState(false);
  const [defaultData, setDefaultData] = useState({
    index: 0,
    data: null,
  });
  const [modalData, setModalData] = useState({
    open: false,
    status: 0,
    content: "",
  });

  const buttonClickHandle = () => {
    setDefaultData(changeData);
    setModalData({ ...modalData, open: false });
  };

  const isLatestRecord = useMemo(() => {
    return defaultData.index === 0;
  }, [defaultData.index]);

  const enableReOpen = useMemo(() => {
    if (!formData) {
      return;
    }
    let formId = Number(formData.id);

    return isLatestRecord && (formId > 350 || [1, 2].includes(formId));
  }, [isLatestRecord, formData]);

  const covertTime = useCallback(
    (date) => {
      return covertToCurrentTime(date, timeContext.timeFormat);
    },
    [timeContext]
  );

  const InitDetailPage = useCallback(() => {
    setFormLoading(true);

    getRequestDetail({ id: recordId })
      .then((res) => {
        if (res.code === 200) {
          let latestRecord = res.data[0];
          res.data.forEach((item) => {
            if (item.createTime > latestRecord.createTime) latestRecord = item;
          });
          setIsApprover(res.approverView);
          setDefaultData({ index: 0, data: latestRecord });
          setTableList(res.data);
          getFormItem({
            id: latestRecord.form_id,
          })
            .then((res2) => {
              if (res2.code === 200) {
                let data = res2.data;
                setFormData(data);
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
  }, [recordId]);

  useEffect(() => {
    setFormLoading(true);
    if (recordId) {
      InitDetailPage();
    }
  }, [recordId, InitDetailPage]);

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
                <FormDataDisplay
                  formId={formData.id}
                  formTemplate={formData}
                  recordId={recordId}
                  approverView={approvedView}
                  isApprover={isApprover}
                  defaultData={defaultData.data}
                  isLatestRecord={isLatestRecord}
                  enableReOpen={enableReOpen}
                  setEditView={setEditView}
                />
                {tableList && tableList.length > 1 && (
                  <div className={styles.history}>
                    <Text type="title">
                      <Intl id="historyRecord" />
                    </Text>
                    <div className={styles.historyTable}>
                      <List>
                        {tableList.map((row, index) => (
                          <ListItem
                            key={index}
                            className={cn(styles.historyItem, {
                              [styles["active"]]: defaultData.index === index,
                            })}
                            onClick={() => {
                              if (editView) {
                                setChangeData({
                                  index: index,
                                  data: row,
                                });
                                setModalData({
                                  ...modalData,
                                  open: true,
                                  status: 1,
                                  content:
                                    "Switch to this record will miss your current input.",
                                });
                              } else {
                                setDefaultData({
                                  index: index,
                                  data: row,
                                });
                              }
                            }}
                          >
                            <div className={styles.historyItemBox}>
                              <div className={styles.timeStamp}>
                                <TodayIcon />
                                {covertTime(row.create_time)}
                              </div>
                              <LaunchIcon className={styles.launchIcon} />
                            </div>
                          </ListItem>
                        ))}
                      </List>
                    </div>
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

export default RequestDetail;

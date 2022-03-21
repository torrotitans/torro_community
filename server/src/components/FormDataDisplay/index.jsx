/* third lib*/
import React, { useEffect, useState, useCallback } from "react";
import { FormattedMessage as Intl } from "react-intl";
import { useForm } from "react-hook-form";
import cn from "classnames";

/* material-ui */
import Paper from "@material-ui/core/Paper";
import InsertDriveFileIcon from "@material-ui/icons/InsertDriveFile";

/* local components & methods */
import ProgressBar from "@comp/ProgressBar";
import FormItem from "@comp/FormItem";
import Button from "@basics/Button";
import HeadLine from "@basics/HeadLine";
import Text from "@basics/Text";
import styles from "./styles.module.scss";
import {
  getFieldDisplayConfig,
  updateFormRequest,
  changeStatus,
} from "@lib/api";
import Loading from "@assets/icons/Loading";
import { sendNotify } from "src/utils/systerm-error";
import CallModal from "@basics/CallModal";
import { SUCCESS } from "src/lib/data/callStatus";
import TextBox from "@basics/TextBox";
import SpecialField from "./SpecialField";
import CommentSection from "../CommentSection";
import { covertToCurrentTime } from "src/utils/timeFormat";
import { useGlobalContext } from "src/context";

import {
  Table,
  TableBody,
  TableContainer,
  TableHead,
  TableRow,
  TableCell,
} from "@basics/Table";
import { STATUS_MAP } from "src/constant";

const FormDataDisplay = ({
  formId,
  formTemplate,
  recordId,
  defaultData,
  enableReOpen,
  setEditView,
  approverView,
  isApprover,
}) => {
  const { handleSubmit, control, register } = useForm(); // initialise the hook
  const { timeContext } = useGlobalContext();

  const [status, setStatus] = useState();
  const [formData, setFormData] = useState(null);
  const [formLoading, setFormLoading] = useState(true);
  const [edit, setEdit] = useState(false);
  const [commentList, setCommentList] = useState(defaultData.comment_history);
  const [specialList, setSpecialList] = useState([]);

  const covertTime = useCallback(
    (date) => {
      return covertToCurrentTime(date, timeContext.timeFormat);
    },
    [timeContext]
  );

  const [submitData, setSubmitData] = useState(null);
  const [comment, setComment] = useState("");
  const [modalData, setModalData] = useState({
    open: false,
    status: 0,
    content: "",
  });

  const buttonClickHandle = useCallback(() => {
    let apiCall;
    let postData;
    let successTips;
    if (submitData.type === "changeStatus") {
      apiCall = changeStatus;
      successTips =
        submitData.data.form_status === 1
          ? "Request have been rejected"
          : "Request have been approved";
      postData = { ...submitData.data, comment: comment || "" };
    } else {
      apiCall = updateFormRequest;
      postData = { ...submitData.data, id: recordId };
      let valueMap = postData.form_field_values_dict;
      successTips = <Intl id="newRequestSubmit" />;
      if (valueMap) {
        let validate = true;
        Object.keys(valueMap).forEach((k) => {
          if (!valueMap[k]) validate = false;
        });
        if (!validate) {
          sendNotify({
            msg: "There are form items not entered",
            status: 3,
            show: true,
          });
          return;
        }
      }
    }

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
  }, [modalData, submitData, recordId, comment]);

  const submitHandle = (data) => {
    setModalData({
      open: true,
      status: 1,
      content: "Do you confirm to raise this request?",
    });
    let files = {};
    Object.keys(data).forEach((key) => {
      if (data[key] instanceof Array && data[key][0] instanceof File) {
        data[key].forEach((item, index) => {
          files[key + "-" + (index + 1)] = item;
        });
        data[key] = [];
      }
    });
    setSubmitData({
      type: "reOpen",
      data: {
        form_id: formId,
        form_field_values_dict: data,
      },
    });
  };

  const renderFormItem = (items) => {
    return items.map((item, index) => {
      return (
        <FormItem
          key={index}
          data={item}
          index={index}
          control={control}
          register={register}
        />
      );
    });
  };

  const handleStatusChange = useCallback(
    (status) => {
      setModalData({
        open: true,
        status: 1,
        content:
          status === 1 ? <Intl id="rejectTips" /> : <Intl id="approveTips" />,
      });
      setComment("");
      setSubmitData({
        type: "changeStatus",
        data: {
          id: recordId,
          form_status: status,
          form_id: formData.id,
        },
      });
    },
    [formData, recordId]
  );

  const renderFieldValue = useCallback(
    (row) => {
      let label = row.label;
      let defaultValue = row.default;
      // let options = row.options;
      let special;
      specialList.forEach((item) => {
        if (
          label === item.label &&
          (item.formId === null ? true : item.formId === formId)
        ) {
          special = item;
        }
      });
      if (special) {
        return (
          <SpecialField formId={formId} special={special} data={defaultValue} />
        );
      }

      if (defaultValue instanceof Array || defaultValue instanceof Object) {
        if (
          defaultValue instanceof Array &&
          defaultValue[0] &&
          defaultValue[0].fileName
        ) {
          return defaultValue.map((item, index) => {
            return (
              <a
                key={index}
                // eslint-disable-next-line react/jsx-no-target-blank
                target="_blank"
                className={styles.fileLink}
                href={item.fileURL}
              >
                <InsertDriveFileIcon />
                {item.fileName}
              </a>
            );
          });
        }
      } else if (typeof defaultValue === "boolean") {
        return String(defaultValue);
      } else if (row.style === 6) {
        return covertTime(defaultValue);
      } else {
        return defaultValue;
      }
    },
    [formId, specialList, covertTime]
  );

  useEffect(() => {
    if (!formTemplate || !defaultData) {
      return;
    }
    let defaultValue = defaultData.form_field_values_dict;
    let data = formTemplate;
    let currenFileList = data.fieldList.map((item) => {
      if (typeof defaultValue[item.id] === "boolean") {
        item.default = String(defaultValue[item.id]);
      } else {
        item.default = defaultValue[item.id] || "";
      }
      return item;
    });
    data = {
      ...data,
      fieldList: currenFileList,
    };
    setStatus(defaultData.form_status);
    setFormData(data);
    setFormLoading(false);
  }, [formTemplate, defaultData]);

  useEffect(() => {
    getFieldDisplayConfig().then((res) => {
      if (res.data) {
        setSpecialList(res.data);
      }
    });
  }, []);

  useEffect(() => {
    setEdit(false);
  }, [defaultData]);

  useEffect(() => {
    setEditView && setEditView(edit);
  }, [edit, setEditView]);

  useEffect(() => {
    setCommentList(defaultData.comment_history);
  }, [defaultData]);

  return (
    <div className={styles.formDataDisplay}>
      {formLoading && <Loading />}
      {!formLoading && formData && (
        <>
          {!edit && (
            <div
              className={cn(styles.status, {
                [styles["expired"]]: !enableReOpen,
              })}
            >
              {enableReOpen ? STATUS_MAP[status] : "expired"}
            </div>
          )}
          <HeadLine>{formData.title}</HeadLine>
          <div className={styles.formDes}>
            <Text>{formData.des}</Text>
          </div>
          {!edit && (
            <div className={styles.viewBox}>
              <div className={styles.viewContext}>
                <div className={styles.readOnlyView}>
                  <div className={styles.submitData}>
                    <div className={styles.requestTitle}>
                      <Text type="title">
                        <Intl id="requestDetail"></Intl>
                      </Text>
                    </div>
                    <TableContainer component={Paper}>
                      <Table size="small" aria-label="a dense table">
                        <TableHead>
                          <TableRow>
                            <TableCell width="30%" align="center">
                              <Intl id="label"></Intl>
                            </TableCell>
                            <TableCell width="70%" align="center">
                              <Intl id="value"></Intl>
                            </TableCell>
                          </TableRow>
                        </TableHead>
                        <TableBody>
                          {formData.fieldList.map((row, index) => {
                            return (
                              <TableRow key={index}>
                                <TableCell width="30%" align="center">
                                  {row.label}
                                </TableCell>
                                <TableCell width="70%" align="center">
                                  {renderFieldValue(row)}
                                </TableCell>
                              </TableRow>
                            );
                          })}
                        </TableBody>
                      </Table>
                    </TableContainer>
                  </div>
                  <div className={styles.progressBox}>
                    <div className={styles.requestTitle}>
                      <Text type="title">
                        <Intl id="requestProgress"></Intl>
                      </Text>
                    </div>
                    <div className={styles.progress}>
                      <ProgressBar progress={defaultData.status_history} />
                    </div>
                  </div>
                </div>
                <CommentSection
                  recordId={recordId}
                  commentList={commentList}
                  statusHistory={defaultData.status_history}
                  handleChange={(data) => {
                    setCommentList(data);
                  }}
                />
              </div>
              {approverView && status === 0 && (
                <div className={styles.buttonWrapper}>
                  <Button
                    className={styles.button}
                    onClick={() => {
                      handleStatusChange(4);
                    }}
                    variant="contained"
                  >
                    <Intl id="approve" />
                  </Button>
                  <Button
                    className={styles.button}
                    onClick={() => {
                      handleStatusChange(1);
                    }}
                    variant="contained"
                  >
                    <Intl id="reject" />
                  </Button>
                </div>
              )}
              {!approverView && enableReOpen && (
                <div className={styles.buttonWrapper}>
                  <Button
                    className={styles.button}
                    onClick={() => {
                      setEdit(true);
                    }}
                    variant="contained"
                  >
                    <Intl id="reOpen" />
                  </Button>
                </div>
              )}
            </div>
          )}
          {edit && (
            <form
              className={styles.form}
              id={`currentForm${formData.id}`}
              onSubmit={handleSubmit(submitHandle)}
            >
              <div className={styles.formOptions}>
                {renderFormItem(formData.fieldList)}
              </div>

              <div className={styles.buttonWrapper}>
                <Button
                  onClick={() => {
                    setEdit(false);
                  }}
                  className={styles.button}
                  variant="contained"
                >
                  <Intl id="cancel" />
                </Button>
                <Button
                  className={styles.button}
                  type="submit"
                  variant="contained"
                >
                  <Intl id="reSubmit" />
                </Button>
              </div>
            </form>
          )}
        </>
      )}
      <CallModal
        open={modalData.open}
        content={modalData.content}
        status={modalData.status}
        buttonClickHandle={buttonClickHandle}
        handleClose={() => {
          setModalData({ ...modalData, open: false });
        }}
      >
        {modalData.status === 1 && (
          <div className={styles.modalCommnet}>
            <div className={styles.modalTitle}>Additional comments</div>
            <TextBox
              value={comment}
              placeholder="Please enter your comment"
              multiline
              rows={4}
              onChange={(value) => {
                setComment(value);
              }}
            />
          </div>
        )}
      </CallModal>
    </div>
  );
};

export default FormDataDisplay;

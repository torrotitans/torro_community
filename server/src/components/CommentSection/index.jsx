/* third lib*/
import React, { useState, useCallback, useMemo } from "react";
import { FormattedMessage as Intl } from "react-intl";

/* material-ui */
import AccountCircleIcon from "@material-ui/icons/AccountCircle";
import Delete from "@material-ui/icons/Delete";

/* local components & methods */
import { postComment, deleteComment } from "@lib/api";
import Text from "@basics/Text";
import styles from "./styles.module.scss";
import TextBox from "@basics/TextBox";
import CallModal from "@basics/CallModal";
import { useGlobalContext } from "src/context";
import Button from "@basics/Button";

const CommentSection = ({
  recordId,
  commentList,
  statusHistory,
  handleChange,
}) => {
  const { authContext } = useGlobalContext();

  const [comment, setComment] = useState("");
  const [modalData, setModalData] = useState({
    open: false,
    status: 0,
    content: "",
  });
  const [deleteId, setDeleteId] = useState(null);

  const currentList = useMemo(() => {
    let combinList = commentList;
    combinList = combinList.sort((a, b) => {
      let aTime = new Date(a.time);
      let bTime = new Date(b.time);
      if (aTime > bTime) {
        return -1;
      }
      if (aTime < bTime) {
        return 1;
      }
      return 0;
    });
    return combinList;
  }, [commentList]);

  const submitHandle = useCallback(() => {
    setDeleteId(null);
    setModalData({
      open: true,
      status: 1,
      content: <Intl id="addNewCommentTips" />,
    });
  }, []);

  const deleteHandle = useCallback((commentId) => {
    setModalData({
      open: true,
      status: 1,
      content: <Intl id="deleteCommentTips" />,
    });
    setDeleteId(commentId);
  }, []);

  const buttonClickHandle = useCallback(() => {
    let apiCall = deleteId ? deleteComment : postComment;

    let postData = deleteId
      ? {
          input_form_id: recordId,
          comment_id: deleteId,
        }
      : {
          input_form_id: recordId,
          comment: comment,
        };

    let successTips = deleteId ? (
      <Intl id="deleteSuccess" />
    ) : (
      <Intl id="addSuccess" />
    );

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
            if (res.code === 200) {
              setModalData({
                open: true,
                status: 2,
                content: successTips,
              });
              if (deleteId) {
                handleChange(
                  commentList.filter((item) => item.comment_id !== deleteId)
                );
                setDeleteId(null);
              } else {
                handleChange([
                  ...commentList,
                  {
                    comment_id: res.data.commentId,
                    comment: comment,
                    time: new Date().toGMTString(),
                    accountId: authContext.accountId,
                  },
                ]);
              }
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
        setDeleteId(null);
        break;
    }
  }, [
    deleteId,
    comment,
    recordId,
    modalData,
    commentList,
    authContext,
    handleChange,
  ]);

  return (
    <div className={styles.formControl}>
      <div className={styles.commentHistory}>
        <Text type="title">
          <Intl id="commnetHistory"></Intl>
        </Text>
        <div className={styles.commentList}>
          {currentList.map((comment, index) => {
            return (
              <div key={index} className={styles.commentRecord}>
                <div className={styles.commnetTitle}>
                  <div className={styles.accountDetail}>
                    <AccountCircleIcon />
                    <div className={styles.commentator}>
                      {comment.accountId}
                      {comment.tag && (
                        <span className={styles.statusTag}>
                          ({comment.tag})
                        </span>
                      )}
                    </div>
                    {!comment.tag && (
                      <div
                        className={styles.deleteIcon}
                        onClick={() => {
                          deleteHandle(comment.comment_id);
                        }}
                      >
                        <Delete />
                      </div>
                    )}
                  </div>
                  <div className={styles.commentTime}>{comment.time}</div>
                </div>
                <div className={styles.commentContent}>{comment.comment}</div>
              </div>
            );
          })}
        </div>
      </div>
      <div className={styles.commentBox}>
        <div className={styles.requestTitle}>
          <Text type="title">
            <Intl id="newComment"></Intl>
          </Text>
        </div>
        <div className={styles.commentOperate}>
          <div className={styles.textArea}>
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
          <div className={styles.addComment}>
            <Button
              className={styles.btn}
              onClick={() => {
                submitHandle();
              }}
              disabled={!comment}
              variant="contained"
              size="small"
            >
              <Intl id="comment" />
            </Button>
          </div>
        </div>
      </div>
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

export default CommentSection;

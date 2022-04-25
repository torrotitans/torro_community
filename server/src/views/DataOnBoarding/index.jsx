/* third lib*/
import React, { useState, useEffect, useMemo, useCallback } from "react";
import { FormattedMessage as Intl } from "react-intl";
import { useForm, useWatch } from "react-hook-form";
import ScrollBar from "react-perfect-scrollbar";
import { useNavigate } from "react-router-dom";

/* material-ui */

/* local components & methods */
import styles from "./styles.module.scss";
import FormItem from "@comp/FormItem";
import HeadLine from "@basics/HeadLine";
import Text from "@basics/Text";
import CallModal from "@basics/CallModal";
import Loading from "@assets/icons/Loading";
import TableTagDisplay from "@comp/TableTag";
import ResourceDetail from "@comp/ResourceDetail";
import {
  getOnBoardDataForm,
  getRequiredTableTag,
  getTableSchema,
  getHiveResource,
  getTags,
  getPolicys,
  raiseFormRequest,
} from "@lib/api";
import { SUCCESS } from "src/lib/data/callStatus";
import Button from "@basics/Button";
import { sendNotify } from "src/utils/systerm-error";
import TableSchema from "./TableSchema";

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
  const [searchQuery, setSearchQuery] = useState();
  const [tableData, setTableData] = useState(null);
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

  const tableTags = useMemo(() => {
    return tableData?.tags || [];
  }, [tableData]);

  const policyMap = useMemo(() => {
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

  const submitHandle = (data) => {
    setSearchQuery(data);
  };

  const closeModal = () => {
    setModalData({ ...modalData, open: false, cb: null });
  };

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
      let apiCall = resourceType === "GCP" ? getTableSchema : getHiveResource;
      apiCall(searchQuery)
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
  }, [searchQuery, requiredTableTag, resourceType]);

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
              <TableSchema
                tableData={tableData}
                tagTemplateList={tagTemplateList}
                policyMap={policyMap}
                tableTags={tableTags}
                fieldsChange={(fields) => {
                  let tmpData = JSON.parse(JSON.stringify(tableData));
                  tmpData.schema.fields = fields;
                  setTableData(tmpData);
                }}
                tableTagsChange={(data) => {
                  let tmpData = JSON.parse(JSON.stringify(tableData));
                  if (!tmpData.tags) {
                    tmpData.tags = [];
                  }
                  tmpData.tags = data;
                  setTableData(tmpData);
                }}
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

/* third lib*/
import React, { useEffect, useState, useCallback, useMemo } from "react";
import cn from "classnames";
import { useForm } from "react-hook-form";
import { FormattedMessage as Intl } from "react-intl";

/* material-ui */
import Delete from "@material-ui/icons/Close";

/* local components & methods */
import styles from "./styles.module.scss";
import Select from "@comp/basics/Select";
import { getTags, getFormItem } from "@lib/api";
import { sendNotify } from "src/utils/systerm-error";
import Text from "@comp/basics/Text";
import Button from "@comp/basics/Button";
import FormItem from "@comp/FormItem";

const AddTag = ({ handleApply, tagTemplateList, type, checkedTagList }) => {
  const [formData, setFormData] = useState();
  const { handleSubmit, control, register, reset } = useForm(); // initialise the hook
  const [tagList, setTagList] = useState(
    checkedTagList?.length > 0 ? checkedTagList : []
  );
  const [selectedTemplate, setSeletedTemplate] = useState("");
  const [currentTag, setCurrentTag] = useState({
    tag_template_form_id: "",
    data: {},
    seq: null,
  });

  const renderFormItem = (items, disabled) => {
    return items.map((item, index) => {
      return (
        <FormItem
          key={index + "default" + item.default}
          data={item}
          index={index}
          control={control}
          register={register}
          disabled={disabled}
          fullWidth
        />
      );
    });
  };

  const templateOption = useMemo(() => {
    let exist = tagList.map((item) => {
      return item.tag_template_form_id;
    });
    let tmp = tagTemplateList.map((item) => {
      return {
        label: item.display_name,
        value: item.tag_template_form_id,
      };
    });

    return tmp.filter((item) => {
      return !exist.includes(item.value);
    });
  }, [tagTemplateList, tagList]);

  const templateNameMap = useMemo(() => {
    let map = {};
    tagTemplateList.forEach((item) => {
      map[item.tag_template_form_id] = item.display_name;
    });

    return map;
  }, [tagTemplateList]);

  const TagTitle = useMemo(() => {
    if (type === 1) {
      return checkedTagList?.length > 0 ? (
        <Intl id="modifyTableTag" />
      ) : (
        <Intl id="addTableTag" />
      );
    } else {
      return checkedTagList?.length > 0 ? (
        <Intl id="modifyColumnTag" />
      ) : (
        <Intl id="addColumnTag" />
      );
    }
  }, [type, checkedTagList]);

  const submitHandle = useCallback(
    (data) => {
      let tmpList = [...tagList];
      if (currentTag.seq !== null) {
        tmpList[currentTag.seq] = {
          tag_template_form_id: currentTag.tag_template_form_id,
          data: data,
        };
      } else {
        tmpList.push({
          tag_template_form_id: currentTag.tag_template_form_id,
          data: data,
        });
      }
      setCurrentTag({
        tag_template_form_id: "",
        data: {},
        seq: null,
      });
      setSeletedTemplate("");
      setTagList(tmpList);
    },
    [tagList, currentTag]
  );

  const handleDeleteTag = useCallback(
    (index) => {
      let tmp = [...tagList];
      tmp.splice(index, 1);
      setTagList(tmp);
    },
    [tagList]
  );

  useEffect(() => {
    if (currentTag.tag_template_form_id) {
      getFormItem({ id: currentTag.tag_template_form_id })
        .then((res) => {
          if (res.data) {
            reset({});
            let tmpFieldList = res.data.fieldList;
            tmpFieldList = tmpFieldList.map((item) => {
              return {
                ...item,
                default: currentTag.data[item.id] || "",
              };
            });

            res.data.fieldList = tmpFieldList;
            setFormData(res.data);
          }
        })
        .catch((e) => {
          sendNotify({ msg: e.message, status: 3, show: true });
        });
    } else {
      reset();
      setFormData(null);
    }
  }, [currentTag, reset]);

  return (
    <div>
      <div className={styles.designerTitle}>
        <Text type="title">{TagTitle}</Text>
      </div>
      <div className={styles.selectTagTemplate}>
        <Select
          value={selectedTemplate}
          options={templateOption}
          onChange={(value) => {
            setSeletedTemplate(value);
            setCurrentTag({
              tag_template_form_id: value,
              data: {},
              seq: null,
            });
          }}
        />
      </div>
      {formData && (
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
              className={styles.button}
              size="small"
              type="submit"
              variant="contained"
            >
              {currentTag.seq !== null ? (
                <Intl id="update" />
              ) : (
                <Intl id="add" />
              )}
            </Button>
          </div>
        </form>
      )}

      <div className={styles.tagList}>
        <div className={styles.designerTitle}>
          <Text type="title">Tags ({tagList.length})</Text>
        </div>

        {tagList.map((item, index) => {
          return (
            <div
              onClick={() => {
                setSeletedTemplate("");
                setCurrentTag({
                  ...item,
                  seq: index,
                });
              }}
              key={index}
              className={styles.tagDisplay}
            >
              <span className={styles.delete}>
                <Delete
                  onClick={(e) => {
                    handleDeleteTag(index);
                    e.stopPropagation();
                  }}
                />
              </span>
              <span className={styles.policyName}>
                {templateNameMap[item.tag_template_form_id]}
              </span>
            </div>
          );
        })}
      </div>
      <div className={styles.buttonWrapper}>
        <Button
          className={styles.button}
          onClick={() => {
            if (tagList.length < 1) {
              sendNotify({
                msg: "Please add at least on tag",
                status: 3,
                show: true,
              });
              return;
            }
            handleApply(tagList, type === 1 ? "TABLETAG" : "COLUMNTAGS");
          }}
        >
          <Intl id="apply" />
        </Button>
      </div>
    </div>
  );
};

export default AddTag;

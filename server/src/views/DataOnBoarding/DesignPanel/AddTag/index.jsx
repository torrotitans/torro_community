/* third lib*/
import React, { useEffect, useState, useCallback, useMemo } from "react";
import cn from "classnames";
import { useForm } from "react-hook-form";
import { FormattedMessage as Intl } from "react-intl";

/* material-ui */
import Delete from "@material-ui/icons/Close";

/* local components & methods */
import styles from "./styles.module.scss";
import Select from "@basics/Select";
import { getFormItem } from "@lib/api";
import { sendNotify } from "src/utils/systerm-error";
import Text from "@basics/Text";
import Button from "@basics/Button";
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
        let tmpTag = tmpList[currentTag.seq];
        tmpList[currentTag.seq] = {
          ...tmpTag,
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

  const applyHandle = useCallback(() => {
    const applyType = type === 1 ? "TABLETAG" : "COLUMNTAGS";
    let avaliable = true;
    if (type === 1) {
      tagList.forEach((item) => {
        if (!item.data) {
          sendNotify({
            msg: "Please fill in the required tag",
            status: 3,
            show: true,
          });
          avaliable = false;
        }
      });
    }
    if (avaliable) {
      handleApply(tagList, applyType);
    }
  }, [tagList, handleApply, type]);

  const tagClickHandle = useCallback((tag) => {
    setSeletedTemplate("");
    setCurrentTag(tag);
  }, []);

  useEffect(() => {
    if (currentTag.tag_template_form_id) {
      getFormItem({ id: currentTag.tag_template_form_id })
        .then((res) => {
          if (res.data) {
            reset({});
            let tmpFieldList = res.data.fieldList;

            if (currentTag.data) {
              tmpFieldList = tmpFieldList.map((item) => {
                return {
                  ...item,
                  default: currentTag.data[item.id] || "",
                };
              });
            }

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

        {tagList.map((tag, index) => {
          return (
            <div
              onClick={() => {
                tagClickHandle({
                  ...tag,
                  seq: index,
                });
              }}
              key={index}
              className={cn(styles.tagDisplay, {
                [styles["alert"]]: tag?.required && tag.data === null,
              })}
            >
              {!tag.required && (
                <span className={styles.delete}>
                  <Delete
                    onClick={(e) => {
                      handleDeleteTag(index);
                      e.stopPropagation();
                    }}
                  />
                </span>
              )}
              <span className={styles.policyName}>
                {templateNameMap[tag.tag_template_form_id]}
              </span>
            </div>
          );
        })}
      </div>
      <div className={styles.buttonWrapper}>
        <Button className={styles.button} onClick={applyHandle}>
          <Intl id="apply" />
        </Button>
      </div>
    </div>
  );
};

export default AddTag;

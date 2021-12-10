/* third lib*/
import React, { useEffect, useState, useCallback, useMemo } from "react";
import cn from "classnames";
import { useForm } from "react-hook-form";
import { FormattedMessage as Intl } from "react-intl";

/* local components & methods */
import styles from "./styles.module.scss";
import Select from "@comp/Select";
import { getTags, getFormItem } from "@lib/api";
import { sendNotify } from "src/utils/systerm-error";
import Text from "@comp/Text";
import Button from "@comp/Button";
import FormItem from "@comp/FormItem";

const AddTag = ({ handleApply, tagTemplateList, type }) => {
  const [tagTemplate, setTagTemplate] = useState("");
  const [formData, setFormData] = useState();
  const { handleSubmit, control, register } = useForm(); // initialise the hook

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
          fullWidth
        />
      );
    });
  };

  const submitHandle = useCallback(
    (data) => {
      handleApply(
        {
          tag_template_form_id: tagTemplate,
          data: data,
        },
        type === 1 ? "TABLETAG" : "COLUMNTAGS"
      );
    },
    [handleApply, tagTemplate, type]
  );

  const templateOption = useMemo(() => {
    return tagTemplateList.map((item) => {
      return {
        label: item.display_name,
        value: item.tag_template_form_id,
      };
    });
  }, [tagTemplateList]);

  useEffect(() => {
    if (tagTemplate) {
      getFormItem({ id: tagTemplate })
        .then((res) => {
          if (res.data) {
            setFormData(res.data);
          }
        })
        .catch((e) => {
          sendNotify({ msg: e.message, status: 3, show: true });
        });
    }
  }, [tagTemplate]);

  return (
    <>
      <div className={styles.designerTitle}>
        <Text type="title">
          {type === 1 ? "Add table tag" : "Add column tags"}
        </Text>
      </div>
      <div className={styles.selectTagTemplate}>
        <Select
          value={tagTemplate}
          options={templateOption}
          onChange={(value) => {
            setTagTemplate(value);
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
              <Intl id="apply" />
            </Button>
          </div>
        </form>
      )}
    </>
  );
};

export default AddTag;

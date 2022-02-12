/* third lib*/
import React, { useEffect, useState } from "react";
import { FormattedMessage as Intl } from "react-intl";
import { useForm } from "react-hook-form";
import Scrollbar from "react-perfect-scrollbar";

/* material-ui */
import FormLabel from "@material-ui/core/FormLabel";

/* local components & methods */
import HeadLine from "@basics/HeadLine";
import FormItem from "@comp/FormItem";
import Button from "@basics/Button";
import Text from "@basics/Text";
import styles from "./styles.module.scss";
import { getPolicyForm, getPolicys } from "@lib/api";
import Loading from "@assets/icons/Loading";
import { sendNotify } from "src/utils/systerm-error";
import PolicyTags from "@comp/PolicyTags";

const Policy = ({ currentId, onBack }) => {
  const { control, register } = useForm(); // initialise the hook
  const [formData, setFormData] = useState(null);
  const [formLoading, setFormLoading] = useState(true);

  const [policTags, setPolicTags] = useState([]);

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

  useEffect(() => {
    getPolicyForm()
      .then((res) => {
        if (res.data) {
          let policyForm = res.data;

          getPolicys()
            .then((res) => {
              let policyTagData = res.data.filter(
                (item) => item.id === currentId
              )[0];

              let tmp = JSON.parse(JSON.stringify(policyForm));
              let tmpFieldList = tmp.fieldList.map((item) => {
                if (item.id && policyTagData[item.id]) {
                  item.default = policyTagData[item.id];
                }
                return item;
              });

              setPolicTags(policyTagData.policy_tags_list);
              setFormData({
                ...tmp,
                fieldList: tmpFieldList,
                title: "Polciy Tag",
              });
              setFormLoading(false);
            })
            .catch((e) => {
              sendNotify({ msg: e.message, status: 3, show: true });
            });
        }
      })
      .catch((e) => {
        sendNotify({ msg: e.message, status: 3, show: true });
      });
  }, [currentId]);

  return (
    <div className={styles.policy}>
      <div className={styles.formView}>
        <Scrollbar>
          {formLoading && <Loading />}
          {!formLoading && formData && (
            <div className={styles.formControl}>
              <HeadLine>{formData.title}</HeadLine>
              <form
                className={styles.form}
                id={`currentForm${formData.id}`}
                // onSubmit={handleSubmit(submitHandle)}
              >
                <div className={styles.formOptions}>
                  {renderFormItem(formData.fieldList)}
                </div>
                <div className={styles.formItemLine}>
                  <div className={styles.formItemTitle}>
                    <FormLabel className={styles.fieldTitle}>
                      <Text type="subTitle">
                        <Intl id="policyTagStru" />
                      </Text>
                    </FormLabel>
                  </div>
                  <PolicyTags
                    value={policTags}
                    onChange={(data) => {
                      setPolicTags(data);
                    }}
                    displayView={true}
                  />
                </div>
                <div className={styles.buttonWrapper}>
                  <Button
                    onClick={() => {
                      onBack();
                    }}
                    className={styles.button}
                    variant="contained"
                  >
                    <Intl id="back" />
                  </Button>
                </div>
              </form>
            </div>
          )}
        </Scrollbar>
      </div>
    </div>
  );
};

export default Policy;

/* third lib*/
import React from "react";
import Scrollbar from "react-perfect-scrollbar";
import cn from "classnames";
import { FormattedMessage as Intl } from "react-intl";

/* material-ui */
import AddIcon from "@material-ui/icons/Add";

/* local components & methods */
import styles from "./styles.module.scss";
import Text from "@comp/Text";
import Delete from "src/icons/Delete";

const FormSelection = ({
  formList,
  currentForm,
  formChange,
  addForm,
  deleteForm,
  tagTemplate,
}) => {
  return (
    <div id="formSelection" className={styles.formSelection}>
      <div className={styles.designerTitle}>
        <Text type="title">
          {tagTemplate ? "Design panel" : "Created form"}
        </Text>
      </div>
      {!tagTemplate && (
        <Scrollbar>
          <div className={styles.createdFormList}>
            {formList.map((item, index) => {
              return (
                <div
                  key={item.id}
                  className={cn(styles.createdFrom, {
                    [styles["active"]]:
                      currentForm && item.id === currentForm.id,
                  })}
                  onClick={() => {
                    formChange(item.id);
                  }}
                >
                  <Text type="subTitle">{item.title}</Text>
                  <Delete
                    onClick={() => {
                      deleteForm(item.id, index);
                    }}
                  />
                </div>
              );
            })}
          </div>
          {currentForm && currentForm.id !== "ADD" && (
            <div
              className={styles.addForm}
              onClick={() => {
                addForm();
              }}
            >
              <AddIcon />
              <Intl id="addForm" />
            </div>
          )}
        </Scrollbar>
      )}
    </div>
  );
};

export default FormSelection;

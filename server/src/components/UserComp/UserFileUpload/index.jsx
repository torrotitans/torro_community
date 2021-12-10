/* third lib*/
import React from "react";
import styles from "./styles.module.scss";

/* material-ui */
import FormLabel from "@material-ui/core/FormLabel";

/* local components & methods */
import Text from "@comp/Text";
import FileUpload from "@comp/FileUpload";

const UserFileUpload = React.forwardRef(({ id, name, label }, ref) => {
  let textId = id;
  let textLabel = label;
  return (
    <div className={styles.formControl}>
      <FormLabel className={styles.label}>
        <Text type="subTitle">{textLabel}</Text>
      </FormLabel>
      <FileUpload ref={ref} id={textId} name={name} />
    </div>
  );
});

export default UserFileUpload;

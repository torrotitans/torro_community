/* third lib*/
import React from "react";

import { Controller } from "react-hook-form";

/* material-ui */
import TextBox from "@comp/TextBox";
import FormLabel from "@material-ui/core/FormLabel";

/* local components */
import Text from "@comp/Text";
import styles from "./styles.module.scss";

const UserInput = ({
  id,
  name,
  control,
  label,
  type,
  placeholder,
  autoFocus,
}) => {
  let textId = id;
  let textLabel = label;
  let defaultValue = "";
  let textName = name;
  let textPlaceholder = placeholder || placeholder;
  let textType = type || "text";

  return (
    <div className={styles.formControl}>
      <FormLabel className={styles.label}>
        <Text type="subTitle">{textLabel}</Text>
      </FormLabel>
      <div className={styles.textInput}>
        <Controller
          name={textName}
          control={control}
          defaultValue={defaultValue}
          render={({
            field: { onChange, onBlur, value, name, ref },
            fieldState: { invalid, isTouched, isDirty, error },
            formState,
          }) => (
            <TextBox
              id={textId}
              name={name}
              value={value}
              onChange={onChange}
              placeholder={textPlaceholder}
              type={textType}
              autoFocus={autoFocus}
            />
          )}
        />
      </div>
    </div>
  );
};

export default UserInput;

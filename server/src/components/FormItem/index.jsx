/* third lib*/
import React, { useCallback, useMemo } from "react";
import cn from "classnames";
import { Controller } from "react-hook-form";
import { FormattedMessage as Intl } from "react-intl";

/* material-ui */
import FormLabel from "@material-ui/core/FormLabel";
import FormHelperText from "@material-ui/core/FormHelperText";
import Edit from "@material-ui/icons/Edit";
import Delete from "@material-ui/icons/Close";
import ArrowUpward from "@material-ui/icons/ArrowUpward";
import ArrowDownward from "@material-ui/icons/ArrowDownward";

/* local components & methods */
import Text from "@basics/Text";
import FileUpload from "@basics/FileUpload";
import DatePicker from "@basics/DatePicker";
import TextBox from "@basics/TextBox";
import Select from "@basics/Select";
import Switch from "@basics/Switch";
import PolicyTags from "@comp/PolicyTags";
import CheckBoxGroup from "@basics/CheckBoxGroup";
import RadioGroup from "@basics/RadioGroup";
import styles from "./styles.module.scss";

const FormItem = ({
  data,
  index,
  onDelete,
  onEdit,
  onUp,
  onDown,
  control,
  editState,
  enableEdit,
  register,
  disabled,
  systemTag,
  fullWidth,
  changeCb,
}) => {
  const FormComponent = useMemo(() => {
    let type = Number(data.style);
    switch (type) {
      case 1:
        return CheckBoxGroup;
      case 2:
        return Select;
      case 4:
        return FileUpload;
      case 5:
        return Switch;
      case 6:
        return DatePicker;
      case 7:
        return PolicyTags;
      case 8:
        return RadioGroup;
      default:
        return TextBox;
    }
  }, [data]);

  const dataProps = useMemo(() => {
    let type = Number(data.style);
    let name = `prop${data.id}`;
    switch (type) {
      case 1:
        return {
          options: data.options,
        };
      case 2:
        return {
          options: data.options,
        };
      case 4:
        return {
          ref: register,
          id: name,
          name: name,
          multiple: true,
        };
      case 5:
        return {};
      case 6:
        return {};
      case 8:
        return {
          options: data.options,
        };
      default:
        return {
          id: name,
          name: name,
          placeholder: data.placeholder,
          type: "text",
        };
    }
  }, [data, register]);

  const preFix = useCallback((style) => {
    switch (style) {
      case 2:
        return "selectEmpty";
      case 6:
        return "dateEmpty";
      default:
        return "textEmptpy";
    }
  }, []);

  const defaultValue = useMemo(() => {
    let type = Number(data.style);
    switch (type) {
      case 1:
        return data.default ? data.default : "";
      case 5:
        return data.default ? data.default : "false";
      case 6:
        return data.default ? new Date(data.default) : new Date();
      default:
        return data.default || "";
    }
  }, [data]);

  const pattern = useMemo(() => {
    switch (data.rule) {
      case 1: {
        return {
          value: /(^[1-9]([0-9]+)?(\.[0-9]{1,2})?$)|(^(0){1}$)|(^[0-9]\.[0-9]([0-9])?$)/,
          message: "Invalid amount, please check.",
        };
      }
      case 2:
        /* eslint-disable */
        return {
          value: /^([a-z0-9]*[-_]?[a-z0-9]+)*@([a-z0-9]*[-_]?[a-z0-9]+)+[\.][a-z]{2,3}([\.][a-z]{2})?$/i,
          message: "Please input correct email",
        };
      /* eslint-disable */

      case 3:
        return {
          value: /^(13[0-9]|14[01456879]|15[0-35-9]|16[2567]|17[0-8]|18[0-9]|19[0-35-9])\d{8}$/,
          message: "Please input correct phone number",
        };
      default:
        return { value: false };
    }
  }, [data.rule]);

  const maxLength = useMemo(() => {
    return {
      value: data.maxLength,
      message: `Please limit your input in ${data.maxLength} letters`,
    };
  }, [data.maxLength]);

  return (
    <div
      key={data.id}
      className={cn(styles.formItem, {
        [styles["edit"]]: editState,
        [styles["flex-basis"]]: data.style === 7,
        [styles["fullWidth"]]: fullWidth,
      })}
      style={{ width: data.width + "%" }}
      onDoubleClick={() => {
        onEdit && onEdit(true);
      }}
    >
      <div className={styles.formControl}>
        <FormLabel className={styles.label}>
          <Text type="subTitle" title={data.des}>
            {data.label}
            {systemTag && (
              <span className={styles.systemTag}>
                (<Intl id="system" />)
              </span>
            )}
            {data.required && <span className={styles.required}>*</span>}
          </Text>
        </FormLabel>
        <div className={styles.textInput}>
          <Controller
            name={`${data.id}`}
            control={control}
            defaultValue={defaultValue}
            rules={{
              required: {
                value: data.required,
                message: (
                  <>
                    <Intl id={preFix(data.style)} />
                    {data.label}.
                  </>
                ),
              },
              maxLength: maxLength,
              pattern: pattern,
            }}
            render={({
              field: { onChange, onBlur, value, name, ref },
              fieldState: { invalid, isTouched, isDirty, error },
              formState,
            }) => {
              return (
                <>
                  <FormComponent
                    {...dataProps}
                    value={value}
                    onChange={(data) => {
                      changeCb && changeCb(data);
                      onChange(data);
                    }}
                    disabled={disabled}
                    inputRef={ref}
                    error={invalid}
                    type={data.rule === 1 || data.rule === 3 ? "number" : ""}
                    maxLength={data.maxLength}
                  />
                  {invalid && (
                    <div className={styles.errorText}>
                      <FormHelperText>{error.message}</FormHelperText>
                    </div>
                  )}
                </>
              );
            }}
          />
        </div>
      </div>
      {enableEdit && (
        <div className={styles.operation}>
          {!editState && (
            <>
              <Edit
                className={styles.icon}
                onClick={(e) => {
                  e.stopPropagation();
                  onEdit(true);
                }}
              />
              <Delete className={styles.icon} onClick={onDelete} />
              {onUp && <ArrowUpward className={styles.icon} onClick={onUp} />}
              {onDown && (
                <ArrowDownward className={styles.icon} onClick={onDown} />
              )}
            </>
          )}
          {editState && (
            <Delete
              className={styles.icon}
              onClick={(e) => {
                e.stopPropagation();
                onEdit(false);
              }}
            />
          )}
        </div>
      )}
    </div>
  );
};

export default FormItem;

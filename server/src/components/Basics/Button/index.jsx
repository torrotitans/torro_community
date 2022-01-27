/* third lib */
import React from "react";
import cn from "classnames";

/* local components & methods */
import Text from "@basics/Text";
import styles from "./styles.module.scss";

const CustomButton = ({
  children,
  type,
  className,
  onClick,
  filled,
  size,
  disabled,
}) => {
  return (
    <button
      onClick={onClick}
      className={cn(
        styles.customButton,
        { [className]: className },
        { [styles["filled"]]: filled },
        { [styles[size]]: size },
        { [styles["disbaled"]]: disabled }
      )}
      type={type}
    >
      <Text type="subTitle">{children}</Text>
    </button>
  );
};

CustomButton.defaultProps = {
  type: "regular",
  filled: false,
};

export default CustomButton;

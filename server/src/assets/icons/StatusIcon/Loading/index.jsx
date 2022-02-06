/* third lib */
import React from "react";

/* material-ui */
import SvgIcon from "@material-ui/core/SvgIcon";
import styles from "./styles.module.scss";

function Loading(props) {
  return (
    <div className={styles.loading}>
      <SvgIcon
        {...props}
        width="30px"
        height="30px"
        viewBox="0 0 50 50"
        enableBackground="new 0 0 40 40"
        xmlSpace="preserve"
      >
        <path
          d="M25.251,6.461c-10.318,0-18.683,8.365-18.683,18.683h4.068c0-8.071,6.543-14.615,14.615-14.615V6.461z"
          transform="rotate(275.098 25 25)"
        >
          <animateTransform
            attributeType="xml"
            attributeName="transform"
            type="rotate"
            from="0 25 25"
            to="360 25 25"
            dur="0.6s"
            repeatCount="indefinite"
          ></animateTransform>
        </path>
      </SvgIcon>
    </div>
  );
}

export default Loading;

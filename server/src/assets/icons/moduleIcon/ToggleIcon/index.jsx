/* third lib */
import React from "react";

/* material-ui */
import SvgIcon from "@material-ui/core/SvgIcon";

function ToggleIcon(props) {
  return (
    <SvgIcon {...props} width="30.5" height="23" viewBox="0 0 30.5 23">
      <defs>
        <filter
          id="椭圆_48"
          x="7.5"
          y="0"
          width="23"
          height="23"
          filterUnits="userSpaceOnUse"
        >
          <feOffset dy="1" input="SourceAlpha" />
          <feGaussianBlur stdDeviation="1.5" result="blur" />
          <feFlood floodOpacity="0.212" />
          <feComposite operator="in" in2="blur" />
          <feComposite in="SourceGraphic" />
        </filter>
      </defs>
      <g
        id="Selection_Control_Switch_On_Enabled"
        data-name="Selection Control / Switch / On / Enabled"
        transform="translate(0 3.5)"
      >
        <rect
          id="矩形_576"
          data-name="矩形 576"
          width="20"
          height="8"
          rx="4"
          transform="translate(0 3)"
          opacity="0.4"
        />
        <g transform="matrix(1, 0, 0, 1, 0, -3.5)" filter="url(#椭圆_48)">
          <circle
            id="椭圆_48-2"
            data-name="椭圆 48"
            cx="7"
            cy="7"
            r="7"
            transform="translate(12 3.5)"
          />
        </g>
      </g>
    </SvgIcon>
  );
}

export default ToggleIcon;

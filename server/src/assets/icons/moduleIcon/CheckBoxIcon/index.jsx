/* third lib */
import React from "react";

/* material-ui */
import SvgIcon from "@material-ui/core/SvgIcon";

function CheckBoxIcon(props) {
  return (
    <SvgIcon {...props} width="24" height="24" viewBox="0 0 24 24">
      <defs>
        <clipPath id="clip-path">
          <rect width="24" height="24" fill="none" />
        </clipPath>
      </defs>
      <g id="组_303" data-name="组 303" transform="translate(0 -2)">
        <g
          id="Selection_Control_Checkbox_On_Enabled"
          data-name="Selection Control / Checkbox / On / Enabled"
          transform="translate(0 2)"
          clipPath="url(#clip-path)"
        >
          <path
            id="Selection_Control_Checkbox_On_Enabled-2"
            data-name="Selection Control / Checkbox / On / Enabled"
            d="M27.333-681H8.667A2.666,2.666,0,0,0,6-678.333v18.667A2.666,2.666,0,0,0,8.667-657H27.333A2.666,2.666,0,0,0,30-659.667v-18.667A2.666,2.666,0,0,0,27.333-681Zm-12,18.667L8.667-669l1.88-1.88,4.787,4.773,10.12-10.12,1.88,1.893Z"
            transform="translate(-6 681)"
          />
        </g>
      </g>
    </SvgIcon>
  );
}

export default CheckBoxIcon;

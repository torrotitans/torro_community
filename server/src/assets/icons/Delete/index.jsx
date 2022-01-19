/* third lib */
import React from "react";

/* material-ui */
import SvgIcon from "@material-ui/core/SvgIcon";

function Delete(props) {
  return (
    <SvgIcon {...props} width="20" height="20" viewBox="0 0 20 20">
      <path
        id="Close-2"
        data-name="Close"
        d="M10,11.818,1.818,20,0,18.181,8.181,10,0,1.818,1.818,0,10,8.181,18.181,0,20,1.818,11.818,10,20,18.181,18.181,20Z"
      />
    </SvgIcon>
  );
}

export default Delete;

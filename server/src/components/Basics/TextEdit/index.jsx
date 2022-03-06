/* third lib*/
import React, { useState, useRef, useMemo } from "react";
import cn from "classnames";

/* material-ui */
import Edit from "@material-ui/icons/Edit";
import Delete from "@material-ui/icons/Clear";

/* local components & methods */
import styles from "./styles.module.scss";

const TextEdit = ({ value, onChange, ...props }) => {
  const [editState, setEditState] = useState(false);
  const textDivRef = useRef();

  const showEdit = useMemo(() => {
    return !value.trim() ? true : false;
  }, [value]);

  return (
    <div className={styles.textEditor}>
      <div
        className={cn(styles.textEditorBox, {
          [styles["editState"]]: editState || showEdit,
        })}
      >
        <div
          className={styles.label}
          ref={textDivRef}
          contentEditable={editState}
          onInput={(e) => {}}
          suppressContentEditableWarning={true}
          onFocus={(e) => {
            textDivRef.current.focus();
            var range = document.createRange();
            var sel = window.getSelection();
            const el = textDivRef.current;
            range.setStart(el, 1);
            range.collapse(true);
            sel.removeAllRanges();
            sel.addRange(range);
          }}
          onBlur={(e) => {
            setEditState(false);
            onChange(e.target.innerText);
          }}
        >
          {value}
          <span></span>
        </div>

        {!editState && (
          <Edit
            className={styles.icon}
            onClick={() => {
              setEditState(true);
              setTimeout(() => {
                textDivRef.current.focus();
              });
            }}
          />
        )}
        {editState && (
          <Delete
            className={styles.icon}
            onClick={() => {
              setEditState(false);
            }}
          />
        )}
      </div>
    </div>
  );
};

export default TextEdit;

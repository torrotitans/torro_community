/* third lib*/
import React, { useState, useMemo, useRef } from "react";
import styles from "./styles.module.scss";
import Paper from "@material-ui/core/Paper";
import MenuItem from "@material-ui/core/MenuItem";
import Popper from "@material-ui/core/Popper";
import ClickAwayListener from "@material-ui/core/ClickAwayListener";
import MenuList from "@material-ui/core/MenuList";
import UploadIcon from "src/icons/moduleIcon/UploadIcon";
import { FormattedMessage as Intl } from "react-intl";
import { useEffect } from "react";
import DeleteIcon from "@material-ui/icons/Delete";

const FileUpload = React.forwardRef(({ id, name, multiple, onChange }, ref) => {
  const anchorRef = useRef(null);
  const inputRef = useRef(null);
  const [refWidth, setRefWidth] = useState(0);
  const [open, setOpen] = useState(false);
  const [fileList, setFileList] = useState([]);

  const handleClose = () => {
    setOpen(false);
  };
  const handleOpen = () => {
    if (fileList.length > 0) {
      setOpen(true);
    } else {
      inputRef.current.click();
    }
  };

  const handleChange = (list) => {
    setFileList(list);
    onChange(
      list.map((item) => {
        return item.file;
      })
    );
  };

  const popupOpen = useMemo(() => {
    return fileList.length > 0 ? open : false;
  }, [fileList, open]);

  useEffect(() => {
    if (open) {
      setRefWidth(anchorRef.current.offsetWidth);
    }
  }, [open]);

  return (
    <div ref={anchorRef} className={styles.fileUploadWraper}>
      <div className={styles.placeHolder} onClick={handleOpen}>
        <div className={styles.fileName}>
          {fileList.length > 0 ? (
            `${fileList.length} files added`
          ) : (
            <Intl id="attachFile" />
          )}
        </div>
        <div className={styles.icon}>
          <input
            ref={inputRef}
            id={id}
            name={name}
            type="file"
            onChange={(e) => {
              let tmpFile = [
                ...fileList,
                {
                  label: e.target.files[0].name,
                  value: e.target.files[0].name,
                  file: e.target.files[0],
                },
              ];
              handleChange(tmpFile);
            }}
            style={{ display: "none" }}
            onClick={(event) => {
              event.stopPropagation();
            }}
          />
          <UploadIcon
            onClick={(event) => {
              event.stopPropagation();
              event.preventDefault();
              inputRef.current.click();
            }}
          />
        </div>
      </div>

      <Popper
        placement="bottom"
        id="simple-menu"
        anchorEl={anchorRef.current}
        open={popupOpen}
      >
        <div className={styles.poppup} style={{ width: refWidth + "px" }}>
          <Paper className={styles.list}>
            <ClickAwayListener onClickAway={handleClose}>
              <MenuList value="">
                {fileList.map((option, index) => (
                  <MenuItem key={index} value={option.value}>
                    <div className={styles.menuItem}>
                      {option.label}
                      <DeleteIcon
                        onClick={() => {
                          let tmpFile = [...fileList];
                          tmpFile.splice(index);
                          handleChange(tmpFile);
                        }}
                      />
                    </div>
                  </MenuItem>
                ))}
              </MenuList>
            </ClickAwayListener>
          </Paper>
        </div>
      </Popper>
    </div>
  );
});

export default FileUpload;

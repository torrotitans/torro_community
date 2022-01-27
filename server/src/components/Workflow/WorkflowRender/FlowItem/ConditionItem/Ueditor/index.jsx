/* third lib*/
import React, { useEffect, useMemo, useState } from "react";

/* material-ui */
import InsertBtn from "@material-ui/core/Button";
import Menu from "@material-ui/core/Menu";
import MenuItem from "@material-ui/core/MenuItem";
import EditIcon from "@material-ui/icons/Edit";

/* local components & methods */
import styles from "./styles.module.scss";
import Button from "@basics/Button";
import Model from "@basics/Modal";

const SimpleMenu = ({ options, insert }) => {
  const [anchorEl, setAnchorEl] = useState(null);

  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  return (
    <div>
      <InsertBtn
        aria-controls="simple-menu"
        aria-haspopup="true"
        onClick={handleClick}
      >
        <span className={styles.menuBtn}> Insert option</span>
      </InsertBtn>
      <Menu
        id="simple-menu"
        anchorEl={anchorEl}
        keepMounted
        open={Boolean(anchorEl)}
        onClose={handleClose}
      >
        {options.map((item, index) => {
          return (
            <MenuItem
              key={index}
              onClick={() => {
                insert(index, item);
                handleClose();
              }}
            >
              {item.label}
            </MenuItem>
          );
        })}
      </Menu>
    </div>
  );
};

const Ueditor = ({ value, options, onChange, handleClose }) => {
  const [content, setContent] = useState("");
  const [ue, setUe] = useState(null);
  const [initicialValue, setIniticialValue] = useState("");

  const deCodeValue = () => {
    let tempDiv = document.createElement("div");
    tempDiv.innerHTML = content;
    if (!tempDiv.childNodes.length) {
      return "";
    }
    let elem = tempDiv.childNodes[0];
    let tmp = "";
    for (let i = 0; i < elem.childNodes.length; i++) {
      let value = elem.childNodes[i];
      if (
        (value.id && value.id.indexOf("s") !== -1) ||
        (value.id && value.id.indexOf("u") !== -1)
      ) {
        tmp += `$(${value.id})`;
      } else {
        tmp +=
          value instanceof HTMLElement
            ? value.innerText
            : value.textContent || value;
      }
    }

    return tmp;
  };
  useEffect(() => {
    let script = document.createElement("script");
    script.setAttribute(
      "src",
      "http://localhost:8080/ueditor/ueditor.config.js"
    );
    document.getElementsByTagName("head")[0].appendChild(script);
    script = document.createElement("script");
    script.setAttribute(
      "src",
      "http://localhost:8080/ueditor/ueditor.all.min.js"
    );
    document.getElementsByTagName("head")[0].appendChild(script);

    script.onload = () => {
      let UE = window.UE;
      var ue = UE.getEditor("container", {
        UEDITOR_HOME_URL: "http://localhost:8080/ueditor/",
        serverUrl: "/ueditor",
        initialFrameHeight: 150,
        toolbars: [[]],
        lang: "en",
        maximumWords: 100,
        elementPathEnabled: false,
      });

      ue.addListener("contentChange", () => {
        setContent(ue.getContent());
        window.a = ue.getContent();
      });

      setUe(ue);
    };
  }, []);

  useEffect(() => {
    var initialContent = value.replace(/\$\(u(\d+)\)/g, (...args) => {
      for (var i = 0; i < options.length; i++) {
        var tmpVariable = options[i];
        var tmpProp = tmpVariable.value;
        if (`$(${tmpProp})` === args[0]) {
          return `<span id='${tmpVariable.value}' style='color: #fff;background: #8fa0f5;border-radius: 4px;padding: 2px;-webkit-user-modify:read-only;-moz-user-modify:read-only;user-modify:read-only;'>${tmpVariable.label}</span>`;
        }
      }
    });
    initialContent = initialContent.replace(/\$\(s(\d+)\)/g, (...args) => {
      for (var i = 0; i < options.length; i++) {
        var tmpVariable = options[i];
        var tmpProp = tmpVariable.value;
        if (`$(${tmpProp})` === args[0]) {
          return `<span id='${tmpVariable.value}' style='color: #fff;background: #8fa0f5;border-radius: 4px;padding: 2px;-webkit-user-modify:read-only;-moz-user-modify:read-only;user-modify:read-only;'>${tmpVariable.label}</span>`;
        }
      }
    });
    setIniticialValue(initialContent);
  }, [value, options]);

  return (
    <Model open={true}>
      <div className={styles.ueditor}>
        <div className={styles.operation}>
          <SimpleMenu
            options={options}
            insert={(index, data) => {
              ue.execCommand(
                "inserthtml",
                `<span id='${data.value}' style='color: #fff;background: #8fa0f5;border-radius: 4px;padding: 2px;-webkit-user-modify:read-only;-moz-user-modify:read-only;user-modify:read-only;'>${data.label}</span>`
              );
            }}
          />
        </div>
        <textarea
          id="container"
          name="blog"
          type="text/plain"
          onChange={() => {}}
          value={initicialValue}
        ></textarea>
      </div>
      <div className={styles.modelOperation}>
        <div className={styles.clear}>
          <Button
            onClick={() => {
              handleClose && handleClose();
            }}
            size="small"
          >
            cancel
          </Button>
        </div>
        <div className={styles.finish}>
          <Button
            onClick={() => {
              onChange(deCodeValue());
              handleClose();
            }}
            size="small"
            filled
          >
            Done
          </Button>
        </div>
      </div>
    </Model>
  );
};
const Default = ({ value, options, onChange }) => {
  const [open, setOpen] = useState(false);
  const displayValue = useMemo(() => {
    var initialContent = value.replace(/\$\(u(\d+)\)/g, (...args) => {
      for (var i = 0; i < options.length; i++) {
        var tmpVariable = options[i];
        var tmpProp = tmpVariable.value;
        if (`$(${tmpProp})` === args[0]) {
          return `<span id='${tmpVariable.value}' style='color: #fff;background: #8fa0f5;border-radius: 4px;padding: 2px;-webkit-user-modify:read-only;-moz-user-modify:read-only;user-modify:read-only;'>${tmpVariable.label}</span>`;
        }
      }
    });
    initialContent = initialContent.replace(/\$\(s(\d+)\)/g, (...args) => {
      for (var i = 0; i < options.length; i++) {
        var tmpVariable = options[i];
        var tmpProp = tmpVariable.value;
        if (`$(${tmpProp})` === args[0]) {
          return `<span id='${tmpVariable.value}' style='color: #fff;background: #8fa0f5;border-radius: 4px;padding: 2px;-webkit-user-modify:read-only;-moz-user-modify:read-only;user-modify:read-only;'>${tmpVariable.label}</span>`;
        }
      }
    });
    return initialContent;
  }, [value, options]);

  return (
    <>
      <div className={styles.valueBox}>
        <div className={styles.displayBox}>
          <div className={styles.displayValue}>
            <div dangerouslySetInnerHTML={{ __html: displayValue }}></div>
          </div>

          <div className={styles.editBtn}>
            <EditIcon
              onClick={() => {
                setOpen(true);
              }}
            />
          </div>
        </div>
      </div>
      {open && (
        <Ueditor
          value={value}
          options={options}
          onChange={onChange}
          handleClose={() => {
            setOpen(false);
          }}
        />
      )}
    </>
  );
};

export default Default;

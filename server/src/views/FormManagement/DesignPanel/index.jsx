/* third lib*/
import React, { useEffect, useState } from "react";
import Scrollbar from "react-perfect-scrollbar";

/* local components & methods */
import styles from "./styles.module.scss";
import FormSelection from "./FormSelection";
import ModuleSelection from "./ModuleSelection";
import { getFieldTemplate } from "@lib/api";
import { sendNotify } from "src/utils/systerm-error";

const DesignPanel = ({
  formList,
  currentForm,
  currentModule,
  onChange,
  formChange,
  addForm,
  deleteForm,
  tagTemplate,
  existIdList,
}) => {
  const [template, setTemplate] = useState([]);

  useEffect(() => {
    getFieldTemplate()
      .then((res) => {
        if (res) {
          let dynamic = res.data.dynamic;
          let system = res.data.system;
          setTemplate([
            {
              style: 1,
              default: {
                style: 1,
                label: "CheckBox",
                default: "",
                options: [{ label: "true" }, { label: "false" }],
              },
              systemList: system[1],
              dynamicList: dynamic[1],
            },
            {
              style: 2,
              default: {
                style: 2,
                label: "Dropdown",
                default: "",
                options: [
                  { label: "Option1", value: "Option1" },
                  { label: "Option2", value: "Option2" },
                ],
              },
              systemList: system[2],
              dynamicList: dynamic[2],
            },
            {
              style: 3,
              default: {
                style: 3,
                label: "Text",
                placeholder: "",
                default: "",
              },
              systemList: system[3],
              dynamicList: dynamic[3],
            },
            {
              style: 4,
              default: {
                style: 4,
                label: "Upload",
                placeholder: "",
                default: "",
                multiple: false,
              },
              systemList: system[4],
              dynamicList: dynamic[4],
            },
            {
              style: 5,
              default: {
                style: 5,
                label: "Switch",
                default: true,
                placeholder: "",
              },
              systemList: system[5],
              dynamicList: dynamic[5],
            },
            {
              style: 6,
              default: {
                style: 6,
                label: "DatePicker",
                placeholder: "",
                default: "",
              },
              systemList: system[6],
              dynamicList: dynamic[6],
            },
          ]);
        }
      })
      .catch((e) => {
        sendNotify({
          msg: "Get field template error.",
          status: 3,
          show: true,
        });
      });
  }, []);

  return (
    <div id="designPanel" className={styles.designerPanel}>
      {!currentModule && (
        <FormSelection
          formList={formList}
          currentForm={currentForm}
          formChange={formChange}
          addForm={addForm}
          deleteForm={deleteForm}
          tagTemplate={tagTemplate}
        />
      )}
      {currentModule && (
        <Scrollbar>
          <ModuleSelection
            template={template}
            data={currentModule}
            onChange={onChange}
            tagTemplate={tagTemplate}
            existIdList={existIdList}
          />
        </Scrollbar>
      )}
    </div>
  );
};

export default DesignPanel;

/* third lib*/
import React, { useEffect, useState } from "react";
import { FormattedMessage as Intl } from "react-intl";

/* material-ui */
import Paper from "@material-ui/core/Paper";

/* local components & methods */
import Text from "@comp/Text";
import { getTags, getFormItem } from "@lib/api";
import styles from "./styles.module.scss";
import { sendNotify } from "src/utils/systerm-error";
import {
  Table,
  TableBody,
  TableContainer,
  TableHead,
  TableRow,
  TableCell,
} from "@comp/Table";

const TableTagDisplay = ({ tags }) => {
  const [formData, setFormData] = useState(null);
  useEffect(() => {
    if (tags) {
      getFormItem({ id: tags[0].tag_template_form_id })
        .then((res) => {
          if (res.data) {
            let data = res.data;
            data.fieldList.map((item) => {
              item.default = tags[0].data[item.id] || "";
              return item;
            });
            setFormData(data);
          }
        })
        .catch((e) => {
          sendNotify({ msg: e.message, status: 3, show: true });
        });
    }
  }, [tags]);

  return (
    <div>
      {formData && (
        <>
          <div className={styles.designerTitle}>
            <Text type="title">Tags ({tags.length})</Text>
          </div>

          <div className={styles.tagCards}>
            <div className={styles.title}>{formData.title}</div>
            <div className={styles.tagDetail}>
              <TableContainer component={Paper}>
                <Table size="small" aria-label="a dense table">
                  <TableHead>
                    <TableRow>
                      <TableCell width="30%" align="center">
                        <Intl id="label"></Intl>
                      </TableCell>
                      <TableCell width="70%" align="center">
                        <Intl id="value"></Intl>
                      </TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {formData.fieldList.map((row, index) => {
                      return (
                        <TableRow key={index}>
                          <TableCell width="30%" align="center">
                            {row.label}
                          </TableCell>
                          <TableCell width="70%" align="center">
                            {row.default}
                          </TableCell>
                        </TableRow>
                      );
                    })}
                  </TableBody>
                </Table>
              </TableContainer>
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default TableTagDisplay;

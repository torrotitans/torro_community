/* third lib*/
import React, { useEffect, useState } from "react";
import { FormattedMessage as Intl } from "react-intl";

/* material-ui */
import Paper from "@material-ui/core/Paper";

/* local components & methods */
import { getFormItem } from "@lib/api";
import styles from "./styles.module.scss";
import { sendNotify } from "src/utils/systerm-error";
import Loading from "@assets/icons/Loading";
import {
  Table,
  TableBody,
  TableContainer,
  TableHead,
  TableRow,
  TableCell,
} from "@basics/Table";

const TableTag = ({ tagData }) => {
  const [formData, setFormData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (tagData) {
      getFormItem({ id: tagData.tag_template_form_id })
        .then((res) => {
          if (res.data) {
            let data = res.data;
            if (tagData.data) {
              data.fieldList.map((item) => {
                item.default = tagData.data[item.id] || "";
                return item;
              });
            }
            setFormData(data);
            setLoading(false);
          }
        })
        .catch((e) => {
          sendNotify({ msg: e.message, status: 3, show: true });
        });
    }
  }, [tagData]);

  return (
    <div className={styles.tagCards}>
      {loading && <Loading />}
      {!loading && (
        <>
          <div className={styles.title}>{formData.title}</div>
          {tagData.required && (
            <div className={styles.required}>
              <Intl id="required_" />
            </div>
          )}
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
        </>
      )}
    </div>
  );
};

export default TableTag;

/* third lib*/
import React, { useEffect, useState } from "react";

/* material-ui */
import Paper from "@material-ui/core/Paper";

/* local components & methods */
import Text from "@basics/Text";
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
import { covertToHKTime } from "src/utils/timeFormat";

const TagDisplay = ({ tagData }) => {
  const [formData, setFormData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (tagData) {
      getFormItem({ id: tagData.tag_template_form_id })
        .then((res) => {
          if (res.data) {
            let data = res.data;
            data.fieldList.map((item) => {
              item.default = tagData.data[item.id] || "";
              return item;
            });
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
    <div className={styles.tagDisplay}>
      {loading && <Loading />}
      {!loading && (
        <>
          <div className={styles.TagTitle}>
            <Text type="title">{formData.title}</Text>
          </div>
          <div className={styles.tagDetail}>
            <TableContainer component={Paper}>
              <Table size="small" aria-label="a dense table">
                <TableHead>
                  <TableRow>
                    <TableCell width="30%" align="center">
                      Label
                    </TableCell>
                    <TableCell width="70%" align="center">
                      Value
                    </TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {formData.fieldList.map((row, index) => {
                    let isDate = row.style === 6;
                    return (
                      <TableRow key={index}>
                        <TableCell width="30%" align="center">
                          {row.label}
                        </TableCell>
                        <TableCell width="70%" align="center">
                          {isDate ? covertToHKTime(row.default) : row.default}
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

export default TagDisplay;

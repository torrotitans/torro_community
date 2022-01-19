/* third lib*/
import React, { useState, useEffect, useMemo } from "react";
import { FormattedMessage as Intl } from "react-intl";

/* material-ui */
import Paper from "@material-ui/core/Paper";
import TablePagination from "@material-ui/core/TablePagination";
import ArrowBackIcon from "@material-ui/icons/ArrowBack";

/* local components & methods */
import styles from "./styles.module.scss";
import Loading from "@assets/icons/Loading";
import Text from "@basics/Text";
import { getTableSchema } from "@lib/api";
import { sendNotify } from "src/utils/systerm-error";
import {
  Table,
  TableBody,
  TableContainer,
  TableHead,
  TableRow,
  TableCell,
} from "@basics/Table";

const TableView = ({ tableId, onBack }) => {
  const [formLoading, setFormLoading] = useState(false);
  const [tableList, setTableList] = useState([]);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);

  const filterTableList = useMemo(() => {
    if (!tableList) {
      return [];
    }
    let tmpList = tableList;
    return tmpList.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage);
  }, [tableList, page, rowsPerPage]);

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  useEffect(() => {
    if (tableId) {
      setFormLoading(true);
      getTableSchema({ id: tableId })
        .then((res) => {
          setTableList(res.schema.fields);
          setFormLoading(false);
        })
        .catch((e) => {
          sendNotify({ msg: e.message, status: 3, show: true });
        });
    }
  }, [tableId]);

  return (
    <div className={styles.tableView}>
      <div className={styles.onBack} onClick={onBack}>
        <ArrowBackIcon />
        <Text type="subTitle">
          <Intl id="back" />
        </Text>
      </div>
      {formLoading && <Loading></Loading>}
      {!formLoading && tableList && (
        <>
          <TableContainer component={Paper}>
            <Table aria-label="simple table">
              <TableHead>
                <TableRow>
                  <TableCell align="center">
                    <Text type="subTitle">
                      <Intl id="fieldName" />
                    </Text>
                  </TableCell>
                  <TableCell align="center">
                    <Text type="subTitle">
                      <Intl id="type" />
                    </Text>
                  </TableCell>
                  <TableCell align="center">
                    <Text type="subTitle">
                      <Intl id="mode" />
                    </Text>
                  </TableCell>
                  <TableCell align="center">
                    <Text type="subTitle">
                      <Intl id="policyTag" />
                    </Text>
                  </TableCell>
                  <TableCell align="center" width="25%">
                    <Text type="subTitle">
                      <Intl id="description" />
                    </Text>
                  </TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {filterTableList.map((row, rowIndex) => (
                  <TableRow key={rowIndex}>
                    <TableCell align="center">{row.name}</TableCell>
                    <TableCell align="center">{row.type}</TableCell>
                    <TableCell align="center">{row.mode}</TableCell>
                    <TableCell align="center">
                      {row.policyTags &&
                        row.policyTags.names.map((item, index) => {
                          return (
                            <div className={styles.policyTag} key={index}>
                              {item}
                            </div>
                          );
                        })}
                    </TableCell>
                    <TableCell align="center">{row.description}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
          <TablePagination
            rowsPerPageOptions={[5, 10, 25]}
            component="div"
            count={tableList.length}
            rowsPerPage={rowsPerPage}
            page={page}
            onChangePage={handleChangePage}
            onChangeRowsPerPage={handleChangeRowsPerPage}
          />
        </>
      )}
    </div>
  );
};

export default TableView;

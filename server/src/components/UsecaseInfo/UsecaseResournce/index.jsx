/* third lib*/
import React, { useCallback, useState } from "react";
import { FormattedMessage as Intl } from "react-intl";

/* material-ui */
import Paper from "@material-ui/core/Paper";
import TablePagination from "@material-ui/core/TablePagination";

/* local components & methods */
import styles from "./styles.module.scss";
import {
  Table,
  TableBody,
  TableContainer,
  TableHead,
  TableRow,
  TableCell,
} from "@basics/Table";
import Text from "@basics/Text";

const UsecaseResournce = ({ resoureList }) => {
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);

  const handleChangePage = useCallback((event, newPage) => {
    setPage(newPage);
  }, []);

  const handleChangeRowsPerPage = useCallback((event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  }, []);

  return (
    <div className={styles.usecaseResournce}>
      <div className={styles.detailBox}>
        <div className={styles.secondTitle}>
          <Text type="title">
            <Intl id="gcpResources" />
          </Text>
        </div>
        {resoureList && resoureList.length > 0 && (
          <>
            <TableContainer component={Paper}>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell align="center">
                      <Text type="subTitle">
                        <Intl id="resourceName"></Intl>
                      </Text>
                    </TableCell>
                    <TableCell align="center">
                      <Text type="subTitle">
                        <Intl id="resourceLabel" />
                      </Text>
                    </TableCell>
                    <TableCell align="center">
                      <Text type="subTitle">
                        <Intl id="accessTime" />
                      </Text>
                    </TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {resoureList.map((data, accessIndex) => (
                    <TableRow key={accessIndex}>
                      <TableCell align="center">
                        <Text>{data.resource_name}</Text>
                      </TableCell>
                      <TableCell align="center">
                        <Text>{data.resource_label}</Text>
                      </TableCell>
                      <TableCell align="center">
                        <Text>{data.create_time}</Text>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
            <TablePagination
              rowsPerPageOptions={[5, 10, 25]}
              component="div"
              count={3}
              rowsPerPage={rowsPerPage}
              page={page}
              onChangePage={handleChangePage}
              onChangeRowsPerPage={handleChangeRowsPerPage}
            />
          </>
        )}
      </div>
    </div>
  );
};

export default UsecaseResournce;

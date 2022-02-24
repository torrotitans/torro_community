import React, { useMemo, useState } from "react";
import { FormattedMessage as Intl } from "react-intl";

/* material-ui */
import Paper from "@material-ui/core/Paper";
import TablePagination from "@material-ui/core/TablePagination";

/* local component */
import {
  Table,
  TableBody,
  TableContainer,
  TableHead,
  TableRow,
  TableCell,
} from "@basics/Table";

const GroupListTable = ({ data, onChange }) => {
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(5);

  const tableList = useMemo(() => {
    if (data.length > 1) {
      return data.filter((item, index) => index !== 0);
    } else {
      return [];
    }
  }, [data]);

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

  return (
    <>
      <TableContainer component={Paper}>
        <Table aria-label="collapsible table">
          <TableHead>
            <TableRow>
              <TableCell align="center">
                <Intl id="ucOwnerGroup" />
              </TableCell>
              <TableCell align="center">
                <Intl id="ucTeamGroup" />
              </TableCell>
              <TableCell align="center">
                <Intl id="adminServiceAcc" />
              </TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {filterTableList.map((rowArr, index) => {
              return (
                <TableRow key={index}>
                  <TableCell align="center">{rowArr[0]}</TableCell>
                  <TableCell align="center">{rowArr[1]}</TableCell>
                  <TableCell align="center">{rowArr[2]}</TableCell>
                </TableRow>
              );
            })}
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
  );
};

export default GroupListTable;

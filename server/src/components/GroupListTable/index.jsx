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
import TextBox from "@basics/TextBox";
import { useCallback } from "react";

const GroupListTable = ({ data, onChange, editable = true }) => {
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(5);

  const filterTableList = useMemo(() => {
    if (!data) {
      return [];
    }
    let tmpList = data;
    return tmpList.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage);
  }, [data, page, rowsPerPage]);

  const setData = useCallback(
    (index, valueIndex, value) => {
      let tmpData = [...data];
      let currentFied = tmpData[page * rowsPerPage + index].resource;
      currentFied[valueIndex] = value;
      onChange(tmpData);
    },
    [data, page, rowsPerPage, onChange]
  );

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
              <TableCell align="center">
                <Intl id="useCase" />
              </TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {filterTableList.map((item, index) => {
              let rowArr = item.resource;
              return (
                <TableRow key={index}>
                  <TableCell align="center">
                    {editable ? (
                      <TextBox
                        value={rowArr[0]}
                        onChange={(value) => {
                          setData(index, 0, value);
                        }}
                      />
                    ) : (
                      rowArr[0]
                    )}
                  </TableCell>
                  <TableCell align="center">
                    {editable ? (
                      <TextBox
                        value={rowArr[1]}
                        onChange={(value) => {
                          setData(index, 1, value);
                        }}
                      />
                    ) : (
                      rowArr[1]
                    )}
                  </TableCell>
                  <TableCell align="center">
                    {editable ? (
                      <TextBox
                        value={rowArr[2]}
                        onChange={(value) => {
                          setData(index, 2, value);
                        }}
                      />
                    ) : (
                      rowArr[2]
                    )}
                  </TableCell>
                  <TableCell align="center">{rowArr[3]}</TableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </TableContainer>
      <TablePagination
        rowsPerPageOptions={[5, 10, 25]}
        component="div"
        count={data.length}
        rowsPerPage={rowsPerPage}
        page={page}
        onChangePage={handleChangePage}
        onChangeRowsPerPage={handleChangeRowsPerPage}
      />
    </>
  );
};

export default GroupListTable;

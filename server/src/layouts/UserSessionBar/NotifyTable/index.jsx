/* third lib*/
import React, { useState, useMemo } from "react";
import { FormattedMessage as Intl } from "react-intl";
import cn from "classnames";
import ScrollBar from "react-perfect-scrollbar";

/* material-ui */
import Paper from "@material-ui/core/Paper";
import VisibilityIcon from "@material-ui/icons/Visibility";
import EmailIcon from "@material-ui/icons/Email";
import TablePagination from "@material-ui/core/TablePagination";
import MarkUnreadChatAltIcon from "@assets/icons/MarkUnreadChatAlt";

/* local components & methods */
import Text from "@basics/Text";
import styles from "./styles.module.scss";
import {
  Table,
  TableBody,
  TableContainer,
  TableHead,
  TableRow,
  TableCell,
} from "@basics/Table";

const NotifyTable = ({ notify, viewRequest, unRead, readAll }) => {
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);

  const filterTableList = useMemo(() => {
    if (!notify) {
      return [];
    }
    let tmpList = notify;
    return tmpList.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage);
  }, [notify, page, rowsPerPage]);

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  return (
    <ScrollBar>
      <div className={styles.notifyTable}>
        <div className={styles.notifyTitle}>
          <Text type="subTitle">
            <Intl id="youGot" />{" "}
            <span className={styles.unread}>{unRead.length}</span>{" "}
            <Intl id="unread" />
          </Text>
          <div className={styles.readAll} onClick={readAll}>
            <Text type="subTitle">
              <Intl id="readAll" />
            </Text>
          </div>
        </div>

        <TableContainer component={Paper}>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell width="10%" align="center">
                  <Intl id="notifyID"></Intl>
                </TableCell>
                <TableCell width="20%" align="center">
                  <Intl id="formName"></Intl>
                </TableCell>
                <TableCell width="40%" align="center">
                  <Intl id="msg"></Intl>
                </TableCell>
                <TableCell width="20%" align="center">
                  <Intl id="time"></Intl>
                </TableCell>
                <TableCell width="10%" align="center">
                  <Intl id="operation"></Intl>
                </TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {filterTableList.map((row, index) => {
                return (
                  <TableRow
                    key={index}
                    className={cn(styles.recordRow, {
                      [styles["active"]]: row.is_read === 0,
                    })}
                  >
                    <TableCell width="10%" align="center">
                      {row.id}
                    </TableCell>
                    <TableCell width="20%" align="center">
                      {row.title}
                    </TableCell>
                    <TableCell width="40%" align="center">
                      {row.comment}
                    </TableCell>
                    <TableCell width="20%" align="center">
                      {row.create_time}
                    </TableCell>
                    <TableCell width="10%" align="center">
                      <div
                        onClick={() => {
                          viewRequest(row.input_form_id, row.id);
                        }}
                        className={styles.viewIcon}
                      >
                        {row.is_read === 0 && <MarkUnreadChatAltIcon />}
                        {row.is_read === 1 && <EmailIcon />}
                      </div>
                    </TableCell>
                  </TableRow>
                );
              })}
            </TableBody>
          </Table>
        </TableContainer>
        <TablePagination
          rowsPerPageOptions={[5, 10, 25]}
          component="div"
          count={notify.length}
          rowsPerPage={rowsPerPage}
          page={page}
          onChangePage={handleChangePage}
          onChangeRowsPerPage={handleChangeRowsPerPage}
        />
      </div>
    </ScrollBar>
  );
};

export default NotifyTable;

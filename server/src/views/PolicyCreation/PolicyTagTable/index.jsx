/* third lib*/
import React, { useEffect, useState, useMemo } from "react";
import { FormattedMessage as Intl } from "react-intl";
import { useNavigate } from "react-router-dom";

/* material-ui */
import EditIcon from "@material-ui/icons/Edit";
import Paper from "@material-ui/core/Paper";
import TablePagination from "@material-ui/core/TablePagination";

/* local components & methods */
import styles from "./styles.module.scss";
import HeadLine from "@basics/HeadLine";
import Text from "@basics/Text";
import Button from "@basics/Button";
import Loading from "@assets/icons/Loading";
import { getPolicys } from "@lib/api";
import { sendNotify } from "src/utils/systerm-error";
import {
  Table,
  TableBody,
  TableContainer,
  TableHead,
  TableRow,
  TableCell,
} from "@basics/Table";

const PolicyTagTable = ({ setStep, setCurrentId }) => {
  const navigate = useNavigate();

  const [policyTagList, setPolicyTagList] = useState([]);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [formLoading, setFormLoading] = useState(true);

  const filterTableList = useMemo(() => {
    let tmpList = policyTagList;
    return tmpList.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage);
  }, [policyTagList, page, rowsPerPage]);

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  useEffect(() => {
    getPolicys()
      .then((res) => {
        setPolicyTagList(res.data);
        setFormLoading(false);
      })
      .catch((e) => {
        sendNotify({ msg: e.message, status: 3, show: true });
      });
  }, []);

  return (
    <div>
      <div className={styles.title}>
        <HeadLine>
          <Intl id="policyMan" />
        </HeadLine>
      </div>
      <div className={styles.filter}>
        <Button
          filled
          onClick={() => {
            navigate(`/app/forms?id=3`);
          }}
        >
          <Intl id="addPolicy" />
        </Button>
      </div>
      {formLoading && <Loading></Loading>}
      {!formLoading && (
        <>
          <TableContainer component={Paper}>
            <Table aria-label="simple table">
              <TableHead>
                <TableRow>
                  <TableCell align="center">
                    <Text type="subTitle">
                      <Intl id="policyId" />
                    </Text>
                  </TableCell>
                  <TableCell align="center">
                    <Text type="subTitle">
                      <Intl id="policyName" />
                    </Text>
                  </TableCell>
                  <TableCell align="center">
                    <Text type="subTitle">
                      <Intl id="description" />
                    </Text>
                  </TableCell>
                  <TableCell align="center">
                    <Text type="subTitle">
                      <Intl id="createtime" />
                    </Text>
                  </TableCell>
                  <TableCell align="center">
                    <Text type="subTitle">
                      <Intl id="operation" />
                    </Text>
                  </TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {filterTableList.map((row, index) => (
                  <TableRow key={index}>
                    <TableCell align="center">{row.id}</TableCell>
                    <TableCell align="center">
                      {row.taxonomy_display_name}
                    </TableCell>
                    <TableCell align="center">{row.description}</TableCell>
                    <TableCell align="center">{row.create_time}</TableCell>
                    <TableCell align="center">
                      <div className={styles.operation}>
                        <EditIcon
                          onClick={() => {
                            setCurrentId(row.id);
                            setStep(1);
                          }}
                        />
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
          <TablePagination
            rowsPerPageOptions={[5, 10, 25]}
            component="div"
            count={policyTagList.length}
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

export default PolicyTagTable;

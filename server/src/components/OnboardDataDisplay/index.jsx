/* third lib*/
import React, { useState, useEffect, useMemo } from "react";
import { FormattedMessage as Intl } from "react-intl";
import ScrollBar from "react-perfect-scrollbar";

/* material-ui */
import Paper from "@material-ui/core/Paper";
import TablePagination from "@material-ui/core/TablePagination";

/* local components & methods */
import styles from "./styles.module.scss";
import Text from "@basics/Text";
import Loading from "@assets/icons/Loading";
import { getTags, getPolicys } from "@lib/api";
import { sendNotify } from "src/utils/systerm-error";
import { openTips } from "src/utils/systemTips";
import {
  Table,
  TableBody,
  TableContainer,
  TableHead,
  TableRow,
  TableCell,
} from "@basics/Table";

const OnboardDataDisplay = ({ tableList }) => {
  const [policys, setPolicys] = useState([]);
  const [formLoading, setFormLoading] = useState(false);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [tagTemplateList, setTagTempalteList] = useState([]);

  const tagTemplateMap = useMemo(() => {
    let map = {};
    tagTemplateList.forEach((item) => {
      map[item.tag_template_form_id] = item.display_name;
    });
    return map;
  }, [tagTemplateList]);

  const filterTableList = useMemo(() => {
    if (!tableList) {
      return [];
    }
    let tmpList = tableList;
    return tmpList.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage);
  }, [tableList, page, rowsPerPage]);

  const policMap = useMemo(() => {
    let map = {};
    if (policys.length > 0) {
      policys.forEach((item) => {
        if (item.policy_tags_dict) {
          map = {
            ...map,
            ...item.policy_tags_dict,
          };
        }
      });
    }
    return map;
  }, [policys]);

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  useEffect(() => {
    setFormLoading(true);
    Promise.all([getPolicys(), getTags()])
      .then((res) => {
        let res1 = res[0];
        let res2 = res[1];

        if (res1.data && res2.data) {
          setPolicys(res1.data);
          setTagTempalteList(res2.data);
          setFormLoading(false);
        }
      })
      .catch((e) => {
        sendNotify({ msg: e.message, status: 3, show: true });
      });
  }, []);

  return (
    <div className={styles.dataOnboarding}>
      <ScrollBar>
        {formLoading && <Loading></Loading>}
        {!formLoading && (
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
                        <Intl id="ColumnTags" />
                      </Text>
                    </TableCell>
                    <TableCell align="center">
                      <Text type="subTitle">
                        <Intl id="policyTagOr" />
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
                        {row.tags &&
                          row.tags.map((item, index) => {
                            return (
                              <div key={index}>
                                {tagTemplateMap[item.tag_template_form_id] && (
                                  <div
                                    className={styles.columnTag}
                                    key={index}
                                    onClick={() => {
                                      openTips({
                                        style: 1,
                                        tagData: item,
                                      });
                                    }}
                                  >
                                    <span className={styles.policyName}>
                                      {
                                        tagTemplateMap[
                                          item.tag_template_form_id
                                        ]
                                      }
                                    </span>
                                  </div>
                                )}
                              </div>
                            );
                          })}
                      </TableCell>
                      <TableCell align="center">
                        {row.policyTags &&
                          row.policyTags.names.map((item, index) => {
                            return (
                              <div key={index}>
                                {policMap[item] && (
                                  <div className={styles.policyTag} key={index}>
                                    <span className={styles.policyName}>
                                      {policMap[item].taxonomy_display_name} :
                                    </span>
                                    <span className={styles.policytagname}>
                                      {policMap[item].display_name}
                                    </span>
                                  </div>
                                )}
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
      </ScrollBar>
    </div>
  );
};

export default OnboardDataDisplay;

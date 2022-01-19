/* third lib*/
import React, { useCallback, useState, useEffect, useMemo } from "react";
import { FormattedMessage as Intl } from "react-intl";

/* material-ui */
import Paper from "@material-ui/core/Paper";
import Box from "@material-ui/core/Box";
import TablePagination from "@material-ui/core/TablePagination";
import Collapse from "@material-ui/core/Collapse";
import IconButton from "@material-ui/core/IconButton";
import KeyboardArrowDownIcon from "@material-ui/icons/KeyboardArrowDown";
import KeyboardArrowUpIcon from "@material-ui/icons/KeyboardArrowUp";

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
import HeadLine from "@basics/HeadLine";
import Text from "@basics/Text";

import {
  getUserCaseMemberConfig,
  getFormItem,
  getUseCaseDetail,
} from "@lib/api";

import { sendNotify } from "src/utils/systerm-error";
const USE_CASE_FORM_ID = 2;

const UseCaseRow = ({ user, userColumnKey }) => {
  const [open, setOpen] = useState(false);

  const leftKey = useMemo(() => {
    let wholeKey = Object.keys(user);
    wholeKey = wholeKey.filter((key) => {
      return !userColumnKey.includes(key);
    });
    return wholeKey;
  }, [userColumnKey, user]);

  return (
    <React.Fragment>
      <TableRow>
        <TableCell width="10%">
          <IconButton
            aria-label="expand row"
            size="small"
            onClick={() => setOpen(!open)}
          >
            {open ? <KeyboardArrowUpIcon /> : <KeyboardArrowDownIcon />}
          </IconButton>
        </TableCell>

        {userColumnKey.map((key, index) => {
          return (
            <TableCell key={index} align="center">
              <Text>{user[key]}</Text>
            </TableCell>
          );
        })}
      </TableRow>
      <TableRow>
        <TableCell style={{ paddingBottom: 0, paddingTop: 0 }} colSpan={6}>
          <Collapse in={open} timeout="auto" unmountOnExit>
            <Box margin={1}>
              <div className={styles.detailBox}>
                <div className={styles.detailHolder}></div>
                {leftKey.map((item, index) => {
                  return (
                    <div key={item + index} className={styles.detailItem}>
                      <div className={styles.detailLabel}>
                        <Text type="subTitle">{item}</Text>
                      </div>
                      <div className={styles.detailValue}>{user[item]}</div>
                    </div>
                  );
                })}
              </div>
            </Box>
          </Collapse>
        </TableCell>
      </TableRow>
    </React.Fragment>
  );
};
const UsecaseInfo = ({ usecaseId }) => {
  const [useCaseDetail, setUseCaseDetail] = useState([]);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [ucData, setUcData] = useState();
  const [useCaseMember, setUseCaseMember] = useState([]);

  const handleChangePage = useCallback((event, newPage) => {
    setPage(newPage);
  }, []);

  const handleChangeRowsPerPage = useCallback((event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  }, []);

  const userColumnKey = useMemo(() => {
    return useCaseMember;
  }, [useCaseMember]);

  useEffect(() => {
    if (!usecaseId) {
      return;
    }

    Promise.all([
      getUserCaseMemberConfig(),
      getUseCaseDetail({ id: usecaseId }),
      getFormItem({
        id: USE_CASE_FORM_ID,
      }),
    ])
      .then((res) => {
        let res1 = res[0];
        let res2 = res[1];
        let res3 = res[2];
        if (res1.data && res2.data && res3.data) {
          let ucData = res2.data;
          setUseCaseMember(res1.data);
          ucData = {
            defaultData: {
              form_id: USE_CASE_FORM_ID,
              id: res.id,
              s1: ucData.region_country,
              u2: ucData.uc_owner_group,
              u3: ucData.uc_team_group,
              u4: ucData.validity_date,
              u5: ucData.usecase_name,
              u6: ucData.uc_des,
              u7: ucData.service_account,
              u8: ucData.budget,
              u9: ucData.resources_access_list,
              u10: ucData.allow_cross_region,
            },
            user_infos: ucData.user_infos,
          };
          let data = res3.data;
          let tempFieldList = data.fieldList.map((item) => {
            if (item.style === 6) {
              item.default = new Date();
            }
            if (item.style === 1) {
              item.default = item.options.map(() => "false").join(",");
            }
            if (item.style === 5) {
              item.default = String(!!item.default);
            }
            if (ucData && ucData?.defaultData[item.id]) {
              item.default = ucData?.defaultData[item.id];
            }
            return item;
          });
          setUcData(ucData);
          setUseCaseDetail(tempFieldList);
        }
      })
      .catch((e) => {
        sendNotify({ msg: e.message, status: 3, show: true });
      });
  }, [usecaseId]);

  return (
    <div className={styles.workspaceCreation}>
      <div className={styles.wsContainer}>
        <div className={styles.title}>
          <HeadLine>
            <Intl id="usecaseInfo" />
          </HeadLine>
        </div>
        <div className={styles.wsDetailBox}>
          <div className={styles.secondTitle}>
            <Text type="title">
              <Intl id="useCaseDetail" />
            </Text>
          </div>
          <div className={styles.detailBox}>
            {useCaseDetail?.length > 0 &&
              useCaseDetail.map((item) => {
                return (
                  <div key={item.id} className={styles.detailItem}>
                    <div className={styles.detailLabel}>
                      <Text type="subTitle">{item.label}</Text>
                    </div>
                    <div className={styles.detailValue}>{item.default}</div>
                  </div>
                );
              })}
          </div>
        </div>
        <div className={styles.wsDetailBox}>
          <div className={styles.secondTitle}>
            <Text type="title">
              <Intl id="useCaseMember" />
            </Text>
          </div>
          {ucData && ucData?.user_infos.length > 0 && (
            <>
              <TableContainer component={Paper}>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell width="10%"></TableCell>
                      {userColumnKey.map((item, index) => {
                        return (
                          <TableCell key={index} align="center">
                            <Text type="subTitle">{item}</Text>
                          </TableCell>
                        );
                      })}
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {ucData.user_infos.map((user, ucIndex) => (
                      <UseCaseRow
                        key={ucIndex}
                        user={user}
                        userColumnKey={userColumnKey}
                      />
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
    </div>
  );
};

export default UsecaseInfo;

/* third lib*/
import React, { useState, useEffect, useMemo, useCallback } from "react";
import { FormattedMessage as Intl } from "react-intl";
import { useForm } from "react-hook-form";
import cn from "classnames";

/* material-ui */
import Paper from "@material-ui/core/Paper";
import TablePagination from "@material-ui/core/TablePagination";
import ArrowBackIcon from "@material-ui/icons/ArrowBack";

/* local components & methods */
import styles from "./styles.module.scss";
import TableView from "./TableView";
import FormItem from "@comp/FormItem";
import HeadLine from "@comp/HeadLine";
import Search from "@comp/Search";
import Text from "@comp/Text";
import CallModal from "@comp/CallModal";
import Loading from "src/icons/Loading";
import { getTableData } from "@lib/api";
import Button from "@comp/Button";
import { sendNotify } from "src/utils/systerm-error";
import {
  Table,
  TableBody,
  TableContainer,
  TableHead,
  TableRow,
  TableCell,
} from "@comp/Table";

const tableForm = [
  {
    default: "",
    des: "Data Assets",
    edit: 1,
    id: "u1",
    label: "Data Assets",
    options: [
      { label: "All available data assets in Torro", value: "1" },
      { label: "All available data assets by the user ", value: "2" },
    ],
    placeholder: "GCP Project",
    style: 1,
  },
  {
    default: "",
    des: "Types",
    edit: 1,
    id: "u2",
    label: "Types",
    options: [
      { label: "GCP Projects", value: "1" },
      { label: "Use cases", value: "2" },
      { label: "Dataset", value: "3" },
      { label: "Table / View", value: "4" },
    ],
    placeholder: "",
    style: 1,
  },
  {
    default: "",
    des: "Data Governance",
    edit: 1,
    id: "u3",
    label: "Data Governance",
    options: [
      { label: "Dataset Owners", value: "1" },
      { label: "Data Governor", value: "2" },
      { label: "Region", value: "3" },
      { label: "Country", value: "4" },
    ],
    placeholder: "",
    style: 1,
  },
];

const DataDiscovery = () => {
  const { handleSubmit, control, register, reset } = useForm(); // initialise the hook

  const [formLoading, setFormLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState();
  const [tableList, setTableList] = useState([]);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [step, setStep] = useState(0);
  const [dataName, setDataName] = useState("");

  const [modalData, setModalData] = useState({
    open: false,
    status: 0,
    content: "",
    cb: null,
  });

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

  const submitHandle = (data) => {
    setSearchQuery(data);
  };

  const renderFormItem = (items, disabled) => {
    return items.map((item, index) => {
      return (
        <FormItem
          key={index}
          data={item}
          index={index}
          control={control}
          register={register}
          disabled={disabled}
          fullWidth
        />
      );
    });
  };

  const closeModal = () => {
    setModalData({ ...modalData, open: false, cb: null });
  };

  const onRowClick = useCallback(() => {
    setStep(1);
  }, []);

  useEffect(() => {
    if (searchQuery) {
      setFormLoading(true);
      getTableData(searchQuery)
        .then((res) => {
          setTableList(res.data);
          setFormLoading(false);
        })
        .catch((e) => {
          sendNotify({ msg: e.message, status: 3, show: true });
        });
    }
  }, [searchQuery]);

  const handleSearch = useCallback(() => {
    setFormLoading(true);
    getTableData(searchQuery)
      .then((res) => {
        setTableList(res.data);
        setFormLoading(false);
      })
      .catch((e) => {
        sendNotify({ msg: e.message, status: 3, show: true });
      });
  }, [searchQuery]);

  return (
    <div className={styles.dataDiscover}>
      {step === 0 && (
        <form
          className={styles.tableSearch}
          id="tableSearch"
          onSubmit={handleSubmit(submitHandle)}
        >
          <div className={styles.dataContainer}>
            <div className={styles.dataLeftPanel}>
              <div className={styles.filterPanel}>
                <div className={styles.leftPanelTitle}>
                  <Text type="title">
                    <Intl id="filters" />
                  </Text>
                  <div
                    className={styles.reset}
                    onClick={() => {
                      reset({ u1: "", u2: "", u3: "" });
                    }}
                  >
                    <Text type="regular">
                      <Intl id="CLEAR" />
                    </Text>
                  </div>
                </div>
                <div className={styles.formOptions}>
                  {renderFormItem(tableForm)}
                </div>
              </div>
            </div>
            <div className={styles.dataRightPanel}>
              <div className={styles.title}>
                <HeadLine>
                  <Intl id="dataDiscovery" />
                </HeadLine>
              </div>
              <div className={styles.filterBox}>
                <div className={styles.filterItem}>
                  <Search
                    fullWidth
                    placeholder="Search by Data name"
                    value={dataName}
                    onChange={(value) => {
                      setDataName(value);
                    }}
                    handleSearch={handleSearch}
                  />
                  <div className={styles.buttonWrapper}>
                    <Button
                      className={styles.button}
                      type="submit"
                      variant="contained"
                    >
                      <Intl id="search" />
                    </Button>
                  </div>
                </div>
              </div>
              <div
                className={cn(styles.dataTable, {
                  [styles["tableLoading"]]: formLoading,
                })}
              >
                <TableContainer component={Paper}>
                  <Table aria-label="simple table">
                    <TableHead>
                      <TableRow>
                        <TableCell align="center">
                          <Text type="subTitle">
                            <Intl id="name" />
                          </Text>
                        </TableCell>
                        <TableCell align="center">
                          <Text type="subTitle">
                            <Intl id="description" />
                          </Text>
                        </TableCell>
                        <TableCell align="center">
                          <Text type="subTitle">
                            <Intl id="type" />
                          </Text>
                        </TableCell>
                        <TableCell align="center">
                          <Text type="subTitle">
                            <Intl id="System" />
                          </Text>
                        </TableCell>
                        <TableCell align="center" width="25%">
                          <Text type="subTitle">
                            <Intl id="project" />
                          </Text>
                        </TableCell>
                        <TableCell align="center" width="25%">
                          <Text type="subTitle">
                            <Intl id="lastModified" />
                          </Text>
                        </TableCell>
                      </TableRow>
                    </TableHead>
                    {formLoading && (
                      <TableBody>
                        <TableRow className={styles.loadingRow}>
                          <TableCell colSpan={6}>
                            <Loading></Loading>
                          </TableCell>
                        </TableRow>
                      </TableBody>
                    )}
                    {!formLoading && tableList.length > 0 && (
                      <TableBody>
                        {filterTableList.map((row, rowIndex) => (
                          <TableRow
                            className={styles.tableRow}
                            key={rowIndex}
                            onClick={() => {
                              onRowClick();
                            }}
                          >
                            <TableCell align="center">{row.name}</TableCell>
                            <TableCell align="center">{row.des}</TableCell>
                            <TableCell align="center">{row.type}</TableCell>
                            <TableCell align="center">{row.system}</TableCell>
                            <TableCell align="center">{row.project}</TableCell>
                            <TableCell align="center">
                              {row.lastmodefied}
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    )}
                  </Table>
                </TableContainer>
              </div>
              <TablePagination
                rowsPerPageOptions={[5, 10, 25]}
                component="div"
                count={tableList.length}
                rowsPerPage={rowsPerPage}
                page={page}
                onChangePage={handleChangePage}
                onChangeRowsPerPage={handleChangeRowsPerPage}
              />
            </div>
          </div>
        </form>
      )}

      {step === 1 && (
        <TableView
          onBack={() => {
            setStep(0);
          }}
          tableId={1}
        />
      )}
      <CallModal
        open={modalData.open}
        content={modalData.content}
        status={modalData.status}
        buttonClickHandle={modalData.cb}
        handleClose={closeModal}
      />
    </div>
  );
};

export default DataDiscovery;

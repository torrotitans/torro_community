/* third lib*/
import React, { useEffect, useState } from "react";
import { FormattedMessage as Intl } from "react-intl";

/* material-ui */
import Checkbox from "@material-ui/core/Checkbox";
import DeleteIcon from "@material-ui/icons/Delete";
import EditIcon from "@material-ui/icons/Edit";

/* local components & methods */
import styles from "./styles.module.scss";
import Text from "@comp/Text";
import Model from "@comp/Model";
import Button from "@comp/Button";
import Select from "@comp/Select";
import TextBox from "@comp/TextBox";
import {
  Table,
  TableBody,
  TableContainer,
  TableHead,
  TableRow,
  TableCell,
} from "@comp/Table";

const typeList = [
  {
    label: "STRING",
    value: "STRING",
  },
  {
    label: "BYTES",
    value: "BYTES",
  },
  {
    label: "INTEGER",
    value: "INTEGER",
  },
  {
    label: "FLOAT",
    value: "FLOAT",
  },
  {
    label: "NUMERIC",
    value: "NUMERIC",
  },
  {
    label: "BIGNUMERIC",
    value: "BIGNUMERIC",
  },
  {
    label: "BYTES",
    value: "BYTES",
  },
];

const modeList = [
  {
    label: "NULLABLE",
    value: "NULLABLE",
  },
  {
    label: "REQUIRED",
    value: "REQUIRED",
  },
  {
    label: "REPEATED",
    value: "REPEATED",
  },
];

const DataTable = ({ value, onChange, handleClose }) => {
  const [rows, setRows] = useState([]);
  useEffect(() => {
    if (value && JSON.parse(value)) {
      setRows(JSON.parse(value));
    } else {
      setRows([]);
    }
  }, [value]);
  return (
    <Model open={true}>
      <div
        className={styles.addRow}
        onClick={() => {
          setRows([...rows, { name: "", type: "Integer", mode: false }]);
        }}
      >
        <Text type="large">Add new row</Text>
      </div>
      <div className={styles.table}>
        <TableContainer>
          <Table aria-label="simple table">
            <TableHead>
              <TableRow>
                <TableCell align="center">
                  <Intl id="name" />
                </TableCell>
                <TableCell align="center">
                  <Intl id="type" />
                </TableCell>
                <TableCell align="center">
                  <Intl id="mode" />
                </TableCell>
                <TableCell align="center">
                  <Intl id="operation" />
                </TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {rows.length < 1 && (
                <TableRow>
                  <TableCell align="center">
                    <Intl id="plsAddSchema" />
                  </TableCell>
                </TableRow>
              )}
              {rows.map((row, index) => (
                <TableRow key={index}>
                  <TableCell align="center">
                    <TextBox
                      value={row.name}
                      onChange={(value) => {
                        let tmp = [...rows];
                        tmp[index].name = value;
                        setRows(tmp);
                      }}
                    />
                  </TableCell>
                  <TableCell align="center">
                    <Select
                      value={row.type}
                      options={typeList}
                      onChange={(value) => {
                        let tmp = [...rows];
                        tmp[index].type = value;
                        setRows(tmp);
                      }}
                    />
                  </TableCell>
                  <TableCell align="center">
                    <Select
                      value={row.mode}
                      options={modeList}
                      onChange={(value) => {
                        let tmp = [...rows];
                        tmp[index].mode = value;
                        setRows(tmp);
                      }}
                    />
                  </TableCell>
                  <TableCell align="center">
                    <div className={styles.delete}>
                      <DeleteIcon
                        onClick={() => {
                          let tmp = [...rows];
                          tmp.splice(index, 1);
                          setRows(tmp);
                        }}
                      />
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </div>
      <div className={styles.modelOperation}>
        <div className={styles.clear}>
          <Button
            onClick={() => {
              handleClose && handleClose();
            }}
            size="small"
          >
            cancel
          </Button>
        </div>
        <div className={styles.finish}>
          <Button
            onClick={() => {
              handleClose();
              onChange(JSON.stringify(rows));
            }}
            size="small"
            filled
          >
            Done
          </Button>
        </div>
      </div>
    </Model>
  );
};
const Schema = ({ value, options, onChange }) => {
  const [open, setOpen] = useState(false);

  return (
    <>
      <div className={styles.valueBox}>
        <div
          onClick={() => {
            setOpen(true);
          }}
          className={styles.schemaHolder}
        >
          <div className={styles.schemaLabel}>Schema</div>
          <div className={styles.editBtn}>
            <EditIcon />
          </div>
        </div>
      </div>
      {open && (
        <DataTable
          value={value}
          options={options}
          onChange={onChange}
          handleClose={() => {
            setOpen(false);
          }}
        />
      )}
    </>
  );
};

export default Schema;

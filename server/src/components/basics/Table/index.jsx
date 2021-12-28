/* third lib */
import React from "react";
import cn from "classnames";

/* material-ui */
import { withStyles } from "@material-ui/core/styles";
import TableR from "@material-ui/core/Table";
import TableBodyR from "@material-ui/core/TableBody";
import TableCellR from "@material-ui/core/TableCell";
import TableContainerR from "@material-ui/core/TableContainer";
import TableHeadR from "@material-ui/core/TableHead";
import TableRowR from "@material-ui/core/TableRow";

/* local components and methods */
import styles from "./styles.module.scss";

export const Table = TableR;
export const TableBody = TableBodyR;
export const TableContainer = TableContainerR;
export const TableHead = TableHeadR;

export const TableRow = withStyles((theme) => ({
  root: {
    "&:nth-of-type(odd)": {
      backgroundColor: "#f7f7f7",
    },
  },
}))(TableRowR);

export const TableCell = withStyles((theme) => ({
  head: {
    backgroundColor: "#5c6bb5",
    color: "#fff",
    padding: "0.75rem",
    fontSize: "0.875rem",
  },
  body: {
    fontSize: "0.875rem",
    padding: "0.75rem",
  },
}))(TableCellR);

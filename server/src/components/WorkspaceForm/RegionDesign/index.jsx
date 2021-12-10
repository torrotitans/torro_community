import React, { useState } from "react";

/* material-ui */
import Box from "@material-ui/core/Box";
import Collapse from "@material-ui/core/Collapse";
import IconButton from "@material-ui/core/IconButton";
import Paper from "@material-ui/core/Paper";
import KeyboardArrowDownIcon from "@material-ui/icons/KeyboardArrowDown";
import KeyboardArrowUpIcon from "@material-ui/icons/KeyboardArrowUp";
import RemoveCircleOutlineIcon from "@material-ui/icons/RemoveCircleOutline";

/* local component */
import TextBox from "@comp/TextBox";
import styles from "./styles.module.scss";
import {
  Table,
  TableBody,
  TableContainer,
  TableHead,
  TableRow,
  TableCell,
} from "@comp/Table";

const Region = ({ row, onChange, onDelete }) => {
  const [open, setOpen] = useState(false);

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
        <TableCell width="25%" component="th" scope="row" align="left">
          <TextBox
            value={row.region}
            onChange={(value) => {
              onChange({
                ...row,
                region: value,
              });
            }}
          />
        </TableCell>
        <TableCell width="25%" align="left">
          <TextBox
            value={row.group}
            onChange={(value) => {
              onChange({
                ...row,
                group: value,
              });
            }}
          />
        </TableCell>
        <TableCell width="25%" align="left">
          <TextBox
            value={row.workflow}
            onChange={(value) => {
              onChange({
                ...row,
                workflow: value,
              });
            }}
          />
        </TableCell>
        <TableCell width="15%" align="center">
          <div className={styles.operaction}>
            <div
              className={styles.icon}
              onClick={() => {
                onDelete();
              }}
            >
              <RemoveCircleOutlineIcon />
            </div>
          </div>
        </TableCell>
      </TableRow>
      <TableRow>
        <TableCell style={{ paddingBottom: 0, paddingTop: 0 }} colSpan={6}>
          <Collapse in={open} timeout="auto" unmountOnExit>
            <Box margin={1}>
              <div className={styles.countryTitle}>
                Country list
                <div
                  className={styles.addCountryBtn}
                  onClick={() => {
                    let tmp = { ...row };
                    tmp.countryList.push({
                      country: "",
                      group: "",
                      workflow: "",
                    });
                    onChange(tmp);
                  }}
                >
                  Add Cournty
                </div>
              </div>
              {row.countryList.length > 0 && (
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell width="10%">Region</TableCell>
                      <TableCell width="25%" align="center">
                        country
                      </TableCell>
                      <TableCell width="25%" align="center">
                        group
                      </TableCell>
                      <TableCell width="25%" align="center">
                        workflow
                      </TableCell>
                      <TableCell width="15%" align="center">
                        operation
                      </TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {row.countryList.map((historyRow, index) => (
                      <TableRow key={index}>
                        <TableCell width="10%">{row.region}</TableCell>
                        <TableCell width="25%" align="center">
                          <TextBox
                            value={historyRow.country}
                            onChange={(value) => {
                              let tmpCoun = [...row.countryList];
                              tmpCoun[index].country = value;
                              onChange({
                                ...row,
                                countryList: tmpCoun,
                              });
                            }}
                          />
                        </TableCell>
                        <TableCell width="25%" align="center">
                          <TextBox
                            value={historyRow.group}
                            onChange={(value) => {
                              let tmpCoun = [...row.countryList];
                              tmpCoun[index].group = value;
                              onChange({
                                ...row,
                                countryList: tmpCoun,
                              });
                            }}
                          />
                        </TableCell>
                        <TableCell width="25%" align="center">
                          <TextBox
                            value={historyRow.workflow}
                            onChange={(value) => {
                              let tmpCoun = [...row.countryList];
                              tmpCoun[index].workflow = value;
                              onChange({
                                ...row,
                                countryList: tmpCoun,
                              });
                            }}
                          />
                        </TableCell>
                        <TableCell width="15%" align="center">
                          <div className={styles.operaction}>
                            <div
                              className={styles.icon}
                              onClick={() => {
                                let tmp = { ...row };
                                tmp.countryList.splice(index, 1);
                                onChange(tmp);
                              }}
                            >
                              <RemoveCircleOutlineIcon />
                            </div>
                          </div>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              )}
            </Box>
          </Collapse>
        </TableCell>
      </TableRow>
    </React.Fragment>
  );
};

const RegionDesign = ({ regions, onChange }) => {
  return (
    <TableContainer component={Paper}>
      <Table aria-label="collapsible table">
        <TableHead>
          <TableRow>
            <TableCell width="10%" />
            <TableCell width="25%" align="left">
              Region
            </TableCell>
            <TableCell width="25%" align="left">
              workspace ad group
            </TableCell>
            <TableCell width="25%" align="left">
              workflow value
            </TableCell>
            <TableCell width="15%" align="center">
              operation
            </TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {regions.map((row, index) => (
            <Region
              key={index}
              row={row}
              onChange={(data) => {
                let tmp = [...regions];
                tmp[index] = data;
                onChange(tmp);
              }}
              onDelete={() => {
                let tmp = [...regions];
                tmp.splice(index, 1);
                onChange(tmp);
              }}
            />
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default RegionDesign;

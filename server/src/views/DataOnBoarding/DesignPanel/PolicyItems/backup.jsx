import React, { useState, useCallback, useMemo } from "react";
import { FormattedMessage as Intl } from "react-intl";
import cn from "classnames";

/* material-ui */
import Checkbox from "@material-ui/core/Checkbox";
import Collapse from "@material-ui/core/Collapse";
import Box from "@material-ui/core/Box";
import IconButton from "@material-ui/core/IconButton";
import KeyboardArrowDownIcon from "@material-ui/icons/KeyboardArrowDown";
import KeyboardArrowUpIcon from "@material-ui/icons/KeyboardArrowUp";
import Paper from "@material-ui/core/Paper";

/* local component */
import styles from "./styles.module.scss";
import Text from "@basics/Text";
import {
  Table,
  TableBody,
  TableContainer,
  TableHead,
  TableRow,
  TableCell,
} from "@basics/Table";

const SubTagList = ({ subTagList, onCheck, checkedList }) => {
  return (
    <div className={styles.subTag}>
      {subTagList.map((item, seq) => {
        return (
          <TagItem
            key={seq}
            data={item}
            checkedList={checkedList}
            onCheck={onCheck}
          />
        );
      })}
    </div>
  );
};

const TagItem = ({ data, onCheck, checkedList }) => {
  const [open, setOpen] = useState(false);

  const isSelected = useMemo(() => {
    return checkedList.includes(data.display_name);
  }, [checkedList, data]);

  return (
    <>
      <TableRow>
        <TableCell align="center">
          <Checkbox
            color="primary"
            checked={isSelected}
            onChange={() => {
              onCheck(data.display_name);
            }}
          />
        </TableCell>
        <TableCell>
          <div className={styles.tagBox}>
            {data.sub_tags && data.sub_tags.length > 0 && (
              <IconButton
                aria-label="expand row"
                size="small"
                onClick={() => setOpen(!open)}
              >
                {open ? <KeyboardArrowUpIcon /> : <KeyboardArrowDownIcon />}
              </IconButton>
            )}
            <div className={styles.tagItem}>{data.display_name}</div>
          </div>
        </TableCell>
        <TableCell>{data.description}</TableCell>
        <TableCell></TableCell>
        <TableCell></TableCell>
      </TableRow>
      {data.sub_tags && data.sub_tags.length > 0 && (
        <TableRow>
          <Collapse in={open} timeout="auto" unmountOnExit>
            <Box margin={1}>
              <SubTagList
                subTagList={data.sub_tags}
                onCheck={onCheck}
                checkedList={checkedList}
              />
            </Box>
          </Collapse>
        </TableRow>
      )}
    </>
  );
};
const PolicyItems = ({ data, checkedList, onCheck }) => {
  return (
    <div className={styles.policyTagGroup}>
      <TableContainer component={Paper}>
        <Table aria-label="simple table">
          <TableHead>
            <TableRow>
              <TableCell align="center"></TableCell>
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
                  <Intl id="policyTags" />
                </Text>
              </TableCell>
              <TableCell align="center">
                <Text type="subTitle">
                  <Intl id="location" />
                </Text>
              </TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {/* {filterTableList.map((row, index) => (
              <TableRow key={index}>
                <TableCell align="center">{row.id}</TableCell>
                <TableCell align="center">{row.workspace_name}</TableCell>
                <TableCell align="center">{row.ws_head_group}</TableCell>
                <TableCell align="center">{row.create_time}</TableCell>
                <TableCell align="center">
                </TableCell>
              </TableRow>
            ))} */}
            {data &&
              data.map((tag, seq) => {
                return (
                  <TagItem
                    key={`level1-${seq}`}
                    index={seq}
                    data={tag}
                    onCheck={onCheck}
                    checkedList={checkedList}
                  />
                );
              })}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );
};

export default PolicyItems;

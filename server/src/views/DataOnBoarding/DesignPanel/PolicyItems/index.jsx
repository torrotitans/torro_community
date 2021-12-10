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
import Text from "@comp/Text";
import {
  Table,
  TableBody,
  TableContainer,
  TableHead,
  TableRow,
  TableCell,
} from "@comp/Table";

/* local component */
import styles from "./styles.module.scss";

const SubTagList = ({ subTagList, onCheck, checkedList, level }) => {
  return (
    <div className={styles.subTag}>
      {subTagList.map((item, seq) => {
        return (
          <TagItem
            key={seq}
            data={item}
            checkedList={checkedList}
            onCheck={onCheck}
            level={level}
          />
        );
      })}
    </div>
  );
};

const TagItem = ({ data, onCheck, checkedList, level }) => {
  const [open, setOpen] = useState(false);

  const isSelected = useMemo(() => {
    return checkedList.includes(data.id);
  }, [checkedList, data]);

  return (
    <div className={styles.tagItemBox}>
      <div className={styles.tagBox}>
        <Checkbox
          color="primary"
          checked={isSelected}
          onChange={() => {
            onCheck(data.id);
          }}
        />
        <div className={cn(styles.policyDetail, styles["level" + level])}>
          <div className={styles.expanderIcon}>
            {data.sub_tags && data.sub_tags.length > 0 && (
              <IconButton
                aria-label="expand row"
                size="small"
                onClick={() => setOpen(!open)}
              >
                {open ? <KeyboardArrowUpIcon /> : <KeyboardArrowDownIcon />}
              </IconButton>
            )}
          </div>
          <div
            className={cn(styles.tagItem, { [styles["selected"]]: isSelected })}
          >
            {data.display_name}
          </div>
        </div>
      </div>
      {data.sub_tags && data.sub_tags.length > 0 && (
        <Collapse in={open} timeout="auto" unmountOnExit>
          <Box margin={1}>
            <SubTagList
              subTagList={data.sub_tags}
              onCheck={onCheck}
              checkedList={checkedList}
              level={level + 1}
            />
          </Box>
        </Collapse>
      )}
    </div>
  );
};

const PolicyItems = ({ item, onCheck, checkedList }) => {
  const [open, setOpen] = useState(false);

  const lenCalc = useMemo(() => {
    let count = 0;

    const mapTags = (item) => {
      if (item.policy_tags_list && item.policy_tags_list.length > 0) {
        count += item.policy_tags_list.length;
        item.policy_tags_list.map((subTag) => {
          mapTags(subTag);
        });
      } else if (item.sub_tags.length && item.sub_tags.length > 0) {
        count += item.sub_tags.length;
        item.sub_tags.map((subTag) => {
          mapTags(subTag);
        });
      }
    };

    if (item.policy_tags_list && item.policy_tags_list.length > 0) {
      mapTags(item);
    }
    return count;
  }, [item]);

  return (
    <>
      <TableRow>
        <TableCell align="left">
          <div className={styles.policyName}>
            <div className={styles.expanderIcon}>
              <IconButton
                aria-label="expand row"
                size="small"
                onClick={() => setOpen(!open)}
              >
                {open ? <KeyboardArrowUpIcon /> : <KeyboardArrowDownIcon />}
              </IconButton>
            </div>
            {item.taxonomy_display_name}
          </div>
        </TableCell>
        <TableCell align="center">{item.description}</TableCell>
        <TableCell align="center">
          {item.policy_tags_list ? lenCalc : 0}
        </TableCell>
        <TableCell align="center">{item.region}</TableCell>
      </TableRow>
      <TableRow>
        <TableCell style={{ paddingBottom: 0, paddingTop: 0 }} colSpan={4}>
          <Collapse in={open} timeout="auto" unmountOnExit>
            <Box margin={0}>
              {item.policy_tags_list &&
                item.policy_tags_list.map((tag, seq) => {
                  return (
                    <TagItem
                      key={`level1-${seq}`}
                      index={seq}
                      data={tag}
                      onCheck={onCheck}
                      checkedList={checkedList}
                      level={1}
                    />
                  );
                })}
            </Box>
          </Collapse>
        </TableCell>
      </TableRow>
    </>
  );
};

const PolicyItemsGroup = ({ data, onCheck, checkedList }) => {
  return (
    <div className={styles.policyTagGroup}>
      <TableContainer component={Paper}>
        <Table aria-label="simple table">
          <TableHead>
            <TableRow>
              <TableCell align="left" width="35%">
                <Text type="subTitle">
                  <Intl id="name" />
                </Text>
              </TableCell>
              <TableCell align="center" width="25%">
                <Text type="subTitle">
                  <Intl id="description" />
                </Text>
              </TableCell>
              <TableCell align="center" width="20%">
                <Text type="subTitle">
                  <Intl id="policyTags" />
                </Text>
              </TableCell>
              <TableCell align="center" width="20%">
                <Text type="subTitle">
                  <Intl id="location" />
                </Text>
              </TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {data.map((item, index) => {
              return (
                <PolicyItems
                  key={index}
                  item={item}
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

export default PolicyItemsGroup;

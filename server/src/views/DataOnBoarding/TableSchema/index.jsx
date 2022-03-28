/* third lib*/
import React, { useState, useMemo, useCallback } from "react";
import { FormattedMessage as Intl } from "react-intl";

/* material-ui */
import Paper from "@material-ui/core/Paper";
import TablePagination from "@material-ui/core/TablePagination";
import Checkbox from "@material-ui/core/Checkbox";
import Delete from "@material-ui/icons/Close";
import IconButton from "@material-ui/core/IconButton";
import KeyboardArrowDownIcon from "@material-ui/icons/KeyboardArrowDown";
import KeyboardArrowUpIcon from "@material-ui/icons/KeyboardArrowUp";

/* local components & methods */
import styles from "./styles.module.scss";
import Button from "@basics/Button";
import Text from "@basics/Text";
import DesignPanel from "../DesignPanel";

import {
  Table,
  TableBody,
  TableContainer,
  TableHead,
  TableRow,
  TableCell,
} from "@basics/Table";

const NestedRowList = ({
  nestedList,
  parentIndex,
  onSelect,
  tagTemplateMap,
  policyMap,
  handleDeletePolicyTag,
  handleDeleteTag,
  openColumnTag,
  selectedList,
  parentChecked,
  parentTags,
  parentPolicyTag,
}) => {
  return (
    <>
      {nestedList.map((childElem, rowIndex) => {
        const schemaRowIndex = `${parentIndex}.${rowIndex}`;
        return (
          <SchemaRow
            key={`${schemaRowIndex}`}
            row={childElem}
            rowIndex={schemaRowIndex}
            onSelect={onSelect}
            tagTemplateMap={tagTemplateMap}
            policyMap={policyMap}
            handleDeletePolicyTag={handleDeletePolicyTag}
            handleDeleteTag={handleDeleteTag}
            openColumnTag={openColumnTag}
            checked={parentChecked || selectedList.includes(schemaRowIndex)}
            selectedList={selectedList}
            parentTags={parentTags}
            parentPolicyTag={parentPolicyTag}
          />
        );
      })}
    </>
  );
};

const SchemaRow = ({
  row,
  rowIndex,
  onSelect,
  checked,
  tagTemplateMap,
  policyMap,
  handleDeletePolicyTag,
  handleDeleteTag,
  selectedList,
  parentTags,
  parentPolicyTag,
  openColumnTag,
}) => {
  const [open, setOpen] = useState(false);
  const schemaRowIndex = rowIndex;

  const indexArr =
    typeof schemaRowIndex === "string"
      ? schemaRowIndex.split(".")
      : [schemaRowIndex];

  const sepPadding = 2;
  const isRecord = row.type === "RECORD";

  console.log(schemaRowIndex, checked);

  return (
    <>
      <TableRow>
        <TableCell align="center">
          <Checkbox
            color="primary"
            checked={checked}
            onChange={() => {
              onSelect(schemaRowIndex);
            }}
          />
        </TableCell>
        <TableCell
          style={{ textIndent: sepPadding * (indexArr.length - 1) + "rem" }}
          align="left"
        >
          {isRecord && (
            <IconButton
              aria-label="expand row"
              size="small"
              onClick={() => setOpen(!open)}
            >
              {open ? <KeyboardArrowUpIcon /> : <KeyboardArrowDownIcon />}
            </IconButton>
          )}
          {row.name}
        </TableCell>
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
                      onClick={(e) => {
                        openColumnTag(e, schemaRowIndex);
                      }}
                    >
                      <span className={styles.delete}>
                        <Delete
                          onClick={(e) => {
                            e.stopPropagation();
                            handleDeleteTag(item, schemaRowIndex);
                          }}
                        />
                      </span>
                      <span className={styles.policyName}>
                        {tagTemplateMap[item.tag_template_form_id]}
                      </span>
                    </div>
                  )}
                </div>
              );
            })}
        </TableCell>
        <TableCell align="center">
          {row.policyTags &&
            row.policyTags.names.map((policTag, tagIndex) => {
              return (
                <div key={tagIndex}>
                  {policyMap[policTag] && (
                    <div className={styles.policyTag} key={tagIndex}>
                      <span className={styles.delete}>
                        <Delete
                          onClick={() => {
                            handleDeletePolicyTag(policTag, schemaRowIndex);
                          }}
                        />
                      </span>
                      <span className={styles.policyName}>
                        {policyMap[policTag].taxonomy_display_name} :
                      </span>
                      <span className={styles.policytagname}>
                        {policyMap[policTag].display_name}
                      </span>
                    </div>
                  )}
                </div>
              );
            })}
        </TableCell>
        <TableCell align="center">{row.description}</TableCell>
      </TableRow>
      {isRecord && open && (
        <NestedRowList
          nestedList={row.fields}
          parentIndex={schemaRowIndex}
          onSelect={onSelect}
          tagTemplateMap={tagTemplateMap}
          policyMap={policyMap}
          handleDeletePolicyTag={handleDeletePolicyTag}
          handleDeleteTag={handleDeleteTag}
          openColumnTag={openColumnTag}
          selectedList={selectedList}
          parentChecked={checked}
          parentTags={row.tag}
          parentPolicyTag={row.policyTags}
        />
      )}
    </>
  );
};

const TableSchema = ({
  tableData,
  policyMap,
  tagTemplateList,
  fieldsChange,
  tableTagsChange,
}) => {
  const [page, setPage] = useState(0);
  const [selectedList, setSelectedList] = useState([]);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [addState, setAddState] = useState(false);
  const [type, setType] = useState(0);

  console.log(tableData);

  const tableList = useMemo(() => {
    return tableData?.schema?.fields;
  }, [tableData]);

  const tableTags = useMemo(() => {
    return tableData?.tags || [];
  }, [tableData]);

  const isView = useMemo(() => {
    // return tableData?.type === "VIEW";
    return false;
  }, [tableData]);

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

  const haveTableTag = useMemo(() => {
    return tableData?.tags.length > 0;
  }, [tableData]);

  const enableAddTagBtn = useMemo(() => {
    return selectedList.length > 0;
  }, [selectedList]);

  const isSelectedAll = useMemo(() => {
    if (!selectedList || !tableList) {
      return false;
    }
    return selectedList.length === tableList.length;
  }, [selectedList, tableList]);

  const checkedTagList = useMemo(() => {
    if (type === 1) {
      return tableTags;
    }
    if (tableList && type === 2 && selectedList.length === 1) {
      let tmpIndex = selectedList[0];
      let indexArr =
        typeof tmpIndex === "string" ? tmpIndex.split(".") : [tmpIndex];
      let objPointer = null;
      let onlySelectItem = null;
      indexArr.forEach((currIndex, index) => {
        if (!objPointer) {
          objPointer = tableList[currIndex];
          if (index === indexArr.length - 1) {
            onlySelectItem = tableList[currIndex].tags;
          }
        } else if (index === indexArr.length - 1) {
          onlySelectItem = objPointer.fields[currIndex].tags;
        } else {
          objPointer = objPointer.fields[currIndex];
        }
      });
      return onlySelectItem || [];
    }

    return [];
  }, [selectedList, tableList, type, tableTags]);

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const onSelectAllClick = useCallback(() => {
    if (isSelectedAll) {
      setSelectedList([]);
    } else {
      let tmp = tableList.map((item, index) => {
        return index;
      });
      setSelectedList(tmp);
    }
  }, [tableList, isSelectedAll, setSelectedList]);

  const onSelect = (currIndex) => {
    if (!selectedList.includes(currIndex)) {
      let tmp = [...selectedList, currIndex];
      setSelectedList(tmp);
    } else {
      let currentIndex = selectedList.indexOf(currIndex);
      let tmp = [...selectedList];
      tmp.splice(currentIndex, 1);
      setSelectedList(tmp);
    }
  };

  const handleDeletePolicyTag = useCallback(
    (tag, delIndex) => {
      let tmp = [...tableList];

      let indexArr =
        typeof delIndex === "string" ? delIndex.split(".") : [delIndex];
      let objPointer = null;
      let delItem = null;
      indexArr.forEach((currIndex, index) => {
        if (!objPointer) {
          objPointer = tmp[currIndex];
          if (index === indexArr.length - 1) {
            delItem = tmp[currIndex].policyTags;
          }
        } else if (index === indexArr.length - 1) {
          delItem = objPointer.fields[currIndex].policyTags;
        } else {
          objPointer = objPointer.fields[currIndex];
        }
      });

      let tagList = delItem.names;
      let tagIndex = tagList.indexOf(tag);
      tagList.splice(tagIndex, 1);
      fieldsChange(tmp);
    },
    [tableList, fieldsChange]
  );

  const handleDeleteTag = useCallback(
    (tag, delIndex) => {
      let tmp = [...tableList];

      let indexArr =
        typeof delIndex === "string" ? delIndex.split(".") : [delIndex];
      let objPointer = null;
      let delItem = null;
      indexArr.forEach((currIndex, index) => {
        if (!objPointer) {
          objPointer = tmp[currIndex];
          if (index === indexArr.length - 1) {
            delItem = tmp[currIndex].tags;
          }
        } else if (index === indexArr.length - 1) {
          delItem = objPointer.fields[currIndex].tags;
        } else {
          objPointer = objPointer.fields[currIndex];
        }
      });

      let tagList = delItem;
      let tagIndex = tagList.indexOf(tag);
      tagList.splice(tagIndex, 1);
      fieldsChange(tmp);
    },
    [tableList, fieldsChange]
  );

  const handleClose = (e) => {
    if (
      e &&
      e.target &&
      e.target.nodeName === "BODY" &&
      e.target.style.overflow === "hidden"
    ) {
      return;
    }
    setAddState(false);
  };

  const handleApply = useCallback(
    (data, type) => {
      if (type === "POLICY") {
        let tmp = [...tableList];
        selectedList.forEach((item, index) => {
          let indexArr = typeof item === "string" ? item.split(".") : [item];
          let objPointer = null;
          indexArr.forEach((currIndex, index) => {
            if (!objPointer) {
              objPointer = tmp[currIndex];
              if (index === indexArr.length - 1) {
                objPointer.policyTags = {
                  names: JSON.parse(JSON.stringify(data)),
                };
              }
            } else if (index === indexArr.length - 1) {
              objPointer.fields[currIndex].policyTags = {
                names: JSON.parse(JSON.stringify(data)),
              };
            } else {
              objPointer = objPointer.fields[currIndex];
            }
          });
        });
        fieldsChange(tmp);
        setAddState(false);
        setSelectedList([]);
      } else if (type === "TABLETAG") {
        tableTagsChange(data);
        setAddState(false);
      } else if (type === "COLUMNTAGS") {
        let tmp = [...tableList];
        selectedList.forEach((item, index) => {
          let indexArr = typeof item === "string" ? item.split(".") : [item];
          let objPointer = null;
          indexArr.forEach((currIndex, index) => {
            if (!objPointer) {
              objPointer = tmp[currIndex];
              if (index === indexArr.length - 1) {
                objPointer.tags = JSON.parse(JSON.stringify(data));
              }
            } else if (index === indexArr.length - 1) {
              objPointer.fields[currIndex].tags = JSON.parse(
                JSON.stringify(data)
              );
            } else {
              objPointer = objPointer.fields[currIndex];
            }
          });
        });
        fieldsChange(tmp);
        setAddState(false);
        setSelectedList([]);
      }
    },
    [selectedList, tableList, fieldsChange, tableTagsChange]
  );

  const openColumnTag = (e, schemaRowIndex) => {
    e.stopPropagation();
    setSelectedList([schemaRowIndex]);
    setType(2);
    setAddState(true);
    setSelectedList([]);
  };

  console.log(selectedList);

  return (
    <>
      <div className={styles.filter}>
        <Button
          filled
          onClick={() => {
            setType(1);
            setAddState(true);
          }}
        >
          {!haveTableTag ? (
            <Intl id="addTableTag" />
          ) : (
            <Intl id="modifyTableTag" />
          )}
        </Button>
        <Button
          filled
          onClick={() => {
            if (enableAddTagBtn) {
              setType(2);
              setAddState(true);
            }
          }}
          disabled={!enableAddTagBtn}
        >
          <Intl id="addColumnTag" />
        </Button>
        {!isView && (
          <Button
            filled
            onClick={() => {
              if (enableAddTagBtn) {
                setType(0);
                setAddState(true);
              }
            }}
            disabled={!enableAddTagBtn}
          >
            <Intl id="addPolicyTag" />
          </Button>
        )}
      </div>
      <TableContainer component={Paper}>
        <Table aria-label="simple table">
          <TableHead>
            <TableRow>
              <TableCell align="center">
                <div className={styles.selectAll}>
                  <Checkbox
                    color="primary"
                    checked={isSelectedAll}
                    onChange={onSelectAllClick}
                  />
                </div>
              </TableCell>
              <TableCell align="left">
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
            {filterTableList.map((row, rowIndex) => {
              const currentIndex = page * rowsPerPage + rowIndex;
              return (
                <SchemaRow
                  key={currentIndex}
                  row={row}
                  rowIndex={currentIndex}
                  tagTemplateMap={tagTemplateMap}
                  policyMap={policyMap}
                  checked={selectedList.includes(currentIndex)}
                  selectedList={selectedList}
                  onSelect={onSelect}
                  openColumnTag={openColumnTag}
                  handleDeletePolicyTag={handleDeletePolicyTag}
                  handleDeleteTag={handleDeleteTag}
                />
              );
            })}
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
      {addState && (
        <DesignPanel
          open={addState}
          handleClose={handleClose}
          handleApply={handleApply}
          tagTemplateList={tagTemplateList}
          type={type}
          checkedTagList={checkedTagList}
        />
      )}
    </>
  );
};

export default TableSchema;

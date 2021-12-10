import React, { useState, useCallback } from "react";
import { FormattedMessage as Intl } from "react-intl";
import cn from "classnames";

/* material-ui */
import Input from "@material-ui/core/Input";
import Collapse from "@material-ui/core/Collapse";
import Box from "@material-ui/core/Box";
import IconButton from "@material-ui/core/IconButton";
import KeyboardArrowDownIcon from "@material-ui/icons/KeyboardArrowDown";
import KeyboardArrowUpIcon from "@material-ui/icons/KeyboardArrowUp";

/* local component */
import styles from "./styles.module.scss";
import Text from "@comp/Text";

const SubTagList = ({ subTagList, level, onChange, displayView }) => {
  const handleChange = useCallback(
    (data, seq) => {
      let tmpList = JSON.parse(JSON.stringify(subTagList));
      tmpList[seq] = data;
      onChange(tmpList);
    },
    [subTagList, onChange]
  );

  const handleAddTag = useCallback(() => {
    let tmpList = JSON.parse(JSON.stringify(subTagList));
    tmpList.push({ display_name: "", description: "", ad_group: "" });
    onChange(tmpList);
  }, [subTagList, onChange]);

  const handleDelete = useCallback(
    (seq) => {
      let tmpList = JSON.parse(JSON.stringify(subTagList));
      tmpList.splice(seq, 1);
      onChange(tmpList);
    },
    [subTagList, onChange]
  );

  return (
    <div className={styles.subTag}>
      {subTagList.map((item, seq) => {
        return (
          <TagItem
            key={`level${level}-${seq}`}
            data={item}
            level={level + 1}
            onChange={(data) => {
              handleChange(data, seq);
            }}
            onDelete={() => {
              handleDelete(seq);
            }}
            displayView={displayView}
          />
        );
      })}
      {!displayView && (
        <div className={styles.tagBox}>
          <div className={styles.addTagSep}></div>
          <div className={styles.addTag} onClick={handleAddTag}>
            <Intl id="addPolicyTag" />
          </div>
        </div>
      )}
    </div>
  );
};

const TagItem = ({
  data,
  level,
  onChange,
  onDelete,
  disbaleDelete = false,
  displayView,
}) => {
  const [open, setOpen] = useState(displayView || false);

  const handleSubChange = useCallback(
    (list) => {
      let levelData = JSON.parse(JSON.stringify(data));
      levelData.sub_tags = list;
      onChange && onChange(levelData);
    },
    [data, onChange]
  );

  const handleSubAdd = () => {
    let levelData = JSON.parse(JSON.stringify(data));
    if (levelData.sub_tags) {
      levelData.sub_tags.push({
        display_name: "",
        description: "",
        ad_group: "",
      });
    } else {
      levelData.sub_tags = [
        { display_name: "", description: "", ad_group: "" },
      ];
    }
    onChange(levelData);
    setOpen(true);
  };

  return (
    <div className={styles.tagItemBox}>
      <div className={styles.tagBox}>
        <div
          className={cn(styles.horizontalSep, {
            [styles["lastLevel"]]: level === 5,
          })}
        ></div>
        {level < 5 && (
          <IconButton
            aria-label="expand row"
            size="small"
            onClick={() => setOpen(!open)}
          >
            {open ? <KeyboardArrowUpIcon /> : <KeyboardArrowDownIcon />}
          </IconButton>
        )}
        <div className={styles.tagItem}>
          <Input
            className={styles.editInput}
            value={data.display_name}
            disableUnderline
            variant="outlined"
            placeholder="Tag name"
            onChange={(e) => {
              onChange({
                ...data,
                display_name: e.target.value,
              });
            }}
            readOnly={displayView}
          />
          <Input
            className={styles.editInput}
            value={data.description}
            disableUnderline
            variant="outlined"
            placeholder="Description"
            onChange={(e) => {
              onChange({
                ...data,
                description: e.target.value,
              });
            }}
            readOnly={displayView}
          />
          <Input
            className={styles.editInput}
            value={data.ad_group}
            disableUnderline
            variant="outlined"
            placeholder="Policy group"
            onChange={(e) => {
              onChange({
                ...data,
                ad_group: e.target.value,
              });
            }}
            readOnly={displayView}
          />

          {!displayView && (
            <>
              {level < 5 && (
                <div
                  className={styles.addTag}
                  onClick={(e) => {
                    handleSubAdd();
                  }}
                >
                  <Intl id="addSubTag" />
                </div>
              )}
              {!disbaleDelete && (
                <div className={styles.addTag} onClick={onDelete}>
                  <Intl id="deleteTag" />
                </div>
              )}
            </>
          )}
        </div>
      </div>
      {data.sub_tags && level < 5 && (
        <Collapse in={open} timeout="auto" unmountOnExit>
          <Box margin={1}>
            <SubTagList
              subTagList={data.sub_tags}
              level={level}
              onChange={(list) => {
                handleSubChange(list);
              }}
              displayView={displayView}
            />
          </Box>
        </Collapse>
      )}
    </div>
  );
};
const PolicyTags = ({ value, onChange, displayView }) => {
  let policTags = value
    ? value
    : [
        {
          display_name: "",
          description: "",
          ad_group: "",
        },
      ];
  const handleChange = useCallback(
    (data, index) => {
      let tmp = JSON.parse(JSON.stringify(policTags));
      tmp[index] = data;
      onChange(tmp);
    },
    [policTags, onChange]
  );

  const handleDelete = useCallback(
    (seq) => {
      let tmp = JSON.parse(JSON.stringify(policTags));
      tmp.splice(seq, 1);
      onChange(tmp);
    },
    [policTags, onChange]
  );
  return (
    <div className={styles.policyTagGroup}>
      {policTags &&
        policTags.map((tag, seq) => {
          return (
            <TagItem
              key={`level1-${seq}`}
              index={seq}
              data={tag}
              level={1}
              onChange={(data) => {
                handleChange(data, seq);
              }}
              disbaleDelete={policTags.length === 1}
              onDelete={() => {
                handleDelete(seq);
              }}
              displayView={displayView}
            />
          );
        })}
    </div>
  );
};

export default PolicyTags;

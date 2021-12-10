/* third lib*/
import React, { useEffect, useState, useCallback, useMemo } from "react";
import cn from "classnames";
import { FormattedMessage as Intl } from "react-intl";

/* local components & methods */
import styles from "./styles.module.scss";
import PolicyItems from "../PolicyItems";
import { getPolicys } from "@lib/api";
import { sendNotify } from "src/utils/systerm-error";
import Text from "@comp/Text";
import Button from "@comp/Button";

const PolicyTagTree = ({ handleApply }) => {
  const [policys, setPolicys] = useState([]);
  const [checkedList, setCheckedList] = useState([]);

  useEffect(() => {
    getPolicys()
      .then((res) => {
        setPolicys(res.data);
      })
      .catch((e) => {
        sendNotify({
          msg: "Get Policy tags error.",
          status: 3,
          show: true,
        });
      });
  }, []);
  const onCheck = useCallback(
    (tag) => {
      let tmp = [...checkedList];
      if (checkedList.includes(tag)) {
        let currIndex = checkedList.indexOf(tag);
        tmp.splice(currIndex, 1);
        setCheckedList(tmp);
      } else {
        tmp.push(tag);
        setCheckedList(tmp);
      }
    },
    [checkedList]
  );

  return (
    <>
      <div className={styles.designerTitle}>
        <Text type="title">Add policy tag</Text>
      </div>
      <PolicyItems data={policys} onCheck={onCheck} checkedList={checkedList} />
      <div className={styles.buttonWrapper}>
        <Button
          className={styles.button}
          size="small"
          type="submit"
          variant="contained"
          onClick={() => {
            handleApply(checkedList, "POLICY");
          }}
        >
          <Intl id="apply" />
        </Button>
      </div>
    </>
  );
};

export default PolicyTagTree;

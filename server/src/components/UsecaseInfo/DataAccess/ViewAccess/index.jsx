/* third lib*/
import React, { useState, useEffect } from "react";
import { FormattedMessage as Intl } from "react-intl";

/* material-ui */
import RemoveRedEye from "@material-ui/icons/RemoveRedEye";

/* local components & methods */
import OnboardDataDisplay from "@comp/OnboardDataDisplay";
import styles from "./styles.module.scss";
import Model from "@basics/Modal";
import { getTableSchema } from "@lib/api";
import TableTagDisplay from "@comp/TableTag";
import Loading from "@assets/icons/Loading";
import Text from "@basics/Text";
import { sendNotify } from "src/utils/systerm-error";

const TableTags = ({ data, resourceDetail }) => {
  const [tableTag, setTableTag] = useState();
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    setLoading(true);
    getTableSchema({
      projectId: resourceDetail.project_id,
      datasetName: resourceDetail.dataset_id,
      tableName: resourceDetail.table_id,
    })
      .then((res) => {
        if (res.data) {
          setTableTag(res.data.tags);
          setLoading(false);
        }
      })
      .catch((e) => {
        sendNotify({ msg: e.message, status: 3, show: true });
      });
  }, [resourceDetail]);

  if (!tableTag || loading) {
    return (
      <div className={styles.loading}>
        <Loading />
      </div>
    );
  }
  return (
    <div>
      {tableTag.map((tag, index) => {
        return <TableTagDisplay key={index} tagData={tag} />;
      })}
    </div>
  );
};

const ViewAccess = ({ data, resourceDetail }) => {
  const [open, setOpen] = useState(false);
  return (
    <div className={styles.viewAccess}>
      <div className={styles.viewIcon}>
        <RemoveRedEye
          onClick={() => {
            setOpen(true);
          }}
        />
      </div>

      <Model
        open={open}
        handleClose={() => {
          setOpen(false);
        }}
      >
        <div className={styles.modalContent}>
          <div className={styles.content}>
            <div className={styles.contentTitle}>
              <Text type="title">
                <Intl id="tableTags" />
              </Text>
            </div>
            <TableTags resourceDetail={resourceDetail} />
          </div>
          <div className={styles.content}>
            <div className={styles.contentTitle}>
              <Text type="title">
                <Intl id="tableSchema" />
              </Text>
            </div>
            <OnboardDataDisplay tableList={data} />
          </div>
        </div>
      </Model>
    </div>
  );
};

export default ViewAccess;

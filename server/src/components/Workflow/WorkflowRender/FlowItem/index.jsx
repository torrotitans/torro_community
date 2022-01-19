/* third lib*/
import React, { useState, useMemo, useEffect } from "react";
import cn from "classnames";
import { FormattedMessage as Intl } from "react-intl";

/* material-ui*/
import EditIcon from "@material-ui/icons/Edit";
import Delete from "@material-ui/icons/Delete";
import CheckIcon from "@material-ui/icons/Check";

/* local components & methods */
import Text from "@basics/Text";
import styles from "./styles.module.scss";
import { Droppable } from "react-beautiful-dnd";
import ConditionItem from "./ConditionItem";
const PLACEHODER = "PLACEHODER";

const FlowItem = ({
  editFlow,
  data,
  index,
  onEdit,
  onDelete,
  closeEdit,
  formFieldOptions,
}) => {
  const [currentData, setCurrentData] = useState(data);
  useEffect(() => {
    setCurrentData(data);
  }, [data]);

  const canDroppable = useMemo(() => {
    return currentData.group === PLACEHODER || editFlow;
  }, [currentData, editFlow]);

  const disableDelete = useMemo(() => {
    return (
      currentData.flowType === "Trigger" || currentData.flowType === "Approval"
    );
  }, [currentData]);

  return (
    <div
      className={cn(styles.flowItem, {
        [styles["editState"]]: editFlow,
      })}
    >
      <Droppable
        droppableId={"droppable" + index}
        isDropDisabled={disableDelete || editFlow || currentData.disabled}
      >
        {(provided, snapshot) => {
          return (
            <div
              className={cn(
                styles.flowContainer,
                styles[currentData.flowType],
                {
                  [styles["draggingOver"]]: snapshot.isDraggingOver,
                  [styles["empty"]]: currentData.group === PLACEHODER,
                }
              )}
              {...provided.droppableProps}
              ref={provided.innerRef}
            >
              <div className={styles.droppableItemLabel}>
                <Text type="large">
                  {currentData.group === PLACEHODER ? (
                    <Intl id="dropwfItem" />
                  ) : (
                    currentData.label
                  )}
                </Text>
                {editFlow && (
                  <div className={styles.operationBox}>
                    <CheckIcon
                      onClick={() => {
                        onEdit(null);
                        closeEdit(currentData);
                      }}
                    />
                  </div>
                )}
                {!canDroppable && (
                  <div className={styles.operationBox}>
                    <EditIcon
                      onClick={() => {
                        onEdit(index, data);
                      }}
                    />
                    {!disableDelete && (
                      <Delete
                        onClick={() => {
                          onDelete(index);
                        }}
                      />
                    )}
                  </div>
                )}
              </div>

              {currentData.group !== PLACEHODER && currentData.condition && (
                <div
                  className={cn(styles.flowMainBox, {
                    [styles["cannotOperate"]]: !editFlow,
                  })}
                >
                  <ConditionItem
                    currentData={currentData}
                    editFlow={editFlow}
                    flowIndex={index}
                    onChange={(data) => {
                      setCurrentData(data);
                    }}
                    formFieldOptions={formFieldOptions}
                  />
                </div>
              )}

              {snapshot.isDraggingOver && (
                <div className={styles.draggingHolder}>
                  <Intl id="dropwfItem" />
                </div>
              )}
              <div className={styles.placeholder}>{provided.placeholder}</div>
            </div>
          );
        }}
      </Droppable>
    </div>
  );
};

export default FlowItem;

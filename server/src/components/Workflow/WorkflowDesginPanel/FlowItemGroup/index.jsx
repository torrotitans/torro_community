/* third lib*/
import React, { useState, useMemo } from "react";
import cn from "classnames";
import { Droppable, Draggable } from "react-beautiful-dnd";

/* material-ui */
import Collapse from "@material-ui/core/Collapse";
import AddIcon from "@material-ui/icons/Add";

/* local components & methods */
import styles from "./styles.module.scss";
import Text from "@comp/Text";

const FlowItemGroup = ({ column }) => {
  const itemList = column.itemList;
  const [open, setOpen] = useState(false);
  const toggleHandle = () => {
    setOpen(!open);
  };
  const currentOpen = useMemo(() => {
    return open;
  }, [open]);

  return (
    <div className={styles.workflowOptions}>
      <div
        className={cn(styles.workflowType, { [styles["active"]]: currentOpen })}
      >
        <Text type="subTitle">{column.label}</Text>
        <div className={styles.addIcon} onClick={toggleHandle}>
          <AddIcon />
        </div>
      </div>
      <Collapse in={currentOpen}>
        <div className={styles.workflowItemList}>
          <Droppable droppableId={column.group} isDropDisabled={true}>
            {(provided, snapshot) => {
              return (
                <div {...provided.droppableProps} ref={provided.innerRef}>
                  {itemList.map((item, index) => {
                    return (
                      <Draggable
                        key={column.group + item.id}
                        draggableId={
                          column.group + "_" + item.id + "_" + item.label
                        }
                        index={index}
                      >
                        {(provided, snapshot) => {
                          return (
                            <React.Fragment>
                              <div
                                ref={provided.innerRef}
                                {...provided.draggableProps}
                                {...provided.dragHandleProps}
                                className={cn(styles.workflowItem, {
                                  [styles["dragging"]]: snapshot.isDragging,
                                })}
                                style={
                                  snapshot.isDragging
                                    ? provided.draggableProps.style
                                    : null
                                }
                              >
                                {item.label}
                              </div>
                              {!column.unique && snapshot.isDragging && (
                                <div className={styles.cloneItem}>
                                  {item.label}
                                </div>
                              )}
                            </React.Fragment>
                          );
                        }}
                      </Draggable>
                    );
                  })}
                  <div style={{ display: "none" }}>{provided.placeholder}</div>
                </div>
              );
            }}
          </Droppable>
        </div>
      </Collapse>
    </div>
  );
};

export default FlowItemGroup;

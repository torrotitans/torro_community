/* third lib*/
import React from "react";
import { FormattedMessage as Intl } from "react-intl";
import cn from "classnames";

/* local components & methods */
import styles from "./styles.module.scss";
import { Droppable } from "react-beautiful-dnd";

const CommonConditionHolder = ({ droppable, index, title }) => {
  return (
    <div className={styles.mainBoxHolder}>
      <Droppable
        droppableId={"droppable" + index + "condition"}
        isDropDisabled={!droppable}
      >
        {(provided, snapshot) => {
          return (
            <div
              className={cn({
                [styles["draggingOver"]]: snapshot.isDraggingOver,
              })}
              {...provided.droppableProps}
              ref={provided.innerRef}
            >
              <div>
                {droppable ? (
                  title || <Intl id="dropCondtion" />
                ) : (
                  <Intl id="plsClickEdit" />
                )}
              </div>

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

export default CommonConditionHolder;

/* third lib*/
import React, { useState } from "react";
import Scrollbar from "react-perfect-scrollbar";

/* local components & methods */
import styles from "./styles.module.scss";
import TagTemplateList from "./TagTemplateList";
import PolicyTagTable from "./PolicyTagTable";
import CallModal from "@basics/CallModal";
import Policy from "./Policy";

const PolicyCreation = () => {
  const [currentId, setCurrentId] = useState(null);
  const [step, setStep] = useState(0);

  const [modalData, setModalData] = useState({
    open: false,
    status: 0,
    content: "",
    cb: null,
  });

  const closeModal = () => {
    setModalData({ ...modalData, open: false, cb: null });
  };

  return (
    <div className={styles.policyCreation}>
      <Scrollbar>
        {step === 0 && (
          <div className={styles.policyContainer}>
            <TagTemplateList setStep={setStep} setCurrentId={setCurrentId} />
            <PolicyTagTable setStep={setStep} setCurrentId={setCurrentId} />
          </div>
        )}
        {step === 1 && (
          <Policy
            onBack={() => {
              setStep(0);
              setCurrentId(null);
            }}
            currentId={currentId}
          />
        )}

        <CallModal
          open={modalData.open}
          content={modalData.content}
          status={modalData.status}
          buttonClickHandle={modalData.cb}
          handleClose={closeModal}
        />
      </Scrollbar>
    </div>
  );
};

export default PolicyCreation;

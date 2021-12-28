/* third lib*/
import React, { useEffect, useState } from "react";
import { FormattedMessage as Intl } from "react-intl";
import Terminal from "terminal-in-react";

/* local component */
import HeadLine from "@comp/basics/HeadLine";
import styles from "./styles.module.scss";
import { getConsole } from "@lib/api";
import { sendNotify } from "src/utils/systerm-error";

const prefixFile = (str) => {
  return `$ ~ "${str}`;
};

const BashCommand = () => {
  const [initPath, setInitPath] = useState("");
  const [currentPath, setCurrentPath] = useState("");
  const [loading, setLoading] = useState(true);
  const [fileStructure, setFileStructure] = useState({});
  const [commands, setCommands] = useState({});

  useEffect(() => {
    Promise.all([getConsole({ command: "pwd" }), getConsole({ command: "ls" })])
      .then((res) => {
        let res1 = res[0];
        let res2 = res[1];
        if (res1.data) {
          setCurrentPath(res1.data.trim());
          setInitPath(prefixFile(res1.data));
        }
        if (res2.data) {
          setFileStructure(res2.data.split("\n"));
        }
        setLoading(false);
      })
      .catch((e) => {
        sendNotify({ msg: "Init terminal Error.", status: 3, show: true });
      });
  }, []);

  useEffect(() => {
    setCommands({
      pwd: (command, print) => {
        getConsole({ command: command.join(" ") })
          .then((res) => {
            if (res.data) {
              print(res.data);
            }
          })
          .catch((e) => {
            sendNotify({ msg: e.message, status: 3, show: true });
          });
      },
      cd: (command, print) => {
        let commandString = command.join(" ");
        let path = command[1];
        commandString = `${commandString} && pwd && ls`;
        getConsole({ command: commandString })
          .then((res) => {
            if (res.data) {
              let PathIndex = res.data.indexOf(path) + path.length;
              let fileName = res.data.slice(0, PathIndex);
              let structure = res.data.slice(PathIndex, res.data.length);
              print(prefixFile(fileName.trim()));
              setCurrentPath(fileName.trim());
              setFileStructure(structure.split("\n"));
            }
          })
          .catch((e) => {
            sendNotify({ msg: e.message, status: 3, show: true });
          });
      },
      ls: (command, print) => {
        let commandString = command.join(" ");
        commandString = `cd ${currentPath} && ls`;
        getConsole({ command: commandString })
          .then((res) => {
            if (res.data) {
              print(res.data);
            }
          })
          .catch((e) => {
            sendNotify({ msg: e.message, status: 3, show: true });
          });
      },
      popup: () => alert("Terminal in React"),
    });
  }, [currentPath]);

  return (
    <div className={styles.bashCommand}>
      {loading && <></>}
      {!loading && (
        <div className={styles.bashCommandContainer}>
          <div className={styles.title}>
            <HeadLine>
              <Intl id="bashCommand" />
            </HeadLine>
          </div>
          <div className={styles.terminal}>
            <Terminal
              commandPassThrough={(command, print) => {
                getConsole({ command: command.join(" ") })
                  .then((res) => {
                    if (res.data) {
                      print(res.data);
                    }
                  })
                  .catch((e) => {
                    sendNotify({ msg: e.message, status: 3, show: true });
                  });
              }}
              color="green"
              backgroundColor="black"
              barColor="black"
              style={{ fontWeight: "bold", fontSize: "1em", width: "100%" }}
              startState="maximised"
              commands={commands}
              descriptions={{
                cd: "opens google.com",
                popup: "alert",
              }}
              msg={initPath}
            />
          </div>
        </div>
      )}
    </div>
  );
};

export default BashCommand;

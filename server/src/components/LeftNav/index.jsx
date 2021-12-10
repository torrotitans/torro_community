/* third lib */
import React, { useState, useEffect, useMemo } from "react";
import cn from "classnames";
import { Link } from "react-router-dom";
import { FormattedMessage as Intl } from "react-intl";

/* local components & methods */
import Text from "@comp/Text";
import Dashboard from "src/icons/Dashboard";
import RaiseTicket from "src/icons/RaiseTicket";
import FormCreation from "src/icons/FormCreation";
import WorkflowCreation from "src/icons/WorkflowCreation";
import Terminal from "src/icons/Terminal";
import { getFormList } from "@lib/api";
import styles from "./styles.module.scss";
import { useGlobalContext } from "src/context";
import { GOVERNOR, IT } from "src/lib/data/roleType.js";
import { SUCCESS } from "src/lib/data/callStatus";

const ROOT = "/app";
const wsItemList = [
  {
    id: "wsMan",
    title: <Intl id="wsMan" />,
    link: `${ROOT}/WorkspaceManage`,
  },
  {
    id: "wsCreate",
    title: <Intl id="createWs" />,
    link: `${ROOT}/WorkspaceCreation`,
  },
  // {
  //   id: "createUc",
  //   title: <Intl id="createUc" />,
  //   link: "${ROOT}/forms?id=2",
  // },
  {
    id: "policyMan",
    title: <Intl id="policyMan" />,
    link: `${ROOT}/policyCreation`,
  },
  {
    id: "dataOnboarding",
    title: <Intl id="dataOnboarding" />,
    link: `${ROOT}/dataOnboarding`,
  },
  {
    id: "dataDiscovery",
    title: <Intl id="dataDiscovery" />,
    link: `${ROOT}/dataDiscovery`,
  },
  {
    id: "getDataAccess",
    title: <Intl id="getDataAccess" />,
    link: `${ROOT}/getDataAccess`,
  },
  {
    id: "visualisation",
    title: <Intl id="visualisation" />,
    link: `${ROOT}/visualisation`,
  },
];

const LeftNav = ({ open, closeHandle }) => {
  const [formList, setFormList] = useState([]);
  const { authContext } = useGlobalContext();
  const navList = useMemo(() => {
    switch (authContext.role) {
      case GOVERNOR:
        return [
          { link: `${ROOT}/dashboard`, id: "dashboard", icon: Dashboard },
          {
            link: "",
            id: "wsManagement",
            leftPanel: true,
            icon: RaiseTicket,
            list: wsItemList,
          },
          {
            link: `${ROOT}/formcreation`,
            id: "formcreation",
            icon: FormCreation,
          },
          {
            link: "",
            id: "raiseTicket",
            leftPanel: true,
            icon: RaiseTicket,
            list: formList || [],
          },
          {
            link: `${ROOT}/workflowcreation`,
            id: "workflowcreation",
            icon: WorkflowCreation,
          },
        ];
      case IT:
        return [
          { link: `${ROOT}/dashboard`, id: "dashboard", icon: Dashboard },
          {
            link: "",
            id: "wsManagement",
            leftPanel: true,
            icon: RaiseTicket,
            list: wsItemList,
          },
          {
            link: `${ROOT}/formcreation`,
            id: "formcreation",
            icon: FormCreation,
          },
          {
            link: "",
            id: "raiseTicket",
            leftPanel: true,
            icon: RaiseTicket,
            list: formList || [],
          },
          {
            link: `${ROOT}/workflowcreation`,
            id: "workflowcreation",
            icon: WorkflowCreation,
          },
          {
            link: `${ROOT}/bashCommand`,
            id: "bashCommand",
            icon: Terminal,
          },
        ];
      default:
        return [
          { link: `${ROOT}/dashboard`, id: "dashboard", icon: Dashboard },
          {
            link: "",
            id: "raiseTicket",
            leftPanel: true,
            icon: RaiseTicket,
            list: formList || [],
          },
        ];
    }
  }, [authContext.role, formList]);

  useEffect(() => {
    getFormList().then((res) => {
      if (res && res.code === SUCCESS) {
        let tempData = res.data.map((item) => {
          return {
            ...item,
            link: `${ROOT}/forms?id=${item.id}`,
          };
        });
        setFormList(tempData);
      }
    });
  }, []);
  return (
    <div
      className={cn(styles.leftNav, {
        [styles["active"]]: open,
      })}
    >
      {navList.map((item) => {
        const Icon = item.icon;
        const LinkWrapper = ({ children }) => {
          if (item.link) {
            return (
              <Link onClick={closeHandle} to={item.link}>
                {children}
              </Link>
            );
          }
          return <>{children}</>;
        };
        return (
          <LinkWrapper key={item.id} to={item.link ? item.link : ""}>
            <div className={styles.navItem}>
              {Icon && <Icon className={styles.navLogo} />}
              <div className={styles.navLabel}>
                <Text type="large">
                  <Intl id={item.id} />
                </Text>
              </div>
              {item.leftPanel && item.list.length > 0 && (
                <div className={styles.secondNavPanel}>
                  <div className={styles.secondTitle}>
                    <Text type="title">
                      <Intl id="ticketAction" />
                    </Text>
                  </div>
                  <div className={styles.secondDes}>
                    <Text>
                      <Intl id="pickStart" />
                    </Text>
                  </div>
                  {item.list.map((item) => {
                    return (
                      <Link
                        onClick={closeHandle}
                        key={`form-${item.id}`}
                        to={item.link}
                      >
                        <div className={styles.secondNav}>
                          <div className={styles.secondNavLabel}>
                            <Text type="subTitle">{item.title}</Text>
                          </div>
                        </div>
                      </Link>
                    );
                  })}
                </div>
              )}
            </div>
          </LinkWrapper>
        );
      })}
    </div>
  );
};

export default LeftNav;

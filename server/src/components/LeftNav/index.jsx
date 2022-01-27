/* third lib */
import React, { useEffect, useMemo } from "react";
import cn from "classnames";
import { Link } from "react-router-dom";
import { FormattedMessage as Intl } from "react-intl";
import ScrollBar from "react-perfect-scrollbar";

/* local components & methods */
import Text from "@basics/Text";
import Dashboard from "@assets/icons/Dashboard";
import RaiseTicket from "@assets/icons/RaiseTicket";
import FormManagement from "@assets/icons/FormManagement";
import WorkflowManagement from "@assets/icons/WorkflowManagement";
import Terminal from "@assets/icons/Terminal";
import { getFormList } from "@lib/api";
import styles from "./styles.module.scss";
import { useGlobalContext } from "src/context";
import { GOVERNOR, IT } from "src/lib/data/roleType.js";
import { SUCCESS } from "src/lib/data/callStatus";

const ROOT = "/app";
const wsItemList = [
  {
    id: "createUc",
    title: <Intl id="createUc" />,
    link: `${ROOT}/forms?id=2`,
  },
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
  const { authContext, formListContext, setFormContext } = useGlobalContext();

  const formList = useMemo(() => {
    return formListContext.userList.map((item) => {
      return {
        ...item,
        link: `${ROOT}/forms?id=${item.id}`,
      };
    });
  }, [formListContext]);

  const navList = useMemo(() => {
    switch (authContext.role) {
      case GOVERNOR:
        return [
          {
            link: `${ROOT}/dashboard`,
            id: "dashboard",
            icon: Dashboard,
          },
          {
            link: "",
            id: "wsManagement",
            leftPanel: true,
            icon: RaiseTicket,
            list: wsItemList,
          },
          {
            link: `${ROOT}/formManagement`,
            id: "formManagement",
            icon: FormManagement,
          },
          {
            link: "",
            id: "raiseTicket",
            leftPanel: true,
            icon: RaiseTicket,
            list: formList || [],
          },
          {
            link: `${ROOT}/workflowManagement`,
            id: "workflowManagement",
            icon: WorkflowManagement,
          },
        ];
      case IT:
        return [
          {
            link: `${ROOT}/dashboard`,
            id: "dashboard",
            icon: Dashboard,
          },
          {
            link: "",
            id: "wsManagement",
            leftPanel: true,
            icon: RaiseTicket,
            list: wsItemList,
          },
          {
            link: `${ROOT}/formManagement`,
            id: "formManagement",
            icon: FormManagement,
          },
          {
            link: "",
            id: "raiseTicket",
            leftPanel: true,
            icon: RaiseTicket,
            list: formList || [],
          },
          {
            link: `${ROOT}/workflowManagement`,
            id: "workflowManagement",
            icon: WorkflowManagement,
          },
          {
            link: `${ROOT}/bashCommand`,
            id: "bashCommand",
            icon: Terminal,
          },
        ];
      default:
        return [
          {
            link: `${ROOT}/dashboard`,
            id: "dashboard",
            icon: Dashboard,
          },
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
        setFormContext(res.data);
      }
    });

    /* eslint-disable */
  }, []);
  /* eslint-disable */

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
                  <div className={styles.childMenus}>
                    <ScrollBar>
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
                    </ScrollBar>
                  </div>
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

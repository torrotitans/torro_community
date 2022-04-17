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
import { GOVERNOR, IT, ADMIN } from "src/lib/data/roleType.js";
import { SUCCESS } from "src/lib/data/callStatus";
import { sendNotify } from "src/utils/systerm-error";

const ROOT = "/app";
const wsCreate = {
  id: "wsCreate",
  title: <Intl id="createWs" />,
  link: `${ROOT}/WorkspaceCreation`,
};
const wsItemList = [
  {
    id: "wsMan",
    title: <Intl id="wsMan" />,
    link: `${ROOT}/WorkspaceManage`,
  },
  {
    id: "policyMan",
    title: <Intl id="policyMan" />,
    link: `${ROOT}/policyCreation`,
  },
  // {
  //   id: "dataDiscovery",
  //   title: <Intl id="dataDiscovery" />,
  //   link: `${ROOT}/dataDiscovery`,
  // },
  // {
  //   id: "visualisation",
  //   title: <Intl id="visualisation" />,
  //   link: `${ROOT}/visualisation`,
  // },
];

const raiseTicketExt = [
  {
    id: "createUc",
    title: <Intl id="createUc" />,
    link: `${ROOT}/forms?id=2`,
  },
  {
    id: "dataOnboarding",
    title: <Intl id="dataOnboarding" />,
    link: `${ROOT}/dataOnboarding`,
  },
  {
    id: "getDataAccess",
    title: <Intl id="getDataAccess" />,
    link: `${ROOT}/getDataAccess`,
  },
];

const LinkWrapper = ({ children, link, closeHandle }) => {
  if (link) {
    return (
      <Link onClick={closeHandle} to={link}>
        {children}
      </Link>
    );
  }
  return <>{children}</>;
};

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
      case ADMIN:
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
            list: [wsCreate].concat(wsItemList),
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
            list: formList ? raiseTicketExt.concat(formList) : raiseTicketExt,
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
            list: formList ? raiseTicketExt.concat(formList) : raiseTicketExt,
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
            list: formList ? raiseTicketExt.concat(formList) : raiseTicketExt,
          },
          {
            link: `${ROOT}/workflowManagement`,
            id: "workflowManagement",
            icon: WorkflowManagement,
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
            list: formList ? raiseTicketExt.concat(formList) : raiseTicketExt,
          },
        ];
    }
  }, [authContext.role, formList]);

  useEffect(() => {
    getFormList()
      .then((res) => {
        if (res && res.code === SUCCESS) {
          setFormContext(res.data);
        }
      })
      .catch((e) => {
        sendNotify({
          msg: e.message,
          status: 3,
          show: true,
        });
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
        return (
          <LinkWrapper key={item.id} link={item.link} closeHandle={closeHandle}>
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

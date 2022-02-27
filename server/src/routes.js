import React from "react";
import { Navigate } from "react-router-dom";
import DashboardLayout from "src/layouts/DashboardLayout";
import MainLayout from "src/layouts/MainLayout";
import NotFoundView from "src/views/Errors/NotFoundView";
import NoWorkspace from "src/views/Errors/NoWorkspace";
import LoginPage from "src/views/Login";
import RoleSelection from "src/views/RoleSelection";
import Dashboard from "src/views/Dashboard";
import FormPage from "src/views/FormPage";
import WorkflowManagement from "src/views/WorkflowManagement";
import BashCommand from "src/views/BashCommand";
import FormManagement from "src/views/FormManagement";
import OrgSetting from "src/views/OrgSetting";
import WorkspaceCreation from "src/views/WorkspaceCreation";
import WorkspaceManage from "src/views/WorkspaceManage";
import PolicyCreation from "src/views/PolicyCreation";
import DataOnBoarding from "src/views/DataOnBoarding";
import DataDiscovery from "src/views/DataDiscovery";
import Visualisation from "src/views/Visualisation";
import GetDataAccess from "src/views/GetDataAccess";
import WorkflowPage from "src/views/WorkflowPage";
import RequestDetailPage from "src/views/RequestDetailPage";

const routes = (language, isLoggedIn, haveRole) => {
  const lanPrefix = ""; //language === "cn" ? "/cn" : "";
  return [
    {
      path: lanPrefix + "/login",
      element: <LoginPage />,
    },
    {
      path: lanPrefix + "/orgSetting",
      element: <OrgSetting />,
    },
    {
      path: lanPrefix + "/roleSelect",
      element: <RoleSelection />,
    },
    {
      path: lanPrefix + "/noWorkspace",
      element: <NoWorkspace />,
    },
    {
      path: lanPrefix + "/app",
      element: <DashboardLayout />,
      children: [
        { path: "/dashboard", element: <Dashboard /> },
        { path: "/forms", element: <FormPage /> },
        { path: "/formManagement", element: <FormManagement /> },
        { path: "/createTagTemplate", element: <FormManagement tagTemplate /> },
        { path: "/workflowManagement", element: <WorkflowManagement /> },
        { path: "/bashCommand", element: <BashCommand /> },
        { path: "/WorkspaceManage", element: <WorkspaceManage /> },
        { path: "/WorkspaceCreation", element: <WorkspaceCreation /> },
        { path: "/policyCreation", element: <PolicyCreation /> },
        { path: "/dataOnboarding", element: <DataOnBoarding /> },
        { path: "/dataDiscovery", element: <DataDiscovery /> },
        { path: "/visualisation", element: <Visualisation /> },
        { path: "/getDataAccess", element: <GetDataAccess /> },
        { path: "/workflow", element: <WorkflowPage /> },
        { path: "/requestDetail", element: <RequestDetailPage /> },
        {
          path: "/approvalFlow",
          element: <RequestDetailPage approved={true} />,
        },
      ],
    },
    {
      path: lanPrefix + "/",
      element: <MainLayout />,
      children: [
        { path: "404", element: <NotFoundView /> },
        {
          path: "/",
          element: <Navigate to="./app/dashboard" />,
        },
        { path: "*", element: <Navigate to="./404" /> },
      ],
    },
  ];
};

export default routes;

DROP TABLE IF EXISTS `orgTable`;
CREATE TABLE `orgTable` (
  `ID` int(11) NOT NULL AUTO_INCREMENT COMMENT 'org_id',
  `ORG_NAME` varchar(128) DEFAULT NULL COMMENT 'org_name',
  `PROJECT_NAME` varchar(128) DEFAULT NULL COMMENT 'project name',
  `AIRFLOW_URL` varchar(1024) DEFAULT NULL COMMENT 'aiflow url',
  `CREATE_TIME` datetime DEFAULT NULL COMMENT 'create_time',
  `DES` varchar(128) DEFAULT NULL COMMENT 'comment',
  PRIMARY KEY (`ID`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=351 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
DROP TABLE IF EXISTS `org_to_adgroupTable`;
CREATE TABLE `org_to_adgroupTable` (
  `ID` int NOT NULL AUTO_INCREMENT COMMENT 'org id',
  `ORG_ID` int DEFAULT NULL COMMENT 'org_id',
  `AD_GROUP_ID` int DEFAULT NULL COMMENT 'ad_group_id',
  `ROLE_LIST` varchar(128) DEFAULT NULL COMMENT 'ad group role list',
  PRIMARY KEY (`ID`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=351 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

DROP TABLE IF EXISTS `workspaceTable`;
CREATE TABLE `workspaceTable` (
  `ID` int NOT NULL AUTO_INCREMENT COMMENT 'workspace_id',
  `WORKSPACE_NAME` varchar(128) DEFAULT NULL COMMENT 'workspace_name',
  `RECERTIFICATION_CYCLE` varchar(128) DEFAULT NULL COMMENT 'recertification cycle',
  `IT_APPROVAL` tinyint(1) DEFAULT '1' COMMENT 'Need workspace IT approval',
  `HEAD_APPROVAL` tinyint(1) DEFAULT '1' COMMENT 'Need workspace Head approval',
  `REGOINS` text COMMENT 'Need workspace Head approval',
  `CREATE_TIME` datetime DEFAULT NULL COMMENT 'create_time',
  `DES` varchar(128) DEFAULT NULL COMMENT 'comment',
  PRIMARY KEY (`ID`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=351 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
DROP TABLE IF EXISTS `workspace_to_adgroupTable`;
CREATE TABLE `workspace_to_adgroupTable` (
  `ID` int NOT NULL AUTO_INCREMENT COMMENT 'id',
  `LABEL_LIST` varchar(128) DEFAULT NULL,
  `WORKSPACE_ID` int DEFAULT NULL COMMENT 'workspace_id',
  `AD_GROUP_ID` int DEFAULT NULL COMMENT 'ad_group_id',
  `ROLE_LIST` varchar(128) DEFAULT NULL COMMENT 'ad group role list',
  PRIMARY KEY (`ID`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=351 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

DROP TABLE IF EXISTS `usecaseResourceTable`;
CREATE TABLE `usecaseResourceTable` (
  `ID` int NOT NULL AUTO_INCREMENT COMMENT 'resource_id',
  `WORKSPACE_ID` int NOT NULL COMMENT 'workspace_id',
  `USECASE_ID` int DEFAULT '-1' COMMENT 'workspace_id',
  `LABEL` varchar(512) DEFAULT NULL COMMENT 'usecase label',
  `OWNER_GROUP` varchar(512) DEFAULT NULL COMMENT 'owner group',
  `TEAM_GROUP` varchar(512) DEFAULT NULL COMMENT 'team group',
  `SERVICE_ACCOUNT` varchar(512) DEFAULT NULL COMMENT 'service account',
  `ITEMS` text COMMENT 'items',
  `AVAILABLE` int DEFAULT '1' COMMENT 'available flag',
  `CREATE_TIME` datetime DEFAULT NULL COMMENT 'create_time',
  `DES` varchar(128) DEFAULT NULL COMMENT 'comment',
  PRIMARY KEY (`ID`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=351 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

DROP TABLE IF EXISTS `gcpResourceTable`;
CREATE TABLE `gcpResourceTable` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'resource_id',
  `workspace_id` int NOT NULL COMMENT 'workspace_id',
  `usecase_id` int DEFAULT '-1' COMMENT 'usecase_id',
  `input_form_id` varchar(512) DEFAULT NULL COMMENT 'resource name',
  `resource_label` varchar(512) DEFAULT NULL COMMENT 'resource label',
  `resource_name` varchar(512) DEFAULT NULL COMMENT 'resource name',
  `create_time` datetime DEFAULT NULL COMMENT 'create_time',
  `des` varchar(128) DEFAULT NULL COMMENT 'comment',
  PRIMARY KEY (`ID`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=351 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

DROP TABLE IF EXISTS `usecaseTable`;
CREATE TABLE `usecaseTable` (
  `ID` int NOT NULL AUTO_INCREMENT COMMENT 'usecase_id',
  `WORKSPACE_ID` int NOT NULL COMMENT 'workspace_id',
  `USECASE_NAME` varchar(128) DEFAULT NULL COMMENT 'usecase_name',
  `VALIDITY_TILL` varchar(128) DEFAULT NULL COMMENT 'usecase_name validity till',
  `BUDGET` varchar(128) DEFAULT NULL COMMENT 'usecase_name budget',
  `INPUT_FORM_ID` int NOT NULL COMMENT 'input_form_id',
  `REGION_COUNTRY` varchar(128) DEFAULT NULL COMMENT 'usecase_name region/country',
  `RESOURCES_ACCESS_LIST` text COMMENT 'usecase_name resource access list',
  `SERVICE_ACCOUNT` text COMMENT 'usecase_name service account',
  `CROSS_REGION` text COMMENT 'will the usecase_name use data cross region',
  `CREATE_TIME` datetime DEFAULT NULL COMMENT 'create_time',
  `DES` varchar(128) DEFAULT NULL COMMENT 'comment',
  PRIMARY KEY (`ID`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=351 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
DROP TABLE IF EXISTS `usecase_to_adgroupTable`;
CREATE TABLE `usecase_to_adgroupTable` (
  `ID` int NOT NULL AUTO_INCREMENT COMMENT 'id',
  `LABEL_LIST` varchar(128) DEFAULT NULL COMMENT 'ad group label list',
  `USECASE_ID` int DEFAULT NULL COMMENT 'usecase_id',
  `AD_GROUP_ID` int DEFAULT NULL COMMENT 'ad_group_id',
  `ROLE_LIST` varchar(128) DEFAULT NULL COMMENT 'ad group role list',
  PRIMARY KEY (`ID`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=351 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;


-- ----------------------------
-- Table structure for ldap [entity]
-- ----------------------------
DROP TABLE IF EXISTS `ldapTable`;
CREATE TABLE `ldapTable` (
  `ID` int NOT NULL AUTO_INCREMENT COMMENT 'ldap_id',
  `HOST` varchar(64) DEFAULT NULL COMMENT 'ldap host',
  `PORT` int DEFAULT NULL COMMENT 'ldap port',
  `CER_PATH` varchar(512) DEFAULT NULL COMMENT 'save ldap cer path',
  `USE_SSL` tinyint(1) DEFAULT '1' COMMENT 'permission type',
  `ADMIN_DN` varchar(256) DEFAULT NULL COMMENT 'admin dn',
  `ADMIN_PWD` varchar(512) DEFAULT NULL COMMENT 'admin password',

  `USER_SEARCH_BASE` varchar(128) DEFAULT NULL COMMENT 'user search base',
  `USER_SERACH_FILTER` varchar(64) DEFAULT NULL COMMENT 'user search filter',
  `DISPLAY_NAME_LDAP_ATTRIBUTE` varchar(64) DEFAULT NULL COMMENT 'display name ldap attribute',
  `EMAIL_ADDRESS_LDAP_ATTRIBUTE` varchar(64) DEFAULT NULL COMMENT 'email address ldap attribute',
  `USER_ADGROUP_ATTRIBUTE` varchar(64) DEFAULT NULL COMMENT 'user adgroup attribute',

  `GROUP_SEARCH_BASE` varchar(128) DEFAULT NULL COMMENT 'group search base',
  `GROUP_SERACH_FILTER` varchar(64) DEFAULT NULL COMMENT 'group search filter',
  `GROUP_MEMBER_ATTRIBUTE` varchar(64) DEFAULT NULL COMMENT 'group member attribute',
  `GROUP_EMAIL_SUFFIX` varchar(128) DEFAULT NULL COMMENT 'group mail suffix',

  `CREATE_TIME` datetime DEFAULT NULL COMMENT 'create_time',
  `TIME_MODIFY` datetime DEFAULT NULL COMMENT 'last_modify_time',
  PRIMARY KEY (`ID`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

DROP TABLE IF EXISTS `smtpTable`;
CREATE TABLE `smtpTable` (
  `ID` int(11) NOT NULL AUTO_INCREMENT COMMENT 'smtp_id',
  `MAIL_HOST` varchar(64) DEFAULT NULL COMMENT 'smtp host',
  `MAIL_USER` varchar(64) DEFAULT NULL COMMENT 'smtp user',
  `MAIL_PASS` varchar(64) DEFAULT NULL COMMENT 'smtp pwd',
  `PORT` int(11) DEFAULT NULL COMMENT 'ldap port',
  `USE_TLS` boolean DEFAULT true COMMENT 'ues tls',
  `CREATE_TIME` datetime DEFAULT NULL COMMENT 'create_time',
  `TIME_MODIFY` datetime DEFAULT NULL COMMENT 'last_modify_time',
  PRIMARY KEY (`ID`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

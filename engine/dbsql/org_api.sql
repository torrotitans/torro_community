DROP TABLE IF EXISTS `orgTable`;
CREATE TABLE `orgTable` (
  `ID` int(11) NOT NULL AUTO_INCREMENT COMMENT 'org_id',
  `ORG_NAME` varchar(128) DEFAULT NULL COMMENT 'org_name',
  `PROJECT_NAME` varchar(128) DEFAULT NULL COMMENT 'project name',
  `CREATE_TIME` datetime DEFAULT NULL COMMENT 'create_time',
  `DES` varchar(128) DEFAULT NULL COMMENT 'comment',
  PRIMARY KEY (`ID`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=351 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
DROP TABLE IF EXISTS `org_to_adgroupTable`;
CREATE TABLE `org_to_adgroupTable` (
  `ID` int(11) NOT NULL AUTO_INCREMENT COMMENT 'org id',
  `ORG_ID` int(11) DEFAULT NULL COMMENT 'org_id',
  `AD_GROUP_ID` int(11) DEFAULT NULL COMMENT 'ad_group_id',
  `ROLE_LIST` varchar(128) DEFAULT NULL COMMENT 'ad group role list',
  PRIMARY KEY (`ID`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=351 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

DROP TABLE IF EXISTS `workspaceTable`;
CREATE TABLE `workspaceTable` (
  `ID` int(11) NOT NULL AUTO_INCREMENT COMMENT 'workspace_id',
  `WORKSPACE_NAME` varchar(128) DEFAULT NULL COMMENT 'workspace_name',
--  `GCP_PROJECT` varchar(128) DEFAULT NULL COMMENT 'gcp_project_name',
--  `ADMIN_SA` varchar(128) DEFAULT NULL COMMENT 'gcp admin service account',
--  `ADMIN_JSON_FILE_PATH` varchar(128) DEFAULT NULL COMMENT 'gcp admin service account jsonkey',
  `RECERTIFICATION_CYCLE` varchar(128) DEFAULT NULL COMMENT 'recertification cycle',
  `IT_APPROVAL` boolean DEFAULT true COMMENT 'Need workspace IT approval',
  `HEAD_APPROVAL` boolean DEFAULT true COMMENT 'Need workspace Head approval',
  `REGOINS` TEXT DEFAULT null COMMENT 'Need workspace Head approval',
  `CREATE_TIME` datetime DEFAULT NULL COMMENT 'create_time',
  `DES` varchar(128) DEFAULT NULL COMMENT 'comment',
  PRIMARY KEY (`ID`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=351 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
DROP TABLE IF EXISTS `workspace_to_adgroupTable`;
CREATE TABLE `workspace_to_adgroupTable` (
  `ID` int(11) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `LABEL_LIST` varchar(128) DEFAULT NULL COMMENT 'ad group label list',
  `WORKSPACE_ID` int(11) DEFAULT NULL COMMENT 'workspace_id',
  `AD_GROUP_ID` int(11) DEFAULT NULL COMMENT 'ad_group_id',
  `ROLE_LIST` varchar(128) DEFAULT NULL COMMENT 'ad group role list',
  PRIMARY KEY (`ID`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=351 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

DROP TABLE IF EXISTS `usecaseTable`;
CREATE TABLE `usecaseTable` (
  `ID` int(11) NOT NULL AUTO_INCREMENT COMMENT 'usecase_id',
  `WORKSPACE_ID` int(11) NOT NULL COMMENT 'workspace_id',
  `USECASE_NAME` varchar(128) DEFAULT NULL COMMENT 'usecase_name',
  `VALIDITY_TILL` varchar(128) DEFAULT NULL COMMENT 'usecase_name validity till',
  `BUDGET` varchar(128) DEFAULT NULL COMMENT 'usecase_name budget',
  `REGION_COUNTRY` varchar(128) DEFAULT NULL COMMENT 'usecase_name region/country',
  `RESOURCES_ACCESS_LIST` TEXT DEFAULT NULL COMMENT 'usecase_name resource access list',
  `SERVICE_ACCOUNT` TEXT DEFAULT NULL COMMENT 'usecase_name service account',
  `CROSS_REGION` TEXT DEFAULT NULL COMMENT 'will the usecase_name use data cross region',
  `CREATE_TIME` datetime DEFAULT NULL COMMENT 'create_time',
  `DES` varchar(128) DEFAULT NULL COMMENT 'comment',
  PRIMARY KEY (`ID`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=351 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
DROP TABLE IF EXISTS `usecase_to_adgroupTable`;
CREATE TABLE `usecase_to_adgroupTable` (
  `ID` int(11) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `LABEL_LIST` varchar(128) DEFAULT NULL COMMENT 'ad group label list',
  `USECASE_ID` int(11) DEFAULT NULL COMMENT 'usecase_id',
  `AD_GROUP_ID` int(11) DEFAULT NULL COMMENT 'ad_group_id',
  `ROLE_LIST` varchar(128) DEFAULT NULL COMMENT 'ad group role list',
  PRIMARY KEY (`ID`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=351 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

DROP TABLE IF EXISTS `teamTable`;
CREATE TABLE `teamTable` (
  `ID` int(11) NOT NULL AUTO_INCREMENT COMMENT 'team_id',
  `TEAM_NAME` varchar(128) DEFAULT NULL COMMENT 'team_name',
  `CREATE_TIME` datetime DEFAULT NULL COMMENT 'create_time',
  `DES` varchar(128) DEFAULT NULL COMMENT 'comment',
  PRIMARY KEY (`ID`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=351 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
DROP TABLE IF EXISTS `team_to_adgroupTable`;
CREATE TABLE `team_to_adgroupTable` (
  `ID` int(11) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `TEAM_ID` int(11) DEFAULT NULL COMMENT 'team_id',
  `AD_GROUP_ID` int(11) DEFAULT NULL COMMENT 'ad_group_id',
  `ROLE_LIST` varchar(128) DEFAULT NULL COMMENT 'ad group role list',
  PRIMARY KEY (`ID`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=351 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Table structure for ldap [entity]
-- ----------------------------
DROP TABLE IF EXISTS `ldapTable`;
CREATE TABLE `ldapTable` (
  `ID` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ldap_id',
  `HOST` varchar(64) DEFAULT NULL COMMENT 'ldap host',
  `PORT` int(11) DEFAULT NULL COMMENT 'ldap port',
  `CER_PATH` varchar(512) DEFAULT NULL COMMENT 'save ldap cer path',
  `USE_SLL` boolean DEFAULT true COMMENT 'permission type',
  `SEARCH_BASE` varchar(64) DEFAULT NULL COMMENT 'search base',
  `ADMIN` varchar(64) DEFAULT NULL COMMENT 'admin email',
  `ADMIN_PWD` varchar(512) DEFAULT NULL COMMENT 'admin password',
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
  `USE_SLL` boolean DEFAULT true COMMENT 'permission type',
  `CREATE_TIME` datetime DEFAULT NULL COMMENT 'create_time',
  `TIME_MODIFY` datetime DEFAULT NULL COMMENT 'last_modify_time',
  PRIMARY KEY (`ID`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

DROP TABLE IF EXISTS `taxonomyTable`;
CREATE TABLE `taxonomyTable` (
  `id` int(3) NOT NULL AUTO_INCREMENT COMMENT 'local policy tag id',
  `workspace_id` int(11) NOT NULL COMMENT 'workspace_id',
  `input_form_id` int(3) NOT NULL COMMENT 'input form id',
  `creator_id` varchar(256) DEFAULT NULL COMMENT 'creator id',
  `project_id` varchar(256) DEFAULT NULL COMMENT 'project id',
  `location` varchar(256) DEFAULT NULL COMMENT 'location',
  `display_name` varchar(256) DEFAULT NULL COMMENT 'display_name',
  `gcp_taxonomy_id` varchar(1024) DEFAULT NULL COMMENT 'taxonomy_id',
  `ad_group` varchar(256) DEFAULT NULL COMMENT 'adgroup id',
  `description` varchar(1024) DEFAULT NULL COMMENT 'description',
  `create_time` datetime DEFAULT NULL COMMENT 'create_time',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

DROP TABLE IF EXISTS `policyTagsTable`;
CREATE TABLE `policyTagsTable` (
  `id` int(3) NOT NULL AUTO_INCREMENT COMMENT 'local policy tag id',
  `local_taxonomy_id` int(3) DEFAULT -1 COMMENT 'taxonomy_id',
  `parent_local_id` int(3) DEFAULT -1 COMMENT 'parent local id',
  `gcp_policy_tag_id` varchar(1024) DEFAULT '' COMMENT 'gcp policy tag id',
  `ad_group` varchar(256) DEFAULT NULL COMMENT 'adgroup id',
  `display_name` varchar(256) DEFAULT NULL COMMENT 'display_name',
  `description` varchar(1024) DEFAULT NULL COMMENT 'description',
  `create_time` datetime DEFAULT NULL COMMENT 'create_time',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

DROP TABLE IF EXISTS `tagTemplatesTable`;
CREATE TABLE `tagTemplatesTable` (
  `input_form_id` int(3) NOT NULL COMMENT 'input form id',
  `workspace_id` int(11) NOT NULL COMMENT 'workspace_id',
  `tag_template_form_id` int(3) DEFAULT NULL COMMENT 'tag_template_form_id',
  `creator_id` varchar(256) DEFAULT NULL COMMENT 'creator id',
  `project_id` varchar(256) DEFAULT NULL COMMENT 'project id',
  `location` varchar(256) DEFAULT NULL COMMENT 'location',
  `display_name` varchar(256) DEFAULT NULL COMMENT 'display_name',
  `tag_template_id` varchar(1024) DEFAULT NULL COMMENT 'tag_template_id',
  `field_list` Text DEFAULT NULL COMMENT 'field_list',
  `description` varchar(1024) DEFAULT NULL COMMENT 'description',
  `create_time` datetime DEFAULT NULL COMMENT 'create_time',  PRIMARY KEY (`input_form_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

DROP TABLE IF EXISTS `tagTemplatesValueTable`;
CREATE TABLE `tagTemplatesValueTable` (
  `id` int(3) NOT NULL AUTO_INCREMENT COMMENT 'tagTemplates value id',
  `form_id` int(11) NOT NULL COMMENT 'form_id',
  `input_form_id` int(3) NOT NULL COMMENT 'input form id',
  `creator_id` varchar(256) DEFAULT NULL COMMENT 'creator id',
  `tag_template_local_id` varchar(256) DEFAULT NULL COMMENT 'tag_template_local_id',
  `field_list` Text DEFAULT NULL COMMENT 'field_list',
  `create_time` datetime DEFAULT NULL COMMENT 'create_time',  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
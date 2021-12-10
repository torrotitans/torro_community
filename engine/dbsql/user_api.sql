/*
 Navicat Premium Data Transfer

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 50725
 Source Host           : localhost:3306
 Source Schema         : user_api

 Target Server Type    : MySQL
 Target Server Version : 50725
 File Encoding         : 65001

 Date: 27/10/2019 17:05:47
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- users -< role        <- user_roles ->
-- role -< permission   <- roles_permission ->
-- api -< api_permission   <- api_permission ->
-- user permission >= api permission [auth_helper.py:144 line]
-- ----------------------------
-- workspace > usecase > team
-- api get [token]
-- [token] get user info
-- [token] in cookie
-- login page name pwd-> api generate [token] -> home

-- role: [api list],
-- w_role>u_role>t_role
-- w/u/t <--> ad group


-- ----------------------------
-- Table structure for users [entity]
-- ----------------------------
DROP TABLE IF EXISTS `userTable`;
CREATE TABLE `userTable` (
  `ID` int(11) NOT NULL AUTO_INCREMENT COMMENT 'user_id',
  `ACCOUNT_NAME` varchar(128) DEFAULT NULL COMMENT 'account_name',
  `ACCOUNT_ID` varchar(128) DEFAULT NULL COMMENT 'account_id',
  `PASS_WORD` varchar(256) DEFAULT NULL COMMENT 'password',
  `GROUP_LIST` varchar(1024) DEFAULT NULL COMMENT 'ad group list',
  `CREATE_TIME` datetime DEFAULT NULL COMMENT 'create_time',
  `DES` varchar(128) DEFAULT NULL COMMENT 'comment',
  PRIMARY KEY (`ID`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=351 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
insert into userTable values (1, 'TorroAdmin', 'TorroAdmin', 'torro123456', '2021-05-29', 'the first user');

DROP TABLE IF EXISTS `user_to_adgroupTable`;
CREATE TABLE `user_to_adgroupTable` (
  `ID` int(11) NOT NULL AUTO_INCREMENT COMMENT 'user ad id',
  `USER_ID` int(11) DEFAULT NULL COMMENT 'user_id',
  `AD_GROUP_ID` int(11) DEFAULT NULL COMMENT 'ad_group_id',
  PRIMARY KEY (`ID`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=351 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

DROP TABLE IF EXISTS `adgroupTable`;
CREATE TABLE `adgroupTable` (
  `ID` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ad_group_id',
  `GROUP_MAIL` varchar(128) DEFAULT NULL COMMENT 'ad_group_email',
  `CREATE_TIME` datetime DEFAULT NULL COMMENT 'create_time',
  `DES` varchar(128) DEFAULT NULL COMMENT 'comment',
  PRIMARY KEY (`ID`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=351 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

DROP TABLE IF EXISTS `roleTable`;
CREATE TABLE `roleTable` (
  `ID` int(11) NOT NULL AUTO_INCREMENT COMMENT 'role_id',
  `NAME` varchar(64) DEFAULT NULL COMMENT 'role_name',
  `API_PERMISSION_LIST` text DEFAULT NULL COMMENT 'api permission list',
  `CREATE_TIME` datetime DEFAULT NULL COMMENT 'create_time',
  `DES` varchar(128) DEFAULT NULL COMMENT 'comment',
  PRIMARY KEY (`ID`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
insert into roleTable values (1, 'admin', '["*-*"]', '2021-05-29', 'the admin role');
insert into roleTable values (2, 'visitor', '[]', '2021-05-29', 'the admin role');
insert into roleTable values (3, 'GOVERNOR', '["*-*"]', '2021-06-06', 'the governor role');
insert into roleTable values (4, 'IT', '["*-*"]', '2021-06-06', 'the it role');
insert into roleTable values (5, 'USER', '["*-*"]', '2021-06-06', 'the user role');


-- go in, set org info+org group+ldap, org group get base access role;
-- login in, get role list and permission list; choose role ->set role (ok):testing

---- ----------------------------
---- Table structure for users [entity]
---- ----------------------------
--DROP TABLE IF EXISTS `userTable`;
--CREATE TABLE `userTable` (
--  `ID` int(11) NOT NULL AUTO_INCREMENT COMMENT 'user_id',
--  `ACCOUNT_NAME` varchar(128) DEFAULT NULL COMMENT 'account_name',
--  `ACCOUNT_ID` varchar(128) DEFAULT NULL COMMENT 'account_id',
--  `PASS_WORD` varchar(256) DEFAULT NULL COMMENT 'password',
--  `TEAM_ROLE_ID_LIST` text DEFAULT NULL COMMENT 'team role id list',
--  `USECASE_ROLE_ID_LIST` text DEFAULT NULL COMMENT 'usecase role id list',
--  `WORKSPACE_ROLE_ID_LIST` text DEFAULT NULL COMMENT 'workspace role id list',
--  `CREATE_TIME` datetime DEFAULT NULL COMMENT 'create_time',
--  `DES` varchar(128) DEFAULT NULL COMMENT 'comment',
--  PRIMARY KEY (`ID`) USING BTREE
--) ENGINE=InnoDB AUTO_INCREMENT=351 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
---- group -- role[api2 api3 api3]
---- ----------------------------
---- Table structure for role [entity]
---- ----------------------------
--DROP TABLE IF EXISTS `roleTable`;
--CREATE TABLE `roleTable` (
--  `ID` int(11) NOT NULL AUTO_INCREMENT COMMENT 'role_id',
--  `NAME` varchar(64) DEFAULT NULL COMMENT 'role_name',
--  `API_PERMISSION_LIST` text DEFAULT NULL COMMENT 'api permission list',
--  `CREATE_TIME` datetime DEFAULT NULL COMMENT 'create_time',
--  `DES` varchar(128) DEFAULT NULL COMMENT 'comment',
--  `TIME_MODIFY` datetime DEFAULT NULL COMMENT 'last_modify_time',
--  PRIMARY KEY (`ID`) USING BTREE
--) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
----- IT: [api1, api2, api3]
--insert into roleTable values (null, 'VIEWER', '["*-GET"]', '2021-05-14', 'can call all get api', '2021-05-14');
--insert into roleTable values (null, 'ADMIN', '["*-*"]', '2021-05-14', 'can call all the api', '2021-05-14');
--insert into userTable values (null, 'second', '45069643', 'pbkdf2:sha256:150000$zaRcpqDl$991ac571b240c1c84ea4d4acb268b5c4a09a12e5b331a9bd656e438390fdda89', '', '{}', '{"1": "15"}', '2021-05-14', 'user second');
--
--
---- ----------------------------
---- Table structure for api [entity]
---- ----------------------------
--DROP TABLE IF EXISTS `apiPermissionTable`;
--CREATE TABLE `apiPermissionTable` (
--  `ID` int(11) NOT NULL AUTO_INCREMENT COMMENT 'api_id',
--  `ENDPOINT` varchar(64) DEFAULT NULL COMMENT 'api_endpoint',
--  `METHOD` varchar(64) DEFAULT NULL COMMENT 'api_method',
--  `PERMISSION_TYPE` varchar(64) DEFAULT NULL COMMENT 'permission type',
--  `PERMISSION_LEVEL` int(11) DEFAULT NULL COMMENT 'permission level',
--  `CREATE_TIME` datetime DEFAULT NULL COMMENT 'create_time',
--  `DES` varchar(128) DEFAULT NULL COMMENT 'comment',
--  `TIME_MODIFY` datetime DEFAULT NULL COMMENT 'last_modify_time',
--  PRIMARY KEY (`ID`) USING BTREE
--) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
--
---- ----------------------------
---- Table structure for ldap [entity]
---- ----------------------------
--DROP TABLE IF EXISTS `ldapTable`;
--CREATE TABLE `ldapTable` (
--  `ID` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ldap_id',
--  `HOST` varchar(64) DEFAULT NULL COMMENT 'ldap host',
--  `PORT` int(11) DEFAULT NULL COMMENT 'ldap port',
--  `CER_PATH` int(11) DEFAULT NULL COMMENT 'save ldap cer path',
--  `USE_SLL` varchar(64) DEFAULT NULL COMMENT 'permission type',
--  `ADMIN` varchar(64) DEFAULT NULL COMMENT 'admin email',
--  `ADMIN_PWD` varchar(512) DEFAULT NULL COMMENT 'admin password',
--  `CREATE_TIME` datetime DEFAULT NULL COMMENT 'create_time',
--  `TIME_MODIFY` datetime DEFAULT NULL COMMENT 'last_modify_time',
--  PRIMARY KEY (`ID`) USING BTREE
--) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
--insert into ldapTable values (null,)
---- ----------------------------
---- Table structure for organization [entity]
---- ----------------------------
--DROP TABLE IF EXISTS `orgTable`;
--CREATE TABLE `orgTable` (
--  `ID` int(11) NOT NULL AUTO_INCREMENT COMMENT 'org_id',
--  `ADMIN_MAIL` varchar(64) DEFAULT NULL COMMENT 'admin id',
--  `LOGIN_TYPE` int(11) DEFAULT NULL COMMENT 'what login method will set',
--  `CREATE_TIME` datetime DEFAULT NULL COMMENT 'create_time',
--  `TIME_MODIFY` datetime DEFAULT NULL COMMENT 'last_modify_time',
--  `DES` varchar(128) DEFAULT NULL COMMENT 'comment',
--  PRIMARY KEY (`ID`) USING BTREE
--) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
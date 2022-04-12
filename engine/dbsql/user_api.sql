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
  `ID` int NOT NULL AUTO_INCREMENT COMMENT 'user_id',
  `ACCOUNT_NAME` varchar(128) DEFAULT NULL COMMENT 'account_name',
  `ACCOUNT_ID` varchar(128) DEFAULT NULL COMMENT 'account_id',
  `ACCOUNT_CN` varchar(128) DEFAULT NULL COMMENT 'account_cn',
  `PASS_WORD` varchar(256) DEFAULT NULL COMMENT 'password',
  `GROUP_LIST` text DEFAULT NULL COMMENT 'ad group list',
  `CREATE_TIME` datetime DEFAULT NULL COMMENT 'create_time',
  `DES` text DEFAULT NULL COMMENT 'comment',
  PRIMARY KEY (`ID`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=351 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
insert into userTable values (1, 'TorroAdmin', 'TorroAdmin', 'TorroAdmin', 'torro123456', '[]', '2021-05-29', 'the first user');

DROP TABLE IF EXISTS `user_to_adgroupTable`;
CREATE TABLE `user_to_adgroupTable` (
  `ID` int NOT NULL AUTO_INCREMENT COMMENT 'user ad id',
  `USER_ID` int DEFAULT NULL COMMENT 'user_id',
  `AD_GROUP_ID` int DEFAULT NULL COMMENT 'ad_group_id',
  PRIMARY KEY (`ID`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=351 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

DROP TABLE IF EXISTS `adgroupTable`;
CREATE TABLE `adgroupTable` (
  `ID` int NOT NULL AUTO_INCREMENT COMMENT 'ad_group_id',
  `GROUP_MAIL` varchar(128) DEFAULT NULL COMMENT 'ad_group_email',
  `CREATE_TIME` datetime DEFAULT NULL COMMENT 'create_time',
  `DES` varchar(128) DEFAULT NULL COMMENT 'comment',
  PRIMARY KEY (`ID`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=351 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

DROP TABLE IF EXISTS `roleTable`;
CREATE TABLE `roleTable` (
  `ID` int NOT NULL AUTO_INCREMENT COMMENT 'role_id',
  `NAME` varchar(64) DEFAULT NULL COMMENT 'role_name',
  `API_PERMISSION_LIST` longtext COMMENT 'api permission list',
  `CREATE_TIME` datetime DEFAULT NULL COMMENT 'create_time',
  `DES` varchar(128) DEFAULT NULL COMMENT 'comment',
  PRIMARY KEY (`ID`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

insert into roleTable values (1, 'admin', '["*-*"]', '2021-06-06', 'the org admin role');
insert into roleTable values (2, 'viewer', '["interfacesystemnotify-*"]', '2021-06-06', 'the org viewer role');
insert into roleTable values (3, 'GOVERNOR', '["interfaceDebug-*, *-GET, interfaceGovernance-*, "]', '2021-06-06', 'the governor role');
insert into roleTable values (4, 'IT', '["interfaceDebug-*, *"]', '2021-06-06', 'the it role');
insert into roleTable values (5, 'USER', '["*-*"]', '2021-06-06', 'the user role');

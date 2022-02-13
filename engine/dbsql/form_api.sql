SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS `formTable`;
CREATE TABLE `formTable` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'form_id',
  `workspace_id` int NOT NULL COMMENT 'workspace id',
  `usecase_id` int NOT NULL DEFAULT '0' COMMENT 'usecase_id',
  `title` varchar(256) DEFAULT NULL COMMENT 'form_title',
  `available` int DEFAULT '1' COMMENT 'available flag',
  `fields_num` int DEFAULT NULL COMMENT 'form fields num',
  `creator_id` varchar(256) DEFAULT NULL COMMENT 'creator id',
  `fields_list` text COMMENT 'field list',
  `hide` int DEFAULT '0' COMMENT 'if show the form in ui or not',
  `create_time` datetime DEFAULT NULL COMMENT 'create_time',
  `updated_time` datetime DEFAULT NULL COMMENT 'last_updated_time',
  `des` varchar(1024) DEFAULT NULL COMMENT 'description',
  `u_max_id` varchar(8) DEFAULT '0' COMMENT 'user field max id',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=351 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
insert into formTable ( id, workspace_id, usecase_id, title, available, fields_num, u_max_id, creator_id, fields_list, hide, create_time, updated_time, des) values (2, 0, 0, 'Create UseCase', 1, 11, 'u11', 1, '[{"id": "s1", "label": "Region / Country"}, {"default": "", "des": "Use case owner AD group", "edit": 1, "id": "u2", "label": "Use case Owner Group", "options": [], "placeholder": "Use case owner AD group", "style": 3}, {"default": "", "des": "Use case team AD group", "edit": 1, "id": "u3", "label": "Use case Team Group", "options": [], "placeholder": "Use case team AD group", "style": 3}, {"default": "2021-08-21T10:59:53.020Z", "des": "Use case validity till date", "edit": 1, "id": "u4", "label": "Validity Date", "options": [], "placeholder": "Use case validity till date", "style": 6}, {"default": "", "des": "Use case name", "edit": 1, "id": "u5", "label": "Use Case Name", "options": [], "placeholder": "Use case name", "style": 3}, {"default": "", "des": "Use case description", "edit": 1, "id": "u6", "label": "Description", "options": [], "placeholder": "Use case description", "style": 3}, {"default": "", "des": "Use case total budget", "edit": 1, "id": "u7", "label": "Budget", "options": [], "placeholder": "Use case total budget", "style": 3}, {"default": "", "des": "Service account", "edit": 1, "id": "u8", "label": "Admin Service Account", "options": [], "placeholder": "Service account", "style": 3}, {"default": "", "des": "Use case resources access", "edit": 1, "id": "u9", "label": "Resources Access", "options": [{"label": "Jupyter", "value": "Jupyter"}, {"label": "Datastudio", "value": "Datastudio"}], "placeholder": "Use case resources access", "style": 1}, {"default": "", "des": "Allow cross region support", "edit": 1, "id": "u10", "label": "Allow Cross Region", "options": [], "placeholder": "Allow cross region support", "style": 5}]', 1, '2021-08-22', '2021-08-22', 'Create UseCase');
insert into formTable ( id, workspace_id, usecase_id, title, available, fields_num, u_max_id, creator_id, fields_list, hide, create_time, updated_time, des) values (1, 0, 0, 'Add user to use case', 1, 7, 'u7', 1, '[{"create_time": "Wed, 08 Dec 2021 10:17:00 GMT", "default": "DNA_CN", "des": null, "id": "d15", "label": "Use case", "options": [{"label": "DNA_CN", "value": "Engineer@torro.ai"}, {"label": "DNA_SG", "value": "Engineer@torro.ai"}], "placeholder": "DNA_CN", "style": 2, "value_num": 2}, {"default": "", "des": "Staff Email", "edit": 1, "id": "u1", "label": "Staff Email", "options": [], "placeholder": "user", "required": true, "style": 3}, {"default": "12345678", "des": "Staff ID", "edit": 1, "id": "u4", "label": "Staff ID", "options": [], "placeholder": "", "required": true, "style": 3}, {"default": "", "des": "Employment Type", "edit": 1, "id": "u5", "label": "Employment Type", "options": [{"label": "Permanent", "value": "perm"}, {"label": "Fixed Term Contractor", "value": "fix"}, {"label": "Project Contractor", "value": "pjt"}], "placeholder": "", "required": true, "style": 2}, {"default": "", "des": "How long do you need access to this use case?", "edit": 1, "id": "u6", "label": "Access Duration", "maxLength": 25, "multiple": false, "options": [{"label": "Option1", "value": "Option1"}, {"label": "Option2", "value": "Option2"}], "placeholder": "", "required": true, "rule": 0, "style": 6}, {"default": "", "des": "Torro Data Analytical Platform", "edit": "0", "id": "s1", "label": "Region / Country", "options": [{"label": "ASP", "value": "ASP"}, {"label": "Hong Kong", "value": "hk"}, {"label": "China", "value": "cn"}, {"label": "Singapore", "value": "sg"}, {"label": "Indonesia", "value": "id"}, {"label": "India", "value": "in"}, {"label": "Sri Lanka", "value": "sl"}, {"label": "EMEA", "value": "EMEA"}, {"label": "United Kingdom", "value": "uk"}, {"label": "France", "value": "fr"}, {"label": "UAE", "value": "uae"}], "placeholder": "", "style": 2, "required": true, "maxLength": 25, "rule": 0, "create_time": "Tue, 21 Dec 2021 14:32:50 GMT", "u_id": 0, "updated_time": "Tue, 21 Dec 2021 14:32:50 GMT", "value_num": 11}, {"default": "", "des": "Anything you want to say to the approvers?", "edit": 1, "id": "u7", "label": "Business Justification", "maxLength": 999, "options": [], "placeholder": "", "required": true, "rule": 0, "style": 3, "width": "100"}]', 0, '2021-12-21', '2021-12-21', 'Add user to use case');
-- insert into formTable ( id, workspace_id, usecase_id, title, available, fields_num, u_max_id, creator_id, fields_list, hide, create_time, updated_time, des) values (3, 0, 0, 'Create Policy', 1, 6, 'u7', 1, '[{"default": "", "des": "Project ID", "edit": 1, "id": "u1", "label": "project_id", "options": [], "placeholder": "", "style": 3}, {"default": "", "des": "Region", "edit": 1, "id": "u2", "label": "region", "options": [], "placeholder": "", "style": 3}, {"default": "", "des": "staff name", "edit": 1, "id": "u3", "label": "policy_name", "options": [], "placeholder": "", "style": 3}, {"default": "", "des": "staff name", "edit": 1, "id": "u4", "label": "policy_description", "options": [], "placeholder": "", "style": 3}, {"default": "", "des": "staff name", "edit": 1, "id": "u5", "label": "policy_approval_ad_group", "options": [], "placeholder": "", "style": 3}, {"default": "", "des": "policy tags", "edit": 1, "id": "u7", "label": "policy_data_structure", "options": [], "placeholder": "", "style": 7}]', 1, '2021-12-21', '2021-12-21', 'Create Policy');
insert into formTable ( id, workspace_id, usecase_id, title, available, fields_num, u_max_id, creator_id, fields_list, hide, create_time, updated_time, des) values (3, 0, 0, 'Create Policy', 1, 6, 'u7', 1, '[{"default": "", "des": "Project ID", "edit": 1, "id": "u1", "label": "Project ID", "options": [], "placeholder": "", "style": 3}, {"default": "", "des": "GCP Region", "edit": 1, "id": "u2", "label": "GCP Region", "options": [], "placeholder": "", "style": 3}, {"default": "", "des": "staff name", "edit": 1, "id": "u3", "label": "Policy Name", "options": [], "placeholder": "", "style": 3}, {"default": "", "des": "staff name", "edit": 1, "id": "u4", "label": "Policy Description", "options": [], "placeholder": "", "style": 3}, {"default": "", "des": "staff name", "edit": 1, "id": "u5", "label": "Policy Approval AD Group", "options": [], "placeholder": "", "style": 3}, {"default": "", "des": "policy tags", "edit": 1, "id": "u7", "label": "Policy Tags", "options": [], "placeholder": "", "style": 7}]', 1, '2021-12-21', '2021-12-21', 'Create Policy');


insert into formTable ( id, workspace_id, usecase_id, title, available, fields_num, u_max_id, creator_id, fields_list, hide, create_time, updated_time, des) values (101, 0, 0, 'Create form', 1, 3, '', 1, '[{"default": "", "des": "", "edit": 1, "id": "u1", "label": "Form Name", "options": [], "placeholder": "", "style": 3}, {"default": "", "des": "", "edit": 1, "id": "u2", "label": "Form Description", "options": [], "placeholder": "", "style": 3}, {"default": "", "des": "", "edit": 1, "id": "u3", "label": "fieldList", "options": [], "placeholder": "", "style": 3}]', 1, '2021-08-22', '2021-08-22', 'Create form');
insert into formTable ( id, workspace_id, usecase_id, title, available, fields_num, u_max_id, creator_id, fields_list, hide, create_time, updated_time, des) values (102, 0, 0, 'Delete form', 1, 1, '', 1, '[{"default": "", "des": "", "edit": 1, "id": "u1", "label": "Form id", "options": [], "placeholder": "", "style": 3}]', 1, '2021-08-22', '2021-08-22', 'Delete from');
insert into formTable ( id, workspace_id, usecase_id, title, available, fields_num, u_max_id, creator_id, fields_list, hide, create_time, updated_time, des) values (103, 0, 0, 'Update form', 1, 4, '', 1, '[{"default": "", "des": "", "edit": 1, "id": "u1", "label": "Form id", "options": [], "placeholder": "", "style": 3}, {"default": "", "des": "", "edit": 1, "id": "u2", "label": "Form Name", "options": [], "placeholder": "", "style": 3}, {"default": "", "des": "", "edit": 1, "id": "u3", "label": "Form Description", "options": [], "placeholder": "", "style": 3}, {"default": "", "des": "", "edit": 1, "id": "u4", "label": "fieldList", "options": [], "placeholder": "", "style": 3}]', 1, '2021-08-22', '2021-08-22', 'Update from');
insert into formTable ( id, workspace_id, usecase_id, title, available, fields_num, u_max_id, creator_id, fields_list, hide, create_time, updated_time, des) values (104, 0, 0, 'Create Tag Template', 1, 3, '', 1, '[{"default": "", "des": "", "edit": 1, "id": "u1", "label": "Tag Template Name", "options": [], "placeholder": "", "style": 3}, {"default": "", "des": "", "edit": 1, "id": "u2", "label": "Tag Template Description", "options": [], "placeholder": "", "style": 3}, {"default": "", "des": "", "edit": 1, "id": "u3", "label": "fieldList", "options": [], "placeholder": "", "style": 3}]', 1, '2021-11-13', '2021-11-13', 'Create tag template');
insert into formTable ( id, workspace_id, usecase_id, title, available, fields_num, u_max_id, creator_id, fields_list, hide, create_time, updated_time, des) values (105, 0, 0, 'Update Tag Template', 1, 4, '', 1, '[{"default": "", "des": "", "edit": 1, "id": "u1", "label": "Tag template form id", "options": [], "placeholder": "", "style": 3}, {"default": "", "des": "", "edit": 1, "id": "u2", "label": "Tag Template Name", "options": [], "placeholder": "", "style": 3}, {"default": "", "des": "", "edit": 1, "id": "u3", "label": "Tag Template Description", "options": [], "placeholder": "", "style": 3}, {"default": "", "des": "", "edit": 1, "id": "u4", "label": "fieldList", "options": [], "placeholder": "", "style": 3}]', 1, '2021-11-13', '2021-11-13', 'Update tag template');
insert into formTable ( id, workspace_id, usecase_id, title, available, fields_num, u_max_id, creator_id, fields_list, hide, create_time, updated_time, des) values (106, 0, 0, 'Delete Tag Template', 1, 1, '', 1, '[{"default": "", "des": "", "edit": 1, "id": "u1", "label": "Tag template form id", "options": [], "placeholder": "", "style": 3}]', 1, '2021-08-22', '2021-08-22', 'Delete Tag Template');
insert into formTable ( id, workspace_id, usecase_id, title, available, fields_num, u_max_id, creator_id, fields_list, hide, create_time, updated_time, des) values (107, 0, 0, 'Data Publishing Request', 1, 5, 'u5', 1, '[{"default": "", "des": "", "edit": 1, "id": "u1", "label": "Project ID", "maxLength": 25, "options": [], "placeholder": "", "required": true, "rule": 0, "style": 3}, {"default": "", "des": "", "edit": 1, "id": "u2", "label": "Location", "maxLength": 25, "options": [], "placeholder": "", "required": true, "rule": 0, "style": 3}, {"default": "", "des": "", "edit": 1, "id": "u3", "label": "Data Set ID", "maxLength": 25, "options": [], "placeholder": "", "required": true, "rule": 0, "style": 3}, {"default": "", "des": "", "edit": 1, "id": "u4", "label": "Table ID", "maxLength": 25, "options": [], "placeholder": "", "required": true, "rule": 0, "style": 3}, {"default": "", "des": "", "edit": 1, "id": "u5", "label": "Fields", "maxLength": "999", "options": [], "placeholder": "", "required": true, "rule": 0, "style": 3}, {"default": "", "des": "", "edit": 1, "id": "u6", "label": "Table Tags", "maxLength": "999", "options": [], "placeholder": "", "required": true, "rule": 0, "style": 3}]', 1, '2021-08-22', '2021-08-22', 'Data Onboarding Request');
insert into formTable ( id, workspace_id, usecase_id, title, available, fields_num, u_max_id, creator_id, fields_list, hide, create_time, updated_time, des) values (108, 0, 0, 'Data Consumption Request', 1, 6, 'u6', 1, '[{"default": "", "des": "", "edit": 1, "id": "u1", "label": "Project ID", "options": [], "placeholder": "", "style": 3, "required": true, "maxLength": 25, "rule": 0}, {"default": "DNA_CN", "des": null, "edit": 1, "id": "d15", "label": "Use case", "options": [{"label": "DNA_CN", "value": "Engineer@torro.ai"}, {"label": "DNA_SG", "value": "Engineer@torro.ai"}], "placeholder": "DNA_CN", "style": 2, "required": true, "maxLength": 25, "rule": 0, "create_time": "Wed, 08 Dec 2021 10:17:00 GMT", "default_value": "DNA_CN", "value_num": 2}, {"default": "", "des": "", "edit": 1, "id": "u3", "label": "Location", "options": [], "placeholder": "", "style": 3, "required": true, "maxLength": 25, "rule": 0}, {"default": "", "des": "", "edit": 1, "id": "u4", "label": "Data Set ID", "options": [], "placeholder": "", "style": 3, "required": true, "maxLength": 25, "rule": 0}, {"default": "", "des": "", "edit": 1, "id": "u5", "label": "Table ID", "options": [], "placeholder": "", "style": 3, "required": true, "maxLength": 25, "rule": 0}, {"default": "", "des": "", "edit": 1, "id": "u6", "label": "Fields", "options": [], "placeholder": "", "style": 3, "required": true, "maxLength": "999", "rule": 0}]', 1, '2021-08-22', '2021-08-22', 'Get Data Access for use case Request');

insert into formTable ( id, workspace_id, usecase_id, title, available, fields_num, u_max_id, creator_id, fields_list, hide, create_time, updated_time, des) values (419, 0, 0, 'Data Approval Tag', 1, 1, 'u1', 1, '[{"default": "", "des": "AD group for Data Approvers", "edit": 1, "id": "u1", "label": "Data Approver AD group", "options": [], "placeholder": "", "style": 3, "required": true, "maxLength": 25, "rule": 0}]', 1, '2021-12-26', '2021-12-26', 'Data Approval Tag');


-- ----------------------------
-- Table structure for field [entity]
-- ----------------------------
DROP TABLE IF EXISTS `fieldTable`;
CREATE TABLE `fieldTable` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'field_id',
  `workspace_id` int NOT NULL COMMENT 'workspace id',
  `u_id` int NOT NULL COMMENT 'field_user_id',
  `style` int DEFAULT NULL COMMENT 'field type',
  `label` varchar(64) DEFAULT NULL COMMENT 'field type name',
  `default_value` varchar(64) DEFAULT NULL COMMENT 'field default value',
  `placeholder` varchar(256) DEFAULT NULL COMMENT 'placeholder',
  `value_num` int DEFAULT NULL COMMENT 'how many value of this fields',
  `value_list` text COMMENT 'value list',
  `edit` varchar(1024) DEFAULT '0' COMMENT 'if this field can be edited',
  `required` tinyint(1) DEFAULT '1' COMMENT 'required field',
  `des` varchar(1024) DEFAULT NULL COMMENT 'description',
  `create_time` datetime DEFAULT NULL COMMENT 'create_time',
  `updated_time` datetime DEFAULT NULL COMMENT 'last_updated_time',
  PRIMARY KEY (`id`,`workspace_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
DROP TABLE IF EXISTS `dynamicFieldTable`;
CREATE TABLE `dynamicFieldTable` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'field_id',
  `style` int DEFAULT NULL COMMENT 'field type',
  `form_id` int NOT NULL COMMENT 'form_id',
  `label` varchar(64) DEFAULT NULL COMMENT 'field type name',
  `default_value` varchar(256) DEFAULT NULL COMMENT 'field default value',
  `placeholder` varchar(256) DEFAULT NULL COMMENT 'placeholder',
  `value_num` int DEFAULT NULL COMMENT 'how many value of this fields',
  `des` varchar(1024) DEFAULT NULL COMMENT 'description',
  `create_time` datetime DEFAULT NULL COMMENT 'create_time',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
insert into dynamicFieldTable values (15, 2, 2, 'Use case', '', '', 0, 'default usecase dynamic field', '2021-12-08 10:17:00');
DROP TABLE IF EXISTS `dynamicFieldValueTable`;
CREATE TABLE `dynamicFieldValueTable` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'field-value id',
  `workspace_id` int NOT NULL COMMENT 'workspace id',
  `dynamic_field_id` int NOT NULL COMMENT 'dynamic field id',
  `input_form_id` int NOT NULL COMMENT 'input form id',
  `option_label` varchar(256) DEFAULT NULL COMMENT 'how many value of this fields',
  `option_value` varchar(256) DEFAULT NULL COMMENT 'how many value of this fields',
  `create_time` datetime DEFAULT NULL COMMENT 'create_time',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `dynamicFieldValueTable_ibfk_1` (`dynamic_field_id`),
  CONSTRAINT `dynamicFieldValueTable_ibfk_1` FOREIGN KEY (`dynamic_field_id`) REFERENCES `dynamicFieldTable` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

DROP TABLE IF EXISTS `dynamicField_to_inputFormTable`;
CREATE TABLE `dynamicField_to_inputFormTable` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'id',
  `dynamic_field_id` varchar(8) NOT NULL COMMENT 'dynamic field id',
  `option_label` varchar(256) DEFAULT NULL,
  `using_form_id` int NOT NULL COMMENT 'which form id this input form belong to',
  `using_input_form_id` int NOT NULL COMMENT 'the input form id using this dynamic field',
  `create_time` datetime DEFAULT NULL COMMENT 'create_time',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;


DROP TABLE IF EXISTS `inputFormIndexTable`;
CREATE TABLE `inputFormIndexTable` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'input form id',
  `creator_id` varchar(256) DEFAULT NULL COMMENT 'creator id',
  `form_id` int NOT NULL COMMENT 'form id',
  `workspace_id` int NOT NULL COMMENT 'workspace id',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=351 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
INSERT INTO `inputFormIndexTable` (`id`, `creator_id`, `form_id`, `workspace_id`) VALUES (498,'354',104,362);
DROP TABLE IF EXISTS `inputFormTable`;
CREATE TABLE `inputFormTable` (
  `id` int NOT NULL COMMENT 'input form id',
  `history_id` int NOT NULL AUTO_INCREMENT COMMENT 'history id',
  `workflow_id` int NOT NULL COMMENT 'workflow id',
  `workflow_name` varchar(256) DEFAULT NULL COMMENT 'workflow_title',
  `fields_num` int DEFAULT NULL COMMENT 'form fields num',
  `stages_num` int DEFAULT NULL COMMENT 'workflow stages num',
  `form_status` int DEFAULT NULL,
  `form_field_values_dict` text COMMENT 'input field values dict',
  `workflow_stages_id_list` text COMMENT 'workflow stages id list',
  `create_time` datetime DEFAULT NULL COMMENT 'create_time',
  `updated_time` datetime DEFAULT NULL COMMENT 'last_updated_time',
  PRIMARY KEY (`history_id`) USING BTREE,
  KEY `inputFormTable_ibfk_1` (`id`),
  CONSTRAINT `inputFormTable_ibfk_1` FOREIGN KEY (`id`) REFERENCES `inputFormIndexTable` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=351 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
INSERT INTO `inputFormTable` (`id`, `history_id`, `workflow_id`, `workflow_name`, `fields_num`, `stages_num`, `form_status`, `form_field_values_dict`, `workflow_stages_id_list`, `create_time`, `updated_time`) VALUES (498,495,428,'new workFlow',3,2,2,'{\"u1\": {\"style\": 3, \"value\": \"Data Approval Tag\"}, \"u3\": {\"style\": 3, \"value\": [{\"default\": \"\", \"des\": \"AD group for Data Approvers\", \"edit\": 1, \"id\": \"u1\", \"label\": \"Data Approver AD group\", \"options\": [], \"placeholder\": \"\", \"style\": 3, \"required\": true, \"maxLength\": 25, \"rule\": 0}]}, \"u2\": {\"style\": 3, \"value\": \"Tag template description\"}}','[499]','2021-12-26 09:28:01','2021-12-26 09:28:39');
DROP TABLE IF EXISTS `inputStageTable`;
CREATE TABLE `inputStageTable` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'stage_id',
  `stage_id` int NOT NULL COMMENT 'stage id',
  `stage_index` int DEFAULT NULL COMMENT 'the stage index',
  `stage_group` varchar(64) DEFAULT NULL COMMENT 'stage type',
  `apiTaskName` varchar(64) DEFAULT NULL COMMENT 'the api task name',
  `condition_value_dict` text COMMENT 'value dict',
  `status` int DEFAULT '0' COMMENT 'the task status, 0:not start, 1:success,-1:failed',
  `logs` text COMMENT 'task logs',
  `comment` text COMMENT 'error handling',
  `create_time` datetime DEFAULT NULL COMMENT 'create_time',
  `updated_time` datetime DEFAULT NULL COMMENT 'last_updated_time',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=351 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
INSERT INTO `inputStageTable` (`id`, `stage_id`, `stage_index`, `stage_group`, `apiTaskName`, `condition_value_dict`, `status`, `logs`, `comment`, `create_time`, `updated_time`) VALUES (499,36,1,'GoogleCloud','CreateTagTemplate','{\"tag_template_display_name\": \"Data Approval Tag\", \"description\": \"Tag template description\", \"field_list\": [{\"default\": \"\", \"des\": \"AD group for Data Approvers\", \"edit\": 1, \"id\": \"u1\", \"label\": \"Data Approver AD group\", \"options\": [], \"placeholder\": \"\", \"style\": 3, \"required\": true, \"maxLength\": 25, \"rule\": 0}]}',1,'create successfully.: 0','create successfully.: 0','2021-12-26 09:28:01','2021-12-26 09:28:39');
DROP TABLE IF EXISTS `inputCommentTable`;
CREATE TABLE `inputCommentTable` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'comment_id',
  `input_form_id` int NOT NULL COMMENT 'input form id',
  `history_id` int NOT NULL COMMENT 'history id',
  `creator_id` varchar(256) DEFAULT NULL COMMENT 'creator id',
  `comment` text COMMENT 'comment',
  `create_time` datetime DEFAULT NULL COMMENT 'create_time',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=351 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
INSERT INTO `inputCommentTable` (`id`, `input_form_id`, `history_id`, `creator_id`, `comment`, `create_time`) VALUES (478,501,498,'354','[|4|]approved','2022-01-04 13:59:27');

DROP TABLE IF EXISTS `inputNotifyTable`;
CREATE TABLE `inputNotifyTable` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'notify_id',
  `account_id` int NOT NULL COMMENT 'account_id',
  `input_form_id` int NOT NULL COMMENT 'input form id',
  `history_id` int NOT NULL COMMENT 'history id',
  `is_read` int(4) DEFAULT 0 COMMENT 'is read',
  `comment` text COMMENT 'comment',
  `create_time` datetime DEFAULT NULL COMMENT 'create_time',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=351 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

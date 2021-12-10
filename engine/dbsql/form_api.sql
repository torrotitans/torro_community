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
create database torro_api
-- ========================================================
-- design structure
-- ----------------------------
-- form -< field                <- form_fields ->
-- field -< value
-- ========================================================

-- ----------------------------
-- Table structure for form [entity]
--  id<351 = system form; id>350 = user define form
-- id<101 = system form:show to user; 100<id<201:hide form
-- ----------------------------
DROP TABLE IF EXISTS `formTable`;
CREATE TABLE `formTable` (

  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'form_id',
  `workspace_id` int(11) NOT NULL COMMENT 'workspace id',
  `usecase_id` int(11) NOT NULL DEFAULT 0 COMMENT 'usecase_id',
  `title` varchar(256) DEFAULT NULL COMMENT 'form_title',
  `available` int(2) DEFAULT 1 COMMENT 'available flag',
  `fields_num` int(10) DEFAULT NULL COMMENT 'form fields num',
  `u_max_id` varchar(8) DEFAULT 0 COMMENT 'user field max id',
  `creator_id` varchar(256) DEFAULT NULL COMMENT 'creator id',
  `fields_list` text DEFAULT NULL COMMENT 'field list',
  `hide` int(2) DEFAULT 0 COMMENT 'if show the form in ui or not',
  `create_time` datetime DEFAULT NULL COMMENT 'create_time',
  `updated_time` datetime DEFAULT NULL COMMENT 'last_updated_time',
  `des` varchar(1024) DEFAULT NULL COMMENT 'description',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=351 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
insert into formTable ( id, workspace_id, usecase_id, title, available, fields_num, u_max_id, creator_id, fields_list, hide, create_time, updated_time, des) values (2, 0, 0, 'Create UseCase', 1, 11, 'u11', 1, '[{"id": "s1", "label": "Region / Country"}, {"default": "", "des": "Use case owner AD group", "edit": 1, "id": "u2", "label": "Use case Owner Group", "options": [], "placeholder": "Use case owner AD group", "style": 3}, {"default": "", "des": "Use case team AD group", "edit": 1, "id": "u3", "label": "Use case Team Group", "options": [], "placeholder": "Use case team AD group", "style": 3}, {"default": "2021-08-21T10:59:53.020Z", "des": "Use case validity till date", "edit": 1, "id": "u4", "label": "Validity Date", "options": [], "placeholder": "Use case validity till date", "style": 6}, {"default": "", "des": "Use case name", "edit": 1, "id": "u5", "label": "Use Case Name", "options": [], "placeholder": "Use case name", "style": 3}, {"default": "", "des": "Use case description", "edit": 1, "id": "u6", "label": "Description", "options": [], "placeholder": "Use case description", "style": 3}, {"default": "", "des": "Use case total budget", "edit": 1, "id": "u7", "label": "Budget", "options": [], "placeholder": "Use case total budget", "style": 3}, {"default": "", "des": "Service account", "edit": 1, "id": "u8", "label": "Admin Service Account", "options": [], "placeholder": "Service account", "style": 3}, {"default": "", "des": "Use case resources access", "edit": 1, "id": "u9", "label": "Resources Access", "options": [{"label": "Jupyter", "value": "Jupyter"}, {"label": "Datastudio", "value": "Datastudio"}], "placeholder": "Use case resources access", "style": 1}, {"default": "", "des": "Allow cross region support", "edit": 1, "id": "u10", "label": "Allow Cross Region", "options": [], "placeholder": "Allow cross region support", "style": 5}]', 0, '2021-08-22', '2021-08-22', 'Create UseCase');
insert into formTable ( id, workspace_id, usecase_id, title, available, fields_num, u_max_id, creator_id, fields_list, hide, create_time, updated_time, des) values (101, 0, 0, 'Create form', 1, 3, '', 1, '[{"default": "", "des": "", "edit": 1, "id": "u1", "label": "Form Name", "options": [], "placeholder": "", "style": 3}, {"default": "", "des": "", "edit": 1, "id": "u2", "label": "Form Description", "options": [], "placeholder": "", "style": 3}, {"default": "", "des": "", "edit": 1, "id": "u3", "label": "fieldList", "options": [], "placeholder": "", "style": 3}]', 1, '2021-08-22', '2021-08-22', 'Create form');
insert into formTable ( id, workspace_id, usecase_id, title, available, fields_num, u_max_id, creator_id, fields_list, hide, create_time, updated_time, des) values (102, 0, 0, 'Delete form', 1, 1, '', 1, '[{"default": "", "des": "", "edit": 1, "id": "u1", "label": "Form id", "options": [], "placeholder": "", "style": 3}]', 1, '2021-08-22', '2021-08-22', 'Delete from');
insert into formTable ( id, workspace_id, usecase_id, title, available, fields_num, u_max_id, creator_id, fields_list, hide, create_time, updated_time, des) values (103, 0, 0, 'Update form', 1, 4, '', 1, '[{"default": "", "des": "", "edit": 1, "id": "u1", "label": "Form id", "options": [], "placeholder": "", "style": 3}, {"default": "", "des": "", "edit": 1, "id": "u2", "label": "Form Name", "options": [], "placeholder": "", "style": 3}, {"default": "", "des": "", "edit": 1, "id": "u3", "label": "Form Description", "options": [], "placeholder": "", "style": 3}, {"default": "", "des": "", "edit": 1, "id": "u4", "label": "fieldList", "options": [], "placeholder": "", "style": 3}]', 1, '2021-08-22', '2021-08-22', 'Update from');
insert into formTable ( id, workspace_id, usecase_id, title, available, fields_num, u_max_id, creator_id, fields_list, hide, create_time, updated_time, des) values (104, 0, 0, 'Create Tag Template', 1, 3, '', 1, '[{"default": "", "des": "", "edit": 1, "id": "u1", "label": "Tag Template Name", "options": [], "placeholder": "", "style": 3}, {"default": "", "des": "", "edit": 1, "id": "u2", "label": "Tag Template Description", "options": [], "placeholder": "", "style": 3}, {"default": "", "des": "", "edit": 1, "id": "u3", "label": "fieldList", "options": [], "placeholder": "", "style": 3}]', 1, '2021-11-13', '2021-11-13', 'Create tag template');
insert into formTable ( id, workspace_id, usecase_id, title, available, fields_num, u_max_id, creator_id, fields_list, hide, create_time, updated_time, des) values (105, 0, 0, 'Update Tag Template', 1, 4, '', 1, '[{"default": "", "des": "", "edit": 1, "id": "u1", "label": "Tag template form id", "options": [], "placeholder": "", "style": 3}, {"default": "", "des": "", "edit": 1, "id": "u2", "label": "Tag Template Name", "options": [], "placeholder": "", "style": 3}, {"default": "", "des": "", "edit": 1, "id": "u3", "label": "Tag Template Description", "options": [], "placeholder": "", "style": 3}, {"default": "", "des": "", "edit": 1, "id": "u4", "label": "fieldList", "options": [], "placeholder": "", "style": 3}]', 1, '2021-11-13', '2021-11-13', 'Update tag template');
insert into formTable ( id, workspace_id, usecase_id, title, available, fields_num, u_max_id, creator_id, fields_list, hide, create_time, updated_time, des) values (106, 0, 0, 'Delete Tag Template', 1, 1, '', 1, '[{"default": "", "des": "", "edit": 1, "id": "u1", "label": "Tag template form id", "options": [], "placeholder": "", "style": 3}]', 1, '2021-08-22', '2021-08-22', 'Delete Tag Template');


-- ----------------------------
-- Table structure for field [entity]
-- ----------------------------
DROP TABLE IF EXISTS `fieldTable`;
CREATE TABLE `fieldTable` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'field_id',
  `workspace_id` int(11) NOT NULL COMMENT 'workspace id',
  `u_id` int(11) NOT NULL COMMENT 'field_user_id',
--  `usecase_id` int(11) NOT NULL COMMENT 'usecase_id',
  `style` int(11) DEFAULT NULL COMMENT 'field type',
  `label` varchar(64) DEFAULT NULL COMMENT 'field type name',
  `default_value` varchar(64) DEFAULT NULL COMMENT 'field default value',
  `placeholder` varchar(256) DEFAULT NULL COMMENT 'placeholder',
  `value_num` int(11) DEFAULT NULL COMMENT 'how many value of this fields',
  `value_list` text DEFAULT NULL COMMENT 'value list',
  `edit` varchar(1024) DEFAULT 0 COMMENT 'if this field can be edited',
  `required` bool DEFAULT 1 COMMENT 'required field',
  `des` varchar(1024) DEFAULT NULL COMMENT 'description',
  `create_time` datetime DEFAULT NULL COMMENT 'create_time',
  `updated_time` datetime DEFAULT NULL COMMENT 'last_updated_time',

  PRIMARY KEY (`id`, `workspace_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
--insert into fieldTable values (1, 362, 0, 2, 'region_country', '', '', 0, '[]', 1, '', '2021-04-16 14:30:00', '2021-04-17 14:30:00');
DROP TABLE IF EXISTS `dynamicFieldTable`;
CREATE TABLE `dynamicFieldTable` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'field_id',
  `workspace_id` int(11) NOT NULL COMMENT 'workspace id',
  `style` int(11) DEFAULT NULL COMMENT 'field type',
   `form_id` int(4) NOT NULL COMMENT 'form_id',
  `label` varchar(64) DEFAULT NULL COMMENT 'field type name',
  `default_value` varchar(256) DEFAULT NULL COMMENT 'field default value',
  `placeholder` varchar(256) DEFAULT NULL COMMENT 'placeholder',
  `value_num` int(11) DEFAULT NULL COMMENT 'how many value of this fields',
  `des` varchar(1024) DEFAULT NULL COMMENT 'description',
  `create_time` datetime DEFAULT NULL COMMENT 'create_time',
  PRIMARY KEY (`id`, `workspace_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
DROP TABLE IF EXISTS `dynamicFieldValueTable`;
CREATE TABLE `dynamicFieldValueTable` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'field-value id',
  `dynamic_field_id` int(11) NOT NULL COMMENT 'dynamic field id',
  `input_form_id` int(11) NOT NULL COMMENT 'input form id',
  `option_label` varchar(256) DEFAULT NULL COMMENT 'how many value of this fields',
  `option_value` varchar(256) DEFAULT NULL COMMENT 'how many value of this fields',
  `create_time` datetime DEFAULT NULL COMMENT 'create_time',
  PRIMARY KEY (`id`) USING BTREE,
  CONSTRAINT `dynamicFieldValueTable_ibfk_1` FOREIGN KEY (`dynamic_field_id`) REFERENCES `dynamicFieldTable` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;


-- #######################################
--DROP TABLE IF EXISTS `formTable`;
--CREATE TABLE `formTable` (
--  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'form_id',
--  `workspace_id` int(11) NOT NULL COMMENT 'workspace_id',
--  `usecase_id` int(11) NOT NULL COMMENT 'usecase_id',
--  `team_id` int(11) NOT NULL COMMENT 'team_id',
--
--  `title` varchar(256) DEFAULT NULL COMMENT 'form_title',
--  `fields_num` int(10) DEFAULT NULL COMMENT 'form fields num',
--  `u_max_id` varchar(8) DEFAULT 0 COMMENT 'user field max id',
--  `creator_id` varchar(256) DEFAULT NULL COMMENT 'creator id',
--  `fields_list` text DEFAULT NULL COMMENT 'field list',
--  `create_time` datetime DEFAULT NULL COMMENT 'create_time',
--  `updated_time` datetime DEFAULT NULL COMMENT 'last_updated_time',
--  `des` varchar(1024) DEFAULT NULL COMMENT 'description',
--  PRIMARY KEY (`id`) USING BTREE
--) ENGINE=InnoDB AUTO_INCREMENT=351 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;


DROP TABLE IF EXISTS `inputFormIndexTable`;
CREATE TABLE `inputFormIndexTable` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'input form id',
  `creator_id` varchar(256) DEFAULT NULL COMMENT 'creator id',
  `form_id` int(11) NOT NULL COMMENT 'form id',
  `workspace_id` int(11) NOT NULL COMMENT 'workspace id',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=351 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

DROP TABLE IF EXISTS `inputFormTable`;
CREATE TABLE `inputFormTable` (
  `id` int(11) NOT NULL COMMENT 'input form id',
  `history_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'history id',
  `workflow_id` int(11) NOT NULL COMMENT 'workflow id',
  `workflow_name` varchar(256) DEFAULT NULL COMMENT 'workflow_title',
  `fields_num` int(10) DEFAULT NULL COMMENT 'form fields num',
  `stages_num` int(10) DEFAULT NULL COMMENT 'workflow stages num',
  `form_status` int(10) DEFAULT 0 COMMENT 'form status',
  `form_field_values_dict` text DEFAULT NULL COMMENT 'input field values dict',
  `workflow_stages_id_list` text DEFAULT NULL COMMENT 'workflow stages id list',
  `create_time` datetime DEFAULT NULL COMMENT 'create_time',
  `updated_time` datetime DEFAULT NULL COMMENT 'last_updated_time',
  PRIMARY KEY (`history_id`) USING BTREE,
  CONSTRAINT `inputFormTable_ibfk_1` FOREIGN KEY (`id`) REFERENCES `inputFormIndexTable` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=351 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

DROP TABLE IF EXISTS `inputStageTable`;
CREATE TABLE `inputStageTable` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'stage_id',
  `stage_id` int(11) NOT NULL COMMENT 'stage id',
  `stage_index` int(11) DEFAULT NULL COMMENT 'the stage index',

  `stage_group` varchar(64) DEFAULT NULL COMMENT 'stage type',
  `apiTaskName` varchar(64) DEFAULT NULL COMMENT 'the api task name',

  `condition_value_dict` text DEFAULT NULL COMMENT 'value dict',
  `status` int(2) DEFAULT 0 COMMENT 'the task status, 0:not start, 1:success,-1:failed',
  `logs` text DEFAULT NULL COMMENT 'task logs',
  `comment` text DEFAULT NULL COMMENT 'error handling',

  `create_time` datetime DEFAULT NULL COMMENT 'create_time',
  `updated_time` datetime DEFAULT NULL COMMENT 'last_updated_time',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=351 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

DROP TABLE IF EXISTS `inputCommentTable`;
CREATE TABLE `inputCommentTable` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'comment_id',

  `input_form_id` int(11) NOT NULL COMMENT 'input form id',
  `history_id` int(11) NOT NULL COMMENT 'history id',
  `creator_id` varchar(256) DEFAULT NULL COMMENT 'creator id',

  `comment` text DEFAULT NULL COMMENT 'comment',

  `create_time` datetime DEFAULT NULL COMMENT 'create_time',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=351 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
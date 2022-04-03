

DROP TABLE IF EXISTS `taxonomyTable`;
CREATE TABLE `taxonomyTable` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'local policy tag id',
  `workspace_id` int NOT NULL COMMENT 'workspace_id',
  `input_form_id` int NOT NULL COMMENT 'input form id',
  `creator_id` varchar(256) DEFAULT NULL COMMENT 'creator id',
  `project_id` varchar(256) DEFAULT NULL COMMENT 'project id',
  `location` varchar(256) DEFAULT NULL COMMENT 'location',
  `display_name` varchar(256) DEFAULT NULL COMMENT 'display_name',
  `gcp_taxonomy_id` varchar(1024) DEFAULT NULL COMMENT 'taxonomy_id',
  `ad_group` varchar(1024) DEFAULT NULL COMMENT 'adgroup id',
  `description` text DEFAULT NULL COMMENT 'description',
  `create_time` datetime DEFAULT NULL COMMENT 'create_time',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

DROP TABLE IF EXISTS `policyTagsTable`;
CREATE TABLE `policyTagsTable` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'local policy tag id',
  `local_taxonomy_id` int DEFAULT '-1' COMMENT 'taxonomy_id',
  `parent_local_id` int DEFAULT '-1' COMMENT 'parent local id',
  `gcp_policy_tag_id` varchar(1024) DEFAULT '' COMMENT 'gcp policy tag id',
  `ad_group` varchar(1024) DEFAULT NULL COMMENT 'adgroup id',
  `display_name` varchar(1024) DEFAULT NULL COMMENT 'display_name',
  `description` text DEFAULT NULL COMMENT 'description',
  `create_time` datetime DEFAULT NULL COMMENT 'create_time',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

DROP TABLE IF EXISTS `tagTemplatesTable`;
CREATE TABLE `tagTemplatesTable` (
  `input_form_id` int NOT NULL COMMENT 'input form id',
  `workspace_id` int NOT NULL COMMENT 'workspace_id',
  `tag_template_form_id` int DEFAULT NULL COMMENT 'tag_template_form_id',
  `creator_id` varchar(256) DEFAULT NULL COMMENT 'creator id',
  `project_id` varchar(256) DEFAULT NULL COMMENT 'project id',
  `location` varchar(256) DEFAULT NULL COMMENT 'location',
  `display_name` varchar(256) DEFAULT NULL COMMENT 'display_name',
  `tag_template_id` varchar(1024) DEFAULT NULL COMMENT 'tag_template_id',
  `field_list` longtext COMMENT 'field_list',
  `description` text DEFAULT NULL COMMENT 'description',
  `create_time` datetime DEFAULT NULL COMMENT 'create_time',
  PRIMARY KEY (`input_form_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
INSERT INTO `tagTemplatesTable` (`input_form_id`, `workspace_id`, `tag_template_form_id`, `creator_id`, `project_id`, `location`, `display_name`, `tag_template_id`, `field_list`, `description`, `create_time`) VALUES (498,0,419,'1','','','Data Approval Tag','data_approval_tag','{\"displayName\": \"Data Approval Tag\", \"fields\": {\"data_approver_ad_group\": {\"displayName\": \"Data Approver AD group\", \"type\": {\"primitiveType\": \"STRING\"}, \"description\": \"AD group for Data Approvers\", \"order\": 1}}}','Tag template description','2021-12-26 09:28:37');

DROP TABLE IF EXISTS `dataOnboardTable`;
CREATE TABLE `dataOnboardTable` (
  `input_form_id` int NOT NULL COMMENT 'input_form_id',
  `data_owner` varchar(256) NOT NULL COMMENT 'data_owner',
  `workspace_id` int NOT NULL COMMENT 'workspace_id',
  `project_id` varchar(256) NOT NULL COMMENT 'project_id',
  `location` varchar(256) NOT NULL COMMENT 'location',
  `dataset_id` varchar(256) NOT NULL COMMENT 'dataset_id',
  `table_id` varchar(256) NOT NULL COMMENT 'table_id',
  `fields` text NOT NULL COMMENT 'fields',
  `table_tags` longtext COMMENT 'table_tags',
  `create_time` datetime DEFAULT NULL COMMENT 'create_time',
  PRIMARY KEY (`input_form_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

DROP TABLE IF EXISTS `dataAccessTable`;
CREATE TABLE `dataAccessTable` (
  `data_access_input_form_id` int NOT NULL COMMENT 'data_access_input_form_id',
  `data_input_form_id` int NOT NULL COMMENT 'input_form_id',
  `usecase_id` varchar(256) NOT NULL COMMENT 'usecase_id',
  `fields` longtext COMMENT 'fields',
  `create_time` datetime DEFAULT NULL COMMENT 'create_time',
  PRIMARY KEY (`data_access_input_form_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
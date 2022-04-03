SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS `workflowTable`;
CREATE TABLE `workflowTable` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'workflow_id',
  `form_id` int NOT NULL COMMENT 'form_id',
  `workflow_name` varchar(256) DEFAULT NULL COMMENT 'form_title',
  `stage_hash` varchar(256) DEFAULT NULL COMMENT 'hash values',
  `stage_num` int DEFAULT NULL COMMENT 'form fields num',
  `creator_id` varchar(256) DEFAULT NULL COMMENT 'creator id',
  `last_modify_id` varchar(256) DEFAULT NULL COMMENT 'last modify id',
  `stages` longtext COMMENT 'stages list',
  `available` int DEFAULT '1' COMMENT 'available flag',
  `create_time` datetime DEFAULT NULL COMMENT 'create_time',
  `updated_time` datetime DEFAULT NULL COMMENT 'last_updated_time',
  `des` varchar(1024) DEFAULT NULL COMMENT 'description',
  `field_id_list` longtext COMMENT 'field_id_list',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=351 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

INSERT INTO `workflowTable` (`id`, `form_id`, `workflow_name`, `stage_hash`, `stage_num`, `creator_id`, `last_modify_id`, `stages`, `available`, `create_time`, `updated_time`, `des`, `field_id_list`) VALUES (null,2,'Create Use Case Workflow','6XZO3zfu02t+ULcbSOcTiw/5p3hUsZJixj6H+XrBPY0=',4,'','','[{"apiTaskName": "", "condition": [], "flowType": "Trigger", "id": 100, "label": "Form | Create Use Case"}, {"apiTaskName": "", "condition": [{"id": 2, "label": "region / Country approval", "style": 6, "value": ""}, {"id": 1, "label": "workspace owner approval", "style": 6, "value": ""}], "flowType": "Approval", "id": 101, "label": "Approval Process"}, {"apiTaskName": "system_add_new_usecase", "condition": [{"id": "usecase_name", "label": "Usecase Name", "style": 5, "value": "u5"}, {"id": "region_country", "label": "Region/Country", "style": 5, "value": "s1"}, {"id": "validity_date", "label": "Validity Date", "style": 5, "value": "u4"}, {"id": "uc_des", "label": "Description", "style": 5, "value": "u6"}, {"id": "admin_sa", "label": "Admin Service Account", "style": 5, "value": "u8"}, {"id": "uc_label", "label": "usecase label", "style": 5, "value": "u11"}, {"id": "budget", "label": "Budget", "style": 5, "value": "u7"}, {"id": "allow_cross_region", "label": "Allow Cross Region", "style": 5, "value": "u10"}, {"id": "resources_access", "label": "Resources Access", "style": 5, "value": "u9"}, {"id": "uc_team_group", "label": "Team group", "style": 5, "value": "u3"}, {"id": "uc_owner_group", "label": "Owner group", "style": 5, "value": "u2"}], "flowType": "System", "id": 17, "label": "Create New Use Case"}, {"apiTaskName": "system_define_field", "condition": [{"id": "FieldLabel", "label": "Field Label", "style": 1, "value": "Use case"}, {"id": "optionLabel", "label": "Option Label", "style": 5, "value": "u5"}, {"id": "optionsValue", "label": "Option Value", "style": 5, "value": "u2"}], "flowType": "System", "id": 14, "label": "Dynamic Approval Field"}]',1,'2021-05-03 00:00:00','2021-05-03 00:00:00','','[]');
INSERT INTO `workflowTable` (`id`, `form_id`, `workflow_name`, `stage_hash`, `stage_num`, `creator_id`, `last_modify_id`, `stages`, `available`, `create_time`, `updated_time`, `des`, `field_id_list`) VALUES (null,3,'Create Policy Workflow','wcHa54gy82QL7R2ajQ5Qz6CFHXnmygJMJzCmjE9Xva4=',3,'','','[{\"apiTaskName\": \"\", \"condition\": [], \"flowType\": \"Trigger\", \"id\": 100, \"label\": \"Form | Create Policy\"}, {\"apiTaskName\": \"\", \"condition\": [{\"id\": 1, \"label\": \"workspace owner approval\", \"style\": 6, \"value\": \"\"}], \"flowType\": \"Approval\", \"id\": 101, \"label\": \"Approval Process\"}, {\"apiTaskName\": \"CreatePolicyTagsV1\", \"condition\": [{\"des\": \"choose your project id\", \"id\": \"porject_id\", \"label\": \"Porject ID\", \"regExp\": \"\", \"style\": 5, \"value\": \"u1\"}, {\"des\": \"input your policy region, need to match gcp region\", \"id\": \"policy_location\", \"label\": \"policy region\", \"regExp\": \"\", \"style\": 5, \"value\": \"u2\"}, {\"des\": \"input your taxonomy display name\", \"id\": \"taxonomy_display_name\", \"label\": \"taxonomy display name\", \"regExp\": \"\", \"style\": 5, \"value\": \"u3\"}, {\"des\": \"input your taxonomy ad group\", \"id\": \"taxonomy_ad_group\", \"label\": \"taxonomy ad group\", \"regExp\": \"\", \"style\": 5, \"value\": \"u5\"}, {\"des\": \"input your taxonomy description\", \"id\": \"description\", \"label\": \"description\", \"regExp\": \"\", \"style\": 5, \"value\": \"u4\"}, {\"des\": \"input your policy tags object\", \"id\": \"policy_tags_list\", \"label\": \"policy_tags_list\", \"regExp\": \"\", \"style\": 5, \"value\": \"u7\"}], \"create_time\": \"Tue, 26 Oct 2021 00:00:00 GMT\", \"des\": \"Create Policy Tags\", \"flowType\": \"GoogleCloud\", \"id\": 40, \"label\": \"Create Policy Tags\", \"stage_group\": \"GoogleCloud\", \"updated_time\": \"Tue, 26 Oct 2021 00:00:00 GMT\"}]',1,'2021-05-03 00:00:00','2021-05-03 00:00:00','','[]');
INSERT INTO `workflowTable` (`id`, `form_id`, `workflow_name`, `stage_hash`, `stage_num`, `creator_id`, `last_modify_id`, `stages`, `available`, `create_time`, `updated_time`, `des`, `field_id_list`) VALUES (null,101,'Create Form Workflow','C3FoiOU5LQd1qg4busMJ54up9EaOFnT4wtMBYZvRzcs=',3,'','','[{\"apiTaskName\": \"\", \"condition\": [], \"flowType\": \"Trigger\", \"id\": 100, \"label\": \"Form | Create Form\"}, {\"apiTaskName\": \"\", \"condition\": [{\"id\": 1, \"label\": \"workspace owner approval\", \"style\": 6, \"value\": \"\"}], \"flowType\": \"Approval\", \"id\": 101, \"label\": \"Approval Process\"}, {\"apiTaskName\": \"system_create_form\", \"condition\": [{\"id\": \"form_name\", \"label\": \"Form Name\", \"style\": 5, \"value\": \"u1\"}, {\"id\": \"description\", \"label\": \"Description\", \"style\": 5, \"value\": \"u2\"}, {\"id\": \"field_list\", \"label\": \"field list\", \"style\": 5, \"value\": \"u3\"}], \"flowType\": \"System\", \"id\": 14, \"label\": \"Create Form\"}]',1,'2021-05-03 00:00:00','2021-05-03 00:00:00','','[]');
INSERT INTO `workflowTable` (`id`, `form_id`, `workflow_name`, `stage_hash`, `stage_num`, `creator_id`, `last_modify_id`, `stages`, `available`, `create_time`, `updated_time`, `des`, `field_id_list`) VALUES (null,103,'Update Form Workflow','PduIG6BUH7GJJ9/eypCQ39h7+1yGU9K3iEfHflK+qKU=',3,'','','[{\"apiTaskName\": \"\", \"condition\": [], \"flowType\": \"Trigger\", \"id\": 100, \"label\": \"Form | Update form\"}, {\"apiTaskName\": \"\", \"condition\": [{\"id\": 1, \"label\": \"workspace owner approval\", \"style\": 6, \"value\": \"\"}], \"flowType\": \"Approval\", \"id\": 101, \"label\": \"Approval Process\"}, {\"apiTaskName\": \"system_update_form\", \"condition\": [{\"id\": \"id\", \"label\": \"Form ID\", \"style\": 5, \"value\": \"u1\"}, {\"id\": \"form_name\", \"label\": \"Form Name\", \"style\": 5, \"value\": \"u2\"}, {\"id\": \"description\", \"label\": \"Description\", \"style\": 5, \"value\": \"u3\"}, {\"id\": \"field_list\", \"label\": \"field list\", \"style\": 5, \"value\": \"u4\"}], \"flowType\": \"System\", \"id\": 14, \"label\": \"Update Form\"}]',1,'2021-05-03 00:00:00','2021-05-03 00:00:00','','[]');
INSERT INTO `workflowTable` (`id`, `form_id`, `workflow_name`, `stage_hash`, `stage_num`, `creator_id`, `last_modify_id`, `stages`, `available`, `create_time`, `updated_time`, `des`, `field_id_list`) VALUES (null,102,'Delete Form Workflow','nlPFVsSdASMpc2INKizlJW1knLrGRvwWS9lTspTyeNU=',4,'','','[{\"apiTaskName\": \"\", \"condition\": [], \"flowType\": \"Trigger\", \"id\": 100, \"label\": \"Form | Delete form\"}, {\"apiTaskName\": \"\", \"condition\": [{\"id\": 1, \"label\": \"workspace owner approval\", \"style\": 6, \"value\": \"\"}], \"flowType\": \"Approval\", \"id\": 101, \"label\": \"Approval Process\"}, {\"apiTaskName\": \"DeleteTagTemplate\", \"condition\": [{\"des\": \"choose your tag_template_form_id\", \"id\": \"tag_template_form_id\", \"label\": \"Tag Template Form ID\", \"regExp\": \"\", \"style\": 5, \"value\": \"u1\"}], \"create_time\": \"Sat, 13 Nov 2021 00:00:00 GMT\", \"des\": \"Delete Tag Template\", \"flowType\": \"GoogleCloud\", \"id\": 38, \"label\": \"Delete Tag Template\", \"stage_group\": \"GoogleCloud\", \"updated_time\": \"Sat, 13 Nov 2021 00:00:00 GMT\"}, {\"apiTaskName\": \"system_delete_form\", \"condition\": [{\"id\": \"id\", \"label\": \"Form ID\", \"style\": 5, \"value\": \"u1\"}], \"flowType\": \"System\", \"id\": 17, \"label\": \"Delete Form\"}]',1,'2021-05-03 00:00:00','2021-05-03 00:00:00','','[]');
INSERT INTO `workflowTable` (`id`, `form_id`, `workflow_name`, `stage_hash`, `stage_num`, `creator_id`, `last_modify_id`, `stages`, `available`, `create_time`, `updated_time`, `des`, `field_id_list`) VALUES (null,104,'Create Tag Template Workflow','GE5m/4PQPLChC5yyFvcQnfMkpDrgCGBr9m+P5r+xe84=',3,'','','[{\"apiTaskName\": \"\", \"condition\": [], \"flowType\": \"Trigger\", \"id\": 100, \"label\": \"Form | Create Tag Template\"}, {\"apiTaskName\": \"\", \"condition\": [{\"id\": 1, \"label\": \"workspace owner approval\", \"style\": 6, \"value\": \"\"}], \"flowType\": \"Approval\", \"id\": 101, \"label\": \"Approval Process\"}, {\"apiTaskName\": \"CreateTagTemplate\", \"condition\": [{\"des\": \"choose your tag_template_display_name\", \"id\": \"tag_template_display_name\", \"label\": \"Tag Template Name\", \"regExp\": \"\", \"style\": 5, \"value\": \"u1\"}, {\"des\": \"input your description\", \"id\": \"description\", \"label\": \"Description\", \"regExp\": \"\", \"style\": 5, \"value\": \"u2\"}, {\"des\": \"input your field_list\", \"id\": \"field_list\", \"label\": \"Field List\", \"regExp\": \"\", \"style\": 5, \"value\": \"u3\"}], \"create_time\": \"Sat, 13 Nov 2021 00:00:00 GMT\", \"des\": \"Create Tag Template\", \"flowType\": \"GoogleCloud\", \"id\": 36, \"label\": \"Create Tag Template\", \"stage_group\": \"GoogleCloud\", \"updated_time\": \"Sat, 13 Nov 2021 00:00:00 GMT\"}]',1,'2021-05-03 00:00:00','2021-05-03 00:00:00','','[]');
INSERT INTO `workflowTable` (`id`, `form_id`, `workflow_name`, `stage_hash`, `stage_num`, `creator_id`, `last_modify_id`, `stages`, `available`, `create_time`, `updated_time`, `des`, `field_id_list`) VALUES (null,105,'Update Tag Template Workflow','5x3jhvAgZM5BlNUZyFmsvD98MA1w72VTLgNPsQdorYw=',3,'','','[{\"apiTaskName\": \"\", \"condition\": [], \"flowType\": \"Trigger\", \"id\": 100, \"label\": \"Form | Update Tag Template\"}, {\"apiTaskName\": \"\", \"condition\": [{\"id\": 1, \"label\": \"workspace owner approval\", \"style\": 6, \"value\": \"\"}], \"flowType\": \"Approval\", \"id\": 101, \"label\": \"Approval Process\"}, {\"apiTaskName\": \"UpdateTagTemplate\", \"condition\": [{\"des\": \"choose your tag_template_form_id\", \"id\": \"tag_template_form_id\", \"label\": \"Tag Template Form ID\", \"regExp\": \"\", \"style\": 5, \"value\": \"u1\"}, {\"des\": \"choose your tag_template_display_name\", \"id\": \"tag_template_display_name\", \"label\": \"Tag Template Name\", \"regExp\": \"\", \"style\": 5, \"value\": \"u2\"}, {\"des\": \"input your description\", \"id\": \"description\", \"label\": \"Description\", \"regExp\": \"\", \"style\": 5, \"value\": \"u3\"}, {\"des\": \"input your field_list\", \"id\": \"field_list\", \"label\": \"Field List\", \"regExp\": \"\", \"style\": 5, \"value\": \"u4\"}], \"create_time\": \"Sat, 13 Nov 2021 00:00:00 GMT\", \"des\": \"Update Tag Template\", \"flowType\": \"GoogleCloud\", \"id\": 39, \"label\": \"Update Tag Template\", \"stage_group\": \"GoogleCloud\", \"updated_time\": \"Sat, 13 Nov 2021 00:00:00 GMT\"}]',1,'2021-05-03 00:00:00','2021-05-03 00:00:00','','[]');
INSERT INTO `workflowTable` (`id`, `form_id`, `workflow_name`, `stage_hash`, `stage_num`, `creator_id`, `last_modify_id`, `stages`, `available`, `create_time`, `updated_time`, `des`, `field_id_list`) VALUES (null,106,'Delete Tag Template Workflow','OOxxgQsm6QqId5nLLt9+CO2w0WlYnBT3w0pSmYKK+N0=',3,'','','[{\"apiTaskName\": \"\", \"condition\": [], \"flowType\": \"Trigger\", \"id\": 100, \"label\": \"Form | Delete Tag Template\"}, {\"apiTaskName\": \"\", \"condition\": [{\"id\": 1, \"label\": \"workspace owner approval\", \"style\": 6, \"value\": \"\"}], \"flowType\": \"Approval\", \"id\": 101, \"label\": \"Approval Process\"}, {\"apiTaskName\": \"DeleteTagTemplate\", \"condition\": [{\"des\": \"choose your tag_template_form_id\", \"id\": \"tag_template_form_id\", \"label\": \"Tag Template Form ID\", \"regExp\": \"\", \"style\": 5, \"value\": \"u1\"}], \"create_time\": \"Sat, 13 Nov 2021 00:00:00 GMT\", \"des\": \"Delete Tag Template\", \"flowType\": \"GoogleCloud\", \"id\": 38, \"label\": \"Delete Tag Template\", \"stage_group\": \"GoogleCloud\", \"updated_time\": \"Sat, 13 Nov 2021 00:00:00 GMT\"}]',1,'2021-05-03 00:00:00','2021-05-03 00:00:00','','[]');
INSERT INTO `workflowTable` (`id`, `form_id`, `workflow_name`, `stage_hash`, `stage_num`, `creator_id`, `last_modify_id`, `stages`, `available`, `create_time`, `updated_time`, `des`, `field_id_list`) VALUES (null,107,'Data Publishing Requeset Workflow','+K2h/rDsQbY0K7WajMfR/9jyfC3yj7dWWMg3bfWuisU=',4,'','','[{\"apiTaskName\": \"\", \"condition\": [], \"flowType\": \"Trigger\", \"id\": 100, \"label\": \"Form | Data Publishing Request\"}, {\"apiTaskName\": \"\", \"condition\": [{\"id\": 1, \"label\": \"Workspace owner\", \"style\": 6, \"value\": \"\"}], \"flowType\": \"Approval\", \"id\": 101, \"label\": \"Approval Process\"}, {\"apiTaskName\": \"ModifyTablePolicyTags\", \"condition\": [{\"des\": \"choose your project_id\", \"id\": \"project_id\", \"label\": \"project id\", \"regExp\": \"\", \"style\": 5, \"value\": \"u1\"}, {\"des\": \"choose your location\", \"id\": \"location\", \"label\": \"location\", \"regExp\": \"\", \"style\": 5, \"value\": \"u2\"}, {\"des\": \"choose your dataset_id\", \"id\": \"dataset_id\", \"label\": \"dataset id\", \"regExp\": \"\", \"style\": 5, \"value\": \"u3\"}, {\"des\": \"choose your table_id\", \"id\": \"table_id\", \"label\": \"Table id\", \"regExp\": \"\", \"style\": 5, \"value\": \"u4\"}, {\"des\": \"choose your Table s fields\", \"id\": \"fields\", \"label\": \"Table s fields\", \"regExp\": \"\", \"style\": 5, \"value\": \"u5\"}], \"create_time\": \"Wed, 15 Dec 2021 00:00:00 GMT\", \"des\": \"Modify Table Policy Tags \", \"flowType\": \"GoogleCloud\", \"id\": 45, \"label\": \"Modify Table Policy Tags\", \"stage_group\": \"GoogleCloud\", \"updated_time\": \"Wed, 15 Dec 2021 00:00:00 GMT\"}, {\"apiTaskName\": \"ModifyTableTags\", \"condition\": [{\"des\": \"choose your project_id\", \"id\": \"project_id\", \"label\": \"project id\", \"regExp\": \"\", \"style\": 5, \"value\": \"u1\"}, {\"des\": \"choose your dataset_id\", \"id\": \"dataset_id\", \"label\": \"dataset id\", \"regExp\": \"\", \"style\": 5, \"value\": \"u3\"}, {\"des\": \"choose your location\", \"id\": \"location\", \"label\": \"location\", \"regExp\": \"\", \"style\": 5, \"value\": \"u2\"}, {\"des\": \"choose your table_id\", \"id\": \"table_id\", \"label\": \"Table id\", \"regExp\": \"\", \"style\": 5, \"value\": \"u4\"}, {\"des\": \"choose your Table s fields\", \"id\": \"fields\", \"label\": \"Table s fields tags\", \"regExp\": \"\", \"style\": 5, \"value\": \"u5\"}, {\"des\": \"choose your table_tags\", \"id\": \"table_tags\", \"label\": \"Table s tags\", \"regExp\": \"\", \"style\": 5, \"value\": \"u6\"}], \"create_time\": \"Wed, 15 Dec 2021 00:00:00 GMT\", \"des\": \"Modify Table Tags\", \"flowType\": \"GoogleCloud\", \"id\": 46, \"label\": \"Modify Table Tags\", \"stage_group\": \"GoogleCloud\", \"updated_time\": \"Wed, 15 Dec 2021 00:00:00 GMT\"}]',1,'2021-05-03 00:00:00','2021-05-03 00:00:00','','[]');
INSERT INTO `workflowTable` (`id`, `form_id`, `workflow_name`, `stage_hash`, `stage_num`, `creator_id`, `last_modify_id`, `stages`, `available`, `create_time`, `updated_time`, `des`, `field_id_list`) VALUES (null,1,'Add User to Use Case Workflow','lSi37jd7wQB8EEzlqER/09w7tlYwL4K1LXt78/46EbM=',2,'','','[{\"apiTaskName\": \"\", \"condition\": [], \"flowType\": \"Trigger\", \"id\": 100, \"label\": \"Form | Add User to Use Case\"}, {\"apiTaskName\": \"\", \"condition\": [{\"id\": 1, \"label\": \"Workspace owner\", \"style\": 6, \"value\": \"\"}, {\"id\": 3, \"label\": \"Use case approval\", \"style\": 6, \"value\": \"d15\"}], \"flowType\": \"Approval\", \"id\": 101, \"label\": \"Approval Process\"}]',1,'2021-05-03 00:00:00','2021-05-03 00:00:00','','[]');
INSERT INTO `workflowTable` (`id`, `form_id`, `workflow_name`, `stage_hash`, `stage_num`, `creator_id`, `last_modify_id`, `stages`, `available`, `create_time`, `updated_time`, `des`, `field_id_list`) VALUES (null,108,'Data Consumption Request Workflow','wuPHzfmE5it3rqfU7ioI0YrBho0o/2R6Vis1foZWiwI=',4,'','','[{\"apiTaskName\": \"\", \"condition\": [], \"flowType\": \"Trigger\", \"id\": 100, \"label\": \"Form | Data Consumption Request\"}, {\"apiTaskName\": \"\", \"condition\": [{\"id\": 1, \"label\": \"Workspace owner\", \"style\": 6, \"value\": \"\"}, {\"id\": 0, \"label\": \"Data owner\", \"style\": 6, \"value\": \"\"}], \"flowType\": \"Approval\", \"id\": 101, \"label\": \"Approval Process\"}, {\"apiTaskName\": \"GrantRoleForBQTable\", \"condition\": [{\"des\": \"choose your project_id\", \"id\": \"project_id\", \"label\": \"project id\", \"regExp\": \"\", \"style\": 5, \"value\": \"u1\"}, {\"des\": \"choose your Use Case Name\", \"id\": \"usecase_name\", \"label\": \"Use Case Name\", \"regExp\": \"\", \"style\": 5, \"value\": \"d15\"}, {\"des\": \"choose your location\", \"id\": \"location\", \"label\": \"Location\", \"regExp\": \"\", \"style\": 5, \"value\": \"u3\"}, {\"des\": \"choose your dataset_id\", \"id\": \"dataset_id\", \"label\": \"dataset id\", \"regExp\": \"\", \"style\": 5, \"value\": \"u4\"}, {\"des\": \"choose your table_id\", \"id\": \"table_id\", \"label\": \"Table id\", \"regExp\": \"\", \"style\": 5, \"value\": \"u5\"}], \"create_time\": \"Wed, 15 Dec 2021 00:00:00 GMT\", \"des\": \"Grant Role For Bigquery Table\", \"flowType\": \"GoogleCloud\", \"id\": 43, \"label\": \"Grant Role For Bigquery Table\", \"stage_group\": \"GoogleCloud\", \"updated_time\": \"Wed, 15 Dec 2021 00:00:00 GMT\"}, {\"apiTaskName\": \"GrantRoleForPolicyTags\", \"condition\": [{\"des\": \"choose your project_id\", \"id\": \"project_id\", \"label\": \"project id\", \"regExp\": \"\", \"style\": 5, \"value\": \"u1\"}, {\"des\": \"choose your Use Case Name\", \"id\": \"usecase_name\", \"label\": \"Use Case Name\", \"regExp\": \"\", \"style\": 5, \"value\": \"d15\"}, {\"des\": \"choose your location\", \"id\": \"location\", \"label\": \"Location\", \"regExp\": \"\", \"style\": 5, \"value\": \"u3\"}, {\"des\": \"choose your dataset_id\", \"id\": \"dataset_id\", \"label\": \"dataset id\", \"regExp\": \"\", \"style\": 5, \"value\": \"u4\"}, {\"des\": \"choose your table_id\", \"id\": \"table_id\", \"label\": \"Table id\", \"regExp\": \"\", \"style\": 5, \"value\": \"u5\"}, {\"des\": \"choose your Table s fields\", \"id\": \"fields\", \"label\": \"Table s fields tags\", \"regExp\": \"\", \"style\": 5, \"value\": \"u6\"}], \"create_time\": \"Wed, 15 Dec 2021 00:00:00 GMT\", \"des\": \"Grant Role For PolicyTags\", \"flowType\": \"GoogleCloud\", \"id\": 44, \"label\": \"Grant Role For PolicyTags\", \"stage_group\": \"GoogleCloud\", \"updated_time\": \"Wed, 15 Dec 2021 00:00:00 GMT\"}]',1,'2021-05-03 00:00:00','2021-05-03 00:00:00','','[]');

-- Table structure for field [entity]
-- ----------------------------
DROP TABLE IF EXISTS `stageTable`;
CREATE TABLE `stageTable` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'stage_id',
  `label` varchar(64) DEFAULT NULL COMMENT 'stage type name',
  `stage_group` varchar(64) DEFAULT NULL COMMENT 'stage type',
  `flowType` varchar(64) DEFAULT NULL COMMENT 'flow type',
  `apiTaskName` varchar(64) DEFAULT NULL COMMENT 'the api task name',
  `condition` longtext COMMENT 'value list',
  `des` varchar(1024) DEFAULT NULL COMMENT 'description',
  `create_time` datetime DEFAULT NULL COMMENT 'create_time',
  `updated_time` datetime DEFAULT NULL COMMENT 'last_updated_time',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

-- bigquery
-- insert into stageTable values (null, 'Create Bigquery Dataset', 'GoogleCloud', 'GoogleCloud', 'GoogleCloud', '[{"id": "porject_id", "style": 3, "label": "Porject ID", "value": "", "des": "input your project id", "regExp": ""}, {"id": "dataset_location", "style": 3, "label": "Dataset Location", "value": "", "des": "choose your dataset region", "regExp": ""}, {"id": "dataset_name", "style": 3, "label": "Dataset Name", "value": "", "des": "input your dataset name", "regExp": ""}, {"id": "dataset_cmek", "style": 3, "label": "Dataset CMEK", "value": "", "des": "input your dataset cmek, will use the default gcp key if no input", "regExp": ""}, {"id": "table_expiration", "style": 1, "label": "Table Expiration", "value": "", "des": "input n days your table expiration, default is None", "regExp": ""}, {"id": "dataset_label", "style": 3, "label": "Dataset Label", "value": "", "des": "input your dataset label, for example: dataset_owner=second,dataset_expire=9days", "regExp": ""}]', 'Create bigquery dataset', '2021-05-09', '2021-05-09');
-- insert into stageTable values (null, 'Create Bigquery Table', 'GoogleCloud', 'GoogleCloud', 'GoogleCloud', '[{"id": "porject_id", "style": 3, "label": "Porject ID", "value": "", "des": "input your project id", "regExp": ""}, {"id": "dataset_name", "style": 3, "label": "Dataset Name", "value": "", "des": "input your dataset name", "regExp": ""}, {"id": "table_name", "style": 3, "label": "Table Name", "value": "", "des": "input your table name", "regExp": ""}, {"id": "fields_schema", "style": 4, "label": "Fields Schema", "value": "", "des": "choose an upload files field in form for the fields schema", "regExp": ""}, {"id": "table_cmek", "style": 3, "label": "Table CMEK", "value": "", "des": "input your table cmek, will use the dataset cmek if no input", "regExp": ""}, {"id": "table_partition", "style": 2, "label": "Table Partitioning Type", "value": "", "des": "choose your table partitioning type", "options": [{"label": "By day", "value": "By day"}, {"label": "By hour", "value": "By hour"}, {"label": "By month", "value": "By month"}, {"label": "By year", "value": "By year"}], "regExp": ""}, {"id": "table_label", "style": 3, "label": "Table Label", "value": "", "des": "input your table label, for example: table_owner=second,table_expire=9days", "regExp": ""}]', 'Create bigquery table', '2021-05-09', '2021-05-09');
-- insert into stageTable values (null, 'Create Bigquery View', 'GoogleCloud', 'GoogleCloud', 'GoogleCloud', '[{"id": "porject_id", "style": 3, "label": "Porject ID", "value": "", "des": "input your project id", "regExp": ""}, {"id": "dataset_name", "style": 3, "label": "Dataset Name", "value": "", "des": "input your dataset name", "regExp": ""}, {"id": "view_name", "style": 3, "label": "View Name", "value": "", "des": "input your view name", "regExp": ""}, {"id": "fields_schema", "style": 4, "label": "Fields Schema", "value": "", "des": "choose your view query schema field in form", "regExp": ""}, {"id": "view_label", "style": 3, "label": "View Label", "value": "", "des": "input your view label, for example: view_owner=second,view_expire=9days", "regExp": ""}]', 'Create bigquery view', '2021-05-09', '2021-05-09');
-- insert into stageTable values (null, 'Bigquery IAM Binding', 'GoogleCloud', 'GoogleCloud', 'GoogleCloud', '[{"id": "porject_id", "style": 3, "label": "Porject ID", "value": "", "des": "input your project id", "regExp": ""}, {"id": "dataset_name", "style": 3, "label": "Dataset Name", "value": "", "des": "input your dataset name", "regExp": ""}, {"id": "binding_list", "style": 3, "label": "Binding List", "value": "", "des": "choose your binding list, for example: [account_type:account_email,account_type:account_email]", "regExp": ""}, {"id": "binding_level", "style": 2, "label": "Binding Level", "value": "", "des": "choose your binding level", "options": [{"label": "dataset", "value": "dataset"}, {"label": "table/view", "value": "table/view"}, {"label": "field", "value": "field"}], "regExp": ""}, {"id": "resource_list", "style": 3, "label": "Resource List", "value": "", "des": "choose your binding resource splice by ,", "regExp": ""}]', 'Bigquery IAM binding', '2021-05-09', '2021-05-09');
insert into stageTable values (14, 'Grant Role For Bigquery Table', 'GoogleCloud', 'GoogleCloud', 'GrantRoleForBQTable', '[{"id": "project_id", "style": 5, "label": "project id", "value": "", "des": "choose your project_id", "regExp": ""}, {"id": "usecase_name", "style": 5, "label": "Use Case Name", "value": "", "des": "choose your Use Case Name", "regExp": ""}, {"id": "location", "style": 5, "label": "Location", "value": "", "des": "choose your location", "regExp": ""}, {"id": "dataset_id", "style": 5, "label": "dataset id", "value": "", "des": "choose your dataset_id", "regExp": ""}, {"id": "table_id", "style": 5, "label": "Table id", "value": "", "des": "choose your table_id", "regExp": ""}]', 'Grant Role For Bigquery Table', '2021-12-15', '2021-12-15');

insert into stageTable values (24, 'Create Bigquery DataSet', 'GoogleCloud', 'GoogleCloud', 'CreateBQDataset', '[{"id": "porject_id", "style": 3, "label": "Porject ID", "value": "", "des": "choose your project id", "regExp": ""}, {"id": "dataset_location", "style": 3, "label": "Dataset Loaction", "value": "", "des": "input your dataset location", "regExp": ""}, {"id": "usecase_name", "style": 5, "label": "Usecase Name", "value": "", "des": "choose your usecase name. can be not", "optional": true, "regExp": ""}, {"id": "dataset_name", "style": 3, "label": "Dataset ID", "value": "", "des": "input your dataset id", "regExp": ""}, {"id": "dataset_cmek", "style": 3, "label": "Dataset CMEK", "value": "", "optional": true, "des": "input your dataset cmek", "regExp": ""}, {"id": "dataset_labels", "style": 3, "label": "Dataset Labels", "value": "", "des": "input your labels, split by , For example: label1:value1,label2:value2...", "regExp": ""}]', 'Create Bigquery DataSet', '2021-06-26', '2021-06-26');
insert into stageTable values (25, 'Create Bigquery Table', 'GoogleCloud', 'GoogleCloud', 'CreateBQTable', '[{"id": "porject_id", "style": 3, "label": "Porject ID", "value": "", "des": "choose your project id", "regExp": ""}, {"id": "usecase_name", "style": 5, "label": "Usecase Name", "value": "", "optional": true, "des": "choose your usecase name. can be not", "regExp": ""}, {"id": "dataset_name", "style": 3, "label": "Dataset ID", "value": "", "des": "input your dataset id", "regExp": ""}, {"id": "table_name", "style": 3, "label": "Table Name", "value": "", "des": "input your use case name", "regExp": ""}, {"id": "table_labels", "style": 3, "label": "Table Labels", "value": "", "des": "input your labels, split by , For example: label1:value1,label2:value2....", "regExp": ""}, {"id": "table_schema_csv", "style": 5, "label": "Table Schema CSV File", "value": "", "des": "Choose your table schema CSV file", "regExp": ""}]', 'Create Bigquery Table', '2021-06-26', '2021-06-26');
insert into stageTable values (26, 'Grant Role For Bigquery DataSet', 'GoogleCloud', 'GoogleCloud', 'GrantRoleForBQDataset', '[{"id": "porject_id", "style": 3, "label": "Porject ID", "value": "", "des": "choose your project id", "regExp": ""}, {"id": "usecase_name", "style": 3, "label": "Use Case Name", "value": "", "des": "input your use case name", "regExp": ""}, {"id": "location", "style": 3, "label": "location", "value": "", "des": "input your dataset location ", "regExp": ""}, {"id": "dataset_id_list", "style": 3, "label": "dataset_id_list", "value": "", "des": "input your dataset ids split by , For example: dataset1,datset2...", "regExp": ""}]', 'Grant Role For Bigquery DataSet', '2021-06-26', '2021-06-26');

-- storage
insert into stageTable values (15, 'Create Storage Bucket', 'GoogleCloud', 'GoogleCloud', 'CreateGCSBucket', '[{"id": "porject_id", "style": 3, "label": "Porject ID", "value": "", "des": "choose your project id", "regExp": ""}, {"id": "bucket_location", "style": 3, "label": "bucket region", "value": "", "des": "input your bucket region, need to match gcp region", "regExp": ""}, {"id": "usecase_name", "style": 5, "label": "Usecase Name", "optional": true, "value": "", "des": "choose your usecase name. can be not", "regExp": ""}, {"id": "bucket_name", "style": 3, "label": "bucket_name", "value": "", "des": "input your bucket name", "regExp": ""}, {"id": "bucket_class", "style": 2, "label": "bucket_class", "value": "", "options": [{"label": "STANDARD", "value": "STANDARD"}, {"label": "NEARLINE", "value": "NEARLINE"}, {"label": "COLDLINE", "value": "COLDLINE"}, {"label": "ARCHIVE", "value": "ARCHIVE"}], "des": "choose your storage class", "regExp": ""}, {"id": "bucket_cmek", "style": 3, "label": "bucket_cmek", "value": "", "optional": true, "des": "input your kms_key_name", "regExp": ""}, {"id": "bucket_labels", "style": 3, "label": "bucket_labels", "value": "", "des": "input your bucket labels and split by , for example: key1=value1,key2=value2 ", "regExp": ""}]', 'Create Storage Bucket', '2021-06-26', '2021-06-26');
insert into stageTable values (16, 'Storage IAM Binding', 'GoogleCloud', 'GoogleCloud', 'GrantRoleForGCSBucket', '[{"id": "porject_id", "style": 3, "label": "Porject ID", "value": "", "des": "choose your project id", "regExp": ""}, {"id": "bucket_name", "style": 3, "label": "bucket_name", "value": "", "des": "input your bucket name", "regExp": ""}, {"id": "member_roles", "style": 3, "label": "member_roles", "value": "", "des": "input your member and roles and split by :and+ for example: type:user1+role1,type:user1+role2,type:user2+role1 ", "regExp": ""}]', 'Storage IAM binding', '2021-06-26', '2021-06-26');

-- data catalog
insert into stageTable values (17, 'Create Policy Tags', 'GoogleCloud', 'GoogleCloud', 'CreatePolicyTagsV1', '[{"id": "porject_id", "style": 5, "label": "Porject ID", "value": "", "des": "choose your project id", "regExp": ""}, {"id": "policy_location", "style": 5, "label": "policy region", "value": "", "des": "input your policy region, need to match gcp region", "regExp": ""}, {"id": "taxonomy_display_name", "style": 5, "label": "taxonomy display name", "value": "", "des": "input your taxonomy display name", "regExp": ""}, {"id": "taxonomy_ad_group", "style": 5, "label": "taxonomy ad group", "value": "", "des": "input your taxonomy ad group", "regExp": ""}, {"id": "description", "style": 5, "label": "description", "value": "", "des": "input your taxonomy description", "regExp": ""}, {"id": "policy_tags_list", "style": 5, "label": "policy_tags_list", "value": "", "des": "input your policy tags object", "regExp": ""}]', 'Create Policy Tags', '2021-10-26', '2021-10-26');
insert into stageTable values (18, 'Create Tag Template', 'GoogleCloud', 'GoogleCloud', 'CreateTagTemplate', '[{"id": "tag_template_display_name", "style": 5, "label": "Tag Template Name", "value": "", "des": "choose your tag_template_display_name", "regExp": ""}, {"id": "description", "style": 5, "label": "Description", "value": "", "des": "input your description", "regExp": ""}, {"id": "field_list", "style": 5, "label": "Field List", "value": "", "des": "input your field_list", "regExp": ""}]', 'Create Tag Template', '2021-11-13', '2021-11-13');
insert into stageTable values (19, 'Update Tag Template', 'GoogleCloud', 'GoogleCloud', 'UpdateTagTemplate', '[{"id": "tag_template_form_id", "style": 5, "label": "Tag Template Form ID", "value": "", "des": "choose your tag_template_form_id", "regExp": ""}, {"id": "tag_template_display_name", "style": 5, "label": "Tag Template Name", "value": "", "des": "choose your tag_template_display_name", "regExp": ""}, {"id": "description", "style": 5, "label": "Description", "value": "", "des": "input your description", "regExp": ""}, {"id": "field_list", "style": 5, "label": "Field List", "value": "", "des": "input your field_list", "regExp": ""}]', 'Update Tag Template', '2021-11-13', '2021-11-13');
insert into stageTable values (20, 'Delete Tag Template', 'GoogleCloud', 'GoogleCloud', 'DeleteTagTemplate', '[{"id": "tag_template_form_id", "style": 5, "label": "Tag Template Form ID", "value": "", "des": "choose your tag_template_form_id", "regExp": ""}]', 'Delete Tag Template', '2021-11-13', '2021-11-13');
insert into stageTable values (21, 'Modify Table Policy Tags', 'GoogleCloud', 'GoogleCloud', 'ModifyTablePolicyTags', '[{"id": "project_id", "style": 5, "label": "project id", "value": "", "des": "choose your project_id", "regExp": ""}, {"id": "location", "style": 5, "label": "location", "value": "", "des": "choose your location", "regExp": ""}, {"id": "dataset_id", "style": 5, "label": "dataset id", "value": "", "des": "choose your dataset_id", "regExp": ""}, {"id": "table_id", "style": 5, "label": "Table id", "value": "", "des": "choose your table_id", "regExp": ""}, {"id": "fields", "style": 5, "label": "Table s fields", "value": "", "des": "choose your Table s fields", "regExp": ""}]', 'Modify Table Policy Tags ', '2021-12-15', '2021-12-15');
insert into stageTable values (22, 'Modify Table Tags', 'GoogleCloud', 'GoogleCloud', 'ModifyTableTags', '[{"id": "project_id", "style": 5, "label": "project id", "value": "", "des": "choose your project_id", "regExp": ""}, {"id": "dataset_id", "style": 5, "label": "dataset id", "value": "", "des": "choose your dataset_id", "regExp": ""}, {"id": "location", "style": 5, "label": "location", "value": "", "des": "choose your location", "regExp": ""}, {"id": "table_id", "style": 5, "label": "Table id", "value": "", "des": "choose your table_id", "regExp": ""}, {"id": "fields", "style": 5, "label": "Table s fields tags", "value": "", "des": "choose your Table s fields", "regExp": ""}, {"id": "table_tags", "style": 5, "label": "Table s tags", "value": "", "des": "choose your table_tags", "regExp": ""}]', 'Modify Table Tags', '2021-12-15', '2021-12-15');
insert into stageTable values (23, 'Grant Role For PolicyTags', 'GoogleCloud', 'GoogleCloud', 'GrantRoleForPolicyTags', '[{"id": "project_id", "style": 5, "label": "project id", "value": "", "des": "choose your project_id", "regExp": ""}, {"id": "usecase_name", "style": 5, "label": "Use Case Name", "value": "", "des": "choose your Use Case Name", "regExp": ""}, {"id": "location", "style": 5, "label": "Location", "value": "", "des": "choose your location", "regExp": ""}, {"id": "dataset_id", "style": 5, "label": "dataset id", "value": "", "des": "choose your dataset_id", "regExp": ""}, {"id": "table_id", "style": 5, "label": "Table id", "value": "", "des": "choose your table_id", "regExp": ""}, {"id": "fields", "style": 5, "label": "Table s fields tags", "value": "", "des": "choose your Table s fields", "regExp": ""}]', 'Grant Role For PolicyTags', '2021-12-15', '2021-12-15');


-- ----------------------------
-- Table structure for form [entity]
-- ----------------------------
DROP TABLE IF EXISTS `approvalTable`;
CREATE TABLE `approvalTable` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'approval_id',
  `input_form_id` int NOT NULL COMMENT 'input_form_id',
  `approval_num` int DEFAULT NULL COMMENT 'form fields num',
  `label` varchar(256) DEFAULT NULL COMMENT 'approval label',
  `ad_group` varchar(256) DEFAULT NULL COMMENT 'approval adgroup',
  `account_id` varchar(256) DEFAULT '' COMMENT 'approver account id',
  `now_approval` int DEFAULT '0' COMMENT 'if the approval process is time for this num',
  `is_approved` int DEFAULT '0' COMMENT 'if this num approval is done',
  `comment` varchar(1024) DEFAULT NULL COMMENT 'description',
  `updated_time` datetime DEFAULT NULL COMMENT 'last_updated_time',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=351 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
INSERT INTO `approvalTable` (`id`, `input_form_id`, `approval_num`, `label`, `ad_group`, `account_id`, `now_approval`, `is_approved`, `comment`, `updated_time`) VALUES (455,498,1,'workspace owner approval','Engineer@torro.ai','torroAdmin@torro.ai',0,1,'','2021-12-26 09:28:37');

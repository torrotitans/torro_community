#!/usr/bin/python
# -*- coding: UTF-8 -*

from flask_restful import Api

from api.form.interface_base_form import interfaceBaseForm
from api.form.interface_detail_form import interfaceDetailForm, interfaceDetailFormList
from api.form.interface_edit_form import interfaceEditForm
from api.form.interface_field_template import interfaceFieldTemplate
from api.workflow.interface_stages import interfaceStages
from api.workflow.interface_edit_workflow import interfaceEditWorkflow
from api.workflow.interface_base_workflow import interfaceBaseWorkflow
from api.workflow.interface_details_workflow import interfaceDetailsWorkflow
from api.user.interface_user_login import interfaceUserLogin
from api.org.interface_org_setting import interfaceOrgSetting
from api.workspace.interface_workspace_info import interfaceWorkspaceInfo
from api.workspace.interface_workspace_setting import interfaceWorkspaceSetting
from api.usecase.interface_usecase_info import interfaceUseCaseInfo
from api.usecase.interface_usecase_setting import interfaceUseCaseSetting
from api.login.interface_login import interfaceLogin
# from api.login.interface_offine import interfaceOffine
from api.it.interface_debug import interfaceDebug
from api.it.interface_torro_config import interfaceTorroConfig

from api.org.interface_role_info import interfaceRoleInfo
from api.gcp.interface_gcp_execute import interfaceGCPExecute
from api.gcp.interface_table_schema import interfaceTableSchema

from api.dashboard.interface_dashboard import interfaceDashboard
from api.input_form.interface_input_form import interfaceInputForm, interfaceInputFormList
from api.input_form.interface_input_form_details import interfaceInputFormDetails, interfaceInputFormDetailsList
from api.governance.interface_governance import interfaceGovernance, interfaceGovernanceBatch
from api.user.interface_user_info import interfaceUserInfo
from api.dashboard.interface_options import interfaceOptions
from api.input_form.interface_comment import interfaceComment
from api.workspace.interface_policy_tags_info import interfacePolicyTagsList
from api.workspace.interface_tag_template_info import interfaceTagTemplateList

from api.system.interface_system_trigger import interfaceSystemTrigger
from api.system.interface_system_notify import interfaceSystemNotify
api = Api()

api.add_resource(
    interfaceSystemTrigger,
    '/api/systemTrigger',
)
api.add_resource(
    interfaceSystemNotify,
    '/api/systemNotify',
)
api.add_resource(
    interfaceTagTemplateList,
    '/api/getTagTemplateList',
)

api.add_resource(
    interfacePolicyTagsList,
    '/api/getPolicyTagsList',
)
api.add_resource(
    interfaceDashboard,
    '/api/getInputFormInfo',
)
api.add_resource(
    interfaceComment,
    '/api/inputFormComment',
)
api.add_resource(
    interfaceInputFormDetails,
    '/api/getInputFormDetails',
)
api.add_resource(
    interfaceInputFormDetailsList,
    '/api/getInputFormDetailsList',
)

api.add_resource(
    interfaceTorroConfig,
    '/api/torroConfig/<string:configName>',
)

api.add_resource(
    interfaceBaseForm,
    '/api/getFormList',
    '/api/getFormList/<int:system>',
)
# get
api.add_resource(
    interfaceOptions,
    '/api/getDashboardOptions',
)
api.add_resource(
    interfaceDetailForm,
    '/api/getFormData',
)
api.add_resource(
    interfaceDetailFormList,
    '/api/getFormDataList',
)
# post: {'id': int}

api.add_resource(
    interfaceEditForm,
    '/api/postFormData'
)

api.add_resource(
    interfaceFieldTemplate,
    '/api/getFieldTemplate'
)
# post: {'style': int}


api.add_resource(
    interfaceStages,
    '/api/getAllStages',
)

api.add_resource(
    interfaceEditWorkflow,
    '/api/postWorkflowData',
)

api.add_resource(
    interfaceBaseWorkflow,
    '/api/getBaseWorkflowListByFormId',
)
api.add_resource(
    interfaceDetailsWorkflow,
    '/api/getDetailsWorkflowDataById',
)


api.add_resource(
    interfaceUserLogin,
    '/api/userLogin',
)
api.add_resource(
    interfaceUserInfo,
    '/api/getUserInfo',
)
api.add_resource(
    interfaceOrgSetting,
    '/api/orgSetting',
)

api.add_resource(
    interfaceLogin,
    '/api/login',
)
# api.add_resource(
#     interfaceOffine,
#     '/api/offline',
# )

api.add_resource(
    interfaceWorkspaceSetting,
    '/api/workspaceSetting',
)

api.add_resource(
    interfaceWorkspaceInfo,
    '/api/workspaceInfo',
)
api.add_resource(
    interfaceUseCaseSetting,
    '/api/usecaseSetting',
)

api.add_resource(
    interfaceUseCaseInfo,
    '/api/usecaseInfo',
)
api.add_resource(
    interfaceDebug,
    '/api/debug',
)

api.add_resource(
    interfaceRoleInfo,
    '/api/getRolesInfo',
)

api.add_resource(
    interfaceGCPExecute,
    '/api/taskExecute'
)
api.add_resource(
    interfaceTableSchema,
    '/api/tableSchema'
)
api.add_resource(
    interfaceInputForm,
    '/api/inputFormData',
)
api.add_resource(
    interfaceInputFormList,
    '/api/inputFormDataList',
)
api.add_resource(
    interfaceGovernance,
    '/api/changeStatus',
)
api.add_resource(
    interfaceGovernanceBatch,
    '/api/changeStatusList',
)
# tbc: org admin, group checking
# workspace:sa, group checking
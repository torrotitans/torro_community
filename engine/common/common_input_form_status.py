class status:
    offline_flag = 0  #: using ldap
    # offline_flag = 1

    pending_approval = 0
    rejected = 1
    completed = 2
    in_porgress = 3
    approved = 4
    cancelled = 5
    failed = 6

    code = {pending_approval: 'pending approval', rejected: 'rejected', completed: 'completed',
            in_porgress: 'in porgress', approved: 'approved',
            cancelled: 'cancelled', failed: 'failed'}
    status_history_mapping = {
        pending_approval: [{'label': 'In Progress', 'operator': '', 'comment': '', 'time': None},
                           {'label': 'Completed', 'operator': '', 'comment': '', 'time': None}],
        rejected: [{'label': 'Rejected', 'operator': '', 'comment': '', 'time': None}],
        completed: [{'label': 'In Progress', 'operator': '', 'comment': '', 'time': None},
                    {'label': 'Completed', 'operator': '', 'comment': '', 'time': None}],
        in_porgress: [{'label': 'In Progress', 'operator': '', 'comment': '', 'time': None},
                      {'label': 'Completed', 'operator': '', 'comment': '', 'time': None}],
        approved: [{'label': 'In Progress', 'operator': '', 'comment': '', 'time': None},
                   {'label': 'Completed', 'operator': '', 'comment': '', 'time': None}],
        cancelled: [{'label': 'Cancelled', 'operator': '', 'comment': '', 'time': None}],
        failed: [{'label': 'Failed', 'operator': '', 'comment': '', 'time': None}],
    }

    system_execute_tasks = ['system_define_field', 'system_create_form', 'system_delete_form', 'system_update_form',
                            'system_create_tag', 'system_create_tag_template_form', 'system_add_new_usecase']

    db_operation_tasks = ['CreatePolicyTagsV1', 'system_create_form', 'system_update_form', 'CreateTagTemplate',
                          'ModifyTablePolicyTags', 'GrantRoleForPolicyTags',
                          'UpdateTagTemplate', 'DeleteTagTemplate', 'system_add_new_usecase', 'system_define_field',
                          'ModifyTableTags', 'GrantRoleForBQTable',
                          'system_create_tag', 'system_create_tag_template_form', 'ModifyTablePolicyTags',
                          'ModifyTableTags']

    system_form_id = {'usecase': 2, 'add_user': 1, 'data_access': 108, 'data_ob': 107, 'data_approval_tag_template': 419,
                      'tag_template': 104}
    system_form_field_id = {'data_access': {'project_id': 'u1',
                                            'location': 'u3',
                                            'dataset_id': 'u4',
                                            'table_id': 'u5',
                                            'field_id': 'u6'},
                            'data_ob': {'project_id': 'u1',
                                            'location': 'u2',
                                            'dataset_id': 'u3',
                                            'table_id': 'u4',
                                            'field_id': 'u5'},
                            'usecase': {
                                'usecase_name': 15,
                                'owner_group': 'u2',
                                'team_group': 'u3',
                                'service_account': 'u8',
                            }
                            }

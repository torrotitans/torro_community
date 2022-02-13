import requests
import json
from common.common_crypto import prpcrypt
from db.org.db_org_mgr import org_mgr


def system_approval(random_token, input_form_id, form_id, workspace_id, approval_order):

    airflow_url = org_mgr.get_airflow_url()
    token_json = {'input_form_id': input_form_id, 'form_id': form_id, 'approval_order': approval_order,
                  'workspace_id': workspace_id, 'token': random_token}
    print('airflow token_json:', token_json)
    print('airflow url:', airflow_url)
    token = prpcrypt.encrypt(json.dumps(token_json))
    payload = {'token': token, 'input_form_id': input_form_id, 'form_id': form_id, 'workspace_id': workspace_id}

    print('airflow payload:', payload)
    return True
    retry = 0
    while retry < 3:
        try:
            requests.post(airflow_url, json=payload, verify=False)
            return True
        except:
            retry += 1
    return False



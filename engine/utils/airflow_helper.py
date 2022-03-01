import requests
import json
from common.common_crypto import prpcrypt
from db.org.db_org_mgr import org_mgr
import logging

logger = logging.getLogger("main." + __name__)

def system_approval(random_token, input_form_id, form_id, workspace_id, approval_order):
    
    try:
        
        airflow_url = org_mgr.get_airflow_url()
        token_json = {'input_form_id': input_form_id, 'form_id': form_id, 'approval_order': approval_order,
                      'workspace_id': workspace_id, 'token': random_token}

        token = prpcrypt.encrypt(json.dumps(token_json))
        payload = {'token': token, 'input_form_id': input_form_id, 'form_id': form_id, 'workspace_id': workspace_id}

        logger.info('FN:system_approval airflow_url:{} payload:{}'.format(airflow_url,payload))
        # return True
        retry = 0
        while retry < 3:
            try:
                requests.post(airflow_url, data=payload, verify=False)
                return True
            except:
                retry += 1
        return False
    
    except:
        logger.info('FN:system_approval airflow_trigger:False')
        # If cant trigger airflow or airflow is not set, then ignore for next approver
        return True


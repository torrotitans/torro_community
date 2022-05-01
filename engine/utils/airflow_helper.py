import requests
import json
from common.common_crypto import prpcrypt
from db.org.db_org_mgr import org_mgr
import traceback
import logging

logger = logging.getLogger("main." + __name__)

def system_approval(random_token, input_form_id, form_id, workspace_id, approval_order):
    
    try:
        
        airflow_url = org_mgr.get_airflow_url()
        airflow_header = {'Content-Type': 'application/json'}
        token_json = {'input_form_id': input_form_id, 'form_id': form_id, 'approval_order': approval_order,
                      'workspace_id': workspace_id, 'token': random_token}

        token = prpcrypt.encrypt(json.dumps(token_json).replace('\\', '\\\\'))
        payload = {"conf":{'token': token, 'input_form_id': input_form_id, 'form_id': form_id, 'workspace_id': workspace_id}}
        payload = json.dumps(payload).replace('\\', '\\\\')

        # return True
        retry = 0
        while retry < 3:
            try:
                logger.info('FN:system_approval airflow_url:{} payload:{}'.format(airflow_url,payload))
                res = requests.post(airflow_url, data=payload, verify=False, headers=airflow_header)
                logger.info("FN:system_approval airflow_response_status_code:{} airflow_response_text:{}".format(res.status_code,res.text))
                
                if res.status_code == 200:
                    logger.info("FN:system_approval airflow_trigger_success:True")
                    return True
                else:
                    retry += 1    
                
            except Exception as e:
                logger.error("FN:system_approval error:{}".format(traceback.format_exc()))
                retry += 1
                
            logger.info("FN:system_approval airflow_trigger_success:False")
        return False
    
    except:
        logger.info('FN:system_approval airflow_trigger:False')
        # If cant trigger airflow or airflow is not set, then ignore for next approver
        return True


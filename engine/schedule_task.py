from api.gcp.interface_gcp_execute import interfaceGCPExecute
import logging

# Get the logger specified in the file
logger = logging.getLogger("main." + __name__)

def tasks_executor():
    # interface_gcp_execute = interfaceGCPExecute()
    # data = interface_gcp_execute.get()
    logger.debug('FN:tasks_executor keepAlive:True')
    
if __name__ == '__main__':
    tasks_executor()

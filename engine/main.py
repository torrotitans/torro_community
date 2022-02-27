#!/usr/bin/python
# -*- coding: UTF-8 -*
"""

"""

import os
# from flask_cors import CORS
from api import create_app
from config import configuration
from logging import config

logging.config.fileConfig(fname='log.conf', disable_existing_loggers=False)

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

# CORS(app, supports_credentials=True)
if __name__ == '__main__':
    host, port, debug = configuration.get_start_config()
    app.run(host=host, port=port, debug=eval(debug))


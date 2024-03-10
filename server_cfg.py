import os
import configparser
import datetime
from typing import Union
from pathlib import Path


def get_project_root() -> Path:
    return Path(__file__)

from constants import *

#
# LOAD INI FILE
#

config = configparser.ConfigParser()
PROJECT_PATH_ROOT = Path(__file__).parent
CONFIG_FILE_PATH = os.path.normpath(os.path.join(PROJECT_PATH_ROOT, CT_CONFIG_FILE_RELATIVE_PATH))
SQLITE_FILE_PATH = os.path.normpath(os.path.join(PROJECT_PATH_ROOT, CT_SQLITE_FILE_RELATIVE_PATH))

if os.path.isfile(CONFIG_FILE_PATH):
    config_file_path = CT_CONFIG_FILE_RELATIVE_PATH
else:
    raise NameError(f'Config ini file not found in {CT_CONFIG_FILE_RELATIVE_PATH}')

config.read(CONFIG_FILE_PATH)

def read_bool_str(value: Union[str, bool], default_value: bool):
    if isinstance(value,bool):
        return value
    elif isinstance(value,str):
        if default_value is True:
            return False if str(value).capitalize() == "False" else True
        else:
            return True if str(value).capitalize() == "True" else False
    else:
        raise TypeError('Unknown type to decode as boolean')
def getServerParam(param_name, param_ini_file_section, is_mandatory=True, default_value=None, possible_values=None,
                   auto_lower=True,is_bool=False):
    """
    Load a server param from venv or ini file
    :param param_name: name of the param to find in the environment variables or in the ini file
    :param param_ini_file_section: name of the ini file section where to find the param
    :param is_mandatory: Stop server if the param value is not found
    :param default_value: value to use when not mandatory and not found
    :param possible_values: set of allowed values in low case
    :param auto_lower: disable auto_lower if value is case-sensitive like password
    :return: (Lowered) param read value or default_value (can be None) if not found
    """
    # Use empty rather than None to raise error in case of None or empty mandatory value
    param_value = os.getenv(param_name, '')

    if param_value == '':
        try:
            param_value = config[param_ini_file_section].get(param_name, '')
        except:
            param_value = ''
    if auto_lower:
        param_value = param_value.lower()

    if param_value == '' and is_mandatory:
        # Mandatory but not found
        message = f"Undefined Mandatory Variable '{param_name}' USE ENVIRONMENT VARIABLE OR INI FILE IN " \
                  f"'{param_ini_file_section}' SECTION"
        general_logger.info(message)
        raise ValueError(message)
    elif is_mandatory and (possible_values is not None) and (param_value not in possible_values):
        # Mandatory but not in allowed values (including '')
        message = f"Unknown mandatory value for variable '{param_name}' USE ONE OF '{possible_values}'"
        general_logger.info(message)
        raise ValueError(message)
    elif (is_mandatory is False) and (param_value == ''):
        # Not mandatory and not found, use default value
        return default_value
    else:
        if possible_values is None:
            # No restriction for found value, return value
            if is_bool:
                return read_bool_str(value=param_value,default_value=default_value)
            else:
                return param_value
        elif param_value in possible_values:
            # Allowed value return value
            return param_value
        elif (param_value not in possible_values) and (is_mandatory is False):
            # Not allowed but not mandatory, use default value
            return default_value
        else:
            raise NameError("Coding missing case !")


#
# LOGGING ROUTERS
# from https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker/issues/19#issuecomment-620810957
#

import logging
from sys import stdout

# Define logger
general_logger = logging.getLogger(__name__)

general_logger.setLevel(logging.DEBUG)  # set logger level
logFormatter = logging.Formatter \
    ("CR-API-LOG %(asctime)-8s : %(levelname)-8s : %(message)s")
consoleHandler = logging.StreamHandler(stdout)  # set streamhandler to stdout
consoleHandler.setFormatter(logFormatter)
general_logger.addHandler(consoleHandler)
# os.environ['TZ']='W. Europe Standard Time'
from fastapi.logger import logger as fastapi_logger

gunicorn_error_logger = logging.getLogger("gunicorn.error")
gunicorn_logger = logging.getLogger("gunicorn")
uvicorn_access_logger = logging.getLogger("uvicorn.access")
loggers_level = getServerParam(param_name='CT_ENV_LOGGING_LEVEL',
                               param_ini_file_section='GENERAL',
                               is_mandatory=False,
                               default_value='INFO')

gunicorn_logger.addHandler(consoleHandler)
gunicorn_error_logger.addHandler(consoleHandler)
uvicorn_access_logger.addHandler(consoleHandler)

# GENERAL_SERVER_EXECUTION_MODE WILL DEFINE LOGS, SECURITY LEVELS AND ALSO DB CREDENTIALS
GENERAL_SERVER_EXECUTION_MODE = getServerParam(param_name=CT_ENV_EXECUTION_MODE,
                                               param_ini_file_section='GENERAL',
                                               is_mandatory=True,
                                               possible_values=CT_ENV_EXECUTION_MODES_LIST)

APP_TITLE = getServerParam(param_name=CT_ENV_APP_TITLE,
                           param_ini_file_section='GENERAL',
                           is_mandatory=False,
                           default_value='UN APP',
                           auto_lower=False)

API_TITLE = getServerParam(param_name=CT_ENV_API_TITLE,
                           param_ini_file_section='GENERAL',
                           is_mandatory=False,
                           default_value=f"{APP_TITLE} API",
                           auto_lower=False)


######################################################################################################################
# GET CONFIGURATION VARIABLES DEPENDING ON THE EXECUTION MODE
######################################################################################################################
def getPwd(execution_mode, keys_dict=CT_DB_USERPWD_KEYS_DICT):
    # Password is either in the system environment variables, in the ini file or in an attached pwd file
    key = keys_dict[execution_mode]
    pwd = getServerParam(param_name=key,
                         param_ini_file_section='DB',
                         is_mandatory=False,
                         default_value='',
                         auto_lower=False)

    if pwd is None:
        # check if file is present
        if not os.path.isfile(PWD_FILE_PATH):
            general_logger.info(f"Could not find password file '{PWD_FILE_PATH}'")
        else:
            try:
                with open(PWD_FILE_PATH, "r") as pwd_file:
                    pwd = pwd_file.read()
                    pwd_file.close()
            except:
                general_logger.info(f"Could find but not read password file '{PWD_FILE_PATH}'")
    return pwd


def getUsername(execution_mode):
    key = CT_DB_USERNAME_KEYS_DICT[execution_mode]
    user = getServerParam(param_name=key,
                          param_ini_file_section='DB',
                          is_mandatory=False,
                          default_value='')
    return user


def getHostname(execution_mode):
    key = CT_DB_HOSTNAME_KEYS_DICT[execution_mode]
    host = getServerParam(param_name=key,
                          param_ini_file_section='DB',
                          default_value='',
                          is_mandatory=False)
    return host


API_DB_PWD = getPwd(execution_mode=GENERAL_SERVER_EXECUTION_MODE)
API_DB_HOSTNAME = getHostname(execution_mode=GENERAL_SERVER_EXECUTION_MODE)
API_DB_USERNAME = getUsername(execution_mode=GENERAL_SERVER_EXECUTION_MODE)

# AUTHENTICATION_MODE DEFINE THE METHOD USED TO AUTHENTICATE USER IDENTITY IF NEEDED
AUTHENTICATION_MODE = getServerParam(param_name=CT_ENV_AUTHENTICATION_MODE,
                                     param_ini_file_section='GENERAL',
                                     is_mandatory=False,
                                     possible_values=CT_ENV_AUTHENTICATION_MODES_LIST,
                                     default_value=CT_ENV_AUTHENTICATION_MODE_FULL)

# SIMPLE AUTHENTICATION MODE IS FORBIDDEN IN PRODUCTION MODE
if (AUTHENTICATION_MODE.lower() == CT_ENV_AUTHENTICATION_MODE_SIMPLE) \
        and (GENERAL_SERVER_EXECUTION_MODE == CT_EXECUTION_MODE_PRODUCTION):
    AUTHENTICATION_MODE = CT_ENV_AUTHENTICATION_MODE_FULL
    general_logger.critical(
        f"{CT_ENV_AUTHENTICATION_MODE_SIMPLE} authentication mode is forbidden in execution mode {CT_EXECUTION_MODE_PRODUCTION}, "
        f"switch to {CT_ENV_AUTHENTICATION_MODE_FULL} authentication mode")

# SECRET_KEY IS THE KEY USED TO DE/CODE TOKEN
SECRET_KEY = getServerParam(param_name=CT_ENV_SECRET_KEY,
                            param_ini_file_section='GENERAL',
                            is_mandatory=True)

# SERVER PARAMS: HOST NAME AND PORT
SERVER_PORT = getServerParam(param_name=CT_ENV_DEV_PORT,
                             param_ini_file_section='NETWORK',
                             is_mandatory=False,
                             default_value='8080')
SERVER_PORT = int(SERVER_PORT)

SERVER_HOSTNAME = getServerParam(param_name=CT_ENV_HOSTNAME,
                                 param_ini_file_section='NETWORK',
                                 is_mandatory=False,
                                 default_value='localhost')

# GLOBAL LOGGING LEVEL
LOGGING_LEVEL = getServerParam(param_name=CT_ENV_LOGGING_LEVEL,
                               param_ini_file_section='GENERAL',
                               is_mandatory=False,
                               possible_values={'debug', 'info', 'warning', 'error', 'critical'},
                               default_value='INFO')

API_UNITEID_GENERIC_PASSWD = getServerParam(param_name=CT_ENV_UNITEID_GENERIC_PASSWD,
                                            param_ini_file_section='GENERAL',
                                            is_mandatory=True,
                                            auto_lower=False)

API_LOGGING_LEVEL = CT_API_LOGGING_LEVELS[LOGGING_LEVEL.lower()]

# DB_ENGINE_ECHO DEFINE THE VERBOSITY OF THE DATABASE ENGINE, IF TRUE, DB MESSAGES WILL BE PROMPTED
DB_ENGINE_ECHO = getServerParam(param_name=CT_ENV_DB_ENGINE_ECHO,
                                param_ini_file_section='DB',
                                is_mandatory=False,
                                is_bool=True,
                                default_value=False)

# DB_ENGINE_CREATE_ALL define if CREATE ... IF NOT EXISTS statements at API init
DB_ENGINE_CREATE_ALL = getServerParam(param_name=CT_ENV_DB_ENGINE_CREATE_ALL,
                                      param_ini_file_section='DB',
                                      is_mandatory=False,
                                      is_bool=True,
                                      default_value=True)

API_DB_DRIVER = getServerParam(param_name=CT_ENV_DB_DRIVER,
                               param_ini_file_section='DB',
                               is_mandatory=False,
                               default_value="ODBC Driver 17 for SQL Server",
                               auto_lower=False)

gunicorn_logger.setLevel(API_LOGGING_LEVEL)
general_logger.setLevel(API_LOGGING_LEVEL)
fastapi_logger.setLevel(API_LOGGING_LEVEL)
gunicorn_error_logger.setLevel(API_LOGGING_LEVEL)
uvicorn_access_logger.handlers = gunicorn_error_logger.handlers
fastapi_logger.handlers = gunicorn_error_logger.handlers

message = "SERVER IS LAUNCHING {} EXECUTION MODE".format(
    GENERAL_SERVER_EXECUTION_MODE.upper())
general_logger.info(message)
message = "AUTHENTICATION MODE {}".format(AUTHENTICATION_MODE.upper())
general_logger.info(message)
message = "DB HOSTNAME {}".format(API_DB_HOSTNAME)
general_logger.info(message)
message = "DB USERNAME {}".format(API_DB_USERNAME)
general_logger.info(message)
message = "API SERVER LOCAL HOSTNAME {}".format(SERVER_HOSTNAME)
general_logger.info(message)
message = "API SERVER LOCAL PORT {}".format(SERVER_PORT)
general_logger.info(message)
API_DB_IS_CONNECTED = False
SERVER_START_TIME = str(datetime.datetime.now().isoformat())

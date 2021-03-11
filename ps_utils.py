from configparser import ConfigParser
import os
from pathlib import Path
import logging


def get_credentials(section_name, db_config_file_name=None):
    """get_credentials for PostgreSQL/Timeseries database"""
    config = ConfigParser()

    if None == db_config_file_name:
        db_config_file_name = ".pg_service.conf"

    # Note: ${HOME}/.pg_service.conf ... if DB2
    # below is portable for *both* Win and Linux!
    cred_file = Path("{}/{}".format(os.environ.get('HOME'), db_config_file_name))
    assert os.path.isfile(cred_file), "error can't read credentials file ... {}".format(cred_file)
    config.read(cred_file)

    host = config.get(section_name, 'host')
    port = config.get(section_name, 'port')
    dbname = config.get(section_name, 'dbname')
    uid = config.get(section_name, 'user')
    pw = config.get(section_name, 'password')

    logging.info("Reading credentials from: {}, using section: {}".format(cred_file, section_name))

    return host, port, dbname, uid, pw

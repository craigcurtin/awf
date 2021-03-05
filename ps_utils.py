from configparser import ConfigParser
import os
from pathlib import Path
import logging


def get_credentials(section_name):
    """get_credentials for PostgreSQL/Timeseries database"""
    config = ConfigParser()

    # Note: ${HOME}/.pg_service.conf
    # below is portable for *both* Win and Linux!
    cred_file = Path("{}/.pg_service.conf".format(os.environ.get('HOME')))
    assert os.path.isfile(cred_file), "error can't read credentials file ... {}".format(cred_file)
    config.read(cred_file)

    host = config.get(section_name, 'host')
    port = config.get(section_name, 'port')
    dbname = config.get(section_name, 'dbname')
    user = config.get(section_name, 'user')
    pw = config.get(section_name, 'password')

    logging.info("Reading credentials from: {}, using section: {}".format(cred_file, section_name))

    return host, port, dbname, user, pw

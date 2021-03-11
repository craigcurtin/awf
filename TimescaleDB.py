import pandas as pd
from sqlalchemy import create_engine

import logging
import psycopg2
from ps_logger import setup_logger
from ps_utils import get_credentials


class TimescaleDB(object):
    """TimescaleDB connection class for PostgreSQL Timeseries instance"""
    def __init__(self, config_tag):
        """create connection to Timescale DB ..."""
        # choose the database to use
        self.config_tag = config_tag
        self.host, self.port, self.dbname, self.user, self.pw = get_credentials(config_tag)
        try:
            # construct an engine connection string
            self.engine_string = "postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}".format(
                host=self.host,
                port=self.port,
                database=self.dbname,
                user=self.user,
                password=self.pw,
            )
            # create sqlalchemy engine
            self.engine = create_engine(self.engine_string)
            # assert (self.engine is None), "Cannot create PostgreSQL connection!!"
        except (IOError, EOFError) as ex:
            logging.exception("Exception: create PostgreSQL connection!!")
            raise
        else:
            masked_login_string = "postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}".format(
                host=self.host,
                port=self.port,
                database=self.dbname,
                user="who is he and what has he done to you?",
                password="No, he don't sell popcorn",
            )
            logging.debug(masked_login_string)

    def validate_db_connect(self):
        """test if connected, reconnect if needed, seamlessly"""
        if self.engine is None:
            # reopen sqlalchemy engine
            self.engine = create_engine(self.engine_string)
            # assert (self.engine is None), "Cannot create PostgreSQL connection!!"
            logging.debug("Reconnecting to PostgreSQL")
        else:
            logging.debug("Connected to PostgreSQL")
        return

    def execute(self, sql_string):
        """execute(sql_string) : return the record_set matching the criteria requested"""
        data_set = []

        # try:
        with self.engine.connect() as con:
            record_set = con.execute(sql_string)
            # logging.debug("Query returned: {} records".format(len(record_set)))
            # if we do client side filtering .... here is where we do it ....
            for record in record_set:
                data_set.append(record)

        # except (IOError, EOFError) as ex:
        #     logging.exception("Error: can't find file or read data")
        #     raise

        return data_set

    def read_table(self, table_name):
        pass


if __name__ == '__main__':
    setup_logger('Timescale_DB', logging.DEBUG)
    config_tag = 'fwa'
    timescale_db = TimescaleDB(config_tag)

    max_records = 10
    base_record = 0
    while True:
        sql_string = 'SELECT * FROM claims  LIMIT {} OFFSET {};'.format(
            max_records,
            base_record)
        logging.info("SQL: [{}]".format(sql_string))
        timescale_db.validate_db_connect()
        records = timescale_db.execute(sql_string)
        for record in records:
            print(record)
        base_record = base_record + max_records

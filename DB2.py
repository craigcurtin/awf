import logging
import pandas as pd
from ps_utils import get_credentials

# import ibm_db

# gouged this class from @Jay Ko ... thanks dude!

class DB2(object):
    def __init__(self, config_tag):
        """"""
        db2_config_file_name = '.db2dsdriver.cfg'

        # choose the database to use
        self.config_tag = config_tag
        self.protocol = 'tcp'
        self.host, self.port, self.dbname, self.uid, self.pw = get_credentials(config_tag, db2_config_file_name)

        self.conn = None
        self.cursor = None
        self.ibm_conn = None
        # call the method to really do the connection ...
        self.ibm_connect()

    def ibm_connect(self):
        try:
            if False:
                self.ibm_conn = ibm_db.connect(
                    "DATABASE={database};HOSTNAME={hostname};PORT={port};PROTOCOL={protocol};UID={uid};PWD={pw}".format(
                        database=self.dbdsn, hostname=self.configuration_dict["DBHostName"], port=self.configuration_dict["Port"],
                        protocol=self.configuration_dict["Protocol"], uid=self.uid, pw=self.pw
                    ), "", ""
                )
                return self.ibm_conn
            else:
                log_db2_conn = "DB2: DATABASE={database};HOSTNAME={hostname};PORT={port};PROTOCOL={protocol};UID={uid};PWD={pw}".format(
                                    database=self.dbname,
                                    hostname="may_the_force_be_with_you",
                                    port="8675309",
                                    protocol=self.protocol,
                                    uid="some luser",
                                    pw="ain't gonna tell",
                    )
                logging.info(log_db2_conn)
        except Exception as ex:
            logging.exception("Exception: {} cannot connect to {}".format(ex, self.dbname))
            raise RuntimeError("Exception: {} cannot connect to {}".format(ex, self.dbname)) from ex

    def connect(self):
        try:
            self.conn = pyodbc.connect('DSN={}; UID={}; PWD={}'.format(
                self.dbdsn, self.uid, self.pwd))
            logging.debug('Connected to {}'.format(self.dbdsn))
            return self.conn
        except Exception as ex:
            ex_message = "Exception: {} cannot connect to {}".format(ex, self.dbdsn)
            print(ex_message)
            logging.exception(ex_message)
            raise RuntimeError(ex_message) from ex

    def get_cursor(self):
        try:
            self.cursor = self.conn.cursor()
            logging.debug("Returning Cursor")
            return self.cursor
        except Exception as ex:
            ex_message = "Exception: {} cannot get cursor".format(ex)
            logging.exception(ex_message)
            raise RuntimeError(ex_message) from ex

    # This will be implemented in data_table
    def execute(self, sql):
        try:
            sql_query = pd.read_sql_query(sql,self.conn)
            #self.cursor.execute(sql)
            logging.debug("Executing SQL Query")
            return sql_query
        except Exception as ex:
            ex_message = "Exception: {} cannot execute sql query".format(ex)
            logging.exception(ex_message)
            raise RuntimeError(ex_message) from ex

    def fetch_one(self):
        return self.cursor.fetchone()

    def fetch_all(self):
        return self.cursor.fetchall()

    def insert(self, sql):
        try:
            self.cursor.execute(sql)
            logging.debug("Executing Insert SQL Query")
        except Exception as ex:
            ex_message = "Exception: {} cannot Insert into the Table".format(ex)
            logging.exception(ex_message)
            raise RuntimeError(ex_message) from ex

    def update(self, sql):
        try:
            self.cursor.execute(sql)
            logging.debug("Executing Update SQL Query")
        except Exception as ex:
            ex_message = "Exception: {} cannot Update Table".format(ex)
            logging.exception(ex_message)
            raise RuntimeError(ex_message) from ex

    def upsert(self, inssql, updsql):
        try:
            self.cursor.execute(inssql)
            logging.debug(("Executing Insert in upsert mode"))
        except Exception as ex:
            if ex.args[0] == '23505':
                try:
                    self.cursor.execute(updsql)
                    logging.debug("Executing update in upsert mode")
                except Exception as ex:
                    ex_message = "Exception: {} cannot Update Table in upser mode".format(ex)
                    logging.exception(ex_message)
                    raise RuntimeError(ex_message) from ex
            else:
                ex_message = "Exception: {} cannot Insert Table ".format(ex)
                logging.exception(ex_message)
                raise RuntimeError(ex_message) from ex

    def commit(self):
        try:
            self.cursor.commit()
            logging.debug("Committing the Records")
        except Exception as ex:
            ex_message = "Exception: {} cannot Commit Records".format(ex)
            logging.exception(ex_message)
            raise RuntimeError(ex_message) from ex


    def close_conn(self):
        try:
            logging.debug("Close DB connection {}".format(self.dbdsn))
            self.conn.close()
        except Exception as ex:
            ex_message = "Exception: {} closing DB2 connection".format(ex)
            logging.exception(ex_message)
            raise RuntimeError(ex_message) from ex

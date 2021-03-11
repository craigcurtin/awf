import pandas as pd
import argparse
import sys
import logging
from ps_logger import setup_logger
from TimescaleDB import TimescaleDB
from DB2 import DB2
from ps_utils import get_credentials

def main(tsdb_config_tag, db2_config_tag, max_records):
    """using credentials from config_tags (DB2+TSDB), starting at record:#base_record, get: #max_records, return data_set"""

    try:
        timescale_db = TimescaleDB(tsdb_config_tag)
        datawarehouse_db2 = DB2(db2_config_tag)
        logging.debug('DB info: ts:{}, db2:{}'.format(timescale_db, datawarehouse_db2))
    except:
        logging.exception("DB exception: {}".format(sys.exc_info()[0]))

    number_of_fetches=5
    base_record=0

    while number_of_fetches > 0 :
        sql_string = 'SELECT * FROM claims  LIMIT {max_records} OFFSET {base_record};'.format(
                                            max_records=max_records,
                                            base_record=base_record)
        logging.debug("SQL: [{}]".format(sql_string))
        timescale_db.validate_db_connect()
        records = timescale_db.execute(sql_string)
        for record in records:
            print(record)
        base_record = base_record + max_records
        number_of_fetches -= 1




# possible arguments to use
# --config_tag fwa --max_records 100
# --config_tag fwa --max_records 1000
# --number_of_fetches 5
# --config_tag fwa --max_records 10000 --log_level INFO

if __name__ == '__main__':
    app_name = 'Measure_Engine'
    parser = argparse.ArgumentParser(description=app_name)
    parser.add_argument('--tsdb_config_tag', action='store', dest='tsdb_config_tag', type=str, help='config_tag')
    parser.add_argument('--db2_config_tag', action='store', dest='db2_config_tag', type=str, help='config_tag')

    parser.add_argument('--max_records', action='store', dest='max_records', type=int, help='max_records')


    parser.add_argument('--log_level', action='store', dest='log_level', type=int,
                        default=logging.DEBUG, help='log_level (int value)')

    args = parser.parse_args()

    if args.db2_config_tag is None:
        args.db2_config_tag = 'dbt_repts'
    if args.tsdb_config_tag is None:
        args.tsdb_config_tag = 'fwa'
    if args.max_records is None:
        args.max_records = 50

    setup_logger(app_name, args.log_level)

    try:
        main(args.tsdb_config_tag, args.db2_config_tag, args.max_records)
        logging.info("Normal Termination")
        sys.exit(0)
    except (Exception, EOFError) as ex:
        logging.exception("uh, oh .... we got an exception!!")
        raise


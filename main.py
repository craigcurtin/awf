import pandas as pd
import argparse
import sys
import logging
from ps_logger import setup_logger
from TimescaleDB import TimescaleDB


def main(config_tag, base_record, max_records, number_of_fetches):
    """using credentials from config_tag, starting at record:#base_record, get: #max_records, return data_set"""

    timescale_db = TimescaleDB(config_tag)

    while number_of_fetches > 0:
        sql_string = 'SELECT * from public.fw9   LIMIT {} OFFSET {};'.format(
            max_records,
            base_record)
        logging.info("SQL: [{}]".format(sql_string))
        try:
            timescale_db.validate_db_connect()
            records = timescale_db.execute(sql_string)
        except Exception as ex:
            logging.info("Exception from TS_DB execute [{}] sql".format(sql_string))
            raise ex

        for record in records:
            print(record)
        base_record = base_record + max_records
        number_of_fetches -= 1


# possible arguments to use
# --config_tag fwa --base_record 23 --max_records 100
# --config_tag fwa --base_record 42 --max_records 1000
# --number_of_fetches 5
# --config_tag fwa --base_record 42 --max_records 10000 --log_level INFO
# --config_tag fwa --base_record 42 --max_records 10000 --log_directory /tmp --log_level INFO

if __name__ == '__main__':
    app_name = 'TimescaleDB'
    print("hi ")
    parser = argparse.ArgumentParser(description=app_name)
    parser.add_argument('--config_tag', action='store', dest='config_tag', type=str, help='config_tag')
    parser.add_argument('--base_record', action='store', dest='base_record', type=int, help='base_record')
    parser.add_argument('--max_records', action='store', dest='max_records', type=int, help='max_records')
    parser.add_argument('--number_of_fetches', action='store', dest='number_of_fetches', type=int,
                        help='number_of_fetches')
    parser.add_argument('--log_directory', action='store', dest='log_directory', type=str,
                        default='./', help='log_directory (str value)')

    parser.add_argument('--log_level', action='store', dest='log_level', type=int,
                        default=logging.DEBUG, help='log_level (int value)')
    print("hi befdore ")
    args = parser.parse_args()
    print("hi befdore ")
    if args.log_directory is None:
        args.log_directory = './'
    if args.config_tag is None:
        args.config_tag = 'fwa'
    if args.base_record is None:
        args.base_record = 0
    if args.max_records is None:
        args.max_records = 50
    if args.number_of_fetches is None:
        args.number_of_fetches = 10
    if args.log_level is None:
        args.log_level = logging.DEBUG
    print("hi befdore ")
    setup_logger(app_name, args.log_directory, args.log_level)

    try:
        main(args.config_tag, args.base_record, args.max_records, args.number_of_fetches)
        logging.info("Normal Termination")
        sys.exit(0)
    except (Exception, EOFError) as ex:
        logging.exception("uh, oh .... we got an exception!!")
        raise

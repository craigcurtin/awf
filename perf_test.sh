#!/usr/bin/env bash

# --config_tag fwa --base_record 42 --max_records 1000
# --number_of_fetches 5
# --config_tag fwa --base_record 42 --max_records 10000 --log_level INFO

SAVE_TIME_ITERATION="/tmp/timer$$"

# we don't care if it is not present
rm -rf ${SAVE_TIME_ITERATION} 2> /dev/null


source venv/bin/activate

echo "main.py --config_tag fwa --base_record 0  --max_records 10 --number_of_fetches 5000" 
# redirect stdout to /dev/null so we don't count internal i/o in metrics
time python3 main.py  --config_tag fwa --base_record 0  --max_records 10 	--number_of_fetches 5000 1> /dev/null | tee -a ${SAVE_TIME_ITERATION}

echo "main.py --config_tag fwa --base_record 0  --max_records 100 --number_of_fetches 500" 
# redirect stdout to /dev/null so we don't count internal i/o in metrics
time python3 main.py  --config_tag fwa --base_record 0  --max_records 100 	--number_of_fetches 500 1> /dev/null | tee -a ${SAVE_TIME_ITERATION}

echo "main.py --config_tag fwa --base_record 0  --max_records 1000 --number_of_fetches 50" 
# redirect stdout to /dev/null so we don't count internal i/o in metrics
time python3 main.py  --config_tag fwa --base_record 0  --max_records 1000 	--number_of_fetches 50 	1> /dev/null | tee -a ${SAVE_TIME_ITERATION}

echo "main.py --config_tag fwa --base_record 0  --max_records 1000 --number_of_fetches 5" 
# redirect stdout to /dev/null so we don't count internal i/o in metrics
time python3 main.py  --config_tag fwa --base_record 0  --max_records 10000 	--number_of_fetches 5 	1> /dev/null | tee -a ${SAVE_TIME_ITERATION}l

cat ${SAVE_TIME_ITERATION}

rm ${SAVE_TIME_ITERATION}


FROM python:3.8-alpine

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt --index-url https://artifacts-scm.dstcorp.net/artifactory/api/pypi/pypi-repos/simple

CMD ["python",  "/app/main.py", "--config_tag",  "fwa",  "--base_record 42",  "--max_records 10000",  "--log_directory /tmp", " --log_level INFO" ]

FROM python:3.7

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --upgrade -r /code/requirements.txt

COPY . /code

ENV ORACLE_USER="SYS"
ENV ORACLE_PASSWORD="example"
ENV ORACLE_URL="oracle:1521/xepdb1"
ENV ORACLE_SCHEMA="CLUB"

ENV MYSQL_USER="root"
ENV MYSQL_PASSWORD="example"
ENV MYSQL_HOST="service"
ENV MYSQL_DATABSE="mysql"

ENV TABID="9999"

CMD ["sh", "loop.sh"]

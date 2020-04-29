#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset



export CELERY_BROKER_URL="${REDIS_URL}"

if [ -z "${POSTGRES_USER}" ]; then
    base_postgres_image_default_user='postgres'
    export POSTGRES_USER="${base_postgres_image_default_user}"
fi
export DATABASE_URL="postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"

if [ -z "${MYSQL_USER}" ]; then
    base_mysql_image_default_user='root'
    export MYSQL_USER="${base_mysql_image_default_user}"
fi
export JOBPLANET_DATABASE_URL="mysql://${MYSQL_USER}:${MYSQL_PASSWORD}@${MYSQL_HOST}:${MYSQL_PORT}/${MYSQL_DB}"

postgres_ready() {
python << END
import sys
import psycopg2

try:
    psycopg2.connect(
        dbname="${POSTGRES_DB}",
        user="${POSTGRES_USER}",
        password="${POSTGRES_PASSWORD}",
        host="${POSTGRES_HOST}",
        port="${POSTGRES_PORT}",
    )
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)

END
}
mysql_ready() {
python << END
import sys
import MySQLdb

try:
    MySQLdb.connect(
        db="${MYSQL_DB}",
        user="${MYSQL_USER}",
        passwd="${MYSQL_PASSWORD}",
        host="${MYSQL_HOST}",
        port=int("${MYSQL_PORT}"),
    )
except MySQLdb.OperationalError:
  sys.exit(-1)
sys.exit(0)

END
}

# until postgres_ready; do
#   >&2 echo 'Waiting for PostgreSQL to become available...'
#   sleep 1
# done
# >&2 echo 'PostgreSQL is available'

until mysql_ready; do
  >&2 echo 'Waiting for MySQL to become available...'
  sleep 1
done
>&2 echo 'MySQL is available'

exec "$@"

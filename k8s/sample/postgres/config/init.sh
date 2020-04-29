#!/bin/bash
set -e

if [[ ${HOSTNAME} == 'postgres-0' ]]; then
  cp /etc/master.conf /etc/master_or_replica.conf

  psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
  	CREATE ROLE replication WITH REPLICATION PASSWORD '$REPLICATION_PASSWORD' LOGIN
  EOSQL

else
  cp /etc/replica.conf /etc/master_or_replica.conf

  echo "Running pg_basebackup to catch up replication server...";
  pg_basebackup -R -h postgres -D "$PGDATA" -P -U replication; 
  chown -R postgres:postgres $PGDATA;
fi

#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

/cloud_sql_proxy --dir=/cloudsql \
	-instances='${GCP_PRJECT_ID}:${GCP_REGION}:{$GCP_CLOUDSQL_INSTANCE}=tcp:{$POSTGRES_PORT}' \
	-credential_file=/secrets/cloudsql/cloudsql-credentials.json
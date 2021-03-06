#!/bin/bash

set -o errexit
set -o nounset

/config/create-ssh-tunnel.sh

celery flower \
    --app=config.celery_app \
    --url_prefix=flower \
    --broker="${CELERY_BROKER_URL}" \
    --basic_auth="${CELERY_FLOWER_USER}:${CELERY_FLOWER_PASSWORD}"

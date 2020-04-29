#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

/config/create-ssh-tunnel.sh

celery -A config.celery_app worker -l INFO

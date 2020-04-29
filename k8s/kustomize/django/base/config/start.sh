#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

/config/create-ssh-tunnel.sh

python manage.py migrate
python manage.py collectstatic --noinput
# python manage.py runserver 0.0.0.0:5000 --settings=config.settings.production

/usr/local/bin/gunicorn config.wsgi -b 0.0.0.0:5000 \
	--chdir=/app \
	--log-level=debug \
	--access-logfile=-
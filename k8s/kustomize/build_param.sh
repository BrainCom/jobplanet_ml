cp -r ./.env/.dev/ ./django/overlays/dev/
cp -r ./.env/.prod/ ./django/overlays/prod/
cp -r ./.env/.dev/ ./celery/overlays/dev/
cp -r ./.env/.prod/ ./celery/overlays/prod/
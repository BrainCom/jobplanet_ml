import os
from .base import *  # noqa
from .base import env
from google.oauth2 import service_account


# GENERAL
# ------------------------------------------------------------------------------
DEBUG = True
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="B2T66Tgb3uLiZHpYi9ksyzFhduLTmY7VbwvLcnzjMnwq9g34UzWy8mCy2isLSChD",
)
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]

# CACHES
# ------------------------------------------------------------------------------
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

# EMAIL
# ------------------------------------------------------------------------------
# EMAIL_BACKEND = env(
#     "DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend"
# )
DEFAULT_FROM_EMAIL = env(
    "DJANGO_DEFAULT_FROM_EMAIL", default="job_recommender <noreply@braincommerce.com>"
)
SERVER_EMAIL = env("DJANGO_SERVER_EMAIL", default=DEFAULT_FROM_EMAIL)
EMAIL_SUBJECT_PREFIX = env(
    "DJANGO_EMAIL_SUBJECT_PREFIX", default="[job_recommender]"
)
# Anymail
# ------------------------------------------------------------------------------
INSTALLED_APPS += ["anymail"]
EMAIL_BACKEND = "anymail.backends.sendgrid.EmailBackend"
ANYMAIL = {
    "SENDGRID_API_KEY": env("SENDGRID_API_KEY"),
    "SENDGRID_GENERATE_MESSAGE_ID": env("SENDGRID_GENERATE_MESSAGE_ID"),
    "SENDGRID_MERGE_FIELD_FORMAT": env("SENDGRID_MERGE_FIELD_FORMAT"),
    "SENDGRID_API_URL": env("SENDGRID_API_URL", default="https://api.sendgrid.com/v3/"),
}

# django-debug-toolbar
# ------------------------------------------------------------------------------
INSTALLED_APPS += ["debug_toolbar"]  # noqa F405
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]  # noqa F405
DEBUG_TOOLBAR_CONFIG = {
    "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
    "SHOW_TEMPLATE_CONTEXT": True,
}
INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]
if env("USE_DOCKER") == "yes":
    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS += [ip[:-1] + "1" for ip in ips]

# django-extensions
# ------------------------------------------------------------------------------
INSTALLED_APPS += ["django_extensions"]  # noqa F405
# Celery
# ------------------------------------------------------------------------------

CELERY_TASK_EAGER_PROPAGATES = True
# CELERY_TASK_ALWAYS_EAGER = True


# Your stuff...
# ------------------------------------------------------------------------------

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.sqlite3',
       'NAME': os.path.join(ROOT_DIR, 'db.sqlite3'),
   },
   'jobplanet': {
       'ENGINE': 'django.db.backends.mysql',
       'NAME': env('MYSQL_DB'),
       'USER': env('MYSQL_USER'),
       'PASSWORD': env('MYSQL_PASSWORD'),
       'HOST': env('MYSQL_HOST'),
       'PORT': env('MYSQL_PORT')
   }
}
# DATABASES = {
#     'default' : {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'job_recommender',              
#         'USER': 'root',                      
#         'PASSWORD': 'root',              
#         'HOST': 'localhost',                 
#         'PORT': '3306',                      
#     }
# }

# STORAGES
# ------------------------------------------------------------------------------
# if unset, falls back to the default inferred from the env(GOOGLE_APPLICATION_CREDENTIALS)
INSTALLED_APPS += ["storages"]
GS_CREDENTIALS_PATH = env("DJANGO_GCP_STORAGE_CREDENTIALS_PATH", default="/secrets/gcp/storage-credentials.json")
GS_CREDENTIALS = service_account.Credentials.from_service_account_file(GS_CREDENTIALS_PATH)
GS_BUCKET_NAME = env("DJANGO_GCP_STORAGE_BUCKET_NAME")
GS_DEFAULT_ACL = "publicRead"
# STATIC
# ------------------------
STATICFILES_STORAGE = "job_recommender.utils.storages.StaticRootGoogleCloudStorage"
COLLECTFAST_STRATEGY = "collectfast.strategies.gcloud.GoogleCloudStrategy"
STATIC_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/static/"
# MEDIA
# ------------------------------------------------------------------------------
DEFAULT_FILE_STORAGE = "job_recommender.utils.storages.MediaRootGoogleCloudStorage"
MEDIA_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/media/"
from storages.backends.gcloud import GoogleCloudStorage

#GCS acl: https://cloud.google.com/storage/docs/access-control/lists#predefined-acl
class StaticRootGoogleCloudStorage(GoogleCloudStorage):
    location = "static"
    default_acl = "publicRead"


class MediaRootGoogleCloudStorage(GoogleCloudStorage):
    location = "media"
    default_acl = "private"
    file_overwrite = False

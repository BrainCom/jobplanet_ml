from django.conf import settings
from django.contrib.auth.hashers import make_password

def users_migration(apps, schema_editor):
    super_users = settings.DEFAULT_USERS['super']
    api_users = settings.DEFAULT_USERS['api']
    arr = []

    User = apps.get_model('users', 'User')
    usernames = User.objects.values_list('username', flat=True)
    if super_users:
        for name in super_users.split(','):
            if name in usernames:
                continue

            arr.append(User(is_superuser=1,
                            username=name, 
                            password=make_password(name)))

    if api_users:
        for name in api_users.split(','):
            if name in usernames:
                continue

            arr.append(User(username=name, 
                            password=make_password(name)))

    User.objects.bulk_create(arr)

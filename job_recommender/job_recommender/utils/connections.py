from django.conf import settings
import prestodb
import psycopg2
import sqlite3

class DBConnection(object):

    def __init__(self, db='default'):
        self.db = db

        if db == 'default':
            if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.postgresql':
                self.engine = 'postgresql'
                self.conn = psycopg2.connect(
                        dbname=settings.DATABASES['default']['NAME'],
                        user=settings.DATABASES['default']['USER'],
                        password=settings.DATABASES['default']['PASSWORD'],
                    )
            elif settings.DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3':
                self.engine = 'sqlite3'
                self.conn = sqlite3.connect(settings.DATABASES['default']['NAME'])
            else:
                raise NotImplementedError

        elif db == 'jobplanet':
            raise NotImplementedError
            
        elif db == 'presto':
            self.engine = 'presto'
            self.conn=prestodb.dbapi.connect(
                host=settings.PRESTO['host'],
                port=settings.PRESTO['port'],
                user=settings.PRESTO['user'],
                catalog=settings.PRESTO['catalog'],
                schema=settings.PRESTO['schema']
            )
        else:
            raise NotImplementedError

    @property
    def connector(self):
        if self.engine == 'postgresql':
            return psycopg2
        elif self.engine == 'sqlite3':
            return sqlite3
        elif self.engine == 'presto':
            return prestodb
        else:
            return None

    @property
    def cursor(self):
        return self.conn.cursor()
from django.conf import settings

class JobplanetRouter:
    db_list = settings.DATABASES.keys()
    route_app_labels = {'jobplanet'}

    def db_for_read(self,model,**hints):
        if model._meta.app_label in self.route_app_labels:
            return 'jobplanet'
         
        return None

    def db_for_write(self,model,**hints):
        if model._meta.app_label in self.route_app_labels:
            return "non-exist db table name to raise error"

        return None

    def allow_relation(self,obj1,obj2,**hints):
        if obj1._state.db in self.db_list and obj2._state.db in self.db_list:
            return True

        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            return False

        return True
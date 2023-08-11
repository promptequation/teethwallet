class PersonalDBRouter:
    personal_models = {'personalinfomodel'}  # доработать списки

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if model_name in self.personal_models:
            allow = (db == 'personal')
            return allow
        return None

    def db_for_read(self, model, **hints):
        if model._meta.model_name in self.personal_models:
            return 'personal'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.model_name in self.personal_models:
            return 'personal'
        return None

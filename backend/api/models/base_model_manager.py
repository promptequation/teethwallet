from django.db import models


class BaseModelManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().exclude(is_deleted=True, is_active=False)

    def all(self):
        return self.get_queryset().exclude(is_deleted=True, is_active=False)

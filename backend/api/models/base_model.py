import datetime
from crequest.middleware import CrequestMiddleware
from django.db import models, transaction
from .base_model_manager import BaseModelManager


class BaseModel(models.Model):
    objects = BaseModelManager()
    all_objects = models.Manager()
    date_created = models.PositiveBigIntegerField(editable=False, default=0)
    created_by = models.ForeignKey(
        'api.User', related_name='+', null=True, blank=True, on_delete=models.SET_NULL)
    last_updated_by = models.ForeignKey(
        'api.User', related_name='+', null=True, blank=True, on_delete=models.SET_NULL)
    last_updated = models.PositiveBigIntegerField(editable=False, default=0)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    last_approved_by = models.ForeignKey(
        'api.User', related_name='+', null=True, blank=True, on_delete=models.SET_NULL)
    type = models.CharField(max_length=200, default='')
    deleted_by = models.ForeignKey(
        'api.User', related_name='+', null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True
        app_label = 'api'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        with transaction.atomic():
            request = CrequestMiddleware.get_request()
            if self.pk is None:
                self.date_created = datetime.datetime.now().timestamp()
                self.type = self.__class__.__name__ if self.type == '' else self.type
                self.created_by = request.c_user if request else None

            self.last_updated = datetime.datetime.now().timestamp()
            self.last_approved_by = request.c_user if request else None
            super(BaseModel, self).save()

    def delete(self, using=None, keep_parents=False):
        with transaction.atomic():
            request = CrequestMiddleware.get_request()
            self.is_deleted = True
            self.is_active = False
            self.deleted_by = request.c_user if request else None
            self.save()

    @property
    def render_timestamp(self, value=None, format=None):
        if value is None:
            return "N/A"
        if format is None:
            format = '%d-%m-%Y'
        return datetime.datetime.fromtimestamp(value).strftime(format)

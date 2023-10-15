from django.db import models
from django.utils import timezone


class CustomModelMixin(models.Model):
    """
    Class for creation of model mixin for reuse.
    """
    created_at = models.DateTimeField(auto_now_add=timezone.now)
    updated_at = models.DateTimeField(auto_now=timezone.now)

    class Meta:
        abstract = True


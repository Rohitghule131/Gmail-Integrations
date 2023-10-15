from django.db import models
from Utilities.utils import CustomModelMixin

# Create your models here.


class GoogleRequestModel(CustomModelMixin):
    """
    Class for create a google request model.
    """
    email = models.EmailField(null=False, blank=False)
    profile_picture = models.URLField(null=True, blank=False)
    name = models.CharField(max_length=100, null=True, blank=False)
    access_token = models.CharField(max_length=500, null=False, blank=False)
    refresh_token = models.CharField(max_length=500, null=True, blank=False)

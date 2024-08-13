from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass

class TrackedGame(models.Model):
    # user
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # search words used
    query = models.CharField(max_length=200)

    # results
    steam_title = models.CharField(max_length=200)
    steam_price = models.CharField(max_length=20)
    
    aband_title = models.CharField(max_length=200)
    aband_price = models.CharField(max_length=20)

    gog_title = models.CharField(max_length=200)
    gog_price = models.CharField(max_length=20)
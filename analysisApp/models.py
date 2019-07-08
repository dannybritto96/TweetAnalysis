from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User,on_delete='cascade')
    screen_name = models.CharField(max_length=200,primary_key=True)
    oauth_token = models.CharField(max_length=200)
    oauth_secret = models.CharField(max_length=200)

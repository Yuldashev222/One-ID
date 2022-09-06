from django.db import models
from django.contrib.auth.models import AbstractBaseUser
# Create your models here.

class Users(AbstractBaseUser):
    age = models.PositiveIntegerField(default=0, blank=True, null=True)
    

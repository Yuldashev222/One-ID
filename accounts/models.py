from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.contrib.auth.models import BaseUserManager
# Create your models here.



class User(AbstractUser):
    address = models.CharField(max_length=1000, blank=True, null=True)
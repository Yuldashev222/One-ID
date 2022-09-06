from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
# Create your models here.




class MyAccountManager(BaseUserManager):
    
    def create_user(self, phone_number, first_name, last_name, password=None):
        if not phone_number:
            raise ValueError('Users must have an tel number!!!')
        if not first_name:
            raise ValueError('Users must have an name!!!')
        if not last_name:
            raise ValueError('Users must have an surname!!!')
        
        user = self.model(
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name
        )
        
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    
    def create_superuser(self, phone_number, first_name, last_name, password):
        user = self.create_user(
            phone_number=phone_number,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user



class Users(AbstractBaseUser):
    age = models.PositiveIntegerField(default=0, blank=True, null=True)
    phone_number = models.CharField(max_length=15)
    date_joined = models.DateTimeField(auto_now_add=True, editable=False)
    last_login = models.DateTimeField(auto_now=True)
        
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
    ]
    
    objects = MyAccountManager()
    
    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
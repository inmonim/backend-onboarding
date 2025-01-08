from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from common.models import BaseModel


class User(AbstractBaseUser):
    
    id = models.BigAutoField(primary_key=True)
    nickname = models.CharField(max_length=50, null=False)
    username = models.CharField(max_length=50, null=False, unique=True)
    password = models.CharField(max_length=255, null=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['nickname']
    
    class Meta:
        db_table = 'users'
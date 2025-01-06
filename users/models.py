from django.db import models

from common.models import BaseModel


class User(BaseModel):
    
    user_id = models.BigAutoField(primary_key=True)
    nickname = models.CharField(max_length=50, null=False)
    username = models.CharField(max_length=50, null=False)
    password = models.CharField(max_length=255, null=False)
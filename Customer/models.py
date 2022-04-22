
from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

class User(AbstractUser):

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    username = None
    first_name = models.CharField(max_length=20,null=True,blank=True)
    last_name = models.CharField(max_length=30,null=True,blank=True)
    phone = models.CharField(max_length=12,unique=True,primary_key=True)
    email = models.EmailField(unique=True,blank=True,null=True)
    point = models.IntegerField(default=0)

    def __str__(self):
        return str(self.email)
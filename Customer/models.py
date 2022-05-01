from django.db import models
from django.contrib.auth.models import AbstractUser

import uuid




#-------------------------------------base user--------------------------------------
class Profile(AbstractUser):

    USERNAME_FIELD = 'id'
    
    # last_login = models.UUIDField(default=uuid.uuid4,editable=True)
    id = models.CharField(max_length=30,primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    is_User = models.BooleanField( default=False)
    is_Residence = models.BooleanField( default=False)

    def __str__(self):
        return str(self.last_name)



#----------------------------------end user (on to on Profile)-----------------------
class User(models.Model):

    USERNAME_FIELD = 'profile'
    REQUIRED_FIELDS = []

    class Meta():
        db_table = 'customer'

    username = None
    # is_authenticated = False
    # is_anonymous = False
    is_active = True
    # last_login = models.CharField(max_length=300,null=True,blank=True)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, primary_key=True,related_name="userTOprofile")
    # first_name = models.CharField(max_length=20,null=True,blank=True)
    # last_name = models.CharField(max_length=30,null=True,blank=True)
    phone = models.CharField(max_length=12,unique=True,verbose_name="phone")
    # email = models.EmailField(unique=True,blank=True,null=True)
    point = models.IntegerField(default=0)
   



    def __str__(self):
        return str(self.phone)

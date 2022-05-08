from django.db import models
from django.contrib.auth.models import AbstractUser
# from Reservation.models import Reserve
# from Supplier.models import *
from .managers import *
import uuid




#-------------------------------------base user--------------------------------------
class Profile(AbstractUser):

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    email = models.EmailField('email address', primary_key=True)
    id = models.CharField(max_length=30,unique=True, default=uuid.uuid4, editable=False)
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
    is_active = True
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, unique=True,null=True,blank=True,related_name="userTOprofile")
    phone = models.CharField(max_length=12,primary_key=True,verbose_name="phone")
    point = models.IntegerField(default=0)
   
    def __str__(self):
        return str(self.phone)


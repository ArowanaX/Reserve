
from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
# from Supplier.models import Residence
# from uuid import uuid4
import uuid


class Profile(AbstractUser):
    USERNAME_FIELD = 'id'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # username = models.UUIDField( default=uuid.uuid4, editable=False)
    username = None
    is_User = models.BooleanField( default=False)
    is_Residence = models.BooleanField( default=False)
    # USER_TYPE_CHOICES = (
    #   (1, 'Customer'),
    #   (2, 'Supplier'),
    # )
    # user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)


class User(models.Model):

    USERNAME_FIELD = 'profile'
    REQUIRED_FIELDS = []
    # objects = CustomUserManager()

    class Meta():
        db_table = 'customer'
        # swappable = 'AUTH_USER_MODEL'

    username = None
    is_authenticated = False
    is_anonymous = False
    is_active = True
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=20,null=True,blank=True)
    last_name = models.CharField(max_length=30,null=True,blank=True)
    phone = models.CharField(max_length=12,unique=True,verbose_name="phone")
    email = models.EmailField(unique=True,blank=True,null=True)
    point = models.IntegerField(default=0)
   



    def __str__(self):
        return str(self.email)

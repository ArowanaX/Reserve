from django.db import models
from django.utils.translation import gettext as _
from Customer.models import User
from django.contrib.auth.models import AbstractUser
from Customer.managers import CustomUserManager



class Residence(User):
    objects = CustomUserManager()

    # class Meta:
        # unique_together = ['name','user']
        # default_related_name = 'residence_asb'
    #location = models.
    user = models.OneToOneField(User,primary_key=True,on_delete=models.CASCADE,related_name="ResidenceToUser")
    name = models.CharField(unique=True,max_length=20,verbose_name="res_name")
    address = models.TextField(verbose_name=_("address"))
    img = models.ImageField(upload_to="supplier/",null=True,blank=True)
    TYPE_CHOICES = (
        ('lux', 'lux hotel'),
        ('h', 'hotel'),
        ('gh', 'guesthouse'),
    )
    type = models.CharField(max_length=10, choices = TYPE_CHOICES)
    TAG_CHOICES = (
        ('res', 'Restaurant'),
        ('lux', 'lux'),
        ('sh', 'Sports hall'),
    )
    tag = models.CharField(max_length=10, choices = TAG_CHOICES,null=True,blank=True)
    service_hours_start = models.IntegerField()
    service_hours_end = models.IntegerField()
    max_reserve = models.IntegerField()
    detail = models.TextField(max_length=300,null=True,blank=True)

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'residiance'
        ordering = ('name',)

class Room(models.Model):
    residence = models.ForeignKey(Residence,on_delete=models.CASCADE,related_name="Residence_Room")
    id = models.IntegerField(primary_key=True)
    room_img1 = models.ImageField(upload_to="supplier/",null=True,blank=True)
    room_img2 = models.ImageField(upload_to="supplier/",null=True,blank=True)
    room_img3 = models.ImageField(upload_to="supplier/",null=True,blank=True)
    numberـofـbed = models.IntegerField()
    STATE_CHOICES = (
        ('F', 'Full'),
        ('E', 'Empty'),
    )
    state = models.CharField(max_length=10, choices = STATE_CHOICES)
    FACILITI_CHOICES = (
        ('lux', 'lux'),
        ('re', 'Refrigerator'),
        ('so', 'Sofa'),
    )
    faciliti = models.CharField(max_length=10, choices = FACILITI_CHOICES)
    price = models.BigIntegerField()

    # def __str__(self):
    #     return self.id
    class Meta:
        db_table = 'room'
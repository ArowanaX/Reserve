from cProfile import Profile
from django.db import models
from Supplier.models import Residence
from Customer.models import User, Profile
import uuid

# Create your models here.
class CustomBooleanField(models.BooleanField):

    def from_db_value(self, value, expression, connection, context=None, default=0, null=True, blank=True):
        if value is None:
            return value
        return int(value) # return 0/1


class Reservation(models.Model):
    
    id = models.CharField(max_length=30, primary_key=True, default=uuid.uuid4, editable=False)
    order_date = models.DateField(auto_now_add=True,null=True,blank=True)
    date_in = models.DateField(null=True,blank=True)
    date_out = models.DateField(null=True,blank=True)
    person_num = models.PositiveSmallIntegerField(default=0,null=True,blank=True)
    TYPE_ROOM = (
        ('off su','Office Suite'),
        ('conf su','Conference Suite'),
        ('jnr su','Junior Suite'),
        ('vip su','VIP Suite'),
        ('fie su','Fiesta Suite'),
        ('sngl','Single Suite'),
    )
    type_room = models.CharField(max_length=50, null=True, blank=True, choices=TYPE_ROOM)
    #type_rooms = models.ForeignKey("TypeRoom", on_delete=models.CASCADE, null=True, blank=True)
    reserver = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True, related_name='ReserveUser')
    hotel = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='ReservingHotel',null=True, blank=True)
    request_user = models.TextField(null=True,blank=True)
    offers = CustomBooleanField(default=0,null=True,blank=True)
    news = CustomBooleanField(default=0,null=True,blank=True)
    sms = CustomBooleanField(default=0,null=True,blank=True)
    

    def __str__(self):
        # return self.hotel+ self.reserver
        return f'{self.hotel} _ {self.reserver}'
    
    class Meta:
        db_table = 'reservation'

class Wishlist(models.Model):
    user=models.ForeignKey(Profile,on_delete=models.CASCADE, related_name="wishlisttocustomer")
    residence=models.ManyToManyField(Residence,related_name="wishlisttoresidence")
    # datetime =models.DateTimeField(auto_now=True,verbose_name=_('date and time'))

    class Meta:
        verbose_name = "Wishlist"
        verbose_name_plural = "Wishlists"

    def __str__(self):
        return str(self.user.email)

class Upcomming(models.Model):
    user=models.ForeignKey(Profile,on_delete=models.CASCADE, related_name="upcommingtocustomer")
    # residence=models.ManyToManyField(Residence,related_name="upcommingtoresidence")
    reserve=models.ManyToManyField(Reservation,related_name="upcommingtoreserve")
    # datetime =models.DateTimeField(auto_now=True,verbose_name=_('date and time'))

    class Meta:
        verbose_name = "Upcomming"
        verbose_name_plural = "Upcommings"

    def __str__(self):
        return str(self.user.email)

class History(models.Model):
    user=models.ForeignKey(Profile,on_delete=models.CASCADE, related_name="historytocustomer")
    reserve=models.ManyToManyField(Reservation,related_name="historytoreserve")
    # datetime =models.DateTimeField(auto_now=True,verbose_name=_('date and time'))

    class Meta:
        verbose_name = "History"
        verbose_name_plural = "History"

    def __str__(self):
        return str(self.user.email)
from django.db import models
from Customer.models import Profile
from Supplier.models import Service



class Reserve(models.Model):
    order_date = models.DateField(auto_now_add=True)
    date_in = models.DateField()
    date_out = models.DateField()
    person_num = models.IntegerField()
    room = models.OneToOneField(Service,on_delete=models.CASCADE,related_name='ReserveRoom')
    user = models.OneToOneField(Profile,on_delete=models.CASCADE,related_name='ReserveUser')

    def __str__(self):
        return self.id+ " " + self.user

class Wishlist(models.Model):
    user=models.ForeignKey(Profile,on_delete=models.CASCADE, related_name="wishlisttocustomer")
    reserve=models.ManyToManyField(Reserve)
    # datetime =models.DateTimeField(auto_now=True,verbose_name=_('date and time'))

    class Meta:
        verbose_name = "Wishlist"
        verbose_name_plural = "Wishlists"


class Upcomming(models.Model):
    user=models.ForeignKey(Profile,on_delete=models.CASCADE, related_name="upcommingtocustomer")
    reserve=models.ManyToManyField(Reserve)
    # datetime =models.DateTimeField(auto_now=True,verbose_name=_('date and time'))

    class Meta:
        verbose_name = "Upcomming"
        verbose_name_plural = "Upcommings"


class History(models.Model):
    user=models.ForeignKey(Profile,on_delete=models.CASCADE, related_name="historytocustomer")
    reserve=models.ManyToManyField(Reserve)
    # datetime =models.DateTimeField(auto_now=True,verbose_name=_('date and time'))

    class Meta:
        verbose_name = "History"
        verbose_name_plural = "History"
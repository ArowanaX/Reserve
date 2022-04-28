from django.db import models
from Customer.models import User
from Supplier.models import Service



class Reserve(models.Model):
    order_date = models.DateField(auto_now_add=True)
    date_in = models.DateField()
    date_out = models.DateField()
    person_num = models.IntegerField()
    room = models.OneToOneField(Service,on_delete=models.CASCADE,related_name='ReserveRoom')
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='ReserveUser')

    def __str__(self):
        return self.id+ " " + self.user
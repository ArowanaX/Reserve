from django.contrib import admin
from .models import Reservation,Wishlist,Upcomming,History

# Register your models here.
admin.site.register(Reservation)
admin.site.register(Wishlist)
admin.site.register(Upcomming)
admin.site.register(History)
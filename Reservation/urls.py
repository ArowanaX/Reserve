from django.urls import path

# from Customer.utils import Send_sms
from .views import *

app_name="Reservation"

urlpatterns = [


#------------------------------serial call for register user---------------------

    path("wishlist/",ShowWishlistAPI.as_view(),name="wishlist"),
    path("addwishlist/",AddWishlistAPI.as_view(),name="addwishlist"),

]

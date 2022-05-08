from django.urls import path

# from Customer.utils import Send_sms
from .views import *

app_name="Reserve"

urlpatterns = [


#------------------------------serial call for register user---------------------
    path("reservation/<str:name>", ReservationAPIView.as_view(), name="reservation"),
    path("wishlist/",ShowWishlistAPI.as_view(),name="wishlist"),
    path("addwishlist/",AddWishlistAPI.as_view(),name="addwishlist"),
    path("upcomming/",ShowUpcommingAPI.as_view(),name="upcomming"),


]

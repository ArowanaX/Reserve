from django.urls import path

# from Customer.utils import Send_sms
from .views import *

app_name="Reserve"

urlpatterns = [


#------------------------------serial call for register user---------------------
    path("reservation/<str:name>", ReservationAPIView.as_view(), name="reservation"),
    path("wishlist/",ShowWishlistAPI.as_view(),name="wishlist"),
    path("addwishlist/",AddWishlistAPI.as_view(),name="addwishlist"),
    path("delwishlist/",DelWishlistAPI.as_view(),name="delwishlist"),
    path("upcomming/",ShowUpcommingAPI.as_view(),name="upcomming"),
    path("addupcomming/",AddToUpcomming.as_view(),name="addupcomming"),
    path("delupcomming/",DelUpcommingAPI.as_view(),name="delupcomming"),



]

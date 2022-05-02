from django.urls import path
from .views import *

app_name="Customer"

urlpatterns = [


#------------------------------serial call for register user---------------------

    path("phone/",PhoneVerifi.as_view(),name="phone"),
    path("activate/<int:phone>", Activate.as_view(), name="activate"),
    path("register/<int:phone>", Register.as_view(), name="register"),


#-----------------------------show user dashboard---------------------------------

    path("accont/", UserAccontAPI.as_view(), name="profile"),


#----------------------------just for develop test-----------------------
    path("logout/", my_logout, name="logout"),
    path("login/", my_login, name="login"),
]

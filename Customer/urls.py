from django.urls import path
from .views import PhoneVerifi,Activate,Register,Profile,my_logout,my_login

app_name="Customer"

urlpatterns = [

    path("phone/",PhoneVerifi.as_view(),name="phone"),
    path("activate/<int:phone>", Activate.as_view(), name="activate"),
    path("register/<int:phone>", Register.as_view(), name="register"),
    path("profile/<str:phone>", Profile.as_view(), name="profile"),
    path("logout/", my_logout, name="logout"),
    path("login/", my_login, name="login"),
    

]

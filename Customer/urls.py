from django.urls import path
from .views import PhoneVerifi,Activate,Register

app_name="Customer"

urlpatterns = [
   
    path("phone",PhoneVerifi.as_view(),name="phone"),
    path("activate/<int:phone>", Activate.as_view(), name="activate"),
    path("register/<int:phone>", Register.as_view(), name="register"),

]

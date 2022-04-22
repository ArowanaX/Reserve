from django.urls import path
from .views import PhoneVerifi,Activate

app_name="Customer"

urlpatterns = [
   
    path("phone",PhoneVerifi.as_view(),name="phone"),
    path("activate/<int:phone>", Activate.as_view(), name="activate"),

]

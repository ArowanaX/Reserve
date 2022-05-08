from os import name
from django.contrib import admin
from django.urls import path,include
from Customer.views import UserType

urlpatterns = [
    path('admin/', admin.site.urls),
    path("Customer/", include("Customer.urls", namespace='customer')),
    path("Supplier/", include("Supplier.urls", namespace='supplier')),
    path("type",UserType.as_view(),name="type"),
    path("Reservation/",include("Reserve.urls", namespace='reservation')),

]
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("Customer/", include("Customer.urls", namespace='customer')),
    path("Supplier/", include("Supplier.urls", namespace='supplier')),
]
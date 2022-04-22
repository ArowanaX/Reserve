from django.urls import path
from .views import RegisterView

app_name="Customer"

urlpatterns = [
   
    path("register",RegisterView.as_view()),
    # path("activate/<int:phone>", Activate.as_view(), name="activate"),

]

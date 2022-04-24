from django.urls import path
from .views import ResidenceAPI,LoginAPI,Profile

app_name="Supplier"

urlpatterns = [
   
    path("residence/",ResidenceAPI.as_view(),name="residence"),
    path("login/",LoginAPI.as_view(),name="login"),
    path("profile/<str:name>",Profile.as_view(),name="profile"),

    

]

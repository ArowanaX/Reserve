from django.urls import path
from .views import ResidenceAPI,LoginAPI,Profile,AddOUTImageAlbum,AddINImageAlbum

app_name="Supplier"

urlpatterns = [
   
    path("residence/",ResidenceAPI.as_view(),name="residence"),
    path("login/",LoginAPI.as_view(),name="login"),
    path("profile/<str:name>",Profile.as_view(),name="profile"),
    path("inimg/<str:residence>",AddINImageAlbum.as_view(),name="add_inimage"),
    path("outimg/<str:residence>",AddOUTImageAlbum.as_view(),name="add_outinimage"),

    

]

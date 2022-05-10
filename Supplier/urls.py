from django.urls import path
from rest_framework.authtoken import views as auth_token
from .views import ResidenceAPI,LoginAPIView,AccountAPIView,AddOUTImageAlbum,AddINImageAlbum,ResidenceRegisterAPI

app_name="Supplier"

urlpatterns = [
   
    path("register/",ResidenceRegisterAPI.as_view(),name="register"),
    path("login/",LoginAPIView.as_view(),name="login"),
    #path('api-token-auth/', auth_token.obtain_auth_token),
    path("account/<str:email>",AccountAPIView.as_view(),name="account"),
    path("inimg/<str:residence>",AddINImageAlbum.as_view(),name="add_inimage"),
    path("outimg/<str:residence>",AddOUTImageAlbum.as_view(),name="add_outinimage"),

    

]

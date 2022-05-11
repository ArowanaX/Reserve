from django.urls import path
from rest_framework.authtoken import views as auth_token
# from .views import ResidenceAPI,LoginAPIView,AccountAPIView,AddOUTImageAlbum,AddINImageAlbum,ResidenceRegisterAPI
from .views import *

app_name="Supplier"

urlpatterns = [
   
    path("register/",ResidenceRegisterAPI.as_view(),name="register"),
    path("login/",LoginAPIView.as_view(),name="login"),
    #path('api-token-auth/', auth_token.obtain_auth_token),
    path("account/<str:email>",AccountAPIView.as_view(),name="account"),
    path("inimg/<str:residence>",AddINImageAlbum.as_view(),name="add_inimage"),
    path("outimg/<str:residence>",AddOUTImageAlbum.as_view(),name="add_outinimage"),
    path("openticket/",OpenTicketAPI.as_view(),name="openticket"),
    path("tikcomment/",AddTikComment.as_view(),name="tikcomment"),
    path("showticket/",ShowTicketAPI.as_view(),name="showticket"),
    path("addcomment/",AddCommentAPI.as_view(),name="addcomment"),
    path("showcomment/",ShowCommentAPI.as_view(),name="showcomment"),
    path("addrate/",AddRateAPI.as_view(),name="addrate"),
    path("Showrate/",ShowRateAPI.as_view(),name="Showrate"),

    

]

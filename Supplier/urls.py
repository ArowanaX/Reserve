from django.urls import path
from rest_framework.authtoken import views as auth_token
from .views import (ResidenceRegisterAPI,LoginAPIView,AccountAPIView,EmailVerifi,VerificationCodeAPIView,ForgetPasswordAPIView,
                    ServiceListAPIView,ServiceCreateAPIView,ServiceUpdateAPIView,MenuListAPIView,MenuCreateAPIView,
                    MenuUpdateAPIView,AddINImageAlbumListAPIView,AddINImageAlbumCreateAPIView,AddINImageAlbumUpdateAPIView,
                    AddOUTImageAlbumListAPIView,AddOUTImageAlbumCreateAPIView,AddOUTImageAlbumUpdateAPIView)

app_name="Supplier"

urlpatterns = [
   
    path("register/",ResidenceRegisterAPI.as_view(),name="register"),
    path("login/",LoginAPIView.as_view(),name="login"),
    #path('api-token-auth/', auth_token.obtain_auth_token),
    path("account/<str:email>",AccountAPIView.as_view(),name="account"),
    path("forget_password/",EmailVerifi.as_view(),name="forget_password"),
    path("verification/<str:email>/",VerificationCodeAPIView.as_view(),name="verification"),
    path("new_password/<str:email>",ForgetPasswordAPIView.as_view(),name="new_password"),
    path("service_list/",ServiceListAPIView.as_view(),name="service_list"),
    path("service_create/",ServiceCreateAPIView.as_view(),name="service_create"),
    path("service_update/<str:residence>/<int:number>/",ServiceUpdateAPIView.as_view(),name="service_update"),
    path("menu_list/",MenuListAPIView.as_view(),name="menu_list"),
    path("menu_create/<int:id>/",MenuCreateAPIView.as_view(),name="menu_create"),
    path("menu_update/<str:residence>/<int:id>/",MenuUpdateAPIView.as_view(),name="menu_update"),
    path("inimg_list/",AddINImageAlbumListAPIView.as_view(),name="add_inimage_list"),
    path("inimg_create/",AddINImageAlbumCreateAPIView.as_view(),name="add_inimage_create"),
    path("inimg_delete/<str:residence>/<int:id>",AddINImageAlbumUpdateAPIView.as_view(),name="add_inimage_update"),
    path("outimg_list/",AddOUTImageAlbumListAPIView.as_view(),name="add_outimage_list"),
    path("outimg_create/",AddOUTImageAlbumCreateAPIView.as_view(),name="add_outimage_create"),
    path("outimg_delete/<str:residence>/<int:id>",AddOUTImageAlbumUpdateAPIView.as_view(),name="add_outimage_update"),
]

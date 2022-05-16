from django.urls import path
from .views import *

app_name="BigAdmin"

urlpatterns = [

 
#------------------------------serial call for register user---------------------

    path("showticketadmin/",ShowTicketAPI.as_view(),name="showticketadmin"),
    path("openticketadmin/",OpenTicketAPI.as_view(),name="openticketadmin"),
    path("tikcommentadmin/",AddTikComment.as_view(),name="tikcommentadmin"),
    path("deluptik/<int:id>",DelUpTikAPI.as_view(),name="deluptik"),
    

]

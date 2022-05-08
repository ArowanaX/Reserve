from django.urls import path
from .views import ReservationAPIView

app_name = 'Reserve'

urlpatterns = [
    path("reservation/<str:name>", ReservationAPIView.as_view(), name="reservation"),
]
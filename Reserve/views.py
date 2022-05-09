from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics,status
from .serializers import *
from .models import Reservation
from Supplier.models import Residence
from Customer.models import Profile
from rest_framework import generics,status
from Customer.models import *
from Reserve.serializers import *
from .models import *
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class ReservationAPIView(generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    lookup_field = "name"
    
    def get_queryset(self):
        name = self.kwargs.get(self.lookup_url_kwarg)
        hotel = Residence.objects.filter(name=name)
        return hotel

    
    def get_serializer_context(self):
         context = super(ReservationAPIView,self).get_serializer_context()
         context.update({"request":self.request})
         print(self.kwargs['name'])
         context.update({"name":self.kwargs['name']})
         return context
         
class ShowWishlistAPI(generics.ListAPIView):
    serializer_class = WishlistSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_serializer_context(self):
        context = super(ShowWishlistAPI, self).get_serializer_context()
        context.update({"request": self.request.user})
        return context

    def get_queryset(self):
        user = get_object_or_404(Profile,id=self.request.user.id,)
        wishlist=Wishlist.objects.get_or_create(user=user)[0]
        return Wishlist.objects.filter(user=user)

class AddWishlistAPI(generics.ListCreateAPIView):
    serializer_class = AddWishlistSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = get_object_or_404(Profile,email=self.request.user.email,)
        wishlist=Wishlist.objects.get_or_create(user=user)[0]
        return Wishlist.objects.filter(user=user)
    
    def get_serializer_context(self):
        context = super(AddWishlistAPI, self).get_serializer_context()
        context.update({"request": self.request})
        return context



class DelWishlistAPI(generics.ListCreateAPIView):
    serializer_class = DelWishlistSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = get_object_or_404(Profile,email=self.request.user.email,)
        wishlist=Wishlist.objects.get_or_create(user=user)[0]
        return Wishlist.objects.filter(user=user)
    
    def get_serializer_context(self):
        context = super(DelWishlistAPI, self).get_serializer_context()
        context.update({"request": self.request})
        return context
#---------------- upcomming for self reserve & invited link-------------
#----------------access from auto reserve & url link--------------------
class AddToUpcomming(generics.ListCreateAPIView):
    serializer_class = AddUpcommingSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = get_object_or_404(Profile,email=self.request.user.email,)
        upcomming=Upcomming.objects.get_or_create(user=user)[0]
        return Upcomming.objects.filter(user=user)

    def get_serializer_context(self):
        context = super(AddToUpcomming, self).get_serializer_context()
        context.update({"request": self.request})
        return context

class ShowUpcommingAPI(generics.ListAPIView):
    serializer_class = UpcommingSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_serializer_context(self):
        context = super(ShowUpcommingAPI, self).get_serializer_context()
        context.update({"request": self.request.user})
        return context

    def get_queryset(self):
        user = get_object_or_404(Profile,email=self.request.user.email,)
        upcomming=Upcomming.objects.get_or_create(user=user)[0]
        return Upcomming.objects.filter(user=user)

class DelUpcommingAPI(generics.ListCreateAPIView):
    serializer_class = DelUpcommingSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = get_object_or_404(Profile,email=self.request.user.email,)
        upcomming=Upcomming.objects.get_or_create(user=user)[0]
        return Upcomming.objects.filter(user=user)

    def get_serializer_context(self):
        context = super(DelUpcommingAPI, self).get_serializer_context()
        context.update({"request": self.request})
        return context
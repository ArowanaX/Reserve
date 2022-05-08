
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


# Create your views here.
class ReservationAPIView(generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    lookup_field = "name"
    
    def get_queryset(self):
        name = self.kwargs.get(self.lookup_url_kwarg)
        hotel = Residence.objects.filter(name=name)
        return hotel
    # def get(self,request,*args,**kwargs):
    #     data = request.GET.get('name')
    #     return Response(data, status=status.HTTP_200_OK)


    # def post(self, request, name):
    #     # def perform_create(self, serializer):
    #     #     serializer.save(reserver=self.request.user)

    #     ser_data = ReservationSerializer(data=request.data)
    #     if ser_data.is_valid():
    #         ser_data.save()
    #         return Response(ser_data.data,status=status.HTTP_201_CREATED)
    #     return Response(ser_data.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def get_serializer_context(self):
         context = super(ReservationAPIView,self).get_serializer_context()
         context.update({"request":self.request})
         print(self.kwargs['name'])
         #print(self.request['name'])
         context.update({"name":self.kwargs['name']})
         return context
         
class ShowWishlistAPI(generics.ListAPIView):
    serializer_class = WishlistSerializer
    
    def get_serializer_context(self):
        context = super(ShowWishlistAPI, self).get_serializer_context()
        context.update({"request": self.request.user})
        return context

    def get_queryset(self):
        user = get_object_or_404(Profile,id=self.request.user.id,)
        wishlist=Wishlist.objects.get_or_create(user=user)[0]
        return Wishlist.objects.filter(user=user)

class AddWishlistAPI(generics.UpdateAPIView):
    serializer_class = AddWishlistSerializer

    def get_queryset(self):
        user = get_object_or_404(Profile,email=self.request.user.email,)
        wishlist=Wishlist.objects.get_or_create(user=user)[0]
        return Wishlist.objects.get(user=user)

    def put(self, request, *args, **kwargs):
        user = get_object_or_404(Profile,email=self.request.user.email,)
        wishlist=Wishlist.objects.get_or_create(user=user)[0]
        reserve= get_object_or_404(Reservation, pk=request.POST.get("id"))
        wishlist.reserve.add(reserve)
        wishlist.save()
        return Wishlist.objects.get(user=user)

#---------------- upcomming for self reserve & invited link-------------
#----------------access from auto reserve & url link--------------------
class AddToUpcomming(generics.UpdateAPIView):
    serializer_class = AddUpcommingSerializer

    def get_queryset(self):
        user = get_object_or_404(Profile,email=self.request.user.email,)
        upcomming=Upcomming.objects.get_or_create(user=user)[0]
        return Upcomming.objects.get(user=user)

    def put(self, request, *args, **kwargs):
        user = get_object_or_404(Profile,email=self.request.user.email,)
        upcomming=Upcomming.objects.get_or_create(user=user)[0]
        reserve= get_object_or_404(Reservation, pk=request.POST.get("id"))
        upcomming.reserve.add(reserve)
        upcomming.save()
        return Upcomming.objects.get(user=user)



class ShowUpcommingAPI(generics.ListAPIView):
    serializer_class = UpcommingSerializer
    
    def get_serializer_context(self):
        context = super(ShowUpcommingAPI, self).get_serializer_context()
        context.update({"request": self.request.user})
        return context

    def get_queryset(self):
        user = get_object_or_404(Profile,email=self.request.user.email,)
        upcomming=Upcomming.objects.get_or_create(user=user)[0]
        return Upcomming.objects.filter(user=user)
import email
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics,status
from .serializers import *
from .models import Reservation
from Supplier.models import Residence
from Customer.models import Profile
from rest_framework import generics,status,mixins
from Customer.models import *
from Reserve.serializers import *
from .models import *
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .utils import send_email, send_mail
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class ReservationAPIView(generics.CreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    
    def get_serializer_context(self):
         context = super(ReservationAPIView,self).get_serializer_context()
         context.update({"request":self.request})
         print(self.kwargs['name'])
         context.update({"name":self.kwargs['name']})
         return context
        
        
    # def post(self, request, name):
    #     ser_data = ReservationSerializer(data=request.data)
    #     user=self.request.user
    #     email = user.email
    #     print(email)
    #     if ser_data.is_valid():
    #         offers = ser_data['offers'].value
    #         news = ser_data['news'].value
    #         #sms = ser_data['sms'].value
    #         print(offers)
    #         if offers==True or news==True :
    #             print('OK')
    #             try:
    #                 send_mail(html=None,text='Email_body',subject='Hello word',from_email='maryamnadeali@yahoo.com',to_emails=[str(email)])
    #             except:
    #                 return Response('email not send....!')
    #         #ser_data.save()
    #         return Response(ser_data.data,status=status.HTTP_201_CREATED)
    #     return Response(ser_data.errors,status=status.HTTP_400_BAD_REQUEST)


class CancelReservationAPI(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Profile.objects.all()
    serializer_class = DelReservationSerializer
    
    def get_queryset(self):
        user = get_object_or_404(Profile,email=self.request.user.email,)
        # user = Profile.objects.filter(email=self.request.user.email)
        print('kkkkkkkkkkkkkkkot')
        print(user)
        res=Reservation.objects.filter(reserver=user)
        print(res)
        # res=Reservation.objects.get_or_create(reserver=user)[0]
        # return Reservation.objects.filter(reserver=user)
        return res

    def get_serializer_context(self):
        context = super(CancelReservationAPI, self).get_serializer_context()
        context.update({"request": self.request.user})
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

class HistoryAPI(generics.ListAPIView):
    serializer_class = HistorySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = get_object_or_404(Profile,email=self.request.user.email,)
        history=History.objects.get_or_create(user=user)[0]
        return History.objects.filter(user=user)

    def get_serializer_context(self):
        context = super(HistoryAPI, self).get_serializer_context()
        context.update({"request": self.request})
        return context


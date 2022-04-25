

from django.urls import reverse

from django.shortcuts import redirect,HttpResponse

from django.core.cache import cache
from requests import request
# from requests import request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics,status
from rest_framework.views import APIView
from django.contrib.auth import logout,login


from .models import User,Profile
from .serializers import UserSerializer,PhoneSerializer,ActivateSerializer,TypeSerializer
import random
from Customer.utils import Send_sms

from Customer import serializers

class UserType(generics.CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = TypeSerializer
  
    # def post(self , request,*args, **kwargs):

    #     serializer = TypeSerializer(data=request.data)
        
    #     if serializer.is_valid():
    #         return super().post(request, *args, **kwargs)
    #     else:
    #         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class PhoneVerifi(generics.CreateAPIView):
 
    queryset = User.objects.all()
    serializer_class = PhoneSerializer

    def post(self , request):
        serializer = PhoneSerializer(data=request.data)
        uid=str(random.randint(100000,999999))
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"+uid+">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        

        if serializer.is_valid():

            phone = str(serializer["phone"].value)
            cache.set(phone,uid,180)
            return redirect(reverse('Customer:activate',kwargs={"phone":str(phone)}))

        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class Activate(generics.CreateAPIView,):
    queryset = User.objects.all()
    serializer_class = ActivateSerializer


    def post(self , request,*args, **kwargs):

        serializer = ActivateSerializer(data=request.data)
        if serializer.is_valid():
            phone = "0"+str(self.kwargs["phone"])
            c_phone=cache.get(phone)
            code = str(serializer["activate_code"].value)
            if code == c_phone:
                return redirect(reverse('Customer:register',kwargs={"phone":phone}))
            else:
                return Response(serializer.errors,status=status.h)

class Register(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def get_serializer_context(self):
        context = super(Register, self).get_serializer_context()
        context.update({"phone": str(self.kwargs["phone"])})
        context.update({"request": self.request})
        return context
    
def my_login(request):
    login(request, User.objects.get(phone = "09120857673" ))

    return HttpResponse("loged in!!!")


def my_logout(request):
    logout(request)
    return HttpResponse("loged out!!!")


class Profile(generics.RetrieveUpdateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'phone'


        


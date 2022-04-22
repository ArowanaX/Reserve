from django.urls import reverse

from django.shortcuts import redirect

from django.core.cache import cache
from rest_framework.response import Response

from rest_framework import generics,status
from rest_framework.views import APIView



from .models import User
from .serializers import UserSerializer,PhoneSerializer
import random
from Customer.utils import Send_sms

from Customer import serializers

class PhoneVerifi(generics.CreateAPIView):
 
    queryset = User.objects.all()
    serializer_class = PhoneSerializer

    def post(self , request):
        serializer = PhoneSerializer(data=request.data)
        uid=str(random.randint(100000,999999))
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"+uid+">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        

        if serializer.is_valid():

            phone = serializer["phone"].value
            cache.set(phone,uid,180)
            Send_sms(phone,uid)
            print(";;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;")
            # return Response(serializer.data, status = status.HTTP_200_OK)
            return redirect(reverse('Customer:activate',kwargs={"phone":phone}))

        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class Activate(generics.CreateAPIView):
    pass





        


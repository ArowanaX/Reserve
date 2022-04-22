
from django.urls import reverse

from django.shortcuts import redirect

from django.core.cache import cache
from rest_framework.response import Response

from rest_framework import generics,status
from rest_framework.views import APIView



from .models import User
from .serializers import UserSerializer,PhoneSerializer,ActivateSerializer
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
                return Response(serializer.errors,status=status.HTTP_226_IM_USED)

class Register(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_context(self):
        context = super(Register, self).get_serializer_context()
        context.update({"phone": str(self.kwargs["phone"])})
        return context


class Profile(generics.RetrieveUpdateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'phone'





        


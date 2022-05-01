from django.urls import reverse
from django.shortcuts import redirect,HttpResponse
from django.core.cache import cache
from django.contrib.auth import logout,login
import os

from rest_framework.response import Response
from rest_framework import generics,status

from .serializers import UserSerializer,PhoneSerializer,ActivateSerializer,TypeSerializer
from .models import User,Profile
import random


# from Customer.utils import Send_sms

from dotenv import load_dotenv, find_dotenv

# env_file = Path(find_dotenv(usecwd=True))
# load_dotenv(verbose=True, dotenv_path=env_file)




#-----------------------------------get type of user(user,Residence)--------------------

class UserType(generics.CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = TypeSerializer
  


#------------------------------------set activation code and send sms----------------------

class PhoneVerifi(generics.CreateAPIView):
 
    queryset = Profile.objects.all()
    serializer_class = PhoneSerializer

    def post(self , request):
        serializer = PhoneSerializer(data=request.data)
        # uid=str(random.randint(100000,999999))
        uid=str(random.randint(1,9))
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"+uid+">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        

        if serializer.is_valid():

            phone = str(serializer["phone"].value)
            cache.set(phone,uid,180)
            return redirect(reverse('Customer:activate',kwargs={"phone":str(phone)}))

        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



#-------------------------check activate code--------------------------------

class Activate(generics.CreateAPIView,):
    queryset = Profile.objects.all()
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
                return Response(serializer.errors,status=status.HTTP_403_FORBIDDEN)


#-----------------------------------register user----------------------------

class Register(generics.CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserSerializer
    def get_serializer_context(self):
        context = super(Register, self).get_serializer_context()
        context.update({"phone": str(self.kwargs["phone"])})
        context.update({"request": self.request})
        return context
    
#-------------------------------user profile set-----------------------------

class Profile(generics.RetrieveUpdateAPIView):

    queryset = Profile.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'phone'


#-----------------------------------just for develop test-----------------------

def my_login(request):
    login(request, User.objects.get(phone = "09120857673" ))

    return HttpResponse("loged in!!!")


def my_logout(request):
    logout(request)
    return HttpResponse("loged out!!!")


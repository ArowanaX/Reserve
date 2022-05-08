# from urllib import request
from genericpath import exists
from django.urls import reverse
from django.shortcuts import redirect,HttpResponse
from django.core.cache import cache
from django.contrib.auth import logout,login
from django.contrib.auth.decorators import login_required
import os
from requests import request

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics,status

from .serializers import *
from .models import *
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
            opt="reg"
            # Send_sms(phone,uid,opt)
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
                return redirect(reverse('Customer:recover',kwargs={"phone":phone}))

            #     if phone is not exists:
            #         return redirect(reverse('Customer:register',kwargs={"phone":phone}))
            #     elif phone is exists:
            #         return redirect(reverse('Customer:recover',kwargs={"phone":phone}))
            #     else:
            #         return Response(serializer.errors,status=status.HTTP_410_GONE)
    
            # else:
            #     return Response(serializer.errors,status=status.HTTP_403_FORBIDDEN)


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

class UserAccontAPI(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Profile.objects.all()
    serializer_class = AccontSerializer
    def get(self, request):
        serializer = AccontSerializer(request.user)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = request.user
        print(instance)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
    
    def get_serializer_context(self):
        context = super(UserAccontAPI, self).get_serializer_context()
        context.update({"request": self.request.user})
        return context


#-----------------------------------just for develop test-----------------------

def my_login(request):
    login(request, User.objects.get(phone = "09120857673" ))

    return HttpResponse("loged in!!!")


def my_logout(request):
    logout(request)
    return HttpResponse("loged out!!!")


class RecoverUserAPI(generics.CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = RecoverSerializer
    def get_serializer_context(self):
        context = super(RecoverUserAPI, self).get_serializer_context()
        context.update({"phone": str(self.kwargs["phone"])})
        context.update({"request": self.request})
        return context




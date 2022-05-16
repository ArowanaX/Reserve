
from genericpath import exists
from django.urls import reverse
from django.shortcuts import redirect,HttpResponse
from django.core.cache import cache
from django.contrib.auth import logout,login
from django.contrib.auth.decorators import login_required
import os
from requests import request

from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.response import Response
from rest_framework import generics,status

# from Reserve.views import AddToUpcomming

from .serializers import *
from Supplier.models import *
import random


# from Customer.utils import Send_sms

from dotenv import load_dotenv, find_dotenv

# env_file = Path(find_dotenv(usecwd=True))
# load_dotenv(verbose=True, dotenv_path=env_file)




class OpenTicketAPI(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset =  Ticket.objects.all()
    serializer_class = OpenTicketserializer
    

    def get_serializer_context(self):
        context = super(OpenTicketAPI, self).get_serializer_context()
        context.update({"request": self.request.user})
        return context
    
    # def get_queryset(self):
    #     ticket = get_object_or_404(Profile,user=self.request.user,)
    #     return ticket


class ShowTicketAPI(generics.ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = ShowTikSerializer
    permission_classes = (IsAdminUser,)
    
    def get_serializer_context(self):
        context = super(ShowTicketAPI, self).get_serializer_context()
        context.update({"request": self.request.user})
        return context

    # def get_queryset(self):
    #     user = get_object_or_404(Profile,email=self.request.user.email,)
    #     return Ticket.objects.filter(residence=user)

class AddTikComment(generics.ListCreateAPIView):
    permission_classes = (IsAdminUser,)
    queryset =  TickComment.objects.all()
    serializer_class = AddTicketserializer

    def get_serializer_context(self):
        context = super(AddTikComment, self).get_serializer_context()
        context.update({"request": self.request.user})
        return context

    # def get_queryset(self):
    #     ticket = get_object_or_404(Ticket,user=self.request.user,)
    #     return ticket

class DelUpTikAPI(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminUser,)
    queryset =  Ticket.objects.all()
    serializer_class = Tikserializer
    lookup_field= 'id'

    def get_serializer_context(self):
        context = super(DelUpTikAPI, self).get_serializer_context()
        context.update({"request": self.request.user})
        return context



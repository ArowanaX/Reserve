from django.contrib.auth import login,authenticate
from django.core.cache import cache
from django.urls import reverse
from django.shortcuts import redirect,HttpResponse
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import AddCommentserializer, AddRateserializer, AddTicketserializer, OpenTicketserializer, ResidenceSerializer,LoginSerializer,AccountSerializer,Add_indoorimage_serializer,Add_outdoorimage_serializer,ResidenceRegisterSerializer, ShowCommentserializer, ShowRateserializer, ShowTikSerializer
from .models import Profile,Residence,ResidenceOutdoorAlbum,Ticket,TickComment,Comment, rate
import json





#-------------------------create residence(register)----------------------------

class ResidenceAPI(generics.CreateAPIView):
    queryset = Residence.objects.all()
    serializer_class = ResidenceSerializer
    
class ResidenceRegisterAPI(generics.CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ResidenceRegisterSerializer
    def post(self, request):
        ser_data = ResidenceRegisterSerializer(data=request.data)
        if ser_data.is_valid():
            #ser_data.create(ser_data.validated_data)
            ser_data.save()
            #return Response(ser_data.data,status=status.HTTP_201_CREATED)
            return redirect(reverse('Supplier:login'))
        return Response(ser_data.errors,status=status.HTTP_400_BAD_REQUEST)
 

#------------------------------login residence---------------------------------

class LoginAPIView(generics.CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = LoginSerializer

    #authentication_classes = (SessionAuthentication, BasicAuthentication)
    def post(self, request):
        
        ser_data = LoginSerializer(instance = request.data)
        email = request.data['email']
            #ser_data.save()
        #return redirect(reverse('Supplier:account',args=[email]))
        
        #return Response(ser_data.errors,status=status.HTTP_400_BAD_REQUEST)
        password = request.data['password']
        user = authenticate(request, email=email, password=password)
            
        if user is not None:
            try:
                login(request, user)
                print("loged in.....!")
                #return Response(ser_data.data,status=status.HTTP_202_ACCEPTED)
                return redirect(reverse('Supplier:account',args=[email]))
            except:
                print("cant login...!")
                return Response(ser_data.errors,status=status.HTTP_403_FORBIDDEN)

        # return Response(ser_data.errors,status=status.HTTP_400_BAD_REQUEST)

#-----------------------------residence show & edit accont----------------------

class AccountAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Profile.objects.all()
    serializer_class = AccountSerializer
    lookup_field = 'email'
    def get(self, request, email):
        serializer = AccountSerializer(request.user)
        return Response(serializer.data)        
   
class AddOUTImageAlbum(generics.ListCreateAPIView):

    queryset = ResidenceOutdoorAlbum.objects.all()
    serializer_class = Add_outdoorimage_serializer
    lookup_field = 'residence'

class AddINImageAlbum(generics.ListCreateAPIView):

    queryset = ResidenceOutdoorAlbum.objects.all()
    serializer_class = Add_indoorimage_serializer
    lookup_field = 'residence'

class OpenTicketAPI(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset =  Ticket.objects.all()
    serializer_class = OpenTicketserializer

    def get_serializer_context(self):
        context = super(OpenTicketAPI, self).get_serializer_context()
        context.update({"request": self.request.user})
        return context

class ShowTicketAPI(generics.ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = ShowTikSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_serializer_context(self):
        context = super(ShowTicketAPI, self).get_serializer_context()
        context.update({"request": self.request.user})
        return context

    def get_queryset(self):
        user = get_object_or_404(Profile,email=self.request.user.email,)
        return Ticket.objects.filter(residence=user)


class AddTikComment(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset =  Ticket.objects.all()
    serializer_class = AddTicketserializer

    def get_serializer_context(self):
        context = super(AddTikComment, self).get_serializer_context()
        context.update({"request": self.request.user})
        return context

    def get_queryset(self):
        ticket = get_object_or_404(Ticket,user=self.request.user,)
        return ticket

class AddCommentAPI(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset =  Profile.objects.all()
    serializer_class = AddCommentserializer

    def get_serializer_context(self):
        context = super(AddCommentAPI, self).get_serializer_context()
        context.update({"request": self.request.user})
        return context

    def get_queryset(self):
        hotel = Profile.objects.filter(is_Residence=True)
        return hotel

class ShowCommentAPI(generics.ListCreateAPIView):
    queryset =  Comment.objects.all()
    serializer_class = ShowCommentserializer

    def get_serializer_context(self):
        context = super(ShowCommentAPI, self).get_serializer_context()
        context.update({"request": self.request.user})
        return context
    
    def post(self, request, *args, **kwargs):
        serializer = ShowCommentAPI(data=request.data['hotel'])
        comment= Comment.objects.filter(hotel = request.data['hotel']).values_list()
        print(comment)
        return Response(comment)

class AddRateAPI(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset =  Profile.objects.all()
    serializer_class = AddRateserializer

    def get_serializer_context(self):
        context = super(AddRateAPI, self).get_serializer_context()
        context.update({"request": self.request.user})
        return context

    def get_queryset(self):
        hotel = Profile.objects.filter(is_Residence=True)
        return hotel

class ShowRateAPI(generics.ListCreateAPIView):
    queryset =  rate.objects.all()
    serializer_class = ShowRateserializer

    def get_serializer_context(self):
        context = super(ShowRateAPI, self).get_serializer_context()
        context.update({"request": self.request.user})
        return context
    
    def post(self, request, *args, **kwargs):
        serializer = ShowRateAPI(data=request.data['hotel'])
        my_rate= rate.objects.filter(hotel = request.data['hotel']).values_list()
        print(my_rate)
        return Response(my_rate)
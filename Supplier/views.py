from django.contrib.auth import login,authenticate
from django.core.cache import cache
from django.urls import reverse
from django.shortcuts import redirect,HttpResponse
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from rest_framework.response import Response
from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import ResidenceSerializer,LoginSerializer,AccountSerializer,VerificationCodeSerializer,Add_indoorimage_serializer,Add_outdoorimage_serializer,ResidenceRegisterSerializer
from .models import Profile,Residence,ResidenceOutdoorAlbum
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
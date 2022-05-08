from django.contrib.auth import login,authenticate
from django.urls import reverse
from django.shortcuts import redirect,HttpResponse
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from rest_framework.response import Response
from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import ResidenceSerializer,LoginSerializer,ProfilSerializer,Add_indoorimage_serializer,Add_outdoorimage_serializer,ResidenceRegisterSerializer
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
        password = request.data['password']
        user = authenticate(request, email=email, password=password)
        if user is not None: 
            try:
                login(request, user, backend='apps.backend.EmailBackend')
                print("loged in.....!")
                #return redirect(reverse('profile/<str:email>'))
                return Response(ser_data.data,status=status.HTTP_202_ACCEPTED)
            except:
                print("cant login...!")
                return Response(ser_data.errors,status=status.HTTP_403_FORBIDDEN)


#-----------------------------residence show & edit accont----------------------

class ProfileView(generics.RetrieveUpdateAPIView):

    queryset = Profile.objects.all()
    serializer_class = ProfilSerializer
    lookup_field = 'email'

class AddOUTImageAlbum(generics.ListCreateAPIView):

    queryset = ResidenceOutdoorAlbum.objects.all()
    serializer_class = Add_outdoorimage_serializer
    lookup_field = 'residence'

class AddINImageAlbum(generics.ListCreateAPIView):

    queryset = ResidenceOutdoorAlbum.objects.all()
    serializer_class = Add_indoorimage_serializer
    lookup_field = 'residence'
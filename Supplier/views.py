from django.contrib.auth import login,authenticate

from rest_framework.response import Response
from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication, SessionAuthentication

from .serializers import ResidenceSerializer,LoginSerializer,ProfilSerializer,Add_indoorimage_serializer,Add_outdoorimage_serializer
from .models import Residence,ResidenceOutdoorAlbum
import json



#-------------------------create residence(register)----------------------------

class ResidenceAPI(generics.CreateAPIView):
    queryset = Residence.objects.all()
    serializer_class = ResidenceSerializer
 

#------------------------------login residence---------------------------------

class LoginAPI(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    def put(self, request):
        query = Residence.objects.get(name=request.data['name'])
        serializer = LoginSerializer(query,data = request.data)
        data = request.data
        name = data.get('name')
        password = data.get('password')
        print(name,password)
        # user = authenticate(name=name, password=password)
        if serializer.is_valid():
            # if user is not None: 
                try:
                    login(request, query)
                    print("loged in.....!")
                    return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
                except:
                    print("cant login...!")
                    return Response(serializer.errors,status=status.HTTP_403_FORBIDDEN)

            # else:
            #     print("user is none........!")
            #     return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors,status=status.HTTP_410_GONE)


#-----------------------------residence show & edit accont----------------------

class Profile(generics.RetrieveUpdateAPIView):

    queryset = Residence.objects.all()
    serializer_class = ProfilSerializer
    lookup_field = 'name'

class AddOUTImageAlbum(generics.ListCreateAPIView):

    queryset = ResidenceOutdoorAlbum.objects.all()
    serializer_class = Add_outdoorimage_serializer
    lookup_field = 'residence'

class AddINImageAlbum(generics.ListCreateAPIView):

    queryset = ResidenceOutdoorAlbum.objects.all()
    serializer_class = Add_indoorimage_serializer
    lookup_field = 'residence'
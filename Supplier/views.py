from cgitb import lookup
from django.shortcuts import render
from rest_framework.response import Response
from .models import Residence
from rest_framework import generics,status
from rest_framework.views import APIView
from .serializers import ResidenceSerializer,LoginSerializer,ProfilSerializer
from django.contrib.auth import authenticate
from django.contrib.auth import logout,login



class ResidenceAPI(generics.CreateAPIView):
    queryset = Residence.objects.all()
    serializer_class = ResidenceSerializer
 


class LoginAPI(APIView):
    def put(self, request):
        query = Residence.objects.get(name=request.data['name'])
        serializer = LoginSerializer(query,data = request.data)
        if serializer.is_valid():
            login(request, query)
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)



class Profile(generics.RetrieveUpdateAPIView):

    queryset = Residence.objects.all()
    serializer_class = ProfilSerializer
    lookup_field = 'name'

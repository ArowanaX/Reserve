from django.contrib.auth import login

from rest_framework.response import Response
from rest_framework import generics,status
from rest_framework.views import APIView


from .serializers import ResidenceSerializer,LoginSerializer,ProfilSerializer
from .models import Residence




#-------------------------create residence(register)----------------------------

class ResidenceAPI(generics.CreateAPIView):
    queryset = Residence.objects.all()
    serializer_class = ResidenceSerializer
 

#------------------------------login residence---------------------------------

class LoginAPI(APIView):
    def put(self, request):
        query = Residence.objects.get(name=request.data['name'])
        serializer = LoginSerializer(query,data = request.data)
        if serializer.is_valid():
            try:
                login(request, query)
                print("loged in.....!")
                return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
            except:
                print("cant login...!")
        else:
            return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)


#-----------------------------residence show & edit accont----------------------

class Profile(generics.RetrieveUpdateAPIView):

    queryset = Residence.objects.all()
    serializer_class = ProfilSerializer
    lookup_field = 'name'

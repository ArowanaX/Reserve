
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics,status
from .serializers import ReservationSerializer
from .models import Reservation
from Supplier.models import Residence
from Customer.models import Profile

# Create your views here.
class ReservationAPIView(generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    lookup_field = "name"
    
    def get_queryset(self):
        name = self.kwargs.get(self.lookup_url_kwarg)
        hotel = Residence.objects.filter(name=name)
        return hotel
    # def get(self,request,*args,**kwargs):
    #     data = request.GET.get('name')
    #     return Response(data, status=status.HTTP_200_OK)


    # def post(self, request, name):
    #     # def perform_create(self, serializer):
    #     #     serializer.save(reserver=self.request.user)

    #     ser_data = ReservationSerializer(data=request.data)
    #     if ser_data.is_valid():
    #         ser_data.save()
    #         return Response(ser_data.data,status=status.HTTP_201_CREATED)
    #     return Response(ser_data.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def get_serializer_context(self):
         context = super(ReservationAPIView,self).get_serializer_context()
         context.update({"request":self.request})
         print(self.kwargs['name'])
         #print(self.request['name'])
         context.update({"name":self.kwargs['name']})
         return context
         

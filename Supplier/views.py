import email
import profile
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

from .serializers import (ResidenceSerializer,LoginSerializer,AccountSerializer,EmailSerializer,VerificationCodeSerializer,
                          ForgetPasswordSerializer,ServiceSerializer,ServiceUpdateSerializer,MenuSerializer,
                          MenuUpdateSerializer,Add_indoorimage_serializer,Add_outdoorimage_serializer,ResidenceRegisterSerializer,
                          Delete_indoorimage_serializer)

from .models import Profile,Residence,Service,RestaurantMenu,ResidenceOutdoorAlbum,ResidenceIndoorAlbum

from Reserve.utils import send_mail

from .serializers import AddCommentserializer, AddRateserializer, AddTicketserializer, OpenTicketserializer, ResidenceSerializer,LoginSerializer,AccountSerializer,Add_indoorimage_serializer,Add_outdoorimage_serializer,ResidenceRegisterSerializer, ShowCommentserializer, ShowRateserializer, ShowTikSerializer
from .models import Profile,Residence,ResidenceOutdoorAlbum,Ticket,TickComment,Comment, rate
import json
import random





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
                login(request, user)
                print("loged in.....!")
                #return Response(ser_data.data,status=status.HTTP_202_ACCEPTED)
                return redirect(reverse('Supplier:account',args=[email]))
            except:
                print("cant login...!")
                return Response(ser_data.errors,status=status.HTTP_403_FORBIDDEN)

        return Response(ser_data.errors,status=status.HTTP_400_BAD_REQUEST)

#-----------------------------residence show & edit accont----------------------

class AccountAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Profile.objects.all()
    serializer_class = AccountSerializer
    lookup_field = 'email'
    def get(self, request, email):
        serializer = AccountSerializer(request.user)
        return Response(serializer.data)
    
#-----------------------------forget password: Get the verification code & enter new password----------------------   
    
class EmailVerifi(generics.CreateAPIView):
 
    queryset = Profile.objects.all()
    serializer_class = EmailSerializer

    def post(self , request):
        serializer = EmailSerializer(instance=request.data)
        email = serializer.data['email']
        print(email)
        user = Profile.objects.get(email=email)
            
        if user is not None:
            uid=str(random.randint(1,9))
            print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"+uid+">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            send_mail(html=None,text=f'vrification_code is {uid}',subject='Verification_code',from_email='maryamnadeali@yahoo.com',to_emails=[str(email)])
            opt="forget_pass"
            #serializer.save()
             # Send_sms(phone,uid,opt)
            cache.set(email,uid,180)
            return redirect(reverse('Supplier:verification',kwargs={"email":str(email)}))
        return print('user not exist!')    
        
        
class VerificationCodeAPIView(generics.CreateAPIView,):
    queryset = Profile.objects.all()
    serializer_class = VerificationCodeSerializer

    def post(self , request, *args, **kwargs):
        serializer = VerificationCodeSerializer(data=request.data)
        #print(serializer)
        if serializer.is_valid():
            email = str(self.kwargs["email"])
            u_email=cache.get(email)
            code = str(serializer["verification_code"].value)
            if code == u_email:
                if not Profile.objects.filter(email=email).exists:
                    return redirect(reverse('Supplier:register'))
                elif Profile.objects.filter(email=email).exists:
                    return redirect(reverse('Supplier:new_password',kwargs={'email':str(email)}))
                else:
                    return Response(serializer.errors,status=status.HTTP_410_GONE)

            else:
                return Response(serializer.errors,status=status.HTTP_403_FORBIDDEN)

            
class ForgetPasswordAPIView(generics.CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ForgetPasswordSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = ForgetPasswordSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            email = str(self.kwargs["email"])
            user = Profile.objects.get(email=email)
            validatedData = serializer.validated_data
            new_password = validatedData.get('new_password')
            user.set_password(new_password)
            user.save()
            return redirect(reverse('Supplier:login'))
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)   

#---------------------------service card --------------------------------------

class ServiceListAPIView(generics.ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer 
    
    def get_queryset(self):
        user = self.request.user
        residence = Residence.objects.get(name=user)
        print(residence)
        return Service.objects.filter(residence=residence)

class ServiceCreateAPIView(generics.CreateAPIView):
    #permission_classes = (IsAuthenticated,)
    queryset = Profile.objects.all()
    serializer_class = ServiceSerializer        
    
    def get_serializer_context(self):
         context = super(ServiceCreateAPIView,self).get_serializer_context()
         context.update({"request":self.request})
         print(self.request)
         return context 
 
class ServiceUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = (IsAuthenticated,)
    #queryset = Service.objects.all()
    serializer_class = ServiceUpdateSerializer 
    lookup_field = 'residence'
    
    def get_queryset(self):
        user = self.request.user
        residence = Residence.objects.get(name=user)
        print(residence)
        number = self.kwargs['number']
        #return Service.objects.get(number=number)
        service = Service.objects.filter(residence=residence).filter(number=number)
        print(type(service))
        return service
    
   
#---------------------------menu of restaurant --------------------------------  

class MenuListAPIView(generics.ListAPIView):
    #permission_classes = (IsAuthenticated,)
    queryset = RestaurantMenu.objects.all()
    serializer_class = MenuSerializer 
    
    def get_queryset(self):
        user = self.request.user
        residence = Residence.objects.get(name=user)
        print(residence)
        return RestaurantMenu.objects.filter(residence=residence)

class MenuCreateAPIView(generics.CreateAPIView):
    #permission_classes = (IsAuthenticated,)
    queryset = RestaurantMenu.objects.all()
    serializer_class = MenuSerializer
    #lookup_field = 'service'
    
    def get_serializer_context(self):
         context = super(MenuCreateAPIView,self).get_serializer_context()
         context.update({"request":self.request})
         print(self.request)
         print(self.kwargs['id'])
         context.update({"id":self.kwargs['id']})
         return context
    
class MenuUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = (IsAuthenticated,)
    #queryset = RestaurantMenu.objects.all()
    serializer_class = MenuUpdateSerializer 
    lookup_field = 'residence'
    
    def get_queryset(self):
        user = self.request.user
        residence = Residence.objects.get(name=user)
        #print(residence)
        service_id = self.kwargs['id']
        #print(service_id)
        menu = RestaurantMenu.objects.filter(residence=residence).filter(id=service_id)
        #print(menu)
        return menu
    
    def get_serializer_context(self):
         context = super(MenuUpdateAPIView,self).get_serializer_context()
         context.update({"request":self.request})
         print(self.request)
         print(self.kwargs['id'])
         context.update({"id":self.kwargs['id']})
         return context

#---------------------------album of outtdooorimage ----------------------------                           
   
class AddOUTImageAlbumListAPIView(generics.ListAPIView):

    queryset = ResidenceOutdoorAlbum.objects.all()
    serializer_class = Add_outdoorimage_serializer
    
    def get_queryset(self):
        user = self.request.user
        residence = Residence.objects.get(name=user)
        print(residence)
        return ResidenceOutdoorAlbum.objects.filter(residence=residence)
    
class AddOUTImageAlbumCreateAPIView(generics.CreateAPIView):
    #permission_classes = (IsAuthenticated,)
    queryset = Service.objects.all()
    serializer_class = Add_outdoorimage_serializer 
    
    def get_serializer_context(self):
         context = super(AddOUTImageAlbumCreateAPIView,self).get_serializer_context()
         context.update({"request":self.request})
         print(self.request)
         return context
    
class AddOUTImageAlbumUpdateAPIView(generics.DestroyAPIView):
    #permission_classes = (IsAuthenticated,)
    queryset = Service.objects.all()
    serializer_class = Delete_indoorimage_serializer 
    lookup_field = 'residence'
    
    def get_queryset(self):
        outdoor_id = self.kwargs['id']
        outdoor_img = ResidenceOutdoorAlbum.objects.filter(id=outdoor_id)
        return outdoor_img
    
#---------------------------album of intdooorimage ---------------------------- 

class AddINImageAlbumListAPIView(generics.ListAPIView):

    #queryset = ResidenceIndoorAlbum.objects.all()
    serializer_class = Add_indoorimage_serializer
    
    def get_queryset(self):
        user = self.request.user
        residence = Residence.objects.get(name=user)
        print(residence)
        return ResidenceIndoorAlbum.objects.filter(residence=residence)
    
class AddINImageAlbumCreateAPIView(generics.CreateAPIView):
    #permission_classes = (IsAuthenticated,)
    queryset = Service.objects.all()
    serializer_class = Add_indoorimage_serializer 
    
    def get_serializer_context(self):
         context = super(AddINImageAlbumCreateAPIView,self).get_serializer_context()
         context.update({"request":self.request})
         print(self.request)
         return context
    
class AddINImageAlbumUpdateAPIView(generics.DestroyAPIView):
    #permission_classes = (IsAuthenticated,)
    queryset = Service.objects.all()
    serializer_class = Delete_indoorimage_serializer 
    lookup_field = 'residence'
     
    def get_queryset(self):
        indoor_id = self.kwargs['id']
        indoor_img = ResidenceIndoorAlbum.objects.filter(id=indoor_id)
        return indoor_img
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

from rest_framework import serializers

from Reserve.models import Wishlist
from django.shortcuts import get_object_or_404
from .models import *
from pkg_resources import require
from requests import request
from rest_framework import serializers
from rest_framework.utils.field_mapping import get_nested_relation_kwargs
from Customer.models import Profile
from Customer.serializers import UserSerializer
from Supplier.models import Residence
from .models import Reservation
from django.urls import reverse




class ReservationSerializer(serializers.ModelSerializer):
    #owner = serializers.HiddenField(
    #default=serializers.CurrentUserDefault()
#)
    class Meta:
        model = Reservation
        fields = ('date_in','date_out','person_num','type_room','request_user','offers','news','sms')
        extra_kwargs = {
            # 'reserver': {'read_only': True},
            # 'hotel': {'read_only': True},
            # 'order_date': {'required': True},
            'date_in': {'required': True},
            'date_out': {'required': True},
            'person_num': {'required': True},
            'type_room': {'required': True},
            'request_user': {'required': True},
            'offers': {'required': True},
            'news': {'required': True},
            'sms': {'required': True},
            #'hotel': {'required': True},
        }
        
        
    def create(self, validated_data):
        # reserver = validated_data['reserver']
        #my_reserve= self.context["request"]
        
        request = self.context["request"]
        print(request)
        reserver = request.user
        my_hotel = self.context["name"]
        hotel = Residence.objects.get(name=my_hotel)
        to_hotel=Profile.objects.get(residenceTOprofile=hotel)
        print(hotel)
        print(reserver)
        #hotel = Residence.objects.get(name=request.POST.get("name",""))
        #hotel = self.hotel
        #print(hotel)
        print('qqqqqqqqqqqqqqqqqqqq')
        reservation = Reservation.objects.create(
            reserver=reserver,
            #hotel = validated_data['hotel'],
            # order_date=validated_data['order_date'],
            hotel =to_hotel,
            date_in=validated_data['date_in'],
            date_out=validated_data['date_out'],
            person_num=validated_data['person_num'],
            type_room=validated_data['type_room'],
            request_user=validated_data['request_user'],
            offers=validated_data['offers'],
            news=validated_data['news'],
            sms=validated_data['sms']
            
        )
        # Profile.objects.create(profile=reservation, **reserver)
        reservation.save()
        # id=reservation.id
        # print("iiiiiiiiiiiiiiiiiiiidddddddddddddddddd")
        # print(id)
        # reverse('Reserve:addupcomming',kwargs={"reserve":id})
        return reservation

class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ('user','residence')
        extra_kwargs = {
        }
    # def create(self, validated_data):
    #     # phone="0"+str(self.context["phone"])
    #     # user = get_object_or_404(Profile, email=request.user.email) 
    #     request = self.context["request"]
    #     print("reqqqqqqqqqqq")
    #     print(request)
    #     user = get_object_or_404(Profile,id=request.id,) 
    #     print("userrrrrrrrrrr")
    #     print(user)
    #     # wishlist = self.context["request"]
    #     wishlist=Wishlist.objects.get_or_create(user=user)

    #     # user=authenticate(request,id=profile.id,password=phone)
    #     print(wishlist[0])
    #     return wishlist
    
class AddWishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ('residence',)
        extra_kwargs = {
        }
    def create(self, validated_data):
        request = self.context["request"]
        user = get_object_or_404(Profile,email=request.user.email,)
        wishlist=Wishlist.objects.get_or_create(user=user)[0]
        residence= Residence.objects.get(pk=validated_data['residence'][0])
        wishlist.residence.add(residence)
        wishlist.save()
        return wishlist

class DelWishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ('residence',)
        extra_kwargs = {
        }
    def create(self, validated_data):
        request = self.context["request"]
        user = get_object_or_404(Profile,email=request.user.email,)
        wishlist=Wishlist.objects.get_or_create(user=user)[0]
        print(type(validated_data['residence'][0]))
        residence= Residence.objects.get(pk=validated_data['residence'][0])
        wishlist.residence.remove(residence)
        wishlist.save()
        return wishlist

class UpcommingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ('user','residence','reserve')
        extra_kwargs = {
        }




class AddUpcommingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upcomming
        fields = ('user','reserve')
        extra_kwargs = {
        }
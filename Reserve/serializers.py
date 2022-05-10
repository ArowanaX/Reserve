from django.http import HttpResponseForbidden
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from Reserve.models import Wishlist
from django.shortcuts import get_object_or_404
from .models import *
from pkg_resources import require
from requests import delete, request
from rest_framework import serializers
from rest_framework.utils.field_mapping import get_nested_relation_kwargs
from Customer.models import Profile
from Customer.serializers import UserSerializer
from Supplier.models import Residence
from .models import Reservation
from django.urls import reverse




class ReservationSerializer(serializers.ModelSerializer):
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
        
        request = self.context["request"]
        reserver = request.user
        my_hotel = self.context["name"]
        hotel = Residence.objects.get(name=my_hotel)
        to_hotel=Profile.objects.get(residenceTOprofile=hotel)
        reservation = Reservation.objects.create(
            reserver=reserver,
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
        reservation.save()
        history=History.objects.get_or_create(user=reserver)[0]
        history.reserve.add(reservation)
        history.save()

        return reservation

class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ('user','residence')
        extra_kwargs = {
        }
    
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
        model = Upcomming
        fields = ('user','reserve')
        extra_kwargs = {
        }




class AddUpcommingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upcomming
        fields = ('reserve',)
        extra_kwargs = {
        }
    def create(self, validated_data):
        request = self.context["request"]
        user = get_object_or_404(Profile,email=request.user.email,)
        upcomming=Upcomming.objects.get_or_create(user=user)[0]
        res=validated_data['reserve'][0]
        reserve= Reservation.objects.get(id=res.id)
        if reserve.reserver==user:
            upcomming.reserve.add(reserve)
            upcomming.save()
            return upcomming
        else:
            return upcomming

class DelUpcommingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upcomming
        fields = ('reserve',)
        extra_kwargs = {
        }
    def create(self, validated_data):
        request = self.context["request"]
        user = get_object_or_404(Profile,email=request.user.email,)
        upcomming=Upcomming.objects.get_or_create(user=user)[0]
        res=validated_data['reserve'][0]
        reserve= Reservation.objects.get(id=res.id)
        upcomming.reserve.remove(reserve)
        upcomming.save()
        return upcomming

class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ('user','reserve')
        extra_kwargs = {
            'reserver': {'read_only': True},
            'user': {'read_only': True},
        }
    # def create(self, validated_data):
    #     request = self.context["request"]
    #     user = get_object_or_404(Profile,email=request.user.email,)
    #     history=History.objects.get_or_create(user=user)[0]
    #     res=validated_data['reserve'][0]
    #     reserve= Reservation.objects.get(id=res.id)
    #     history.reserve.add(reserve)
    #     history.save()
    #     return history
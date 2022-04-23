

from django.utils.translation import gettext as _
from django.contrib.auth.models import User

import random
from django.core.cache import cache
# from requests import request


from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from Customer.utils import Send_sms
from django.shortcuts import redirect
from django.contrib.auth import login

from .models import User


class PhoneSerializer(serializers.ModelSerializer):
    phone = serializers.CharField()
    class Meta:
        model = User
        fields = ('phone',)
        extra_kwargs = {
            'phone': {'required': True},
        }

class ActivateSerializer(serializers.ModelSerializer):
    activate_code = serializers.CharField()
    class Meta:
        model = User
        fields = ('activate_code',)
        extra_kwargs = {
            'activate_code': {'required': True},
        }

    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name','email')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
        }
    def create(self, validated_data):
        user = User.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone="0"+str(self.context["phone"]),
            email=validated_data['email']
        )
        user.save()
        
        request = self.context["request"]
        
        try:
            login(request,User.objects.get(phone="0"+str(self.context["phone"])))
            
        except:
            print("cant find...!")
        
        return user

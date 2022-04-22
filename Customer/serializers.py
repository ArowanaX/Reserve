from wsgiref import validate
from django.utils.translation import gettext as _
from django.contrib.auth.models import User

import random
from django.core.cache import cache


from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from Customer.utils import Send_sms
from django.shortcuts import redirect


from .models import User


class PhoneSerializer(serializers.ModelSerializer):
    phone = serializers.IntegerField()
    class Meta:
        model = User
        fields = ('phone',)
        extra_kwargs = {
            'phone': {'required': True},
        }

class UserSerializer(serializers.ModelSerializer):
    pass
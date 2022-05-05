import profile
from wsgiref.validate import validator
from django.utils.translation import gettext as _
# from django.contrib.auth.models import User
from django.core.cache import cache
from django.contrib.auth import login , authenticate
from requests import request
from rest_framework.utils.field_mapping import get_nested_relation_kwargs
from rest_framework.validators import UniqueValidator
from rest_framework import serializers


from .models import User,Profile


# from Customer.utils import Send_sms
# from django.shortcuts import redirect




#-------------------------------------for type of user (user,Residence)----------

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("is_User","is_Residence")
        extra_kwargs = {
            # 'is_User':{'required': True},
            # 'is_Residence': {'required': True},
        }

    

#-----------------------------get phone from User-----------------------------    

class PhoneSerializer(serializers.ModelSerializer):
    phone = serializers.CharField()
    class Meta:
        model = Profile
        fields = ('phone',)
        extra_kwargs = {
            'phone': {'required': True},
        }


#----------------------------get activate code from user--------------------

class ActivateSerializer(serializers.ModelSerializer):
    activate_code = serializers.CharField()
    class Meta:
        model = Profile
        fields = ('activate_code',)
        extra_kwargs = {
            'activate_code': {'required': True},
        }

    

#------------------------------------- other user fields & create--------------------

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name','email')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
        }
    def create(self, validated_data):
        user = Profile.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email']
        )
        phone="0"+str(self.context["phone"])
        user.set_password(phone)
        user.save()
        user.userTOprofile= User.objects.create(
                phone="0"+str(self.context["phone"]),
                profile= user
            )
        profile=Profile.objects.latest('date_joined').id
        request = self.context["request"]
        user=authenticate(request,id=profile,password=phone)
        
    
        try:
            login(request,user)
            print("user loged in....!")
            return user 

        except:
            print("cant log...!")
            return user


class UserAccontSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = User
        fields = ('phone', 'point')
        extra_kwargs = {
            'phone': {'read_only': False},
            'point': {'read_only': True},
            
        }

class AccontSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields =  ('first_name','last_name','email','userTOprofile')
        extra_kwargs = {
            'first_name': {'read_only': False},
            'last_name': {'read_only': False},
            'email': {'read_only': True},
            'userTOprofile': {'read_only': False},
        }
        depth = 1
        
    def build_nested_field(self, field_name, relation_info, nested_depth):
       
        if field_name == 'userTOprofile': 
            field_class = UserAccontSerializer
            field_kwargs = get_nested_relation_kwargs(relation_info)
            return field_class, field_kwargs
        return super().build_nested_field(field_name, relation_info, nested_depth)



class RecoverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name','email')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
        }
    def create(self, validated_data):
        phone="0"+str(self.context["phone"])
        profile = Profile.objects.get(userTOprofile=phone) 
        request = self.context["request"]
        user=authenticate(request,id=profile.id,password=phone)
        print(user)
        try:
            login(request,user)
            print("user loged in....!")
            return user 

        except:
            print("cant log...!")
            return user

        
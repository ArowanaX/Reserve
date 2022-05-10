from dataclasses import fields
import email
#from typing_extensions import Required
#from typing_extensions import Self
from django.contrib.auth.password_validation import validate_password
from pkg_resources import require
from rest_framework.utils.field_mapping import get_nested_relation_kwargs
from django.contrib.auth import login,authenticate


from rest_framework import serializers


from .models import Residence,ResidenceOutdoorAlbum,ResidenceIndoorAlbum
from Customer.models import Profile


#-----------------------------------residence register & validator-------------


class ResidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Residence
        fields =  ('name','city','address','img','type','tag','service_hours_start','service_hours_end','max_reserve','detail','phone')
        
        extra_kwargs = {
            'name': {'required': True},
            'address': {'required': True},
            # 'img': {'required': True},
            'type': {'required': True},
            # 'tag': {'required': True},
            'service_hours_start': {'required': True},
            'service_hours_end': {'required': True},
            'max_reserve': {'required': True},
            # 'detail': {'required': True},
            # 'email': {'required': True},
            'phone': {'required': True},
            'password': {'required': True},
            're_password': {'required': True},
        }

        
class ResidenceRegisterSerializer(serializers.ModelSerializer):
    residenceTOprofile = ResidenceSerializer(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    re_password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = Profile
        fields = ('first_name','last_name','email','residenceTOprofile','password','re_password')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
        }
        
        depth = 1
        
    def build_nested_field(self, field_name, relation_info, nested_depth):
       
        if field_name == 'residenceTOprofile': 
            field_class = ResidenceSerializer
            field_kwargs = get_nested_relation_kwargs(relation_info)
            return field_class, field_kwargs
        return super().build_nested_field(field_name, relation_info, nested_depth)
    
    def create(self, validated_data):
        del validated_data['re_password']
        residence_data = validated_data.pop('residenceTOprofile', None)
        profile = Profile.objects.create(**validated_data)
        profile.is_Residence = True
        Residence.objects.create(profile=profile, **residence_data)
        profile.set_password(validated_data['password'])
        profile.save()
        return profile
    
        
    def validate(self, attrs):
        if attrs['password'] != attrs['re_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    

#--------------------------------------residence login with password & name---------------

class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = Profile
        fields =  ('email','password')
        extra_kwargs = {
            'email': {'required': True},
            'password': {'required': True},
            }
    # def create(self, validated_data):
    #     email = validated_data['email']
    #     password = validated_data['password']
    #     request = self.context["request"]
    #     user=authenticate(request,email=email,password=password)
        
    
    #     try:
    #         login(request,user)
    #         print("user loged in....!")
    #         return user 

    #     except:
    #         print("cant log...!")
    #         return user
    

#---------------------------residence show & edit acconts----------------------------

class ResidenceAccountSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Residence
        fields =  ('name','city','address','img','type','tag','service_hours_start','service_hours_end','max_reserve','detail','phone')
        
        extra_kwargs = {
            'name': {'read_only': True},
            'address': {'read_only': False},
            # 'img': {'read_only': False},
            'type': {'read_only': False},
            # 'tag': {'read_only': False},
            'service_hours_start': {'read_only': False},
            'service_hours_end': {'read_only': False},
            'max_reserve': {'read_only': False},
            # 'detail': {'read_only': False},
            'phone': {'read_only': True},
        }

    
class AccountSerializer(serializers.ModelSerializer):
    residenceTOprofile = ResidenceAccountSerializer()
    class Meta:
        model = Profile
        fields =  ('first_name','last_name','email','residenceTOprofile')
        extra_kwargs = {
            'first_name': {'read_only': False},
            'last_name': {'read_only': False},
            'email': {'read_only': True},
        }
        
        depth = 1
        
    def build_nested_field(self, field_name, relation_info, nested_depth):
       
        if field_name == 'residenceTOprofile': 
            field_class = ResidenceAccountSerializer
            field_kwargs = get_nested_relation_kwargs(relation_info)
            return field_class, field_kwargs
        return super().build_nested_field(field_name, relation_info, nested_depth)
    
    def update(self, instance, validated_data):
        # CHANGE "'residenceTOprofile'" here to match your one-to-one field name
        if 'residenceTOprofile' in validated_data:
            nested_serializer = self.fields['residenceTOprofile']
            nested_instance = instance.residenceTOprofile
            nested_data = validated_data.pop('residenceTOprofile')

            # Runs the update on whatever serializer the nested data belongs to
            nested_serializer.update(nested_instance, nested_data)

        # Runs the original parent update(), since the nested fields were
        # "popped" out of the data
        return super(AccountSerializer, self).update(instance, validated_data)
            
        

class Add_outdoorimage_serializer(serializers.ModelSerializer):
    class Meta:
        model = ResidenceOutdoorAlbum
        fields ='__all__'
        extra_kwargs = {}

class Add_indoorimage_serializer(serializers.ModelSerializer):
    class Meta:
        model = ResidenceIndoorAlbum
        fields ='__all__'
        extra_kwargs = {}
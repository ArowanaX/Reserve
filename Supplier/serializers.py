from requests import Response
from rest_framework import serializers
from .models import Residence
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import logout,login
from django.contrib.auth import authenticate



class ResidenceSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    re_password = serializers.CharField(write_only=True, required=True)
    
  

    class Meta:
        model = Residence
        fields =  ('name', 'user','address','img','type','tag','service_hours_start','service_hours_end','max_reserve','detail','password','re_password')
        # fields = '__all__'
        extra_kwargs = {
            'name': {'required': True},
            'user': {'required': True},
            'address': {'required': True},
            # 'img': {'required': True},
            'type': {'required': True},
            # 'tag': {'required': True},
            'service_hours_start': {'required': True},
            'service_hours_end': {'required': True},
            'max_reserve': {'required': True},
            # 'detail': {'required': True},
            'password': {'required': True},
            're_password': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['re_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        residence = Residence.objects.create(
            name=validated_data['name'],
            user=validated_data['user'],
            address=validated_data['address'],
            img=validated_data['img'],
            type=validated_data['type'],
            tag=validated_data['tag'],
            service_hours_start=validated_data['service_hours_start'],
            service_hours_end=validated_data['service_hours_end'],
            max_reserve=validated_data['max_reserve'],
            detail=validated_data['detail']
        )
        residence.set_password(validated_data['password'])
        residence.save()

        return residence
    

class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = Residence
        fields =  ('name','password')
        extra_kwargs = {
            'name': {'required': True},
            'password': {'required': True},
            }
    # def update(self, instance, validated_data):
    #     print("baz hello")
    #     # residence = Residence.objects.get(
    #     #     name=validated_data['name'],
    #     # )
    #     residence=authenticate(name=validated_data['name'],password=validated_data['password'])
    #     print(residence)
    #     request = self.context["request"]
    #     print(request)
    #     try:
    #         login(request, residence)
    #     except:
    #         print("cant...")
    #     return super().update(instance, validated_data)
    # def create(self, validated_data):
    #     print("hello")
    #     residence=authenticate(name=validated_data['name'],password=validated_data['password'])

    #     print(residence)
    #     request = self.context["request"]
    #     print(request)
    #     try:
    #         login(request, residence)
    #     except:
    #         print("cant...")
    #     return None
class ProfilSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    
    class Meta:
        model = Residence
        fields =  ('name','user', 'address','img','type','tag','service_hours_start','service_hours_end','max_reserve','detail','password')
        extra_kwargs = {
            'name': {'required': True},
            'user': {'required': True},
            'address': {'required': True},
            # 'img': {'required': True},
            'type': {'required': True},
            # 'tag': {'required': True},
            'service_hours_start': {'required': True},
            'service_hours_end': {'required': True},
            'max_reserve': {'required': True},
            # 'detail': {'required': True},
            'password': {'required': True},
        }
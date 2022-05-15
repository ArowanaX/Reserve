from dataclasses import fields
import email
from turtle import update
#from typing_extensions import Required
#from typing_extensions import Self
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from django.forms import CharField
from django.shortcuts import get_object_or_404
from pkg_resources import require
from rest_framework.utils.field_mapping import get_nested_relation_kwargs
from django.contrib.auth import login,authenticate


from rest_framework import serializers


from .models import Residence,ResidenceOutdoorAlbum,ResidenceIndoorAlbum, Service, RestaurantMenu
from Customer.models import Profile


#-----------------------------------residence register & validator-------------


class ResidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Residence
        fields =  ('name','city','address','img','type','service_hours_start','service_hours_end','max_reserve','detail','phone')
        
        extra_kwargs = {
            'name': {'required': True},
            'address': {'required': True},
            # 'img': {'required': True},
            'type': {'required': True},
            #'tag': {'required': True},
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
    
#---------------------------forget password: Get the verification code & enter new password ----------------------------

class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("email",)
        extra_kwargs = {
            "email": {"required":True}       
        }
    
class VerificationCodeSerializer(serializers.ModelSerializer):
    verification_code = serializers.CharField()
    class Meta:
        model = Profile
        fields = ('verification_code',)
        extra_kwargs = {
            'verification_code': {'required': True},
        }

class ForgetPasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(write_only=True, required=True) 
    re_new_password = serializers.CharField(write_only=True, required=True) 
    class Meta:
        model = Profile
        fields = ('new_password','re_new_password')
        extra_kwargs = {
            'new_password': {'required': True},
            're_new_password': {'required': True},
            
        }
        
    def validate(self, attrs):
        if attrs['new_password'] != attrs['re_new_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
#---------------------------service card ----------------------------

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ("title","number","type","state","faciliti")
        extra_kwargs = {
            'title': {'required': True},
            'number': {'required': True},
            'type': {'required': True},
            'state': {'required': True},
            'faciliti': {'required': True},
            #'id': {'read_only': True},
        }
      
    def create(self, validated_data):
        request = self.context["request"]
        residence = request.user
        #print(residence)
        my_residence= Residence.objects.get(name=residence)
        #print(my_residence)
        service = Service.objects.create(
            residence=my_residence,
            title=validated_data['title'],
            number=validated_data['number'],
            type=validated_data['type'],
            state=validated_data['state'],
            faciliti=validated_data['faciliti'],
        )
        #service.save()
        #history=History.objects.get_or_create(user=reserver)[0]
        #history.reserve.add(reservation)
        #history.save()

        return service
    
class ServiceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ("title","number","type","state","faciliti","id")
        extra_kwargs = {
            'title': {'read_only': False},
            'number': {'read_only': True},
            'type': {'read_only': False},
            'state': {'read_only': False},
            'faciliti': {'read_only': False},
            'id': {'read_only': True},
        }
        
#---------------------------menu of restaurant ----------------------------  

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantMenu  
        fields = ("title","describtion","price",'id')
        extra_kwargs = {
            'title': {'required': True},
            'describtion': {'required': True},
            'price': {'required': True},
            'id': {'read_only': True},
        } 
        
    def create(self, validated_data):
        request = self.context["request"]
        residence = request.user
        #print(residence)
        my_residence = Residence.objects.get(name=residence)
        service_id = self.context["id"]
        my_service = Service.objects.get(id=service_id)
        #to_hotel=Profile.objects.get(residenceTOprofile=hotel)
        #my_service = Service.object.get()
        print(my_service)
        menu = RestaurantMenu.objects.create(
            residence=my_residence,
            service=my_service,
            title=validated_data['title'],
            describtion=validated_data['describtion'],
            price=validated_data['price'],
        )
        #menu.save()
        #history=History.objects.get_or_create(user=reserver)[0]
        #history.reserve.add(reservation)
        #history.save()

        return menu  
    
class MenuUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantMenu
        fields = ("title","describtion","price","id")
        extra_kwargs = {
            'title': {'read_only': False},
            'describtion': {'read_only': False},
            'price': {'read_only': False},
            'id': {'read_only': True},
        }
        
    def update(self,instance,validated_data):
        request = self.context["request"]
        residence = request.user
        #print(residence)
        my_residence = Residence.objects.get(name=residence)
        menu_id = self.context["id"]
        my_menu = RestaurantMenu.objects.get(id=menu_id)
        title_service = my_menu.title
        instance.residance = my_residence
        instance.title = validated_data.get('title',instance.title)
        instance.describtion = validated_data.get('describtion',instance.describtion)
        instance.price = validated_data.get('price',instance.price)
        instance.save()
        return instance
        
 
 #---------------------------album of outdooorimage ----------------------------         
class Add_outdoorimage_serializer(serializers.ModelSerializer):
    class Meta:
        model = ResidenceOutdoorAlbum
        fields = ('img_name','img_outdoor')
        extra_kwargs = {
            'img_name': {'required':True},
            'img_outdoor': {'required':True},
        }
        
    def create(self, validated_data):
        request = self.context["request"]
        residence = request.user
        #print(residence)
        my_residence = Residence.objects.get(name=residence)
        # service_id = self.context["id"]
        # my_service = Service.objects.get(id=service_id)
        #to_hotel=Profile.objects.get(residenceTOprofile=hotel)
        #my_service = Service.object.get()
        # print(my_service)
        outdoor = ResidenceOutdoorAlbum.objects.create(
            residence=my_residence,
            img_name=validated_data['img_name'],
            img_outdoor=validated_data['img_outdoor'],
        )
        #menu.save()
        #history=History.objects.get_or_create(user=reserver)[0]
        #history.reserve.add(reservation)
        #history.save()

        return outdoor 
        
class Delete_outdoorimage_serializer(serializers.ModelSerializer):
    class Meta:
        model = ResidenceIndoorAlbum
        fields = ('img_name','img_outdoor',"id")
        extra_kwargs = {
            'img_name': {'read_only':False},
            'img_outdoor': {'read_only':False},
            'id': {'read_only': True},
        }

#---------------------------album of intdooorimage ---------------------------- 

class Add_indoorimage_serializer(serializers.ModelSerializer):
    class Meta:
        model = ResidenceIndoorAlbum
        fields = ('img_name','img_indoor')
        extra_kwargs = {
            'img_name': {'required':True},
            'img_indoor': {'required':True},
        }
        
    def create(self, validated_data):
        request = self.context["request"]
        residence = request.user
        #print(residence)
        my_residence = Residence.objects.get(name=residence)
        # service_id = self.context["id"]
        # my_service = Service.objects.get(id=service_id)
        #to_hotel=Profile.objects.get(residenceTOprofile=hotel)
        #my_service = Service.object.get()
        # print(my_service)
        indoor = ResidenceIndoorAlbum.objects.create(
            residence=my_residence,
            img_name=validated_data['img_name'],
            img_indoor=validated_data['img_indoor'],
        )
        #menu.save()
        #history=History.objects.get_or_create(user=reserver)[0]
        #history.reserve.add(reservation)
        #history.save()

        return indoor  
        
class Delete_indoorimage_serializer(serializers.ModelSerializer):
    class Meta:
        model = ResidenceIndoorAlbum
        fields = ('img_name','img_indoor','id')
        extra_kwargs = {
            'img_name': {'read_only':False},
            'img_indoor': {'read_only':False},
            'id': {'read_only': True},
        }
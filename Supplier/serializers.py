from dataclasses import fields

from django.contrib.auth.password_validation import validate_password
from django.forms import CharField
from pkg_resources import require
from rest_framework.utils.field_mapping import get_nested_relation_kwargs
from django.contrib.auth import login,authenticate


from rest_framework import serializers


from .models import *
from Customer.models import Profile


#-----------------------------------residence register & validator-------------


class ResidenceSerializer(serializers.ModelSerializer):
    # location = serializers.ListField(child=serializers.DecimalField(max_digits=7, decimal_places=5), max_length=2, min_length=2)

    class Meta:
        model = Residence
        fields =  ('name','city','address','img','type','tag','service_hours_start','service_hours_end','max_reserve','detail','phone','location',)
        
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
    

# class LocationSerializer(serializers.Serializer):
#     location = serializers.ListField(child=serializers.DecimalField(max_digits=7, decimal_places=5), max_length=2, min_length=2)
    
#     def create(self, validated_data):
#         validated_data['location_point'] = Point(validated_data.pop('location'))
#         location = Location(**validated_data)
#         location.save()
#         return location
        
#     def update(self, instance, validated_data):
#         if validated_data.get('location'):
#             instance.location_point = Point(validated_data.pop('location'))
#         return instance

#     def to_representation(self, instance):
#         instance.location = json.loads(instance.location_point.geojson)['coordinates']
#         instance = super().to_representation(instance)
#         return instance
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

class OpenTicketserializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields =  ('title','describtion','att_file')
        extra_kwargs = {
            'title': {'required': True},
            'describtion': {'required': True},
            'att_file': {'required': False},
        }

    def create(self, validated_data):
        user= self.context["request"]
        ticket = Ticket.objects.create(
            title=validated_data['title'],
            describtion=validated_data['describtion'],
            att_file=validated_data['att_file'],
            residence=user
        )
        ticket.save()
        return ticket 


class ShowTikSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields =  ('title','CommentToTicket')
        extra_kwargs = {
            'title': {'read_only': True,'label':"title"},
            'CommentToTicket': {'read_only': True},
        }
        depth = 1
        
    def build_nested_field(self, field_name, relation_info, nested_depth):
       
        if field_name == 'CommentToTicket': 
            field_class = NastedTicketserializer
            field_kwargs = get_nested_relation_kwargs(relation_info)
            return field_class, field_kwargs
        return super().build_nested_field(field_name, relation_info, nested_depth)
    



class AddTicketserializer(serializers.ModelSerializer):
    class Meta:
        model = TickComment
        fields =  ('ticket','comment')
        extra_kwargs = {
            'comment': {'required': True},
            'ticket': {'required': True,'label':"ticket"},
        }
    def create(self, validated_data):
        ticket= validated_data['ticket']
        print(self)
        comment = TickComment.objects.create(
            user=self.context["request"],
            ticket=ticket,
            comment=validated_data['comment'],
        )
        comment.save()
        return comment 

class NastedTicketserializer(serializers.ModelSerializer):
    class Meta:
        model = TickComment
        fields =  ('ticket','comment')
        extra_kwargs = {
            'comment': {'required': True},
            'ticket': {'required': True,'label':"ticket"},
        }
        

class AddCommentserializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields =  ('hotel','comment')
        extra_kwargs = {
            'comment': {'required': True},
            'hotel': {'required': True},
        }
    def create(self, validated_data):
        request = self.context['request']
        comment= Comment.objects.create(
            user=request,
            hotel=validated_data['hotel'],
            comment=validated_data['comment'],
            )
        comment.save()
        return comment

class ShowCommentserializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields =  ('user','hotel','comment')
        extra_kwargs = {
            'user': {'read_only': True},
            'comment': {'read_only': True},
            'hotel': {'required': True},
        }
    def create(self, validated_data):
        request = self.context['request']
        return request

class AddRateserializer(serializers.ModelSerializer):
    class Meta:
        model = rate
        fields =  ('hotel','rate')
        extra_kwargs = {
            'rate': {'required': True},
            'hotel': {'required': True},
        }
    def create(self, validated_data):
        request = self.context['request']
        my_rate= rate.objects.create(
            user=request,
            hotel=validated_data['hotel'],
            rate=validated_data['rate'],
            )
        my_rate.save()
        return my_rate

class ShowRateserializer(serializers.ModelSerializer):
    class Meta:
        model = rate
        fields =  ('user','hotel','rate')
        extra_kwargs = {
            'user': {'read_only': True},
            'rate': {'read_only': True},
            'hotel': {'required': True},
        }
    def create(self, validated_data):
        request = self.context['request']
        return request
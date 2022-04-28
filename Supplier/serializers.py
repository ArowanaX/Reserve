import email
from django.contrib.auth.password_validation import validate_password


from rest_framework import serializers


from .models import Residence,ResidenceOutdoorAlbum,ResidenceIndoorAlbum
from Customer.models import Profile


#-----------------------------------residence register & validator-------------


class ResidenceSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    re_password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = Residence
        fields =  ('name','city','address','img','type','tag','service_hours_start','service_hours_end','max_reserve','detail','email','phone','password','re_password')
        
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


    def validate(self, attrs):
        if attrs['password'] != attrs['re_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        residence = Residence.objects.create(
            name=validated_data['name'],
            profile=Profile.objects.latest('date_joined'),
            city = validated_data['city'],
            address=validated_data['address'],
            img=validated_data['img'],
            type=validated_data['type'],
            tag=validated_data['tag'],
            service_hours_start=validated_data['service_hours_start'],
            service_hours_end=validated_data['service_hours_end'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            max_reserve=validated_data['max_reserve'],
            detail=validated_data['detail']
        )
        residence.profile.set_password(validated_data['password'])
        residence.save()

        return residence
    

#--------------------------------------residence login with password & name---------------

class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = Residence
        fields =  ('name','password')
        extra_kwargs = {
            'name': {'required': True},
            'password': {'required': True},
            }
    

#---------------------------residence show & edit acconts----------------------------

class ProfilSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    # outdoor_img= serializers.PrimaryKeyRelatedField(many=True,read_only='True')
    class Meta:
        model = Residence
        fields =  ('name','outdootTOresident','indootTOresident','city','address','img','type','tag','service_hours_start','service_hours_end','max_reserve','detail','email','phone','password')
        extra_kwargs = {
            # 'name': {'required': True},
            # 'profile': {'required': True},
            # 'address': {'required': True},
            # 'img': {'required': True},
            # 'type': {'required': True},
            # 'tag': {'required': True},
            # 'service_hours_start': {'required': True},
            # 'service_hours_end': {'required': True},
            # 'max_reserve': {'required': True},
            # 'detail': {'required': True},
            'password': {'required': True},
        }

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
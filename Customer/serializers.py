from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from django.core.cache import cache
from django.contrib.auth import login , authenticate


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
            userTOprofile= User.objects.create(
                phone="0"+str(self.context["phone"]),
                profile= Profile.objects.latest('date_joined')
            ),
            email=validated_data['email']
        )
        phone="0"+str(self.context["phone"])
        user.set_password(phone)
        user.save()
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

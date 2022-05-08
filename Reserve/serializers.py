from pkg_resources import require
from requests import request
from rest_framework import serializers
from rest_framework.utils.field_mapping import get_nested_relation_kwargs
from Customer.models import Profile
from Customer.serializers import UserSerializer
from Supplier.models import Residence
from .models import Reservation


class ReservationSerializer(serializers.ModelSerializer):
    #owner = serializers.HiddenField(
    #default=serializers.CurrentUserDefault()
#)
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
        # reserver = validated_data['reserver']
        #my_reserve= self.context["request"]
        
        request = self.context["request"]
        print(request)
        reserver = request.user
        my_hotel = self.context["name"]
        hotel = Residence.objects.get(name=my_hotel)
        to_hotel=Profile.objects.get(residenceTOprofile=hotel)
        print(hotel)
        print(reserver)
        #hotel = Residence.objects.get(name=request.POST.get("name",""))
        #hotel = self.hotel
        #print(hotel)
        print('qqqqqqqqqqqqqqqqqqqq')
        reservation = Reservation.objects.create(
            reserver=reserver,
            #hotel = validated_data['hotel'],
            # order_date=validated_data['order_date'],
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
        # Profile.objects.create(profile=reservation, **reserver)
        reservation.save()
        return reservation
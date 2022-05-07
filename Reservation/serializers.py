from rest_framework import serializers

from Reservation.models import Wishlist
from django.shortcuts import get_object_or_404
from .models import *




class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ('user','reserve')
        extra_kwargs = {
        }
    # def create(self, validated_data):
    #     # phone="0"+str(self.context["phone"])
    #     # user = get_object_or_404(Profile, email=request.user.email) 
    #     request = self.context["request"]
    #     print("reqqqqqqqqqqq")
    #     print(request)
    #     user = get_object_or_404(Profile,id=request.id,) 
    #     print("userrrrrrrrrrr")
    #     print(user)
    #     # wishlist = self.context["request"]
    #     wishlist=Wishlist.objects.get_or_create(user=user)

    #     # user=authenticate(request,id=profile.id,password=phone)
    #     print(wishlist[0])
    #     return wishlist
    
class AddWishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ('user','reserve')
        extra_kwargs = {
        }
    # def update(self, instance, validated_data):


    #     return super().update(instance, validated_data)
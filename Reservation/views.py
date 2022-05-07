from rest_framework import generics,status
from Customer.models import *
from Reservation.serializers import *
from .models import *
from django.shortcuts import get_object_or_404
from rest_framework.response import Response





class ShowWishlistAPI(generics.ListAPIView):
    serializer_class = WishlistSerializer
    
    def get_serializer_context(self):
        context = super(ShowWishlistAPI, self).get_serializer_context()
        context.update({"request": self.request.user})
        return context

    def get_queryset(self):
        user = get_object_or_404(Profile,id=self.request.user.id,)
        wishlist=Wishlist.objects.get_or_create(user=user)[0]
        return Wishlist.objects.filter(user=user)

class AddWishlistAPI(generics.UpdateAPIView):
    serializer_class = AddWishlistSerializer

    def get_queryset(self):
        user = get_object_or_404(Profile,id=self.request.user.id,)
        wishlist=Wishlist.objects.get_or_create(user=user)[0]
        return Wishlist.objects.get(user=user)

    def put(self, request, *args, **kwargs):
        user = get_object_or_404(Profile,id=self.request.user.id,)
        wishlist=Wishlist.objects.get_or_create(user=user)[0]
        reserve= get_object_or_404(Reserve, pk=request.POST.get("id"))
        wishlist.reserve.add(reserve)
        wishlist.save()
        return Wishlist.objects.get(user=user)
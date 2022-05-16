from dataclasses import fields

from django.contrib.auth.password_validation import validate_password
from django.forms import CharField
from django.shortcuts import get_object_or_404
from pkg_resources import require
from rest_framework.utils.field_mapping import get_nested_relation_kwargs
from django.contrib.auth import login,authenticate


from rest_framework import serializers

from Supplier.models import *


from .models import *
from Customer.models import Profile


#-----------------------------------residence register & validator-------------
class NastedTicketserializer(serializers.ModelSerializer):
    class Meta:
        model = TickComment
        fields =  ('ticket','comment')
        extra_kwargs = {
            'comment': {'required': True},
            'ticket': {'required': True,'label':"ticket"},
        }

class OpenTicketserializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields =  ('residence','title','describtion','att_file')
        extra_kwargs = {
            'title': {'required': True},
            'describtion': {'required': True},
            'att_file': {'required': False},
            'residence': {'required': False},
        }

    def create(self, validated_data):
        adminprf= self.context["request"]
        print(adminprf)
        print("LLLLLLLLLLLLLLLLLLLLLLLLLLLLLl")
        admin=get_object_or_404(Profile,pk=adminprf.pk)
        print(admin)
        print(type(admin))
        # print(type(validated_data['residence']))
        print("reeeeeeeeeeeeeees")
        # residence=Profile.objects.get(residenceTOprofile=validated_data['residence'])
        residence=get_object_or_404(Residence,pk=validated_data['residence'])
        prof=get_object_or_404(Profile,residenceTOprofile=residence)
        print(residence)
        print(prof)
        ticket = Ticket.objects.create(
            title=validated_data['title'],
            describtion=validated_data['describtion'],
            att_file=validated_data['att_file'],
            residence=prof,
            admin = admin,
        )
        print("salam")
        # ticket.admin.set(admin.pk)
        print("byby")

        ticket.save()
        print("ooodafez")
        return ticket 


class ShowTikSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields =  ('admin','residence','title','CommentToTicket')
        extra_kwargs = {
            'title': {'read_only': True,'label':"title"},
            'CommentToTicket': {'read_only': True},
            'residence': {'read_only': True},
            'admin': {'read_only': True},
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

class Tikserializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields =  ('id','residence','title','describtion','att_file','status')
        extra_kwargs = {
            # 'id': {'required': True},
            'title': {'required': True},
            'describtion': {'required': True},
            'att_file': {'required': False},
            'residence': {'read_only': True},
        }

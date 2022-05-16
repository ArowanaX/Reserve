# import email
# from django.contrib.admin.sites import AdminSite,login
# from django.contrib import admin
# from Customer.models import Profile

# from django import forms

# class TodoAdminForm(forms.ModelForm):


       
# def clean(self):
# 	email=self.cleaned_data.get('email'),
#     password=self.cleaned_data.get('password'),
#     return super().clean()

        

# @admin.register(Profile)
# class TodoAdmin(admin.ModelAdmin):
# 	form = TodoAdminForm
# 	list_display = ('email','password')
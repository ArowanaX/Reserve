# from django.utils.translation import ugettext as _

import email
from django.contrib.auth.base_user import BaseUserManager
from pkg_resources import require


class CustomUserManager(BaseUserManager):
   
    def create_user(self,phone ,**extra_fields):
       
   
            user = self.model(phone=phone, **extra_fields)
            user.save()
            print("user....")
            return user

    def create_superuser(self, email, password, **extra_fields):
       
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.createsup_user(email,password ,**extra_fields)

    def createsup_user(self,email,password ,**extra_fields):
       
            user = self.model(email=email, **extra_fields)
            user.set_password(password)
            user.save()
            print("super.......")
            # raise ValueError('The phone must be set')

            return user
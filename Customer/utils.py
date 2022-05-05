from melipayamak import Api
from rest_framework.response import Response
from rest_framework import status
import os

#------------------------------------send sms activation code--------------------------------

def Send_sms(phone,uid,opt):

    try:
        username =os.environ.get("SMS_HOST_USERNAME","")
        password =os.environ.get("SMS_HOST_PASSWORD","")
        print(username)
        print(password)
        api = Api(username,password)
        sms = api.sms()
        to = phone
        _from = os.environ.get("SMS_HOST_SENDER","")
        text = 'کد تاییدیه شما از طرف هوگامان'+' '+ uid
        response = sms.send(to,_from,text)
        print(response)
        return Response(status=status.HTTP_200_OK)
    except:
        print("sms dont send.................................")
        return Response(status=status.HTTP_403_FORBIDDEN)
        
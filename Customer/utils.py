from melipayamak import Api
from rest_framework.response import Response
from rest_framework import status
import os

import requests
import json
from rest_framework import generics,status

from Customer.models import Profile



#------------------------------------send sms activation code--------------------------------

def Send_sms(phone,uid,opt):

    try:
        username =os.environ.get("SMS_HOST_USERNAME","")
        password =os.environ.get("SMS_HOST_PASSWORD","")
        api = Api(username,password)
        sms = api.sms()
        to = phone
        _from = os.environ.get("SMS_HOST_SENDER","")
        if opt=="reg":
            text = 'کد تاییدیه شما از طرف هوگامان'+' '+ uid
        if opt=="inv":
            text = 'شما به هتل ما دعوت شدید'+ uid
        print(text)
        # response = sms.send(to,_from,text)
        # print(response)
        return Response(status=status.HTTP_200_OK)
    except:
        print("sms dont send.................................")
        return Response(status=status.HTTP_403_FORBIDDEN)




#------------------send notification-----------------------------
        
def Notification(request):
    YOUR_TOKEN = 'put your token here ...'
    YOUR_APP_ID = 'put your app id here ...'

    url = f'https://api.pushe.co/v2/messaging/notifications/'

    headers = {
        'Authorization': f'Token {YOUR_TOKEN}',
        'Content-Type': 'application/json'
    }
    phone=request.user.phone
    payload = json.dumps({
        'app_ids': YOUR_APP_ID,
        'data': {
            'title': 'عنوان اعلان',
            'content': 'متن اعلان'
        },
        'filters': {
            'phone_number': [
                phone, 
                'phone_num2'
            ]
        }
    })

    r = requests.post(url, data=payload, headers=headers)

    print(r.status_code)




#---------------------- create invite link----------------------------

from melipayamak import Api
from rest_framework.response import Response
from rest_framework import status
import os
# from twilio.rest import Client
from django.urls import reverse
import requests
import json
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

def InviteLink(request,res_id,ph_list):
    link=reverse("customer:phone",kwargs={"valid":res_id})
    link_domin= "127.0.0.1:8000"+link
    phone=request.user.phone
    Notification(request)
    for elm in ph_list:
        Send_sms(elm,link_domin,"inv")
    


# class Whatsapp():
#     account_sid = os.environ['TWILIO_ACCOUNT_SID']
#     auth_token = os.environ['TWILIO_AUTH_TOKEN']
#     client = Client(account_sid, auth_token)

#     message = client.messages \
#                     .create(
#                         body="Join Earth's mightiest heroes. Like Kevin Bacon.",
#                         from_='+15017122661',
#                         to='+15558675310'
#                     )

    # print(message.sid)
    
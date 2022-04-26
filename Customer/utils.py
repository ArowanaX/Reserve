from kavenegar import *



#------------------------------------send sms activation code--------------------------------

def Send_sms(to_phone,uid):

    try:
        api = KavenegarAPI('774E597277394F4F73686F64396B577344752B6751464861725559774464713543567463305451702B59733D')
        params = { 'sender' : '100047778', 'receptor': '09120857673', 'message' :'.وب سرویس پیام کوتاه کاوه نگار' }
        response = api.sms_send( params)
        
    except:
        print("sms is sending.................................")
        return









    # try:
    #     api = KavenegarAPI('Your APIKey', timeout=20)
    #     params = {
    #         'receptor': to_phone,
    #         'message': uid,
    #     } 
    #     response = api.sms_send(params)
    #     print(response)
    # except APIException as e: 
    #     print(e)
    # except HTTPException as e: 
    #     print(e)
from twilio.rest import Client
from django.conf import settings
from django.http import HttpResponse
# QKV5EHKDUP4N8UHND8ST6VNW
import os


 #Your Account SID from twilio.com/console
account_sid = "AC1fa752de0f2bbda9e8dd96089873b81a" #your account SID from twilio console

 #Your Auth Token from twilio.com/console
auth_token  = "07a660337961b926d52c5625f07cc004" #your auth token from twilio console

client = Client(account_sid, auth_token)
try:
    def send_sms(user_code,):
     message = client.messages.create(
        
       
       
         body=f"message body mmmmmmmmmmmmmmmmmmmmmmmmmmmmmm",
         from_="+16066719464",

        #  to = f"{last_name}",
         to= "+2001555023696",
         ),
     if message.sid:
        print('send sessssssssss')
        # response = HttpResponse("Here's the text of the web page.")
     else:
        print('send erorrr')
        # response = HttpResponse("Here's the text of theccccc web page.")
       
except:
     response = HttpResponse("Here's the text of the web page.")
   



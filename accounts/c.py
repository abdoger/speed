from twilio.rest import Client
from django.conf import settings
from django.http import HttpResponse
# QKV5EHKDUP4N8UHND8ST6VNW
import os

# X18KWU9BQTX7N6YR635EFSZH
 #Your Account SID from twilio.com/console
account_sid = "ACe68d71ec3970f95445fe1b521177db2f" #your account SID from twilio console

 #Your Auth Token from twilio.com/console
auth_token  = "e88ee2fdeb85d049768e696210b2033b" #your auth token from twilio console

client = Client(account_sid, auth_token)
try:
    def send_sms(nember,user_code):
     message = client.messages.create(
        
       
       
         body=f'Hi your verification code is {user_code}',
         from_="+16184004808",

         to = f"{nember}",
        #  to= "+01555023696",
         ),
     if message.sid:
        print('send sessssssssss')
        # response = HttpResponse("Here's the text of the web page.")
     else:
        print('send erorrr')
        # response = HttpResponse("Here's the text of theccccc web page.")
       
except:
     response = HttpResponse("Here's the text of the web page.")
   


from django.db.models import OuterRef,Subquery,Exists
from orders.models import *
def orderOrder(request):
   
    
    orser = Order.objects.all()
    g = OrderDetails.objects.filter(order=OuterRef('pk')).order_by('pk')
    orser = orser.annotate(
        price= Subquery(g.values('price')[:1])
    )
    for v in orser:
        print(f"{v.pk} -   {v.price}")

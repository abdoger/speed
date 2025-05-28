import http.client
import json
import requests

def sms(request):
     
     conn = http.client.HTTPSConnection("v3xelr.api.infobip.com")
     payload = json.dumps({
         "messages": [
             {
                 "destinations": [{"to":"201555023696"}],
                 "from": "447491163443",
                 "text": "Congratulations on sending your first message. Go ahead and check the delivery report in the next step."
             }
         ]
     })
     headers = {
         'Authorization': 'e2942c2f7c3023c07b1d38a3be0d3104-44809705-52d3-45af-8665-e4b7263dc5a4',
         'Content-Type': 'application/json',
         'Accept': 'application/json'
     }
     conn.request("POST", "/sms/2/text/advanced", payload, headers)
     res = conn.getresponse()
     data = res.read()
     print(data.decode("utf-8"))
     
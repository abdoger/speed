from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from .models import *
from accounts.models import Video,UserProfile
from django.contrib import messages
from accounts.models import *
from django.http import JsonResponse
from django.core import serializers
from django.db.models import Sum,F,Count
from product.decorators import aminnUsers


# from django_ratelimit.decorators import ratelimit


# Create your views here.




from django.utils import timezone
def ajexd(request):
     #    pro_id = request.GET.get('pro_id')
    
     #    colar =  request.GET.get('colar')
 
        sizedata = Lists.objects.filter(massages='bbbbb',created_dt=timezone.now() + timezone.timedelta(minutes=9))
        if sizedata:
            sizedata = Lists.objects.filter(massages='bbbbb',created_dt=timezone.now() + timezone.timedelta(minutes=9))
       
            result = {
                    
                    "data": serializers.serialize("json", sizedata)
                   
                }
        else:
            result = {
                    
                    "data": ''
                   
                }

        return JsonResponse(result)
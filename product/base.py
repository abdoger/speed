from orders.models import Clint

from django.utils import timezone


def dase(request):
    if request.user.groups.filter(name='adminCastomar') or request.user.groups.filter(name='groadmin'):
        tr = True
        t = True
    else:
        tr = False
        t = False
    castomar = None
    if request.user.groups.filter(name='castomar') :
        castomar = True
       
    else:
        castomar = False
       

    if request.user.groups.filter(name='hr') or request.user.groups.filter(name='staff'):
        hrr = True
   
    else:
        hrr = False

    if request.user.groups.filter(name='factory') :
        factory = True
   
    else:
        factory = False

    if request.user.groups.filter(name='Shippingcompanies') :
        Shippingcompanies = True
   
    else:
        Shippingcompanies = False
    
    time_start  = timezone.now()
    time_end = '2025-01-01'
    request_user = request.user

    return {'request_user':request_user, 'hrr':hrr, 'tr':tr,'t':t,'factory':factory,'Shippingcompanies':Shippingcompanies,'castomar':castomar,'time_start':time_start,'time_end':time_end}

def cint(request):
    clint = Clint.objects.all()
    return { 'cint':clint, }

import pyttsx3
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from product.models import *
from .models import Order
from product.decorators import aminnUsers
from .models import *
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.http import HttpResponse
from django.db.models import Sum,F,Count,Value
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Payment
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from orders.forms import RrgisterForm,EmailPostForm
from accounts.models import OtpToken,Profile
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import Group
from django.core import serializers
from product.decorators import aminnUsers
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from product.decorators import allowedUsers,allowedCastomar
from .forms import * 
from django_ratelimit.decorators import ratelimit
from django.core.mail import send_mail 
from django.template.loader import render_to_string
from django.db import transaction
from django.http import HttpResponse
from django.core.mail import EmailMessage
import requests
from django.template.loader import get_template
from io import BytesIO
from xhtml2pdf import pisa
from accounts.models import UserProfile
import pyttsx3
# import weasyprint
# import matplotlib.pyplot as plt
from django.template.loader import render_to_string
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from django.conf import settings
from django.http import JsonResponse
import os

def order_to_pdf(tamplate_scr,context_dict={}):
   tamplate = get_template(tamplate_scr)
   html = tamplate.render(context_dict)
   result = BytesIO()
   pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")),result)
   if not pdf.err:
       return HttpResponse(result.getvalue(),content_type='application/pdf')
   return None
      
from django.views.generic import View

# @stafftamplate_member_required
class Gennerpdf(View):
    # Получаем заказ по ID:
    def get (self,request,*args,**kwargs):
        order = Namepartener.objects.all()
        # Передаем объект в функцию render_to через генерацию шаблона pdf.html HTML в виде строки:
        phf = order_to_pdf('pages/order_admin_pdf.html')
        # Создаем объект овтета с типом содержимого application/pdf и заголовком Content-Disposition:
        if phf:
            response = HttpResponse(phf,content_type='application/pdf')
            response['Content-Disposition'] = 'filename=order.pdf'
            return response
        return HttpResponse("ohgi")

# @allowedUsers(allowedGroups=['hr'])
@login_required(login_url='signin')
@ratelimit(key='user_or_ip', rate='50/m')
def castomar(request):
    group = Group.objects.get(name='castomar')
    users = User.objects.filter(groups=group)
    userProfile = UserProfile.objects.all().filter(user__groups=group)
   
    context={
        'users':userProfile
        }
    return render(request,'orders/castomar.html',context)



@login_required(login_url='signin')
@ratelimit(key='user_or_ip', rate='50/m')
def castomarorder(request,id):
    users = User.objects.get(id=id)
    total_oos = 0
    total_ssa = 0
    ordes_castomar = Order.objects.filter(user=users)
    for i in ordes_castomar:
        orderDetails__castomar = OrderDetails.objects.filter(order__pk=i.pk)
        for j in orderDetails__castomar:
            total_oos += int(j.product.qus) * int(j.quantity)
            total_ssa += int(j.product.qus ) * int(j.ba)
    y = Order.objects.filter(user=users).exclude(coin=None)
    s = 0
    for i in y:
        s += int(i.coin)
    total_nsd = total_ssa - s
    users = User.objects.get(id=id)
    coin = Order.objects.filter(user=users).aggregate(Sum('coin'))['coin__sum']
    d = Order.objects.filter(user=users).aggregate(total_order = Sum(F('orderss__ba') * F('details__price')))
    print(d)
    order = Order.objects.filter(user=users).annotate(
      cionss =   F('orderss__ba') * F('details__qus'),
    )
    if request.method =="POST":
            try:
               id =request.POST.get('id')
               quset = order.filter(
                    id__icontains = id,
                     )
               context={
                       'order':order
                         }
               messages.success(request, _('عملية بحث ناجحه'))
               return render(request,'orders/castomarorder.html',{'order':quset,'coin':coin,'d':d,'total_nsd':total_nsd,'total_ssa':total_ssa})
            except:
                messages.error(request, _('عملية بحث فاشله '))
                context={
                    'order':order
                       }
                return render(request,'orders/castomarorder.html',{'order':order})
    return render(request,'orders/castomarorder.html',{'total_ssa':total_ssa,'order':order,'coin':coin,'d':d,'total_nsd':total_nsd})

@allowedUsers(allowedGroups=['staff'])
@login_required(login_url='signin')
@ratelimit(key='user_or_ip', rate='50/m')
def deletepartener(request,id):
     pro_delete = get_object_or_404(Namepartener, id=id)
     if request.method == 'POST':
          pro_delete.delete()
          messages.success(request, 'تم الحذف')
          return redirect('rnamepartener')
     return render(request,'pages/delete.html',)

@allowedUsers(allowedGroups=['staff'])
@login_required(login_url='signin')
@ratelimit(key='user_or_ip', rate='50/m')
def updatepartener(request, id):
    book_id = Namepartener.objects.get(id=id)

    if request.method == 'POST':

            book_save = Namepartenerform(request.POST, request.FILES ,instance=book_id)
            if book_save.is_valid():
                t = book_save.save()
                messages.success(request, 'تم التعديل')
                return redirect('rnamepartener')

    else:
      
    
        context ={
            'form':Namepartenerform(instance=book_id),
         }
        return render(request, 'pages/update.html',context)


def redds(request,id,rd,fd):
            order = Order.objects.get(id=id)
            py = Payment.objects.get(order=order)
            ne = Namepartener.objects.get(id=rd)
            orderDetails = OrderDetails.objects.filter(order_id=order)
            s = 0
            for i in orderDetails:
                 s += i.ba * i.product.price
            total = s+ py.na
            from_email =settings.EMAIL_HOST_USER
            subject = 'فاتورة شحن '
            receiver =[ne.email,] 
            messages = f"""
             تم ارسال فاتورة شحن
            """
      
            to = receiver
            render_temp  = render_to_string('main_ta.html',{'order':order,'py':py ,'orderDetails':orderDetails,'total':total,"fd":fd})
            send_mail(
               subject,
               messages,
               from_email,
               to,
               fail_silently=False,
               html_message=render_temp
           )


def reportpartener(request,id):
    order = Order.objects.get(id=id)
    
    py = Payment.objects.get(order=order)
    
    orderDetails = OrderDetails.objects.filter(order_id=order)
    s = 0
    for i in orderDetails:
        s += i.ba * i.product.price
    total = s+ py.na
    
    a = Order.objects.filter(id=id,status=Order.Typechoices.a)
    n = Order.objects.filter(id=id,status=None)
    
    y = 0
    d= 0
    s = 0 
    fd = 0
    for i in orderDetails:
        y += i.ba * i.product.price
        d += i.ba
        s += i.ba * i.product.qus
    
    if  order.user_group.name == 'castomar':
       fd = py.na + y + s
    else:
       fd = py.na + y 

    book_id = Order.objects.get(id=id)
    if request.user.groups.filter(name='hr') :
        if book_id.order_updated is not None:
             if book_id.order_updated <  timezone.now() :
                 messages.error(request, _('  تم انتهاء مدة التعديل '))
                 return redirect('orderOrder') 
    
    if request.method == 'POST': 
        
        
        uus = request.POST.get('uus')
        uus = fd
        if  order.statusu == 'completed' :
                messages.error(request, _(' الطلب اكتمل ولا يمكن التعديل عليه '))
                return redirect("orderOrder") 
        elif a or n: 
            messages.error(request, _('يجب ان تختار حاله'))
            return redirect("orderOrder") 
        
        elif d == 0:
               messages.error(request, _(' العمل فى الطلب اولا'))
               return redirect("orderOrder") 
        elif int(uus)  > int(fd): 
            messages.error(request, _('   القيمه الواصله اكبر من قيمة التقرير'))
            return redirect("orderOrder") 
        
        
        elif order.posta == True: 
            messages.error(request, _('هذا الطلب تم الايضافه الى بوسطه من قبل'))
            return redirect("orderOrder") 
        elif not order.is_finished == True: 
            messages.error(request, _('يجب تاكيد الطلب اولا'))
            return redirect("orderOrder") 
    
        order = Order.objects.get(id=id)
        if order.is_Orderpartener == True:
            messages.error(request, ' هذا الطلب تم العمل موسبقا')
            return redirect('reportpartener', id=id)

        if  request.POST.get('ramepartener') == '': 
           messages.error(request, ' مربع الاسم شركه فارغ ')
           return redirect('reportpartener', id=id) 
        if  request.POST.get('uus') == '': 
           messages.error(request, ' مربع القيمة الواصله فارغ ')
           return redirect('reportpartener', id=id)
       
        
        add_category= Reportpartenerform(request.POST)
        rd = request.POST['ramepartener']
        
        ne = Namepartener.objects.get(id=rd)
        if add_category.is_valid():
            hhr = add_category.save(commit=False)
            hhr.id_order = order
            hhr.user_add = request.user
            hhr.uus = fd
           
            # redds(request,id,rd,fd)
            hhr.save()
            order = Order.objects.filter(id=id).update(is_Orderpartener=True,Orderpartener_id=hhr.id)

            messages.success(request,"تم  ايضافة تقرير")
            return redirect("orderOrder") 
    context = {
        'form':Reportpartenerform(),
        'd':fd
        
    }
    return render(request,'pages/dfnamepartener.html',context)


def rnamepartener(request):
    r = Namepartener.objects.all()
    return render(request,'pages/rnamepartener.html',{'r':r,})

def dseportpartener(request,id):
    namepartener = Namepartener.objects.get(id=id)
    sud = Reportpartener.objects.filter(ramepartener=namepartener.id).aggregate(Sum('uus'))['uus__sum']
    
    d = Deportpartener.objects.filter(ramepartener=namepartener.id)
    sd = Deportpartener.objects.filter(ramepartener=namepartener.id).aggregate(Sum('uus'))['uus__sum']
    return render(request,'pages/dsnamepartener.html',{'r':d,'sd':sd,'sud':sud,'namepartener':namepartener})

@allowedUsers(allowedGroups=['staff'])
@login_required(login_url='signin')
@ratelimit(key='user_or_ip', rate='50/m')
def deleteDeportpartener(request,id,di):     
     pro_delete = get_object_or_404(Deportpartener,ramepartener__id=id ,id=di)
     if request.method == 'POST':
          pro_delete.delete()
          messages.success(request, 'تم الحذف')
          return redirect('dseportpartener',id=id)
     else:
         return render(request,'pages/delete.html',)

@allowedUsers(allowedGroups=['staff'])
@login_required(login_url='signin')
@ratelimit(key='user_or_ip', rate='50/m')
def updateDeportpartener(request,id,di):
    namepartener = Namepartener.objects.get(id=id)
    gx = get_object_or_404(Deportpartener,ramepartener__id=id ,id=di)
    sd = Deportpartener.objects.filter(ramepartener=namepartener.id).aggregate(Sum('uus'))['uus__sum']


    sud = Reportpartener.objects.filter(ramepartener=namepartener.id).aggregate(Sum('uus'))['uus__sum']

    # print(sd) 
    # print( sud)

    if request.method == 'POST' :
            uus = request.POST['uus']
            if not int(sud ) >= int(sd - gx.uus ) + int(uus) :
                messages.error(request,_("القيمه الراجعه الكبر من القيمة الواصله"))
                
                return redirect('dseportpartener',id=id)
      
            book_save = Deportpartenerform(request.POST, request.FILES ,instance=gx)
            if book_save.is_valid():
                book_save.save()
                messages.success(request, 'تم التعديل')
                return redirect('dseportpartener',id=id)

    else:
            book_save =Deportpartenerform(instance=gx)

    context ={
            'form':book_save,
        }
    return render(request, 'pages/update.html',context)



def deportpartener(request,id):
    namepartener = Namepartener.objects.get(id=id)
    namepartener = Namepartener.objects.get(id=id)
    sd = Deportpartener.objects.filter(ramepartener=namepartener.id).aggregate(Sum('uus'))['uus__sum']
    sud = Reportpartener.objects.filter(ramepartener=namepartener.id).aggregate(Sum('uus'))['uus__sum']
    if sd == None:
        sd = 0
   
    if request.method == 'POST' :
        uus = request.POST['uus']
        if not int(sud ) >= int(sd ) + int(uus) :
                messages.error(request,_("القيمه الراجعه الكبر من القيمة الواصله"))
                
                return redirect('dseportpartener',id=id)
        if  request.POST.get('uus') == '': 
           messages.error(request, ' مربع القيمة الواصله فارغ ')
           return redirect('reportpartener', id=id)
        add_category= Deportpartenerform(request.POST)
        if add_category.is_valid():
            hhr = add_category.save(commit=False)
            hhr.ramepartener = namepartener
            hhr.user_add = request.user

            hhr.save()
            messages.success(request,"تم  اضافة تقرير")
            return redirect('dseportpartener',id=id) 
    context = {
        'form':Deportpartenerform(),
        'namepartener':Namepartener.objects.get(id=id),
        
    }
    return render(request,'pages/namepartener.html',context)



def rsreportpartener(request,id):
    sd = 0
    # user = User.objects.get(id=id)

    if Namepartener.objects.filter(id=id).exists():
         namepartener = Namepartener.objects.get(id=id)
         ms = Deportpartener.objects.filter(ramepartener=namepartener.id)
         for k in ms:
            sd += int(k.uus)
    namepartener = Namepartener.objects.get(id=id)
    sshg = Reportpartener.objects.filter(ramepartener__email=namepartener.email,id_order__status_copping='الطلب ملغى').aggregate(Sum('uus'))['uus__sum']

    s = 0
    z = 0
    x = 0
    gggcd=0
    bas = 0
    r =  Reportpartener.objects.filter(ramepartener__email=namepartener.email)
    kj = 0
    for re in r:
        x += re.uus
        order = Order.objects.filter(Orderpartener=re).annotate(
        totalsb = Sum(F('orders__uus')  ),
        total = Sum(F('orderss__copping') * F('orderss__price')),
        ba = Sum(F('orderss__ba') * F('orderss__price')),
        )
        orders= Order.objects.filter(Orderpartener=re,user_group__name='castomar').annotate(
          total__ba = Sum(F('orderss__copping') * F('details__qus')),
        )
        for i in order:
            bas +=  i.ba
            s += i.total
            gggcd += i.totalsb
        for xd in orders:
             kj += int(xd.total__ba)
             print(int(xd.total__ba))
    h  =  x - s
   
    re = Namepartener.objects.get(id=id)
    r = Reportpartener.objects.filter(ramepartener__id=re.id)
    order = Order.objects.filter(Orderpartener__ramepartener__id=re.id).annotate(total = (F("orderss__product__price") * F("orderss__ba")) + F("Payments__na"),
                                                      jx = (F("orderss__product__price") * F("orderss__ba")) + F("Payments__na")  + F("details__qus") *  F("orderss__ba"))
   
    er = Order.objects.filter(Orderpartener__ramepartener__id=re.id).annotate(total = (F("orderss__product__price") * F("orderss__ba")) + F("Payments__na"),
                                                      jx = (F("orderss__product__price") * F("orderss__ba")) + F("Payments__na")  + F("details__qus") *  F("orderss__ba"))
   
    if request.method =="POST":
          try:
               
               gr =request.POST.get('gr')
               mr =request.POST.get('mr')
               id =request.POST.get('id')
               

               quset = r.filter(
                    
                     reportpostas_date__range = [
                           gr,
                            mr,
                     ],
                    id_order__id__icontains = id,
                     )
               context ={
                   'r':quset,
                   'r':r,
                   "s":s,
                   'z':h,
                   "sd":sd,
                   "sshg":sshg,
                   'bas':bas,
                   'kj':kj
                  
               } 
               messages.success(request, _('عملية بحث ناجحه'))
               return render(request, 'pages/rsreportpartener.html', context) 
          
          except:
                messages.error(request, _('عملية بحث فاشله '))
                return render(request,'pages/rsreportpartener.html',{'r':r,'r':r,"s":s,'z':h,"sd":sd,"sshg":sshg,'bas':bas,'kj':kj})
    

    return render(request,'pages/rsreportpartener.html',{'r':r,'r':r,"s":s,'z':h,"sd":sd,'gggcd':gggcd,"sshg":sshg,'bas':bas,'kj':kj})


def namepartener(request):

    if request.method == 'POST' :
        if  request.POST.get('name') == '': 
           messages.error(request, ' مربع الاسم فارغ ')
           return redirect('namepartener') 
        if  request.POST.get('tital') == '': 
           messages.error(request, ' مربع العنوان فارغ ')
           return redirect('namepartener')
        if  request.POST.get('number') == '': 
           messages.error(request, ' مربع رقم الهاتف فارغ ')
           return redirect('namepartener')
        
        add_category= Namepartenerform(request.POST)
        
        if add_category.is_valid():
            add_category.save()
            

            messages.success(request,"تم  ايضافة شركه")
            return redirect('rnamepartener') 
    context = {
        'form':Namepartenerform(),
        
    }
    return render(request,'pages/namepartener.html',context)


@allowedUsers(allowedGroups=['staff'])

@login_required(login_url='signin')
@ratelimit(key='user_or_ip', rate='50/m')
def Rdelete(request,id):
     pro_delete = get_object_or_404(Reportpostas, id=id)
     
     if request.method == 'POST':
          pro_delete.delete()
          messages.success(request, 'تم الحذف')

          return redirect('dreportpost')

     return render(request,'pages/delete.html',)
       
@allowedUsers(allowedGroups=['staff'])
@login_required(login_url='signin')
@ratelimit(key='user_or_ip', rate='50/m')
def dsdupdate(request, id):
    book_id = get_object_or_404(Reportpostas, id=id)
    # v = Order.objects.filter(posta=True).annotate(total= (F("orderss__product__price") * F("orderss__ba")) + F("Payments__na") ).aggregate(Sum('total'))['total__sum']
    vd = 0
    vs = 0
    vd = Order.objects.filter(posta=True).filter(user_group__name="castomar").annotate(total= (F("orderss__product__price") * F("orderss__ba")) + F("Payments__na")  + F("details__qus") *  F("orderss__ba") ).aggregate(Sum('total'))['total__sum']
    
    vs = Order.objects.filter(posta=True).filter(user_group__name="admin").annotate(total= (F("orderss__product__price") * F("orderss__ba")) + F("Payments__na") ).aggregate(Sum('total'))['total__sum']
    if vs == None:
        vs = 0
    if vd == None:
        vd = 0
    v = vd + vs
    if request.method == 'POST':
        uus = request.POST.get('uus') 
        q  = Reportpostas.objects.all().aggregate(Sum("uus"))['uus__sum']
        if q :
                q = q
        else:
                q = 0
        w = int(uus) + int(q)
        print(w)
        if not v >=  w - book_id.uus :
            messages.error(request, ' عمليه خاطئه')
            return redirect('dsdupdate' , id=id)
        book_save = Reportpostasform(request.POST, request.FILES ,instance=book_id)
        if book_save.is_valid():
                t = book_save.save()
                messages.success(request, 'تم التعديل')
                return redirect('dreportpost')
    else:
            book_save =Reportpostasform(instance=book_id)
    context ={
            'form':book_save,
        }
    return render(request, 'pages/update.html',context)


@allowedUsers(allowedGroups=['staff'])

@login_required(login_url='signin')
@ratelimit(key='user_or_ip', rate='50/m')
def dreportpost(request):
    k = 0
    n = Order.objects.filter(posta=True)
    for i in n:
        k += int(i.total_pasta)
    vd = Order.objects.filter(posta=True).filter(user_group__name="castomar").annotate(total= (F("orderss__product__price") * F("orderss__ba")) + F("Payments__na")  + F("details__qus") *  F("orderss__ba") ).aggregate(Sum('total'))['total__sum']
    if vd == None:
        vd = 0
    vs = Order.objects.filter(posta=True).filter(user_group__name="admin").annotate(total= (F("orderss__product__price") * F("orderss__ba")) + F("Payments__na") ).aggregate(Sum('total'))['total__sum']
    if vs == None:
        vs = 0
    v = vd + vs
    # v = Order.objects.filter(posta=True).annotate(total= (F("orderss__product__price") * F("orderss__ba")) + F("Payments__na") ).aggregate(Sum('total'))['total__sum']
    r = Reportpostas.objects.all()
    context = {
        'r':r,
        'y':k
    }
    return render(request,'pages/dreportpost.html',context)
def reportpost(request):
    k = 0
    n = Order.objects.filter(posta=True)
    for i in n:
        k += int(i.total_pasta)
    # v = Order.objects.filter(posta=True).annotate(total= (F("orderss__product__price") * F("orderss__ba")) + F("Payments__na") ).aggregate(Sum('total'))['total__sum']
    vd = Order.objects.filter(posta=True).filter(user_group__name="castomar").annotate(total= (F("orderss__product__price") * F("orderss__ba")) + F("Payments__na")  + F("details__qus") *  F("orderss__ba") ).aggregate(Sum('total'))['total__sum']
    if vd == None:
        vd = 0
    vs = Order.objects.filter(posta=True).filter(user_group__name="admin").annotate(total= (F("orderss__product__price") * F("orderss__ba")) + F("Payments__na") ).aggregate(Sum('total'))['total__sum']
   
    if vs == None:
        vs = 0
    v = k
    if request.method == 'POST' :
        if  request.POST.get('name') == '': 
           messages.error(request, ' مربع الاسم فارغ ')
           return redirect('reportpost') 
        if  request.POST.get('uus') == '': 
           messages.error(request, ' مربع التقرير فارغ ')
           return redirect('reportpost')
        uus = request.POST.get('uus') 
        q  = Reportpostas.objects.all().aggregate(Sum("uus"))['uus__sum']
        if q :
                q = q
        else:
                q = 0
    
                
        w = int(uus) + int(q)
        if v == None:
            v = 0
        if not v >=  w :
            messages.error(request, ' عمليه خاطئه')
            return redirect('reportpost')

            
        add_category= Reportpostasform(request.POST)
        
        if add_category.is_valid():
            add_category.save()
            
            messages.success(request,_(" تم اضافة الطلب الى شركة الشحن "))
            return redirect('dreportpost') 
    context = {
        'form':Reportpostasform(),
        'y':v
    }
    return render(request,'pages/reportpost.html',context)
def posta(request):
    k = 0
    n = Order.objects.filter(posta=True)
    for i in n:
        k += int(i.total_pasta)
    vd = Order.objects.filter(posta=True).filter(user_group__name="castomar").annotate(total= (F("orderss__product__price") * F("orderss__ba")) + F("Payments__na")  + (F("details__qus") *  F("orderss__ba")) ).aggregate(Sum('total'))['total__sum']
    if vd == None:
        vd = 0
    vs = Order.objects.filter(posta=True).filter(user_group__name="admin").annotate(total= (F("orderss__product__price") * F("orderss__ba")) + F("Payments__na") ).aggregate(Sum('total'))['total__sum']
    if vs == None:
        vs = 0
    v = vd + vs
    order = Order.objects.filter(posta=True)
   
    return render(request,'pages/postap.html',{'x':order,'y':k})


@ratelimit(key='user_or_ip', rate='50/m')
@login_required(login_url='signin')
@allowedUsers(allowedGroups=['hr','staff'])
@transaction.atomic
def pdf(request,id):
    order = Order.objects.get(id=id)
    det = OrderDetails.objects.filter(id=order.pk)

     
    template_path = 'reqqer/pdf.html'
    context = {'order':order,"det":det}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=order.pdf'
    template = get_template(template_path)
    html  = template.render(context)

    
    pisa_status = pisa.CreatePDF(
       html , dest= response
    )
    if pisa_status.err:
        return HttpResponse("Invalid PDF <pre>"+html+'</pre>')
    return response
@ratelimit(key='user_or_ip', rate='50/m')
@login_required(login_url='signin')
@allowedUsers(allowedGroups=['hr','staff'])
@transaction.atomic
def gdx(request,id):
    order = Order.objects.get(id=id)
    py = Payment.objects.get(order=order)
    pyment = Payment.objects.get(order_id=order)
    OrderDetailsd = OrderDetails.objects.filter(order_id=order).count()
    orderDetails = OrderDetails.objects.filter(order_id=order)
    a = Order.objects.filter(id=id,status=Order.Typechoices.a)
    n = Order.objects.filter(id=id,status=None)
    OrderDetailsda = OrderDetails.objects.filter(order_id=order,product__facat=True)
    OrderDetailsdas = OrderDetails.objects.filter(order_id=order).exclude(product__facat=True)
    qy = 0
    qys = 0

    for yo in OrderDetailsda:
        qy += yo.ba  * int(2)
    for yos in OrderDetailsdas:
        qys += yos.ba  
   
    zoron = qy + qys
  
    fd = 0
    book_id = Order.objects.get(id=id)
    if request.user.groups.filter(name='hr') :
        if book_id.order_updated is not None:
             if book_id.order_updated <  timezone.now() :
                 messages.error(request, _('  تم انتهاء مدة التعديل '))
                 return redirect('orderOrder') 
    if request.method == 'POST': 
        
        y = 0
        d= 0
        nd= 0
       
        for i in orderDetails:
               y += i.ba * i.product.price
               nd += i.ba * i.product.qus
               d += i.ba
        
        if  order.user_group.name == 'castomar':
           fd = py.na + y + nd
        elif order.user_group.name == 'admin':
            fd = py.na + y
        if  order.statusu == 'completed' :
                messages.error(request, _(' الطلب اكتمل ولا يمكن التعديل عليه '))
                return redirect("orderOrder") 
        elif a and n: 
            messages.error(request, _('يجب ان تختار حاله'))
            return redirect("orderOrder") 
        
        elif d == 0:
               messages.error(request, _(' العمل فى الطلب اولا'))
               return redirect("orderOrder") 
        
        
        elif order.posta == True: 
            messages.error(request, _('هذا الطلب تم الايضافه الى بوسطه من قبل'))
            return redirect("orderOrder") 
        elif order.is_Orderpartener == True: 
            messages.error(request, _('هذا الطلب تم الايضافه الى شركة شحن من قبل'))
            return redirect("orderOrder") 
        elif not order.is_finished == True: 
            messages.error(request, _('يجب تاكيد الطلب اولا'))
            return redirect("orderOrder") 
        else:
            url = "http://api.bosta.co/api/v2/deliveries"
            headers ={
                      'Authorization':"e25c6741e96a2a6c0f2ec34dc37c652e4fb434f409340cb3302f6acf57cfdeca" ,
                     'Content-Type': "application/json",
                } 
            data = {
  "allowToOpenPackage": "true",
  "cod": fd,
  "dropOffAddress": {
    "apartment": "#",
    "buildingNumber": "#",
    "districtId": "g_Jm66OFdv-",
    "floor": "#",
    "secondLine": pyment.districtid,
    "firstLine": str(pyment.mo) +','+ str(pyment.mr) ,
  },
  "notes": pyment.momr,
  "receiver": {
    "secondPhone": pyment.shipment_phone_to,
   "phone": pyment.shipment_phone,
   "fullName": pyment.name,
    
  },
  "specs": {
    "packageDetails": {
      "description": "#",
      "itemsCount": zoron,
    }
  },
   "locationName": "#",
  "type": 10
}                     
           
   
          
           
                 
            res = requests.post(url,headers=headers,data=json.dumps(data)).json()
            print(res)
            if res['success'] == True:

                o = Order.objects.filter(id=id).update(posta = True ,total_pasta=fd)
           
                messages.success(request, _('تم الضافة الى بوسطه'))
                return redirect("orderOrder") 
            else:
                 messages.success(request, _('kkk'))
                 return redirect("orderOrder") 
       
    return render(request,'pages/posta.html',{'x':order})

@transaction.atomic
def generateKashierOrderHash(request):
  
     
     mid = "MID-31645-261"  # Your merchant ID
     amount = str(8) # e.g., 100
     currency = 'EGP'  # e.g., "EGP"
     orderId = str(9)  # e.g., 99
     CustomerReference = "1"  # Your customer ID for saving the card
     path = f"/?payment={mid}.{orderId}.{amount}.{currency}"
     if CustomerReference:
         path += f".{CustomerReference}"
     secret = "d922afae-f6f4-44f9-b43c-c2a14ab353d5"
     return hmac.new(secret.encode('utf-8'), path.encode('utf-8'), hashlib.sha256).hexdigest()





@ratelimit(key='ip', rate='10000/m')
@transaction.atomic
def signupp(request):
    form = RrgisterForm()
    if request.method == "POST":
        form =  RrgisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Accomnt email'))
            return redirect("verify_email",username=request.POST['username'])
            # return render(request,'pages/update.html',)
    context = {"form":form}
    return render(request,'pages/update.html',context)


@allowedUsers(allowedGroups=['staff','adminCastomar'])
@login_required(login_url='signin')
@ratelimit(key='user_or_ip', rate='50/m')
def updateordercom(request,id,):
    gx = Order.objects.get(id=id)
   
    if request.method == 'POST' :
      
            book_save = ordercomform(request.POST, request.FILES ,instance=gx)
            if book_save.is_valid():
                book_save.save()
                messages.success(request, 'تم التعديل')
                return redirect('orderOrder')

    else:
            book_save =ordercomform(instance=gx)

    context ={
            'form':book_save,
        }
    return render(request, 'pages/update.html',context)






@ratelimit(key='ip', rate='10000/m')
@transaction.atomic
def verify_email(request,username):
    user = User.objects.get(username=username)
    user_otp = OtpToken.objects.filter(user=user).last()
    # print(user_otp.osp_code)
    if request.method == "POST":
        if user_otp.osp_code ==  request.POST['otp_code']:
            if user_otp.opt_expires_at > timezone.now():
                user.is_active = True
                user.save()
              
                messages.success(request, _(' تفعيل الحساب'))
                return redirect('signin')
            else:
                 messages.warning(request, _(' انتهت صلاحيت رقم التفعيل'))
                 return redirect("verify_email",username=user.username)
        else:
             messages.warning(request, _(' رقم تفعيل خاطئ'))
             return redirect("verify_email",username=user.username)   

    context ={

    } 
    return render(request,"verify_token.html",) 

def rotp(request,user,otp):
    from_email =settings.EMAIL_HOST_USER
    subject =  'التحقق من الحساب'
    h = request.get_host()
   
    message =f"""
    انقر على هذا الرابط  الذى امامك واكتب رمز  التفعيل

    http://{h}/ar/orders/verify_email/{user.username}
    """
    m = "http://{h}/ar/orders/verify_email/{user.username}"
    receiver =[user.email,]
    to = receiver
    render_temp  = render_to_string('main_temp.html',{'m':m,'t':message,'otp':otp.osp_code ,'user':user.username})
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = "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"
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": user.email }],
        sender={"email": settings.DEFAULT_FROM_EMAIL},
        subject=subject,
        html_content=render_temp ,
       
    )
    try:
        api_instance.send_transac_email(email)
        return JsonResponse({"message": "تم إرسال البريد بنجاح!"})
    except ApiException as e:
        return JsonResponse({"error": f"خطأ في إرسال البريد: {e}"}, status=500)
    
    # send_mail(
    #            subject,
    #            message,
    #            from_email,
    #            to,
    #            fail_silently=False,
    #            html_message=render_temp
    #        )
    

@ratelimit(key='ip', rate='10000/m')
@transaction.atomic
def ressend_otp(request):
    if request.method == 'POST':   
        user_email = request.POST["otp_email"]
        if  get_user_model().objects.filter(email=user_email).exists():
            user = get_user_model().objects.filter(email=user_email).last()
            otp = OtpToken.objects.create(user=user,opt_expires_at=timezone.now()+timezone.timedelta(minutes=10))
            rotp(request,user,otp)
            # from_email =settings.EMAIL_HOST_USER
            subject =  'التحقق من الحساب'
            h = request.get_host()
           
            message =f"""
             
            {user.username},هذا رقم التفعيل
               {otp.osp_code}
               انقر على هذا الرابط  الذى امامك واكتب رمز  التفعيل
            http://{h}/ar/orders/verify-email/{user.username}
            """
            receiver =[user.email,]
            to = receiver

            configuration = sib_api_v3_sdk.Configuration()
            configuration.api_key['api-key'] = "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"
            api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
            email = sib_api_v3_sdk.SendSmtpEmail(
                 to=[{"email": user.email }],
                 sender={"email": settings.DEFAULT_FROM_EMAIL},
                 subject=subject,
                 html_content=message ,
                
             )
            try:
                 api_instance.send_transac_email(email)
                 messages.success(request, _('تم ارسال الرمز الى حسابك'))
                 return redirect("verify_email",username=user.username)
            except ApiException as e:
                 return JsonResponse({"error": f"خطأ في إرسال البريد: {e}"}, status=500)
            # send_mail(
            #        subject,
            #        message,
            #        from_email,
            #        to,
            #        fail_silently=True
            #     )
            
            # messages.success(request, _('تم ارسال الرمز الى حسابك'))
            # return redirect("verify_email",username=user.username)
         
           
 
        else:
             messages.warning(request, _('الرجاء ارسال ايميل صالح'))
             return redirect("ressend_otp") 

    else:
          form = EmailPostForm()  

    context ={
        'form':form,
    } 
    return render(request,"resend_otp.html",context)  
from django.http import JsonResponse
from django.core import serializers
from django.db.models import Sum,F,Count




@ratelimit(key='user_or_ip', rate='50/m')
@login_required(login_url='signin')
@allowedUsers(allowedGroups=['staff','Shippingcompanies'])
@transaction.atomic
def status__copping(request,id):
        order = Order.objects.get(id=id)
        if order.statusu == 'completed':
            messages.error(request, _(' الطلب اكتمل ولا يمكن التعديل عليه '))
            return redirect("shipping" )
        if request.method == "POST":
            order.status_copping = request.POST['mo']
            order.save()
            messages.success(request, _('تم انشا حاله'))
            return redirect("shipping" )
        return render(request, "pages/status__copping.html",)
@ratelimit(key='user_or_ip', rate='50/m')
@login_required(login_url='signin')
@allowedUsers(allowedGroups=['staff','Shippingcompanies'])
@transaction.atomic
def update__copping(request,id_order,id):
    order = Order.objects.get(id=id_order)

    book_id =  OrderDetails.objects.get(order=order,id=id)
    if  order.statusu == 'completed' :
                messages.error(request, _(' الطلب اكتمل ولا يمكن التعديل عليه '))
                return redirect("order__shipping"  ,id=id_order )
    if request.method == "POST":
            hr =  request.POST['copping']
            
            if not int(book_id.ba) >= int(hr):
                messages.error(request, _(' يجب ان يكون الكميه الواصله الكبر من او يساوى اقيمه الواصله'))
                return redirect("order__shipping"  ,id=id_order )
            book_save = Coppingform(request.POST, request.FILES ,instance=book_id)
            if book_save.is_valid():
                book_save.save()
                messages.success(request, _('عمليه ناجحه'))
                return redirect("order__shipping"  ,id=id_order )
    else:
        book_save =Coppingform(instance=book_id)
  
        context ={
            'form':book_save,
        
        }
        return render(request, 'pages/update.html',context)
       


def ajex_order_not_sh(request):
        r = Clint.objects.all()
        sizedatas =    Order.objects.filter(status=Order.Typechoices.a)

        if (sizedatas):
            date =  Order.objects.filter(status=Order.Typechoices.a)
            for i in date:
                from_email =settings.EMAIL_HOST_USER
                subject = ' طلب لم يتم الشحن '
                receiver =[i.user.email,] 
                messages = f"""
                  speed futhur
                """
      
                to = receiver
                render_temp  = render_to_string('norder.html',{'order':i.pk,'py':receiver ,'r':r})
                send_mail(
                   subject,
                   messages,
                   from_email,
                   to,
                   fail_silently=False,
                    html_message=render_temp
                  )
       
                result = {
                    
                    "data": serializers.serialize("json", sizedatas)
                   
                }
        else:
            result = {
                    
                    "data": ''
                   
                }

        return JsonResponse(result)



@transaction.atomic
def ajex(request):
        pro_id = request.GET.get('pro_id')
    
        colar =  request.GET.get('colar')
 
        sizedata = Sise.objects.filter(productsise__productcolor__id=pro_id,productsise__name=colar)
        if (colar):
            sizedata = Sise.objects.filter(productsise__productcolor__id=pro_id,productsise__name=colar)
       
            result = {
                    
                    "data": serializers.serialize("json", sizedata)
                   
                }
        else:
            result = {
                    
                    "data": ''
                   
                }

        return JsonResponse(result)



@ratelimit(key='user_or_ip', rate='50/m')
@login_required(login_url='signin')
@allowedUsers(allowedGroups=['adminCastomar','factory','groadmin'])
@transaction.atomic
def w_to_colar(request,id):

    pro = Product.objects.get(pk=id)
   
    if not pro.pro_date + timezone.timedelta(minutes=10) > timezone.now() and  request.user.groups.filter(name='factory') :
        messages.error(request, ' تم انتهاء المدة  ')
        return render(request, '404.html')
        
 
    
    pro = Product.objects.get(pk=id)
    # color = Color.objects.filter(pk=pro.id)
 
    context ={
        'color' :pro,
         
       
    }
    return render(request, 'prodects/deteilcolar.html',context,)
@ratelimit(key='user_or_ip', rate='50/m')
@transaction.atomic
@login_required(login_url='signin')
@allowedUsers(allowedGroups=['adminCastomar','factory','groadmin'])

def add_to_colar(request,id):
 
    
    pro = get_object_or_404(Product,pk=id)
    print(pro.qu)
    q  = Color.objects.filter(productcolor=pro).aggregate(Sum("qucolor"))['qucolor__sum']
   
  
    if request.method == 'POST':
        if 'name' in request.POST :
            name = request.POST.get('name')
        else:
            messages.warning(request, _('  مربع اللون فارغ '))
            return redirect('add_to_colar',id=id)
        if 'asname' in request.POST :
            asname = request.POST.get('asname')
        else:
            messages.warning(request, _('  مربع اللون فارغ '))
            return redirect('add_to_colar',id=id)
        if 'qucolor' in request.POST :
            qucolor = request.POST.get('qucolor')
        else:
            messages.warning(request, _('  مربع   الكمية فارغ '))
            return redirect('add_to_colar',id=id)
       
        tr = Product.objects.get(pk=id)
        ca = Color.objects.filter(productcolor=tr)
        for i in ca:
            if i.name == request.POST.get('name'):
                messages.warning(request, _('هذا اللون موجود مسبقا من هذا المنتج'))
                return redirect('add_to_colar',id=id)
           
        if name or qucolor :
            pro = get_object_or_404(Product,pk=id)
            q  = Color.objects.filter(productcolor=pro).aggregate(Sum("qucolor"))['qucolor__sum']
            if q :
                q = q
            else:
                q = 0
    
                
            w = int(qucolor) + int(q)
            print(w)
            if pro.qu >=  w :
           

                color = Color.objects.create(  
                     productcolor=pro,
                     asname=asname,
                        name=name,
                        qucolor=qucolor,
                        color= request.FILES["color"]
                        )
                messages.success(request, _('تمت العمليه بنجاح'))
                return redirect('w_to_colar' , id=id )
            else:
                 messages.warning(request, _('  الكمية غير   كافية'))
                 return redirect('add_to_colar',id=id) 
        else:
                 messages.warning(request, _('يوجد مربع فارغ'))
                 return redirect('add_to_colar',id=id) 
        
    if request.user.groups.filter(name='adminCastomar'):
        tr = True
        t = True
    else:
        tr = False
        t = False

    if request.user.groups.filter(name='hr'):
        hrr = True
   
    else:
        hrr = False    
    return render(request, 'prodects/addcolar.html',{'form' : Colorform(),
                                                      'hrr':hrr,
       'tr':tr,
       't':t,})

@ratelimit(key='user_or_ip', rate='40/m')
@login_required(login_url='signin')
@allowedUsers(allowedGroups=['adminCastomar','factory','groadmin'])

@transaction.atomic
def add_to_size(request,id_pro,id_color):
 
    
    pro = get_object_or_404(Product,pk=id_pro)
    colorr = Color.objects.get(productcolor_id=pro,id=id_color)
   
 
    q  = Sise.objects.filter(productsise=colorr).aggregate(Sum("qusise"))['qusise__sum']
    print(q)
   
  
    if request.method == 'POST':
        if 'sisel' in request.POST :
            sisel = request.POST.get('sisel')
        else:
            messages.warning(request, _('  مربع المقاس فارغ '))
            return redirect('add_to_size',id_pro=id_pro,id_color=id_color)
        if 'qusise' in request.POST :
            qusise = request.POST.get('qusise')
        else:
            messages.error(request, _('  مربع   الكمية فارغ '))
            return redirect('add_to_size',id_pro=id_pro,id_color=id_color)
        tr = get_object_or_404(Product,pk=id_pro)
        ca = Color.objects.get(productcolor_id=tr,id=id_color)
        qk  = Sise.objects.filter(productsise=ca,sisel=sisel).exists() 
        if qk:
                messages.warning(request, _('هذا المقاس موجود مسبقا من هذا اللون'))
                return redirect('add_to_size',id_pro=id_pro,id_color=id_color)
        elif sisel or qusise :
            pro = get_object_or_404(Product,pk=id_pro)
            colorr = Color.objects.get(productcolor_id=pro,id=id_color)
            q  = Sise.objects.filter(productsise=colorr).aggregate(Sum("qusise"))['qusise__sum']
            print(q)
            if q :
                q = q
            else:
                q = 0
    
            w = int(qusise) + int(q)
            print(w)
            if colorr.qucolor >=  w :
                color = Sise.objects.create(  
                        productsise=colorr,
                        sisel=sisel,
                        qusise=qusise,
                  
                        )
                messages.success(request, _('تمت العمليه بنجاح'))
                return redirect('w_size',id_pro=id_pro,id_color=id_color )
            else:
                 messages.warning(request, _('  الكمية غير   كافية'))
                 return redirect('add_to_size',id_pro=id_pro,id_color=id_color)
        else:
                 messages.warning(request, _('يوجد مربع فارغ'))
                 return redirect('add_to_size',id_pro=id_pro,id_color=id_color)
    
    if request.user.groups.filter(name='adminCastomar'):
        tr = True
        t = True
    else:
        tr = False
        t = False

    if request.user.groups.filter(name='hr'):
        hrr = True
   
    else:
        hrr = False
    return render(request, 'prodects/addsize.html',{ 'hrr':hrr,
       'tr':tr,
       't':t,})


@ratelimit(key='user_or_ip', rate='50/m')
@login_required(login_url='signin')
@allowedUsers(allowedGroups=['adminCastomar','factory','groadmin'])

@transaction.atomic
def w_size(request,id_pro,id_color):

    pro = get_object_or_404(Product,pk=id_pro)
    color = Color.objects.get(productcolor_id=pro,pk=id_color)
    sizes = Sise.objects.filter(productsise__productcolor_id=pro,productsise__name=color)
   

    if request.user.groups.filter(name='adminCastomar'):
        tr = True
        t = True
    else:
        tr = False
        t = False

    if request.user.groups.filter(name='hr'):
        hrr = True
   
    else:
        hrr = False
    return render(request, 'prodects/w_size.html',{'sizes':sizes,'pro':pro,'color':color,'pro':pro, 'hrr':hrr,
       'tr':tr,
       't':t,})
@ratelimit(key='user_or_ip', rate='50/m')
@login_required(login_url='signin')
@allowedUsers(allowedGroups=['adminCastomar','factory','groadmin'])

@transaction.atomic
def d_color(request,id_pro,id_color):
    pro = get_object_or_404(Product,pk=id_pro)
  
    if request.method == 'POST':
          pro = get_object_or_404(Product,pk=id_pro)
          color = Color.objects.filter(productcolor_id=pro,pk=id_color)
          color.delete()
          messages.success(request, _('تم الحذف بنجاح'))
          return redirect('w_to_colar' , id=id_pro )

    else:
         if request.user.groups.filter(name='adminCastomar'):
            tr = True
            t = True
         else:
            tr = False
            t = False

         if request.user.groups.filter(name='hr'):
            hrr = True
   
         else:
            hrr = False
         return render(request, 'pages/delete.html',{ 'hrr':hrr,
       'tr':tr,
       't':t,})

@ratelimit(key='user_or_ip', rate='50/m')
@login_required(login_url='signin')
@allowedUsers(allowedGroups=['adminCastomar','factory','groadmin'])

@transaction.atomic
def d_size(request,id,id_pro,id_color):
    
  
    if request.method == 'POST':
       
          sizes = Sise.objects.get(productsise__productcolor_id=id,productsise__id=id_pro,id=id_color)
          sizes.delete()
          messages.success(request, _('تم الحذف بنجاح'))
          return redirect('w_size',id_pro=id,id_color=id_pro )
   
    else:
         if request.user.groups.filter(name='adminCastomar'):
              tr = True
              t = True
         else:
           tr = False
           t = False

         if request.user.groups.filter(name='hr'):
           hrr = True
   
         else:
           hrr = False
         return render(request, 'pages/delete.html',{ 'hrr':hrr,
       'tr':tr,
       't':t,})
@ratelimit(key='user_or_ip', rate='50/m')
@login_required(login_url='signin')
@allowedUsers(allowedGroups=['adminCastomar','factory','groadmin'])

@transaction.atomic
def update_size(request ,id,id_pro,id_color):
     book_id =   Sise.objects.get(productsise__productcolor__id=id,productsise__id=id_pro,id=id_color)
     if request.method =='POST':
          book_id =   Sise.objects.get(productsise__productcolor__id=id,productsise__id=id_pro,id=id_color)
          book_save = Sizeform(request.POST, request.FILES, instance=book_id)
          pro = get_object_or_404(Product,pk=id)
          colorr = Color.objects.get(productcolor_id=pro,id=id_pro)
          gg =  request.POST.get("qusise")
          qs  = Sise.objects.filter(productsise=colorr).aggregate(Sum("qusise"))['qusise__sum']
          ddv = Sise.objects.get(productsise=colorr , id=id_color)
          q = qs - ddv.qusise
          if q :
              q = q
          else:
              q = 0
    
          w = int(gg) + int(q)
            
          if  colorr.qucolor >=  w :
                if book_save.is_valid():
                     book_save.save(),
                     messages.success(request, _('تم التعديل بنجاح'))

                     return redirect('w_size',id_pro=id,id_color=id_pro )
                
          else:
              messages.warning(request, _('  الكمية غير   كافية'))

              return redirect('update_size',id=id,id_pro=id_pro,id_color=id_color )
     else:
         book_save = Sizeform(instance=book_id)
     
         context ={
              'form':book_save,
         

         }
     return render(request,'pages/update.html',context,)

@ratelimit(key='user_or_ip', rate='50/m')
@login_required(login_url='signin')
@allowedUsers(allowedGroups=['adminCastomar','factory','groadmin'])

@transaction.atomic
def update_color(request ,id_pro,id_color):
     pro = get_object_or_404(Product,pk=id_pro)
     book_id = Color.objects.get(productcolor_id=pro,pk=id_color)
     pro = get_object_or_404(Product,pk=id_pro)
     

     if request.method =='POST':
        qs = Color.objects.filter(productcolor_id=pro).aggregate(Sum("qucolor"))['qucolor__sum']
        hh = Color.objects.get(productcolor_id=pro,id=id_color)
        q = qs - hh.qucolor
        gg =  request.POST.get("qucolor")
      
             
        if q :
                 q = q
        else:
                 q = 0
       
        w = int(gg) + int(q)
        print(w)
        
               
        if  pro.qu >=  w :
          book_save = Colorform(request.POST, request.FILES, instance=book_id)
          if book_save.is_valid():
               book_save.save()
               messages.success(request, _('تم التعديل بنجاح'))
               return redirect('w_to_colar' , id=id_pro )
        else:
              messages.warning(request, _('الكمية غير   كافية'))

              return redirect('update_color',id_pro=id_pro,id_color=id_color )
     else:
         book_save = Colorform(instance=book_id)
         if request.user.groups.filter(name='adminCastomar'):
           tr = True
           t = True
         else:
             tr = False
             t = False
     
         if request.user.groups.filter(name='hr'):
             hrr = True
        
         else:
             hrr = False
         context ={
              'form':book_save,
               'hrr':hrr,
       'tr':tr,
       't':t,

         }
     return render(request,'pages/update.html',context)


from django.db.models import Sum,F,Count
@login_required(login_url='signin')
@ratelimit(key='user_or_ip', rate='100/m')
@transaction.atomic
def add_to_cart(request):
    orderf = None
    if 'pro_id' in request.GET :
        qty = request.GET['qty']
        pro_id = request.GET['pro_id']
   
    if not request.user.is_authenticated and not request.user.is_anonymous:
        messages.error(request, _('سجل الدخول اولا'))
        return redirect('prodects')
    
    elif not int(qty) >= 1 :
        messages.error(request, _('قيمه خاطئه '))
        return redirect('prodect' ,uuid=uuid)

    elif 'pro_id' in request.GET and 'qty' in request.GET and 'price' in request.GET and request.user.is_authenticated and not request.user.is_anonymous:
        pro_id = request.GET['pro_id']
        uuid = request.GET['uuid']

        qty = request.GET['qty']
        order = Order.objects.all().filter(user=request.user, is_finished=False)
        # orderf = Order.objects.all().get(user=request.user, is_finished=False)
        if not Product.objects.all().filter(id=pro_id).exists():
            return redirect('prodects')
        pro = Product.objects.get(id=pro_id)
        proo = Product.objects.filter(id=pro_id,facat =True)
        colar = None
        size = None
        namei = None
        if proo:
             if 'colar' in request.GET :
                 colar = request.GET['colar']
             else:
                 messages.error(request, _('  مربع اللون فارغ '))
                 return redirect('prodect' ,uuid=uuid)
             if 'size' in request.GET : 
                size = request.GET['size']
             else:
                 messages.error(request, _('  مربع المقاس فارغ '))
                 return redirect('prodect' ,uuid=uuid)
        prog = Product.objects.filter(id=pro_id,boonimg  =True)
        if prog:
            if 'namei' in request.GET  :
                namei = request.GET['namei']
            else:
                messages.error(request, _('  مربع الون فارغ '))
                return redirect('prodect' ,uuid=uuid)
        

        if order:
        
            ord_order = Order.objects.get(user=request.user, is_finished=False)

            if OrderDetails.objects.all().filter(order=ord_order,product=pro,size=size,colar=colar).filter(product__facat =True).exclude(product__boonimg =True).exists():
                pros = Product.objects.get(id=pro_id)
                if   pros.qu > int(qty) :
                    orderdetails =OrderDetails.objects.all().get(order=ord_order,product=pro,size=size,colar=colar)
                    pros = Product.objects.get(id=pro_id)
                    ids = request.GET['pro_id']
                   
                 
                    proo = Product.objects.filter(id=pro_id,facat =True)
                    if proo:
                             if 'colar' in request.GET or proo:
                                 colar = request.GET['colar']
                             else:
                                 messages.error(request, _('  مربع الون فارغ '))
                                 return redirect('prodect' ,uuid=uuid)
    
                             if 'size' in request.GET or proo: 
                                size = request.GET['size']
                             else:
                                 messages.error(request, _('  مربع المقاس فارغ '))
                                 return redirect('prodect' ,uuid=uuid)
                  
                             ids = request.GET['pro_id']
                             p = Product.objects.get(id=ids)
             
                             colorr = Color.objects.get(productcolor_id=ids,name=colar)
                             sizes = Sise.objects.get(productsise=colorr,sisel=size)
                             if not sizes.qusise >= int(qty) + int(orderdetails.quantity) or sizes.qusise <= 0 or sizes.qusise < int(orderdetails.quantity) + int(qty):
                                
                                messages.error(request, _(f' كمية هذا المقاس  {sizes.sisel}   غير   كافية يوجد الان   كمية {sizes.qusise}'))
                                return redirect('prodect' ,uuid=uuid)
                             
                       
                              
                             else:
                             
                                colorr = Color.objects.get(productcolor_id=ids,name=colar)
                                if not  colorr.qucolor >= int(qty) or colorr.qucolor <=0  :
                                    messages.error(request, _(' كمية هذا الون غير   كافية '))
                                    
                                    return redirect('prodect' ,uuid=uuid)
                                   
    
                                else:
                                  
                                   orderdetails.quantity += int(qty)
                           
                                   orderdetails.save()
                                   ddf = Fintion.objects.filter(order_detils = orderdetails.pk,fintion=orderdetails.product.pk, order_idsid=orderdetails.order.pk)
                                   if ddf:
                                        Fintion.objects.filter(order_detils = orderdetails.pk,fintion=orderdetails.product.pk, order_idsid=orderdetails.order.pk).update(usus = int(orderdetails.quantity))
                                   else:
                                      Fintion.objects.create(
                                       fintion=orderdetails.product.pk,
                                       order_idsid=orderdetails.order.pk,
                                       usus = int(orderdetails.quantity),
                                       order_detils = orderdetails.pk,

                                     )
                                   messages.success(request,  _(f'تم زيادة الكمية بامقدار {qty}'))
                    # else:
                    #     orderdetails.quantity += int(qty)
                    #     orderdetails.save()           
   
                else:
                      messages.error(request, _('الكمية غير   كافية'))
                      return redirect('prodect' ,uuid=uuid)
            elif OrderDetails.objects.all().filter(order=ord_order,product=pro,nameimg=namei,product__boonimg =True).exclude(product__facat =True).exists():
                pros = Product.objects.get(id=pro_id)
              
              
                orderdetailsd = OrderDetails.objects.get(order=ord_order,product=pros,product__boonimg =True,nameimg=namei)

                orderdey = OrderDetails.objects.filter(order=ord_order,product=pros)
                
              
                if 'namei' in request.GET or boonimg:
                             namei = request.GET['namei']
                else:
                             messages.error(request, _('  مربع اللون فارغ '))
                             return redirect('prodect' ,uuid=uuid)
                pros = Img.objects.get(i__name=pros,name=namei)
               

                if   int(pros.quimg) >= int(qty ) + int(orderdetailsd.quantity):
                            orderdetails =OrderDetails.objects.get(order=ord_order,product=pro,nameimg=namei)
                            pros = Product.objects.get(id=pro_id)
                            ids = request.GET['pro_id']
                  
                            orderdetails.quantity += int(qty)
                           
                            orderdetails.save()
                            ddf = Fintion.objects.filter(order_detils = orderdetails.pk,fintion=orderdetails.product.pk, order_idsid=orderdetails.order.pk)
                            if ddf:
                                        Fintion.objects.filter(order_detils = orderdetails.pk,fintion=orderdetails.product.pk, order_idsid=orderdetails.order.pk).update(usus = int(orderdetails.quantity))
                            else:
                                      Fintion.objects.create(
                                       fintion=orderdetails.product.pk,
                                       order_idsid=orderdetails.order.pk,
                                       usus = int(orderdetails.quantity),
                                       order_detils = orderdetails.pk,

                                     )
                            messages.success(request, _(f'تم زيادة هذا المنتج  {pros.name}   بقيمة  {qty}'))
    
                       
                else:
                      messages.error(request, _(f'كمية هذا المنتج  {pros.name} غير   كافية يوجد الان   كمية {pros.quimg}' ))
                      return redirect('prodect' ,uuid=uuid)
            elif OrderDetails.objects.all().filter(order=ord_order,product=pro).filter(product__facat =False,product__boonimg =False).exists():
                pros = Product.objects.get(id=pro_id)
             
                orderdetailsd = OrderDetails.objects.get(order=ord_order,product=pro)
       
                orderdey = OrderDetails.objects.filter(order=ord_order,product=pros)
     
                pros = Product.objects.get(id=pro_id)
               

                if   int(pros.qu) >= int(qty ) + int(orderdetailsd.quantity):
                            orderdetails =OrderDetails.objects.get(order=ord_order,product=pro)
                            pros = Product.objects.get(id=pro_id)
                            ids = request.GET['pro_id']
                  
                            orderdetails.quantity += int(qty)
                           
                            orderdetails.save()
                            ddf = Fintion.objects.filter(order_detils = orderdetails.pk,fintion=orderdetails.product.pk, order_idsid=orderdetails.order.pk)
                            if ddf:
                                        Fintion.objects.filter(order_detils = orderdetails.pk,fintion=orderdetails.product.pk, order_idsid=orderdetails.order.pk).update(usus = int(orderdetails.quantity))
                            else:
                                      Fintion.objects.create(
                                       fintion=orderdetails.product.pk,
                                       order_idsid=orderdetails.order.pk,
                                       usus = int(orderdetails.quantity),
                                       order_detils = orderdetails.pk,

                                     )
                            messages.success(request, _(f'تم زيادة هذا المنتج  {pros.name}   بقيمة  {qty}'))
    
                       
                else:
                      messages.error(request, _(f'كمية هذا المنتج  {pros.name} غير   كافية يوجد الان   كمية {pros.qu}'))
                      return redirect('prodect' ,uuid=uuid)
    
            else:
               
                 pros = Product.objects.get(id=pro_id)
                 if   pros.qu >= int(qty) :
                      boonimg = Product.objects.filter(id=pro_id,boonimg =True)
                      pro = Product.objects.filter(id=pro_id,facat =True)
                      if pro:
                         if 'colar' in request.GET or proo:
                             colar = request.GET['colar']
                         else:
                             messages.error(request, _('  مربع اللون فارغ '))
                             return redirect('prodect' ,uuid=uuid)
              
                         ids = request.GET['pro_id']
                         if 'size' in request.GET or proo: 
                            size = request.GET['size']
                         else:
                             messages.error(request, _('  مربع المقاس فارغ '))
                             return redirect('prodect' ,uuid=uuid)
                      
                         colorr = Color.objects.get(productcolor_id=ids,name=colar)
                         sizes = Sise.objects.get(productsise=colorr,sisel=size)
                         if not sizes.qusise >= int(qty) or sizes.qusise < 0:
                           
                             messages.error(request,_( f'   كمية هذا المقاس  {sizes.sisel}  غير   كافية  يوجد الان   كمية {sizes.qusise}'))
                             return redirect('prodect' ,uuid=uuid)
                         else:
                         
                            if not colorr.qucolor >= int(qty) or colorr.qucolor < 0:
                               messages.error(request, _(' كمية هذا اللون غير   كافية '))
                               return redirect('prodect' ,uuid=uuid)
                            else:
                             
                                pro_id = request.GET['pro_id']
                                qty = request.GET['qty']
                                order = Order.objects.all().filter(user=request.user, is_finished=False)
                                orderf = Order.objects.all().get(user=request.user, is_finished=False)
                                pro = Product.objects.get(id=pro_id)
                                ids = request.GET['pro_id']
                                colorr = Color.objects.get(productcolor_id=ids,name=colar)
                                orderdetails = OrderDetails.objects.create(product=pro,order=ord_order,price=pro.price,quantity=qty,s=qty,size=size,colar=colar,OrderDetailsimg=colorr.color)
                                ddf = Fintion.objects.filter(order_detils = orderdetails.pk,fintion=pro, order_idsid=orderf)
                                if ddf:
                                   Fintion.objects.filter(order_detils = orderdetails.pk,fintion=pro, order_idsid=orderf).update(usus = int(orderdetails.quantity))
                                else:
                                   Fintion.objects.create(
                                       fintion=pro,
                                       order_idsid=orderf,
                                       usus = int(orderdetails.quantity),
                                       order_detils = orderdetails.pk,

                                    )
                                messages.success(request,  _('  تم الطلب بنجاح'))
                     
                      elif boonimg:
                         img=None
                         if 'namei' in request.GET or boonimg:
                             namei = request.GET['namei']
                             ids = request.GET['pro_id']
                             img = Img.objects.get(i__id=ids,name=namei)
                         else:
                             messages.error(request, _('  مربع اللون فارغ '))
                             return redirect('prodect' ,uuid=uuid)
                         
                         
                         
                         if not img.quimg >= int(qty) or img.quimg < 0:
                           
                             messages.error(request, _(f'   كمية هذا المنتج  {img.name}  غير   كافية  يوجد الان   كمية {img.quimg}'))
                             return redirect('prodect' ,uuid=uuid)
                         else:
                         
                                pro_id = request.GET['pro_id']
                                qty = request.GET['qty']
                                order = Order.objects.all().filter(user=request.user, is_finished=False)
                                orderf = Order.objects.all().get(user=request.user, is_finished=False)
                                pro = Product.objects.get(id=pro_id)
                                ids = request.GET['pro_id']
                                imgf = Img.objects.get(i_id=ids,name=namei)
                                orderdetails = OrderDetails.objects.create(product=pro,order=ord_order,price=pro.price,quantity=qty,s=qty,size=size,colar=colar,OrderDetailsimg=imgf.photos,nameimg=namei)
                                ddf = Fintion.objects.filter(order_detils = orderdetails.pk,fintion=pro, order_idsid=orderf)
                                if ddf:
                                   Fintion.objects.filter(order_detils = orderdetails.pk,fintion=pro, order_idsid=orderf).update(usus = int(orderdetails.quantity))
                                else:
                                   Fintion.objects.create(
                                       fintion=pro,
                                       order_idsid=orderf,
                                       usus = int(orderdetails.quantity),
                                       order_detils = orderdetails.pk,

                                    )
                                messages.success(request,  _('  تم الطلب بنجاح'))
                      else:
                           pro_id = request.GET['pro_id']
                           qty = request.GET['qty']
                           order = Order.objects.all().filter(user=request.user, is_finished=False)
                           orderf = Order.objects.all().get(user=request.user, is_finished=False)
                           pro = Product.objects.get(id=pro_id)
                          
                           orderdetails = OrderDetails.objects.create(product=pro,order=ord_order,price=pro.price,quantity=qty,s=qty)
                           ddf = Fintion.objects.filter(order_detils = orderdetails.pk,fintion=pro, order_idsid=orderf)
                           if ddf:
                              Fintion.objects.filter(order_detils = orderdetails.pk,fintion=pro, order_idsid=orderf).update(usus = int(orderdetails.quantity))
                           else:
                              Fintion.objects.create(
                                  fintion=pro,
                                  order_idsid=orderf,
                                  usus = int(orderdetails.quantity),
                                  order_detils = orderdetails.pk   
                               )
                     
                           messages.success(request,  _('  تم الطلب بنجاح'))
                           return redirect('prodects')
              
                    
                 else:
                      messages.error(request, _(f'الكمية التى طلبتها من هذا المنتج {pros.name} غير   كافية يوجد الان   كمية {pros.qu}'))
                      return redirect('prodect' ,uuid=uuid)
     
    
        else:
            g= Group.objects.get(name='castomar')
            if request.user.groups.filter(name=g.name):
                #  messages.success(request, '  تم الطلب بنجاح')
                 pros = Product.objects.get(id=pro_id)
                 if   pros.qu >= int(qty) and pros.qu >= 0:
                      
                      pro = Product.objects.filter(id=pro_id,facat =True)
                      ret = Product.objects.filter(id=pro_id,boonimg =True)
                      if pro:
                         if 'colar' in request.GET :
                             colar = request.GET['colar']
                         else:
                              messages.error(request, _('  مربع الون فارغ '))
                              return redirect('prodect' ,uuid=uuid)
                         if 'size' in request.GET : 
                              size = request.GET['size']
                         else:
                            messages.error(request, _('  مربع المقاس فارغ '))
                            return redirect('prodect' ,uuid=uuid)
                         
                         ids = request.GET['pro_id']
                         colorr = Color.objects.get(productcolor_id=ids,name=colar)
                         sizes = Sise.objects.get(productsise__name=colorr,sisel=size)
                       
                         if not sizes.qusise >= int(qty) or sizes.qusise <= 0:
                             messages.error(request, _(f' كمية هذا المقاس {sizes.sisel} غير   كافية يوجد الان   كمية {sizes.qusise}'))
                             return redirect('prodect' ,uuid=uuid)
                         
                   
                          
                         else:
                         
                            colorr = Color.objects.get(productcolor_id=ids,name=colar)
                            if not  colorr.qucolor >= int(qty) or colorr.qucolor <=0  :
                                messages.error(request, _(' كمية هذا اللون غير   كافية '))
                               
                                return redirect('prodect' ,uuid=uuid)
                               

                            else:
                              
                               new_order=Order()
                               new_order.user= request.user
                               new_order.order_date =timezone.now()
                               new_order.is_finished = False
                               user = User()
                               new_order.user_group = g
                               new_order.save()
                                    
                            
                               pro_id = request.GET['pro_id']
                               qty = request.GET['qty']
                               order = Order.objects.all().filter(user=request.user, is_finished=False)
                               orderf = Order.objects.all().get(user=request.user, is_finished=False)
                               pro = Product.objects.get(id=pro_id)
                                
                               ids = request.GET['pro_id']
                               colorr = Color.objects.get(productcolor_id=ids,name=colar)

                               orderdetails = OrderDetails.objects.create(product=pro,order=new_order,price=pro.price,quantity=qty,s=qty,size=size,colar=colar,OrderDetailsimg=colorr.color)
                               ddf = Fintion.objects.filter(order_detils = orderdetails.pk,fintion=pro, order_idsid=orderf)
                               if ddf:
                                   Fintion.objects.filter(order_detils = orderdetails.pk,fintion=pro, order_idsid=orderf).update(usus = int(orderdetails.quantity))
                               else:
                                   Fintion.objects.create(
                                       fintion=pro,
                                       order_idsid=orderf,
                                       usus = int(orderdetails.quantity),
                                       order_detils = orderdetails.pk,

                                    )
                               messages.success(request, _('  تم الطلب بنجاح'))
                            
           
                      elif ret:
                            if 'namei' in request.GET :
                                namei = request.GET['namei']
                            else:
                                 messages.error(request, _('  مربع المنتج فارغ '))
                                 return redirect('prodect' ,uuid=uuid)
                            
                            
                            ids = request.GET['pro_id']
                            imdfg = Img.objects.get(i__id=ids,name=namei)
                            
                          
                            if not imdfg.quimg >= int(qty) or imdfg.quimg <= 0:
                                messages.error(request, _(f' كمية هذا المنتج {imdfg.name} غير   كافية يوجد الان   كمية {imdfg.quimg}'))
                                return redirect('prodect' ,uuid=uuid)
                            
                      
                             
                            else:
                            
                       
                                  new_order=Order()
                                  new_order.user= request.user
                                  new_order.order_date =timezone.now()
                                  new_order.is_finished = False
                                  user = User()
                                  new_order.user_group = g
                                  new_order.save()
                                       
                               
                                  pro_id = request.GET['pro_id']
                                  qty = request.GET['qty']
                                  order = Order.objects.all().filter(user=request.user, is_finished=False)
                                  orderf = Order.objects.all().get(user=request.user, is_finished=False)
                                  pro = Product.objects.get(id=pro_id)
                                   
                                  ids = request.GET['pro_id']
                                  imgd = Img.objects.get(i__id=ids,name=namei)
   
                                  orderdetails = OrderDetails.objects.create(product=pro,order=new_order,price=pro.price,quantity=qty,s=qty,size=size,colar=colar,OrderDetailsimg=imgd.photos,nameimg=namei)
                                  ddf = Fintion.objects.filter(order_detils = orderdetails.pk,fintion=pro, order_idsid=orderf)
                                  if ddf:
                                     Fintion.objects.filter(order_detils = orderdetails.pk,fintion=pro, order_idsid=orderf).update(usus = int(orderdetails.quantity))
                                  else:
                                     Fintion.objects.create(
                                         fintion=pro,
                                         order_idsid=orderf,
                                         usus = int(orderdetails.quantity),
                                         order_detils = orderdetails.pk,

                                      )
                                  messages.success(request,_( '  تم الطلب بنجاح'))
                         
                         
   
                      else:
                         new_order=Order()
                         new_order.user= request.user
                         new_order.order_date =timezone.now()
                         new_order.is_finished = False
                         user = User()
                         new_order.user_group = g
                         new_order.save()
                     
                         pro_id = request.GET['pro_id']
                         qty = request.GET['qty']
                         
            
                         order = Order.objects.all().filter(user=request.user, is_finished=False)
                         orderf = Order.objects.all().get(user=request.user, is_finished=False)
                         pro = Product.objects.get(id=pro_id)

                         orderdetails = OrderDetails.objects.create(product=pro,order=new_order,price=pro.price,quantity=qty,s=qty)
                         ddf = Fintion.objects.filter(order_detils = orderdetails.pk,fintion=pro, order_idsid=orderf)
                         if ddf:
                                   Fintion.objects.filter(order_detils = orderdetails.pk,fintion=pro, order_idsid=orderf).update(usus =int(orderdetails.quantity))
                         else:
                                   Fintion.objects.create(
                                       fintion=pro,
                                       order_idsid=orderf,
                                       usus = int(orderdetails.quantity),
                                       order_detils = orderdetails.pk,

                                    )
                         messages.success(request, _('  تم الطلب بنجاح'))

                        #  orderdetails.quantity == int(orderdetails.quantity) + int(qty)
                      
                        #  orderdetails.save()
                
                 else:
                      messages.error(request, _('  الكمية غير   كافية'))
                      return redirect('prodect' ,uuid=uuid)
                

            else:
             
                group = Group.objects.get(name='admin')
                if request.user.groups.filter(name=group.name):
                    # messages.success(request,  '  تم الطلب بنجاح')
                    pros = Product.objects.get(id=pro_id)
                    if   pros.qu >= int(qty) and pros.qu > 0:
                         
                         pro = Product.objects.filter(id=pro_id,facat =True)
                         ret = Product.objects.filter(id=pro_id,boonimg =True)
                         rget = Product.objects.filter(id=pro_id,boonimg =False,facat =False)

                         if pro:
                 
                            ids = request.GET['pro_id']
                            colorr = Color.objects.get(productcolor_id=ids,name=colar)
                            size = request.GET['size']
                            sizes = Sise.objects.get(productsise__productcolor_id=ids,sisel=size)
                            
                            
                            if not sizes.qusise >= int(qty) or sizes.qusise <= 0:
                                messages.error(request, _(f' كمية هذا المقاس  {sizes.sisel} غير   كافية يوجد الان   كمية {sizes.qusise}'))
                                return redirect('prodect' ,uuid=uuid)
                            
                      
                             
                            else:
                               colar = request.GET['colar']
                               colorr = Color.objects.get(productcolor_id=ids,name=colar)
                               if not  colorr.qucolor > int(qty) or colorr.qucolor <=0  :
                                   messages.error(request, _(' كمية هذا اللون غير   كافية '))
                                  
                                   return redirect('prodect' ,uuid=uuid)
                                  
   
                               else:
                                
                                  new_order=Order()
                                  new_order.user= request.user
                                  new_order.order_date =timezone.now()
                                  new_order.is_finished = False
                                  user = User()
                                  new_order.user_group = Group.objects.get(name='admin')
                                  new_order.save()
                                       
                               
                                  pro_id = request.GET['pro_id']
                                  qty = request.GET['qty']
                                  order = Order.objects.all().filter(user=request.user, is_finished=False)
                                  orderf = Order.objects.all().get(user=request.user, is_finished=False)
                                  pro = Product.objects.get(id=pro_id)
   
   
                                  ids = request.GET['pro_id']
                                  colorr = Color.objects.get(productcolor_id=ids,name=colar)
                                  orderdetails = OrderDetails.objects.create(product=pro,order=new_order,price=pro.price,quantity=qty,s=qty,size=size,colar=colar,OrderDetailsimg=colorr.color)
                                  ddf = Fintion.objects.filter(order_detils = orderdetails.pk,fintion=pro, order_idsid=orderf.pk)
                                  if ddf:
                                         Fintion.objects.filter(order_detils = orderdetails.pk,fintion=pro, order_idsid=order).update(usus = int(orderdetails.quantity))
                                  else:
                                         Fintion.objects.create(
                                             fintion=pro,
                                             order_idsid=orderf,
                                             usus = int(orderdetails.quantity),
                                             order_detils = orderdetails.pk,
      
                                          )
                                  messages.success(request, _('  تم الطلب بنجاح'))

                                #   orderdetails.quantity == int(orderdetails.quantity) + int(qty)
                      
                                #   orderdetails.save()
                         
                                
                         elif ret:
                            if 'namei' in request.GET :
                                namei = request.GET['namei']
                            else:
                                 messages.error(request, _('  مربع المنتج فارغ '))
                                 return redirect('prodect' ,uuid=uuid)
                            
                            
                            ids = request.GET['pro_id']
                            imdfg = Img.objects.get(i__id=ids,name=namei)
                            
                          
                            if not imdfg.quimg >= int(qty) or imdfg.quimg <= 0:
                                messages.error(request,_( f' كمية هذا المقاس {imdfg.name} غير   كافية يوجد الان   كمية {imdfg.quimg}'))
                                return redirect('prodect' ,uuid=uuid)
                            
                      
                             
                            else:
                            
                       
                                  new_order=Order()
                                  new_order.user= request.user
                                  new_order.order_date =timezone.now()
                                  new_order.is_finished = False
                                  user = User()
                                  new_order.user_group = Group.objects.get(name='admin')
                                  new_order.save()
                                       
                               
                                  pro_id = request.GET['pro_id']
                                  qty = request.GET['qty']
                                  order = Order.objects.all().filter(user=request.user, is_finished=False)
                                  orderf = Order.objects.all().get(user=request.user, is_finished=False)
                                  pro = Product.objects.get(id=pro_id)
                                   
                                  ids = request.GET['pro_id']
                                  imgd = Img.objects.get(i__id=ids,name=namei)
   
                                  orderdetails = OrderDetails.objects.create(product=pro,order=new_order,price=pro.price,quantity=qty,s=qty,size=size,colar=colar,OrderDetailsimg=imgd.photos,nameimg=namei)
                                  ddf = Fintion.objects.filter(order_detils = orderdetails.pk,fintion=pro, order_idsid=orderf.pk)
                                  if ddf:
                                         Fintion.objects.filter(order_detils = orderdetails.pk,fintion=pro, order_idsid=order).update(usus = int(orderdetails.quantity))
                                  else:
                                         Fintion.objects.create(
                                             fintion=pro,
                                             order_idsid=orderf,
                                             usus = int(orderdetails.quantity),
                                             order_detils = orderdetails.pk,

                                          )
                                  messages.success(request, _('  تم الطلب بنجاح'))
                         
                         
   
                         elif rget:
                            new_order=Order()
                            new_order.user= request.user
                            new_order.order_date =timezone.now()
                            new_order.is_finished = False
                            user = User()
                            new_order.user_group = Group.objects.get(name='admin')
                            new_order.save()
                                 
                           
                            pro_id = request.GET['pro_id']
                            qty = request.GET['qty']
                            
                            order = Order.objects.all().filter(user=request.user, is_finished=False)
                            orderf = Order.objects.all().get(user=request.user, is_finished=False)

                            pro = Product.objects.get(id=pro_id)
                           
                            orderdetails = OrderDetails.objects.create(product=pro,order=new_order,price=pro.price,quantity=qty,s=qty)
                            ddf = Fintion.objects.filter(order_detils = orderdetails.pk,fintion=pro, order_idsid=orderf.pk)
                            if ddf:
                                   Fintion.objects.filter(order_detils = orderdetails.pk,fintion=pro, order_idsid=order).update(usus =int(orderdetails.quantity))
                            else:
                                   Fintion.objects.create(
                                       fintion=pro,
                                       order_idsid=orderf,
                                       usus = int(orderdetails.quantity),
                                       order_detils = orderdetails.pk,

                                    )
                            messages.success(request, _('  تم الطلب بنجاح'))

                            
                    else:
                         messages.error(request, _('الكمية غير   كافية'))
                         return redirect('prodect' ,uuid=uuid)

        return redirect('prodects')
    else:
       if 'pro_id' in request.GET:
           messages.error(request, _('هذا المنتج غير موجود'))
           return redirect('prodects')
       else:
           return redirect('prodects')




@ratelimit(key='user_or_ip', rate='50/m')
@login_required(login_url='signin')
@transaction.atomic
def cart(request):
    group = Group.objects.get(name='castomar')
    usery = User.objects.filter(groups__name=group)
    # print(usery)
    if request.user in usery:
        t = True
       
    else :
        t = False
    context = None
    if  request.user.is_authenticated and not request.user.is_anonymous:
        if Order.objects.all().filter(user=request.user, is_finished=False):
            order = Order.objects.get(user=request.user, is_finished=False)
            orderdetails = OrderDetails.objects.all().filter(order=order)
            total = 0
            for  sub in orderdetails:
                 total += sub.price * sub.quantity


            context ={
                'order':order,
                'orderdetails':orderdetails,
                'total':total,
                't':t,
                'Order':Order,
                'category':Category.objects.all(),

                }

    
    return render(request, 'orders/card.html',context, )




from product.models import *
@ratelimit(key='user_or_ip', rate='50/m')
@login_required(login_url='signin')
@transaction.atomic
def remove_from_card(request, orderdetails_id):
    if request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id:
        orderdetails = OrderDetails.objects.get(id=orderdetails_id)
        if orderdetails.order.user.id == request.user.id:
            ddf = Fintion.objects.filter(order_detils = orderdetails.pk,fintion=orderdetails.product)
            if ddf:
                 Fintion.objects.filter(order_detils = orderdetails.pk,fintion=orderdetails.product).delete()
            orderdetails.delete()
            messages.success(request, _( f' تم خذف المنتج {orderdetails.product.name} '))
    return redirect('cart')



@ratelimit(key='user_or_ip', rate='50/m')
@login_required(login_url='signin')
@transaction.atomic
def add_qty(request, orderdetails_id):
    if request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id:
        orderdetails = OrderDetails.objects.get(id=orderdetails_id)
        pro = Product.objects.get(pk=orderdetails.product.pk)
        proo = Product.objects.filter(id=orderdetails.product.pk,facat =True)
        imgd = Product.objects.filter(id=orderdetails.product.pk,boonimg =True)
        if proo:
         orderdetails = OrderDetails.objects.get(id=orderdetails_id,order__user=request.user)
         proi = Product.objects.get(id=orderdetails.product.id)
         colorr = Color.objects.get(productcolor_id=pro,name=orderdetails.colar)
         sizes = Sise.objects.get(productsise__name=colorr,sisel=orderdetails.size)
         if  sizes.qusise > orderdetails.quantity:
            orderdetails = OrderDetails.objects.get(id=orderdetails_id)
            orderdetails.quantity += 1
            orderdetails.save()
            ordelsde =  OrderDetails.objects.get(id=orderdetails_id,order__user=request.user)
            ddf = Fintion.objects.filter(order_detils = orderdetails.pk,fintion=orderdetails.product.pk,order_idsid=orderdetails.order.pk)
            print(ddf)
            if ddf:
                   ddddf =  Fintion.objects.filter(order_detils = orderdetails.pk,fintion=orderdetails.product.pk,order_idsid=orderdetails.order.pk).update(usus = int(orderdetails.quantity))
                
            messages.success(request,_('تم زيادة الكمية بقيمة واحد'))
         else:
              messages.error(request, _(f' كمية هذا المقاس {sizes.sisel}  غير   كافية يوجد الان   كمية {sizes.qusise } ولا يمكن الاضافة عليها'))
              return redirect('cart')
        elif imgd:
         orderdetails = OrderDetails.objects.get(id=orderdetails_id,order__user=request.user)
         proi = Product.objects.get(id=orderdetails.product.id)
         imfg = Img.objects.get(i_id=pro,name=orderdetails.nameimg)
         if  imfg.quimg > orderdetails.quantity:
            orderdetails = OrderDetails.objects.get(id=orderdetails_id)
            orderdetails.quantity += 1
            orderdetails.save()
            proi = Product.objects.get(id=orderdetails.product.id)
            ddf = Fintion.objects.filter(order_detils = orderdetails.pk,fintion=orderdetails.product.pk,order_idsid=orderdetails.order.pk)
        
            if ddf:
                   ddddf =  Fintion.objects.filter(order_detils = orderdetails.pk,fintion=orderdetails.product.pk,order_idsid=orderdetails.order.pk).update(usus = int(orderdetails.quantity))
                
            messages.success(request,_('تم زيادة الكمية   بقيمة واحد'))
         else:
              messages.error(request, _(f' كمية هذا المقاس {imfg.name}  غير   كافية يوجد الان   كمية {imfg.quimg} ولا يمكن   الاضافة عليها'))
              return redirect('cart')
        else:
            fs = Product.objects.filter(id=orderdetails.product.pk,facat =False)
            if fs:
                o= Product.objects.get(id=orderdetails.product.pk,facat =False)
                if o.qu > orderdetails.quantity:
                   orderdetails = OrderDetails.objects.get(id=orderdetails_id)
                   orderdetails.quantity += 1
                   orderdetails.save()
                   proi = Product.objects.get(id=orderdetails.product.id)
                   ddf = Fintion.objects.filter(order_detils = orderdetails.pk,fintion=orderdetails.product.pk,order_idsid=orderdetails.order.pk)
     
                   if ddf:
                       ddddf =  Fintion.objects.filter(order_detils = orderdetails.pk,fintion=orderdetails.product.pk,order_idsid=orderdetails.order.pk).update(usus = int(orderdetails.quantity))
                
                   messages.success(request,_('تم زيادة الكمية بمقدار واحد'))
                else:
                    messages.error(request,_(f' كمية هذا المنتج {orderdetails.product.name} غير كفيه يوجد الان   كمية {o.qu} ولا يمكن الاضافة'))
                    return redirect('cart')
    return redirect('cart')


@ratelimit(key='user_or_ip', rate='50/m')
@login_required(login_url='signin')
@transaction.atomic
def sub_qty(request, orderdetails_id):
    if request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id:
        orderdetails = OrderDetails.objects.get(id=orderdetails_id)
        pro = Product.objects.get(pk=orderdetails.product.pk)
        if orderdetails.quantity > 1:
            orderdetails.quantity -= 1
            orderdetails.save()
            ddf = Fintion.objects.filter(order_detils = orderdetails.pk,fintion=pro)
            if ddf:
                Fintion.objects.filter(order_detils = orderdetails.pk,fintion=pro).update(usus = orderdetails.quantity)
            messages.success(request,  _(f'تم تقليل الكمية بمقدار واحد '))
    return redirect('cart')

# from .test import sms
from celery import shared_task
@shared_task
@ratelimit(key='user_or_ip', rate='50/m')
@login_required(login_url='signin')
@transaction.atomic
def igggggggggggggg(request,order):
                        ordelsde =  OrderDetails.objects.filter(order=order)
                        no = None
                        he = None
                        usercastomar = request.user.groups.filter(name='castomar')
                        if usercastomar:
                            he = True
                        if request.method == 'POST':
                           no = request.POST['no']
                        s = 0
                        n = 0
                        for i in ordelsde:
                            s += i.quantity * i.product.price
                            n += i.quantity * i.product.qus
                        if usercastomar:
                            ru = int(s) + int(no) + int(n)
                        else:
                            ru = int(s) + int(no)

                        from_email = settings.EMAIL_HOST_USER
                        subject = f'order__{order.id}'
                        to = [request.user.email]
                        messages = _(" الفاتوره")
                        
                        html  = render_to_string('pyorder.html',{'he':he,'n':n,'t':messages,'order':ordelsde,'orders_id':order,'s':s,'no':no,'ru':ru})
                        send_mail(
                             subject ,
                             messages,
                             from_email ,
                             to ,
                             messages ,
                             html_message=html,
                        
                              )

import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from django.conf import settings
from django.http import JsonResponse
from celery import shared_task
@shared_task
def send_email_via_brevo(request,order):
    ordelsde =  OrderDetails.objects.filter(order=order).annotate(total_osa = F("price") * F("quantity")) 
    no = None
    he = None
    usercastomar = request.user.groups.filter(name='castomar')
    if usercastomar:
        he = True
    if request.method == 'POST':
       no = request.POST['no']
    s = 0
    n = 0
    for i in ordelsde:
        s += i.quantity * i.product.price
        n += i.quantity * i.product.qus
    if usercastomar:
        ru = int(s) + int(no) + int(n)
    else:
        ru = int(s) + int(no)

    from_email = settings.EMAIL_HOST_USER
    subject = f'order__{order.id}'
    to = [request.user.email]
    messages = " فاطوره من المستقبل السريع"
                        
    html_content   = render_to_string('pyorder.html',{'he':he,'n':n,'t':messages,'order':ordelsde,'orders_id':order,'s':s,'no':no,'ru':ru})
    
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = "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"

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": request.user.email}],
        sender={"email": settings.DEFAULT_FROM_EMAIL},
        subject=messages,
        html_content=html_content ,
       
    )

    try:
        api_instance.send_transac_email(email)
        return JsonResponse({"message": "تم إرسال البريد بنجاح!"})
    except ApiException as e:
        return JsonResponse({"error": f"خطأ في إرسال البريد: {e}"}, status=500)


# @ratelimit(kay='127.0.0.1', rate='3/m')
@login_required(login_url='signin')
@transaction.atomic
def payment(request):
    context = None
    ship_address = None
    ship_phone = None
    is_added = None
    if request.method == 'POST' and 'btnpayment' in request.POST  : 
        ship_address = request.POST['ship_address']
        ship_phone = request.POST['ship_phone']
        name = request.POST['name']
        mo = request.POST['mo']
        no = request.POST['no']
        momr = request.POST['momr']
        shipment_phone_to = request.POST['shipment_phone_to']
        districtid = request.POST['districtid']
        mr = request.POST['mr']
        if 'mr' in  request.POST : 
            mr = request.POST['mr']
        else:
           messages.error(request, _("مربع المركز فارغ"))
           return redirect('payment')
        if ship_address and ship_phone and name and mo and no and momr and  shipment_phone_to and districtid and mr:

                if  request.user.is_authenticated and not request.user.is_anonymous:
                    if Order.objects.all().filter(user=request.user, is_finished=False):
                        order = Order.objects.get(user=request.user, is_finished=False) 
                        payment = Payment(order=order,shipment_address=ship_address,shipment_phone=ship_phone,name=name,mo=mo,na=no,mr=mr,momr=momr,districtid=districtid,shipment_phone_to=shipment_phone_to)
                       
                        if   len(request.POST['ship_phone']) !=  int(11) :
                            messages.error(request, _('لبد ان يكون رقم الهاتف  يسوى 11 رقم'))
                            return redirect('payment')    
                        elif not  request.POST['ship_phone'].startswith('010') and not request.POST['ship_phone'].startswith('011')  and not request.POST['ship_phone'].startswith('012') and not request.POST['ship_phone'].startswith('015') :
                            messages.error(request, _('رقم الهاتف ليس صحيح'))
                            return redirect('payment')  
                        elif   len(request.POST['shipment_phone_to']) !=  int(11) :
                                messages.error(request, _('يجب ان يكون رقم الهاتف الاضافى يسوى 11 رقم'))
                                return redirect('payment')    
                        elif not  request.POST['shipment_phone_to'].startswith('010') and not request.POST['shipment_phone_to'].startswith('011')  and not request.POST['shipment_phone_to'].startswith('012') and not request.POST['shipment_phone_to'].startswith('015') :
                                messages.error(request, _('رقم الهاتف الاضافى ليس صالح'))
                                return redirect('payment')  
                        else:
                             orders = Order.objects.get(user=request.user, is_finished=False) 
                             ordelsde =  OrderDetails.objects.filter(order=orders)
                             for i in ordelsde:
                                if i.product.facat == True and i.product.boonimg == False:
                                    color = Color.objects.filter(productcolor__id=i.product.pk,name=i.colar)
                                    for c in color:
                                        if not i.quantity <= c.qucolor :
                                            messages.error(request, f'  كمية هذا اللون {c.name} غير كفيه يوجد   كمية {c.qucolor}')
                                            return redirect('payment')
                                        else:
                                            size = Sise.objects.filter(productsise__name=c.name,sisel=i.size)
                                            for s in size:
                                                if not i.quantity <= s.qusise :
                                                    messages.error(request, f'  كمية هذا المقاس {s.sisel} غير كفيه يوجد   كمية {s.qusise}')
                                                    return redirect('payment')
                                                else:
                                                    i.product.qu -= int(i.quantity)
                                                    i.product.save() 
                                                    color = Color.objects.filter(productcolor__id=i.product.pk,name=i.colar)
                                                    for c in color:
                                                        c.qucolor -= int(i.quantity)
                                                        c.save()
                                                        size = Sise.objects.filter(productsise__name=c.name,sisel=i.size)
                                                        for s in size:
                                                            s.qusise -= int(i.quantity)
                                                            s.save() 
                                elif  i.product.boonimg == True and i.product.facat == False:
                                      img = Img.objects.filter(i__id=i.product.pk,name=i.nameimg)
                                      for im in img:
                                        if not i.quantity <= im.quimg :
                                            messages.error(request, _(f'  كمية هذا المنتج {im.name} غير كفيه يوجد   كمية {im.quimg}'))
                                            return redirect('payment')
                                        else:
                                            i.product.qu -= int(i.quantity)
                                            i.product.save() 
                                            for im in img:
                                                    im.quimg -= int(i.quantity)
                                                    im.save()
                                elif  i.product.boonimg == False and i.product.facat == False:
                                    if i.product.qu >= int(i.quantity):
                                         i.product.qu -= int(i.quantity)
                                         i.product.save() 
                                    else:
                                        messages.error(request, f' كمية هذا المنتج  {i.product.name}  غير كفيه يوجد   كمية {i.product.qu} ' )
                                        return redirect('payment')
                                # orders = Order.objects.get(user=request.user, is_finished=False) 
                                ordelsde =  OrderDetails.objects.filter(order=order)
                                for i in ordelsde:
                                    ddf = Fintion.objects.filter(order_detils = i.pk,fintion=i.product.pk, order_idsid=orders.pk)
                                    if ddf:
                                         Fintion.objects.filter(order_detils = i.pk,fintion=i.product.pk, order_idsid=order.pk).update(usus =int(i.quantity))
                                    else:
                                         Fintion.objects.create(
                                             fintion=i.product.pk,
                                             order_idsid=orders.pk,
                                             usus = int(i.quantity),
                                             order_detils = i.pk
                                            )
                                is_added = True
                                # igggggggggggggg(request,order)
                                # send_email_via_brevo(request,order)
                                payment.save()
                                order.is_finished=True
                                order.save()
               
                    messages.success(request, 'تم تاكيد الطلب بنجاح' )
                    return redirect('/')
                context = {
            'ship_address':ship_address,
            'ship_phone':ship_phone,
            'mo':mo,
            'no':mo,
            'mo':Mo.objects.all(),
            'mr': Mr.objects.all(),
            'category':Category.objects.all(),
            'is_added':is_added,
        }
        else:
           messages.error(request, _("  يوجد مربع فارغ"))
           return redirect('payment')
    else:
        if  request.user.is_authenticated and not request.user.is_anonymous:
            if Order.objects.all().filter(user=request.user, is_finished=False):
                order = Order.objects.get(user=request.user, is_finished=False)
                orderdetails = OrderDetails.objects.all().filter(order=order)
                total = 0
                td = 0
                css = 0
                for  sub in orderdetails:
                    total += sub.price * sub.quantity
                    td  += sub.product.qus * sub.quantity
                css = total + td
                sd = None
                if request.user.groups.filter(name='castomar'):
                    sd = True
                else:
                    sd = False
                context ={
                    'css':css,
                    'td':td,
                    'sd':sd,
                    'order':order,
                    'orderdetails':orderdetails,
                    'mo':Mo.objects.all(),
                    'mr': Mr.objects.all(),
                    'total':total,
                    'category':Category.objects.all(),
                }
    return render(request,'orders/payment.html',context)



@transaction.atomic
def ajexpay(request):
        mo = request.GET.get('mo')
        print(mo)
    
 
        sizedata = Mo.objects.filter(mo=mo)
        sizedatar = Mr.objects.filter(mo__mo=mo)
        print(sizedatar)

        if (mo):
            sizedata = Mo.objects.filter(mo=mo)
       
            result = {
                    
                    "data": serializers.serialize("json", sizedata),
                    "l": serializers.serialize("json", sizedatar)

                   
                }
        else:
            result = {
                    
                    "data": ''
                   
                }

        return JsonResponse(result)



@transaction.atomic
def ajexpayment(request):
        if  request.user.is_authenticated and not request.user.is_anonymous:
            f = Order.objects.filter(user=request.user, is_finished=False,).last()
            if f.order_delete + timezone.timedelta(minutes=120) < timezone.now()  :
                order = Order.objects.get(user=request.user, is_finished=False)
                orderdetails = OrderDetails.objects.all().filter(order=order)
                for i in orderdetails:
                     ddf = Fintion.objects.filter(order_detils = i.pk,fintion=i.product.pk, order_idsid=order)
                     if ddf:
                              Fintion.objects.filter(order_detils = i.pk,fintion=i.product.pk, order_idsid=order).delete()
                orderdetails.delete()
                order.delete()
                
                
                result = {
                    "data": serializers.serialize("json", orderdetails),
                }
                return JsonResponse(result)
            else:
                result = {
                    "data": serializers.serialize("json", ''),
                }
                return JsonResponse(result)

        



@ratelimit(key='user_or_ip', rate='50/m')
@login_required(login_url='signin')
@transaction.atomic
def show_orders(request):
    context = None
    all_orders = None
    orderdetails = None
    if  request.user.is_authenticated and not request.user.is_anonymous:
        all_orders = Order.objects.all().filter(user=request.user)
        if all_orders:
            for x in all_orders:
               order = Order.objects.get(id=x.id)
               orderdetails = OrderDetails.objects.all().filter(order=order)
               total = 0
               for  sub in orderdetails:
                  total += sub.price * sub.quantity
               x.totle = total
               x.items_count= orderdetails.count
              
  
    context = {
        'all_orders':all_orders,
        'category':Category.objects.all(),
        }

    return render(request, 'orders/show_orders.html',context )



import json
@ratelimit(key='user_or_ip', rate='50/m')
@login_required(login_url='signin')
@transaction.atomic
def order_complted(request):
     body = json.loads(request.body)
     product = Product.objects.get(id=body['prodect_id'])
     Order.objects.create(
         details = product,
         is_finished = True,
         user = request.user,
  
     )
     order = Order.objects.get(user=request.user, is_finished=False) 
     order.is_finished = True
     order.save()
    
     
     return JsonResponse('payment comlted')
@ratelimit(key='user_or_ip', rate='50/m')
@login_required(login_url='signin')
@aminnUsers(adminGroups=['groadmin'])
@transaction.atomic
def mo(request):
    no = Mo.objects.all()
    if request.method == 'POST' : 
       mo = request.POST ['mo']
       na = request.POST ['na']
     
       
       t =  Mo()
       t.mo = mo
       t.mo = na
       t.save()
       
       return render(request, 'orders/mo.html')
    else:
    
        result = {
                    
                    "na": Mo.objects.all()
                   
                }
        return render(request, 'orders/mo.html',result,{'no':no})

@aminnUsers(adminGroups=['groadmin'])
@login_required(login_url='signin')
@ratelimit(key='user_or_ip', rate='50/m')
@transaction.atomic
def mor(request):
    no = Mo.objects.all()
    if request.method == 'POST' : 
        if Mo.objects.filter(mo=request.POST.get('mo')).exists():
            messages.error(request, _(' هذة المحافظة موجود مسبقا'))
            return redirect('mor')
        else:
            mo = request.POST ['mo']
            na = request.POST ['na']
            t =  Mo()
            t.mo = mo
            t.na = na
            t.save()
            return redirect( 'mo')

                   
       
    return render(request, 'orders/mo.html',)

@aminnUsers(adminGroups=['groadmin'])
@login_required(login_url='signin')
@ratelimit(key='user_or_ip', rate='50/m')
@transaction.atomic
def mo(request):
    no = Mo.objects.all()

    return render(request, 'orders/mor.html',{'no':no})


@aminnUsers(adminGroups=['groadmin'])
@login_required(login_url='signin')
@ratelimit(key='user_or_ip', rate='50/m')
@transaction.atomic
def updatemo(request,id):
    book_id = Mo.objects.get(id=id)


    if request.method == 'POST':
        book_save = Moform(request.POST, request.FILES ,instance=book_id)
        if book_save.is_valid():
            book_save.save()
            return redirect('mo')

    else:
            book_save =Moform(instance=book_id)
    context ={
            'form':book_save,
            'category':Category.objects.all(),
        }

    return render(request, 'pages/update.html',context)



@aminnUsers(adminGroups=['groadmin'])

@login_required(login_url='signin')
@ratelimit(key='user_or_ip', rate='50/m')
@transaction.atomic
def modelete(request,id):
     pro_delete =get_object_or_404(Mo, id=id)
     if request.method == 'POST':
          pro_delete.delete()
          return redirect('mo')

     else:
         return render(request,'pages/delete.html')
     

@ratelimit(key='user_or_ip', rate='50/m')
@login_required(login_url='signin')
@aminnUsers(adminGroups=['groadmin'])
@transaction.atomic
def readMr(request,id):

    mo = get_object_or_404(Mo,pk=id)
    return render(request, 'orders/readMR.html',{'mo':mo})






@ratelimit(key='user_or_ip', rate='50/m')
@login_required(login_url='signin')
@aminnUsers(adminGroups=['groadmin'])
@transaction.atomic
def add_to_Mr(request,id):
    mo = get_object_or_404(Mo,pk=id)
    mor = get_object_or_404(Mo,id=id)
    print(mor)
    if request.method == "POST":
        if 'mr' in request.POST :
            mr = request.POST.get('mr')
        else:
            messages.error(request, _('    مربع المركز فارغ '))
            return redirect('add_to_Mr',id=id)
        if Mr.objects.filter(mr=request.POST.get('mr')).exists():
            messages.error(request, _(' هذا المركز موجود مسبقا'))
            return redirect('add_to_Mr',id=id)
        elif mr:
            mm = Mr()
            mm.mo = mor
            mm.mr=mr
            mm.save()
       
            messages.success(request, _('تمت العملية بنجاح'))
            return redirect('readMr',id=id)
        else:
            messages.warning(request, _('    مربع المركز فارغ '))
            return redirect('add_to_Mr',id=id)
     
          
    return render(request, 'orders/MR.html',{'mo':mo,'category':Category.objects.all(),})

@aminnUsers(adminGroups=['groadmin'])
@login_required(login_url='signin')
@ratelimit(key='user_or_ip', rate='50/m')
@transaction.atomic
def MRelete(request,id,mr_id):
     
     pro_delete =get_object_or_404(Mr,mo__id = id , id=mr_id)
     if request.method == 'POST':
          pro_delete.delete()
       
          return redirect('readMr',id=id)

     else:
         return render(request,'pages/delete.html')



@ratelimit(key='user_or_ip', rate='50/m')
@login_required(login_url='signin')
@aminnUsers(adminGroups=['groadmin'])
@transaction.atomic
def update_mr(request ,id,mr_id):
     pro_update = get_object_or_404(Mr,mo__id = id , id=mr_id)
     if request.method =='POST':
     
        pro_update = get_object_or_404(Mr,mo__id = id , id=mr_id)

        book_save = Mrform(request.POST, request.FILES, instance=pro_update)
        if book_save.is_valid():
               book_save.save()
               messages.success(request, _('تم التعديل بنجاح'))
               return redirect('readMr',id=id)
        else:
              messages.warning(request, _('  الكمية غير   كافية'))

              return redirect('update_color',id=id,update_mr=update_mr )
     else:
         book_save = Mrform(instance=pro_update)
         if request.user.groups.filter(name='adminCastomar'):
             tr = True
             t = True
         else:
             tr = False
             t = False
     
         if request.user.groups.filter(name='hr'):
             hrr = True
        
         else:
             hrr = False
         context ={
              'form':book_save,
               'hrr':hrr,
       'tr':tr,
       't':t,
       'category':Category.objects.all(),

         }
     return render(request,'pages/update.html',context)





# خاص بلاردرات

@ratelimit(key='user_or_ip', rate='50/m')
@login_required(login_url='signin')
@transaction.atomic
def show_orders_detels(request,id):
    group = Group.objects.get(name='castomar')
    usery = User.objects.filter(groups__name=group)
    # print(usery)
    if request.user in usery:
        t = True
       
    else :
        t = False
    context = None
    if  request.user.is_authenticated and not request.user.is_anonymous:
        order = Order.objects.filter(user=request.user, id=id ,is_finished= True)
        if not order:
             messages.warning(request, _("أكد الطلب اولا ثم عدل فيه"))

             return redirect('show_orders')
        else:
            if Order.objects.all().filter(user=request.user,id=id):
                order = Order.objects.get(user=request.user, id=id)
                tty = None
                if Payment.objects.filter(order=order):
                   tty = Payment.objects.get(order=order)
              
                orderdetails = OrderDetails.objects.all().filter(order=order)
                total = 0
                for  sub in orderdetails:
                     total += sub.price * sub.quantity
    
    
                context ={
                    'order':order,
                    'orderdetails':orderdetails,
                    'total':total,
                    't':t,
                    'Ordersd':Order.objects.all().filter(user=request.user,id=id),
                    'Payment':tty,
                    'category':Category.objects.all(),
    
                    }
    

    return render(request, 'orders/detelscardorder.html',context )

from product.models import *
@ratelimit(key='user_or_ip', rate='50/m')
@login_required(login_url='signin')
@transaction.atomic
def remove_from_card_detels(request, id, orderdetails_id):
    
    orderdetails = OrderDetails.objects.get(id=orderdetails_id)
    if request.user.is_authenticated and  orderdetails.order.user.id==request.user.id and not request.user.is_anonymous and id and orderdetails_id:
        redersd = Order.objects.filter(id=id,user=request.user,status=Order.Typechoices.b)
        if redersd:
            messages.warning(request, _("الطلب   تم تأكيده ولا يمكن التعديل عليه"))

            return redirect('show_orders_detels',id=id )
    

        elif Order.objects.filter(id=id,user=request.user,status=Order.Typechoices.c):
            messages.warning(request, _("الطلب  قيد الوصول ولا يمكن التعديل عليه"))

            return redirect('show_orders_detels',id=id )
        elif Order.objects.filter(id=id,user=request.user,status=Order.Typechoices.d):
            messages.warning(request, _("     الطلب ملغي ولا يمكن التعديل عليه"))

            return redirect('show_orders_detels',id=id )
        elif Order.objects.filter(id=id,user=request.user,status=Order.Typechoices.f):
            messages.warning(request, _("لم يتم الرد على الطلب  ولا يمكن التعديل عليه"))

            return redirect('show_orders_detels',id=id )
        elif Order.objects.filter(id=id,user=request.user,status=Order.Typechoices.g):
            messages.warning(request, _("   الطلب  اتشحن ولا يمكن التعديل عليه"))

            return redirect('show_orders_detels',id=id )
        elif Order.objects.filter(id=id,user=request.user,status=Order.Typechoices.h):
            messages.warning(request, _("الطلب   مرتج ولا يمكن التعديل عليه"))

            return redirect('show_orders_detels',id=id )
        elif Order.objects.filter(id=id,user=request.user,status=Order.Typechoices.m):
            messages.warning(request,_( "الطلب فى  التوصيل ولا يمكن التعديل عليه"))

            return redirect('show_orders_detels',id=id )
        
        elif Order.objects.filter(id=id,user=request.user,status=Order.Typechoices.sold):
            messages.warning(request,_( "تم حذف الطلب  ولا يمكن التعديل عليه"))

            return redirect('show_orders_detels',id=id )
        else:
            orderdetails = OrderDetails.objects.get(id=orderdetails_id)
            
            pro = Product.objects.get(pk=orderdetails.product.pk)
            prosa = Product.objects.filter(id=orderdetails.product.pk,facat =False,boonimg=True)

            proo = Product.objects.filter(id=orderdetails.product.pk,facat =True,boonimg=False)
            if proo:
        
                remove = orderdetails.quantity 
                testing = orderdetails.testing
                pro = Product.objects.get(pk=orderdetails.product.pk)
                
                pro.qu += remove
                pro.qu -= testing
                pro.save()
              
                orderdetails = OrderDetails.objects.get(id=orderdetails_id)
                colorr = Color.objects.get(productcolor_id=pro,name=orderdetails.colar)
                colorr.qucolor += remove
                colorr.save()
                orderdetails = OrderDetails.objects.get(id=orderdetails_id,order__user=request.user)
                
                proi = Product.objects.get(id=orderdetails.product.id)
               
                sizes = Sise.objects.get(productsise__name=colorr,sisel=orderdetails.size)
                sizes.qusise += remove
                sizes.save()
                if orderdetails.order.user.id == request.user.id:
                   ddf = Fintion.objects.filter(order_idsid=orderdetails.order.pk,order_detils = orderdetails.pk,fintion=orderdetails.product.pk)
                   if ddf:
                      Fintion.objects.filter(order_idsid=orderdetails.order.pk,order_detils = orderdetails.pk,fintion=orderdetails.product.pk).delete()
                   orderdetails.delete()
                
            elif prosa:
                remove = orderdetails.quantity 
                testing = orderdetails.testing
                pro = Product.objects.get(pk=orderdetails.product.pk)
                
                pro.qu += remove
                pro.qu -= testing
                pro.save()
              
                orderdetails = OrderDetails.objects.get(id=orderdetails_id)
                img = Img.objects.get(i_id=pro,name=orderdetails.nameimg)
                img.quimg += remove
                img.save()
                orderdetails = OrderDetails.objects.get(id=orderdetails_id,order__user=request.user)
                
                proi = Product.objects.get(id=orderdetails.product.id)
           
                if orderdetails.order.user.id == request.user.id:
                #    orderdetails.delete()
                   ddf = Fintion.objects.filter(order_idsid=orderdetails.order.pk,order_detils = orderdetails.pk,fintion=orderdetails.product.pk)
                   if ddf:
                      Fintion.objects.filter(order_idsid=orderdetails.order.pk,order_detils = orderdetails.pk,fintion=orderdetails.product.pk).delete()
                   orderdetails.delete()
            else:
                remove = orderdetails.quantity 
                testing = orderdetails.testing
                pro = Product.objects.get(pk=orderdetails.product.pk)
                
                pro.qu += remove
                pro.qu -= testing
                pro.save()
                if orderdetails.order.user.id==request.user.id:
                   ddf = Fintion.objects.filter(order_idsid=orderdetails.order.pk,order_detils = orderdetails.pk,fintion=orderdetails.product.pk)
                   if ddf:
                      Fintion.objects.filter(order_idsid=orderdetails.order.pk,order_detils = orderdetails.pk,fintion=orderdetails.product.pk).delete()
                   orderdetails.delete()
                
    return redirect('show_orders_detels',id=id )



@ratelimit(key='user_or_ip', rate='50/m')
@login_required(login_url='signin')
@transaction.atomic
def add_qty_detels(request,id , orderdetails_id):
    # redersf = None
    if request.user.is_authenticated and not request.user.is_anonymous and id and  orderdetails_id:
       
        redersd = Order.objects.filter(id=id,user=request.user,status=Order.Typechoices.b)
        if redersd:
            messages.warning(request, _("تم التاكيد الطلب ولا يمكن التعديل عليه"))

            return redirect('show_orders_detels',id=id )
        elif Order.objects.filter(id=id,user=request.user,status=Order.Typechoices.c):
            messages.warning(request, _("الطلب  قيد الوصول ولا يمكن التعديل عليه"))

            return redirect('show_orders_detels',id=id )
        elif Order.objects.filter(id=id,user=request.user,status=Order.Typechoices.d):
            messages.warning(request,_( "     الطلب ملغى ولا يمكن التعديل عليه"))

            return redirect('show_orders_detels',id=id )
        elif Order.objects.filter(id=id,user=request.user,status=Order.Typechoices.f):
            messages.warning(request, _("لم يتم الرد على الطلب  ولا يمكن التعديل عليه"))

            return redirect('show_orders_detels',id=id )
        elif Order.objects.filter(id=id,user=request.user,status=Order.Typechoices.g):
            messages.warning(request, _("   تم شحن الطلب  ولا يمكن التعديل عليه"))

            return redirect('show_orders_detels',id=id )
        elif Order.objects.filter(id=id,user=request.user,status=Order.Typechoices.h):
            messages.warning(request, _("الطلب   مرتج ولا يمكن التعديل عليه"))

            return redirect('show_orders_detels',id=id )
        elif Order.objects.filter(id=id,user=request.user,status=Order.Typechoices.m):
            messages.warning(request, _("الطلب   قيد الوصول ولا يمكن التعديل عليه"))

            return redirect('show_orders_detels',id=id )
        
        elif Order.objects.filter(id=id,user=request.user,status=Order.Typechoices.sold):
            messages.warning(request, _("تم حذف الطلب  ولا يمكن التعديل عليه"))

            return redirect('show_orders_detels',id=id )
        else:

            orderdetails = OrderDetails.objects.get(id=orderdetails_id)
      
            pro = Product.objects.get(pk=orderdetails.product.pk)
          
            proo = Product.objects.filter(id=orderdetails.product.pk,facat =True,boonimg=False)
            prosa = Product.objects.filter(id=orderdetails.product.pk,facat =False,boonimg=True)


            if proo:
             orderdetails = OrderDetails.objects.get(id=orderdetails_id,order__user=request.user)
            
             proi = Product.objects.get(id=orderdetails.product.id)
             colorr = Color.objects.get(productcolor_id=pro,name=orderdetails.colar)
             sizes = Sise.objects.get(productsise__name=colorr,sisel=orderdetails.size)
            
             if not sizes.qusise > 0:
                 messages.error(request, _('   كمية هذا المقاس غير  كافية '))
                 return redirect('show_orders_detels',id=id )
           
             else:
                 sizes.qusise -= 1
                 sizes.save()
                  
                  
                 orderdetails = OrderDetails.objects.get(id=orderdetails_id)
                 pro = Product.objects.get(id=orderdetails.product.pk)
             
                 
            
                 colorr = Color.objects.get(productcolor_id=pro,name=orderdetails.colar)
                 
                 if  colorr.qucolor > 0:
                      colorr.qucolor -= 1
                      colorr.save()
                      orderdetails = OrderDetails.objects.get(id=orderdetails_id)
          
                      pro = Product.objects.get(pk=orderdetails.product.pk)
                      
                      pro.qu -= 1
       
                      pro.save()
                      orderdetails.quantity += 1
                  
                      orderdetails.save()
                      orderdetails = OrderDetails.objects.get(pk=orderdetails_id)
                      ddf = Fintion.objects.filter(order_detils = orderdetails.pk,fintion=orderdetails.product.pk,order_idsid=orderdetails.order.pk)
                      if ddf:
                         ddddf =  Fintion.objects.filter(order_detils = orderdetails.pk,fintion=orderdetails.product.pk,order_idsid=orderdetails.order.pk).update(usus = orderdetails.quantity)
                  
                      messages.success(request, _(' تم زيادة الكمية بامقدار واحد'))
                      return redirect('show_orders_detels',id=id )
                 else:
                    messages.error(request, _('   كمية هذا اللون غير   كافية '))
                    return redirect('show_orders_detels',id=id )
            
            elif prosa:
              
             orderdetails = OrderDetails.objects.get(id=orderdetails_id,order__user=request.user)
            
             proi = Product.objects.get(id=orderdetails.product.id)
             img = Img.objects.get(i_id=pro,name=orderdetails.nameimg)
            
             if not img.quimg > 0:
                 messages.error(request, _(' كمية   هذا المنتج غير   كافية '))
                 return redirect('show_orders_detels',id=id )
           
             else:
                 img.quimg -= 1
                 img.save()
                  
                  
                 orderdetails = OrderDetails.objects.get(id=orderdetails_id)
                 pro = Product.objects.get(id=orderdetails.product.pk)
                 
            
                 img = Img.objects.get(i_id=pro,name=orderdetails.nameimg)

                 
                 orderdetails = OrderDetails.objects.get(id=orderdetails_id)
          
                 pro = Product.objects.get(pk=orderdetails.product.pk)
                      
                 pro.qu -= 1
                 pro.save()
       
                 orderdetails.quantity += 1
                  
                 orderdetails.save()
                 ddf = Fintion.objects.filter(order_detils = orderdetails.pk,fintion=orderdetails.product.pk,order_idsid=orderdetails.order.pk)
                 if ddf:
                         ddddf =  Fintion.objects.filter(order_detils = orderdetails.pk,fintion=orderdetails.product.pk,order_idsid=orderdetails.order.pk).update(usus = orderdetails.quantity)
                  
                 messages.success(request, _(' تم زيادة الكمية بامقدار واحد'))
                 return redirect('show_orders_detels',id=id )
               
        

            
            else:
             
                 orderdetails = OrderDetails.objects.get(id=orderdetails_id)
          
                 pro = Product.objects.get(pk=orderdetails.product.pk)
                 if pro.qu > 0:
                    pro.qu -= 1
                    pro.save()
                    orderdetails.quantity += 1
                    orderdetails.save()
                    ddf = Fintion.objects.filter(order_detils = orderdetails.pk,fintion=orderdetails.product.pk,order_idsid=orderdetails.order.pk)
                    if ddf:
                       ddddf =  Fintion.objects.filter(order_detils = orderdetails.pk,fintion=orderdetails.product.pk,order_idsid=orderdetails.order.pk).update(usus = orderdetails.quantity)
                    messages.success(request,_(f'تم زيادة هذا المنتج {pro.name}    بقيمة واحد' ))
                    return redirect('show_orders_detels',id=id )
                 else:
                    messages.error(request,_( f'كمية هذا المنتج {pro.name} غير كافيه'))
                    return redirect('show_orders_detels',id=id )

    return redirect('show_orders_detels',id=id )


@ratelimit(key='user_or_ip', rate='50/m')
@login_required(login_url='signin')
@transaction.atomic
def detils_updect_color(request,id , orderdetails_id):
    # redersf = None
    if request.user.is_authenticated and not request.user.is_anonymous and id and  orderdetails_id:
  
        order = Order.objects.get(user=request.user,id=id,is_finished=True)
        orderdetails = OrderDetails.objects.get(order=order,id=orderdetails_id)
        pro = Product.objects.get(id=orderdetails.product.pk)
        color = Color.objects.filter(productcolor_id=pro)
        if Order.objects.filter(id=id,user=request.user,status=Order.Typechoices.c):
            messages.warning(request, _("الطلب قيد الوصول ولا يمكن التعديل عليه"))

            return redirect('show_orders_detels',id=id )
        elif Order.objects.filter(id=id,user=request.user,status=Order.Typechoices.d):
            messages.warning(request, _("     تم الغاء الطلب  ولا يمكن التعديل عليه"))

            return redirect('show_orders_detels',id=id )
        elif Order.objects.filter(id=id,user=request.user,status=Order.Typechoices.f):
            messages.warning(request, _(" لم يتم الرد على الطلب  ولا يمكن التعديل عليه"))


            return redirect('show_orders_detels',id=id )
        elif Order.objects.filter(id=id,user=request.user,status=Order.Typechoices.g):
            messages.warning(request, _("     تم شحن الطلب ولا يمكن التعديل عليه"))

            return redirect('show_orders_detels',id=id )
        elif Order.objects.filter(id=id,user=request.user,status=Order.Typechoices.h):
            messages.warning(request, _("الطلب   مرتج ولا يمكن التعديل عليه"))

            return redirect('show_orders_detels',id=id )
        elif Order.objects.filter(id=id,user=request.user,status=Order.Typechoices.m):
            messages.warning(request, _("الطلب قيد  التوصيل ولا يمكن التعديل عليه"))

            return redirect('show_orders_detels',id=id )
        
        elif Order.objects.filter(id=id,user=request.user,status=Order.Typechoices.sold):
            messages.warning(request, _("   تم حذف الطلب ولا يمكن التعديل عليه"))

            return redirect('show_orders_detels',id=id )
        
        elif request.method == 'POST':
            col =None
            sisel = None
            if not 'color' in request.POST:
                messages.warning(request, _("  مربع الون فارغ"))
                return redirect('show_orders_detels',id=id )
                
            else:
                col = request.POST['color']

                
                if not 'sisel' in request.POST:
                    messages.warning(request, _("   مربع الون فارغ"))
                    return redirect('show_orders_detels',id=id )
                    

                else:
                    sisel = request.POST['sisel']

              

                    colorsa = Color.objects.get(productcolor_id=pro,name=col)
                    size = Sise.objects.get(productsise__name=colorsa,productsise__productcolor_id=pro,sisel=sisel)
                    
                    if size.qusise >= orderdetails.quantity:
           
                        order = Order.objects.get(user=request.user,id=id,is_finished=True)
                        print(order)
                        orderdetails = OrderDetails.objects.get(order=order,id=orderdetails_id)
        
                        print(orderdetails.quantity)
                        pro = Product.objects.get(id=orderdetails.product.pk)
                        colorr = Color.objects.get(productcolor_id=pro,name=orderdetails.colar)
                        sizee = Sise.objects.get(productsise__productcolor_id=pro,productsise__name=colorr,sisel=orderdetails.size)
                        sizee.qusise += int(orderdetails.quantity)
                        sizee.save()
                        colorr.qucolor += int(orderdetails.quantity)
                        colorr.save()
                        
        
                        color = Color.objects.filter(productcolor_id=pro)
                        col = request.POST['color']
                        orderdetails.colar = col
                        orderdetails.save()
                        # sizees = Sise.objects.filter(productsise__name=color)
                        orderdetails.size = sisel
                        orderdetails.save()
                        sisel = request.POST['sisel']
                        colorsa = Color.objects.get(productcolor_id=pro,name=col)
                       
        
                        sizees = Sise.objects.get(productsise__productcolor_id=pro,productsise__name=colorsa,sisel=sisel)
                      
                        colorsa.qucolor -= int(orderdetails.quantity)
                        colorsa.save()
        
                        sizees.qusise -= int(orderdetails.quantity)
                        sizees.save()
                        messages.success(request, _('عملية ناجحه'))
        
                        return redirect('show_orders_detels',id=id )
                    else:
                       messages.error(request, _('   كمية هذا المقاس غير   كافية '))
                       return redirect('show_orders_detels',id=id )

        

    return render(request, 'orders/updeacolora.html',{'color':color,'id':id,"orderdetails_id":orderdetails_id})
@transaction.atomic
def ajex__color_detelis(request,id , orderdetails_id):
        order = Order.objects.get(user=request.user,id=id,is_finished=True)
        orderdetails = OrderDetails.objects.get(order=order,id=orderdetails_id)
        pro = Product.objects.get(id=orderdetails.product.pk)
        
        col = request.GET['color']
      
        
        color = Color.objects.get(productcolor_id=pro,name=col)
  
        if (col):
            sizedata = Sise.objects.filter(productsise__productcolor__id=pro.pk,productsise__name=color)
            print(sizedata)
            result = {
                    
                    "data": serializers.serialize("json", sizedata
                                                  ) }
        else:
            result = {
                    
                    "data": ''
                   
                }

        return JsonResponse(result)

@ratelimit(key='user_or_ip', rate='50/m')
@login_required(login_url='signin')
@transaction.atomic
def sub_qty_detels(request,id, orderdetails_id):
    if request.user.is_authenticated and not request.user.is_anonymous and id and orderdetails_id:
        redersd = Order.objects.filter(id=id,user=request.user,status=Order.Typechoices.b)
        if redersd:
            messages.warning(request,_( "   تم تاكيد الطلب ولا يمكن التعديل عليه"))

            return redirect('show_orders_detels',id=id )
        elif Order.objects.filter(id=id,user=request.user,status=Order.Typechoices.c):
            messages.warning(request,_( "الطلب  قيد الوصول ولا يمكن التعديل عليه"))

            return redirect('show_orders_detels',id=id )
        elif Order.objects.filter(id=id,user=request.user,status=Order.Typechoices.d):
            messages.warning(request, _("      تم الغاء الطلب ولا يمكن التعديل عليه"))

            return redirect('show_orders_detels',id=id )
        elif Order.objects.filter(id=id,user=request.user,status=Order.Typechoices.f):
            messages.warning(request, _(" لم يتم الرد على الطلب  ولا يمكن التعديل عليه"))

            return redirect('show_orders_detels',id=id )
        elif Order.objects.filter(id=id,user=request.user,status=Order.Typechoices.g):
            messages.warning(request,_( "   تم شحن الطلب ولا يمكن التعديل عليه"))

            return redirect('show_orders_detels',id=id )
        elif Order.objects.filter(id=id,user=request.user,status=Order.Typechoices.h):
            messages.warning(request,_( "الطلب مرتج ولا يمكن التعديل عليه"))

            return redirect('show_orders_detels',id=id )
        elif Order.objects.filter(id=id,user=request.user,status=Order.Typechoices.m):
            messages.warning(request, _("الطلب فى  التوصيل ولا يمكن التعديل عليه"))

            return redirect('show_orders_detels',id=id )
        
        elif Order.objects.filter(id=id,user=request.user,status=Order.Typechoices.sold):
            messages.warning(request, _("الطلب   اتحذف ولا يمكن التعديل عليه"))

            return redirect('show_orders_detels',id=id )
        else:
            orderdetails = OrderDetails.objects.get(id=orderdetails_id)
            pro = Product.objects.get(pk=orderdetails.product.pk)
            
            proo = Product.objects.filter(id=orderdetails.product.pk,facat =True,boonimg=False)
            prosa = Product.objects.filter(id=orderdetails.product.pk,facat =False,boonimg=True)

            if proo:
             orderdetails = OrderDetails.objects.get(id=orderdetails_id,order__user=request.user)
            
             proi = Product.objects.get(id=orderdetails.product.id)
             colorr = Color.objects.get(productcolor_id=pro,name=orderdetails.colar)
             sizes = Sise.objects.get(productsise__name=colorr,sisel=orderdetails.size)
          
             sfx = OrderDetails.objects.all().get(id=orderdetails_id)
             if not sfx.quantity != 1 :
                
                 messages.error(request, _('لا يمكن ان تقل   الكمية عن واحد '))
                 return redirect('show_orders_detels',id=id )
            
             else:
                 sizes.qusise += 1
                 sizes.save()
                  
                  
                 orderdetails = OrderDetails.objects.get(id=orderdetails_id)
                 pro = Product.objects.get(id=orderdetails.product.pk)
            
                 colorr = Color.objects.get(productcolor_id=pro,name=orderdetails.colar)
                 
                 if  colorr:
                      colorr.qucolor += 1
                      colorr.save()
                 else:
                    messages.error(request, _('لا يمكن ان تقل الكمية عن واحد '))
                    return redirect('show_orders_detels',id=id )
                 if  orderdetails.quantity != 1:
                    pro = Product.objects.get(pk=orderdetails.product.pk)
                    pro.qu += 1
                    pro.save()
                    orderdetails.quantity -= 1
                    orderdetails.save()
                    ddf = Fintion.objects.filter(order_detils = orderdetails.pk,fintion=orderdetails.product.pk,order_idsid=orderdetails.order.pk)
                    
                    if ddf:
                       
                       ddddf =  Fintion.objects.filter(order_detils = orderdetails.pk,fintion=orderdetails.product.pk,order_idsid=orderdetails.order.pk).update(usus = orderdetails.quantity)
                       
                    messages.success(request, _(' تم تقليل   الكمية بامقدار واحد'))
                    return redirect('show_orders_detels',id=id )
           
           
            
            elif prosa:
             orderdetails = OrderDetails.objects.get(id=orderdetails_id,order__user=request.user)
            
             proi = Product.objects.get(id=orderdetails.product.id)
             img = Img.objects.get(i_id=pro,name=orderdetails.nameimg)
           
             sfx = OrderDetails.objects.all().get(id=orderdetails_id)
             if not sfx.quantity != 1 :
                
                 messages.error(request, _('لا يمكن ان تقل   الكمية عن واحد '))
                 return redirect('show_orders_detels',id=id )
            
             else:
                 img.quimg += 1
                 img.save()
                  
                  
                 orderdetails = OrderDetails.objects.get(id=orderdetails_id)
                 pro = Product.objects.get(id=orderdetails.product.pk)
            
                 if  orderdetails.quantity != 1:
                    pro = Product.objects.get(pk=orderdetails.product.pk)
                    pro.qu += 1
                
        
                    pro.save()
                    orderdetails.quantity -= 1
          
                    orderdetails.save()
                    ddf = Fintion.objects.filter(order_detils = orderdetails.pk,fintion=orderdetails.product.pk,order_idsid=orderdetails.order.pk)
                    if ddf:
                       ddddf =  Fintion.objects.filter(order_detils = orderdetails.pk,fintion=orderdetails.product.pk,order_idsid=orderdetails.order.pk).update(usus = orderdetails.quantity)
                    messages.success(request, _(' تم تقليل   الكمية بامقدار واحد'))
                    return redirect('show_orders_detels',id=id )
           
            else:
                if orderdetails.quantity != 1:
                    pro = Product.objects.get(pk=orderdetails.product.pk)
                    pro.qu += 1
              
                    pro.save()
                    orderdetails.quantity -= 1
          
                    orderdetails.save()
                    ddf = Fintion.objects.filter(order_detils = orderdetails.pk,fintion=orderdetails.product.pk,order_idsid=orderdetails.order.pk)
                    if ddf:
                       ddddf =  Fintion.objects.filter(order_detils = orderdetails.pk,fintion=orderdetails.product.pk,order_idsid=orderdetails.order.pk).update(usus = orderdetails.quantity)
                    messages.success(request, _(' تم تقليل   الكمية بامقدار واحد'))
                    return redirect('show_orders_detels',id=id )

                else:
                    messages.error(request, _('لا يمكن   الكمية عن تقل عن واحد'))
                    return redirect('show_orders_detels',id=id )


                
    return redirect('show_orders_detels',id=id )



@login_required(login_url='signin')
@ratelimit(key='user_or_ip', rate='50/m')
@transaction.atomic
def updatePayment(request, id ,id__Paymen):
    
    redersd = Order.objects.filter(id=id,user=request.user,status=Order.Typechoices.b)
    if redersd:
            messages.warning(request, _("   تم توصيل الطلب ولا يمكن التعديل عليه"))

            return redirect('show_orders_detels',id=id )
    elif Order.objects.filter(id=id,user=request.user,status=Order.Typechoices.c):
            messages.warning(request, _("الطلب  قيد الوصول ولا يمكن التعديل عليه"))

            return redirect('show_orders_detels',id=id )
    elif Order.objects.filter(id=id,user=request.user,status=Order.Typechoices.d):
        messages.warning(request, _("      تم الغاء الطلب ولا يمكن التعديل عليه"))

        return redirect('show_orders_detels',id=id )
    elif Order.objects.filter(id=id,user=request.user,status=Order.Typechoices.f):
        messages.warning(request, _("لم يتم الرد على الطلب ولا يمكن التعديل عليه"))

        return redirect('show_orders_detels',id=id )
    elif Order.objects.filter(id=id,user=request.user,status=Order.Typechoices.g):
        messages.warning(request, _("تم شحن الطلب ولا يمكن التعديل عليه"))

        return redirect('show_orders_detels',id=id )
    elif Order.objects.filter(id=id,user=request.user,status=Order.Typechoices.h):
        messages.warning(request, _("الطلب   مرتج ولا يمكن التعديل عليه"))

        return redirect('show_orders_detels',id=id )
    elif Order.objects.filter(id=id,user=request.user,status=Order.Typechoices.m):
        messages.warning(request, _("جارى توصيل الطلب ولا يمكن التعديل عليه"))

        return redirect('show_orders_detels',id=id )
    
    elif Order.objects.filter(id=id,user=request.user,status=Order.Typechoices.sold):
        messages.warning(request, _("تم حذف الطلب ولا يمكن التعديل عليه"))

        return redirect('show_orders_detels',id=id )
    else:


        if request.method == 'POST':
            if  len(request.POST['ship_phone'] ) !=  int(11) :
                             messages.error(request, _('يجب ان يكون رقم الهاتف  مكون من 11 رقم'))
                             return redirect('updatePayment',id=id)
            else:
             shipment_address = request.POST['ship_address']
             shipment_phone = request.POST['ship_phone']
             name = request.POST['name']
             mo = request.POST['mo']
             na = request.POST['na']
             mr = request.POST['mr']

             book_id = Payment.objects.get(order__id=id,id=id__Paymen)
             book_id.shipment_address = shipment_address
             book_id.shipment_phone = shipment_phone
             book_id.name = name
             book_id.mo = mo
             book_id.na = request.POST['na']
             book_id.mr = mr
             book_id.save()
             return redirect('show_orders_detels',id=id )

        book_id = Payment.objects.get(order__id=id,id=id__Paymen)
        context ={
               
                'mo':Mo.objects.all(),
                'mr': Mr.objects.all(),
                'category':Category.objects.all(),
                'v':book_id.shipment_address ,
                'name':book_id.name,
                'phone':book_id.shipment_phone ,
                # 'mo':book_id.mo,
                # 'mr':book_id.mr 


            }
        return render(request, 'orders/updeateorde.html',context)


@transaction.atomic
def es(request):
    total_oos = 0
    total_ssa = 0
    ordes_castomar = Order.objects.filter(user=request.user)
    for i in ordes_castomar:
        orderDetails__castomar = OrderDetails.objects.filter(order__pk=i.pk)
        for j in orderDetails__castomar:
            
            total_oos += int(j.product.qus) * int(j.quantity)
            total_ssa += int(j.product.qus ) * int(j.ba)

    
    if request.user.groups.filter(name='Castomar'):
        tbbn = True
    else:
        tbbn = False

    y = Order.objects.filter(user=request.user ,).exclude(coin=None)
    s = 0
    for i in y:
        s += int(i.coin)
    total_nsd = total_ssa - s
    context = {
     "a":Order.objects.filter(user=request.user,status=Order.Typechoices.a).count() , 
     "b":Order.objects.filter(user=request.user,status=Order.Typechoices.b).count() ,    
     "c":Order.objects.filter(user=request.user,status=Order.Typechoices.c).count() ,    
     "d":Order.objects.filter(user=request.user,status=Order.Typechoices.d).count() ,    
     "f":Order.objects.filter(user=request.user,status=Order.Typechoices.f).count() ,    
     "g":Order.objects.filter(user=request.user,status=Order.Typechoices.g).count() , 
     "h":Order.objects.filter(user=request.user,status=Order.Typechoices.h).count() ,    
     "m":Order.objects.filter(user=request.user,status=Order.Typechoices.m).count() ,  
     "y" :s,
     'tbbn':tbbn,
     'total_nsd':total_nsd,
     'total_oos':total_oos,
     'total_ssa':total_ssa

    }
    return render(request, 'orders/es.html',context)


@allowedUsers(allowedGroups=['hr','staff',])
@login_required(login_url='signin')
@ratelimit(key='user_or_ip', rate='50/m')
def Status_pay(request, id):
    book_id = Order.objects.get(id=id)
    l = 0
    order = get_object_or_404(Order,pk=id)
    gf = OrderDetails.objects.filter(order__pk=id ).exclude(order__status=Order.Typechoices.a)

    if    not gf :
                  messages.error(request, _("يجب ان تختار حاله"))
                  return redirect('orderOrder',)
    elif order.status == None :
                  messages.error(request,_( "يجب ان تختار حاله"))
                  return redirect('orderOrder',)
    orderDetails = OrderDetails.objects.all().filter(order=order)
    y = 0
    d= 0
    for i in orderDetails:
        y += i.ba * i.product.qus
        d += i.ba
    if d == 0:
        messages.error(request, _(' العمل فى الطلب اولا'))
        return redirect('orderOrder' )
   
    if request.user.groups.filter(name='hr') :
        if not request.user == book_id.user_updete:
            messages.error(request, _(' انت لست اليوزر الذى اخترت الحاله'))
            return redirect('orderOrder',)

        if book_id.order_updated is not None:
             if book_id.order_updated <  timezone.now() :
                 messages.error(request, _('  تم انتهاء مدة التعديل '))
                 return redirect('orderOrder',)
    if  book_id.statusu == 'completed' :
            messages.error(request, _(' الطلب اكتمل ولا يمكن التعديل عليه '))
            return redirect('orderOrder',)
    if request.method == 'POST':
            book_save = Status_payform(request.POST, request.FILES ,instance=book_id)
            if book_save.is_valid():
                book_save.save()
                messages.success(request, 'تم الدفع')
                return redirect('orderOrder')
    else:
        book_save =Status_payform(instance=book_id)
    context ={
            'form':Status_payform,
        }
    return render(request, 'pages/update.html',context)


from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile
from django.utils.translation import gettext_lazy as _
import re
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from .backends import EmailBackend as em

from django.contrib import auth
from product.models import Product
from orders.models import Order,OrderDetails
import requests
from django.db.models import Sum,F,Count,Value
from django.conf import settings
from django.contrib.auth.models import Group
from .forms import EmailPostForm,OrderFrom
from .models import OtpToken,Profile
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import  *
from pages.models import  *
from product.decorators import aminnUsers

from django.core.mail import send_mail
from django_ratelimit.decorators import ratelimit
from product.decorators import allowedUsers,allowedCastomar
from .decoration import *
from django.db import transaction
import requests
from django.conf import settings
from product.forms import *
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
from django.template.loader import render_to_string
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from django.conf import settings
from django.http import JsonResponse


def send_reset_password_email(request):
    print(request.get_host())
    if request.method == "POST":
        email = request.POST.get("email")
        user = User.objects.filter(email=email)

        if user:

            try:
                      
                      user = User.objects.filter(email=email).last()
                      print(user.email)
                      token = default_token_generator.make_token(user)
                      uid = urlsafe_base64_encode(force_bytes(user.pk))
                      reset_url = request.build_absolute_uri(f"reset-password-confirm/{uid}/{token}/")
                      url = request.get_host()
                      past = f"fhttp://{url}/ar/accounts/reset-password-confirm/{uid}/{token}/"
                      
                      subject = "إعادة تعيين كلمة المرور"
                      message = f"<h5>انقر على الرابط التالي لإعادة تعيين كلمة المرور:\n{past}</h5>"
                      configuration = sib_api_v3_sdk.Configuration()
                      configuration.api_key['api-key'] = "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"
                      api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
                      email = sib_api_v3_sdk.SendSmtpEmail(
                          to=[{"email": user.email }],
                          sender={"email": settings.DEFAULT_FROM_EMAIL},
                          subject=subject,
                          html_content=message ,
                         
                      )
                      # send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
                      try:
                          api_instance.send_transac_email(email)
                          messages.success(request, "✅ تم إرسال رابط إعادة تعيين كلمة المرور")
                          return redirect('password_reset_done' )
                      except ApiException as e:
                          return JsonResponse({"error": f"خطأ في إرسال البريد: {e}"}, status=500)
                    #   send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
    
                # return JsonResponse({"message": "✅ تم إرسال رابط إعادة تعيين كلمة المرور"})
                # messages.success(request, "✅ تم إرسال رابط إعادة تعيين كلمة المرور")
                # return redirect('password_reset_done' )
            except User.DoesNotExist:
                 return JsonResponse({"error": "❌ لا يوجد مستخدم بهذا البريد الإلكتروني"}, status=404)
    
    return render(request, 'password_reset_form.html')




from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode

def reset_password_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)

        if default_token_generator.check_token(user, token):
            if request.method == "POST":
                new_password = request.POST.get("password")
                user.set_password(new_password)
                user.save()
                messages.success(request, "✅ تم تغيير كلمة المرور بنجاح")
                return redirect('login' )
            return render(request, "reset_password_form.html", {"validlink": True})
        else:
            messages.error(request, "❌ الرابط غير صالح أو منتهي")
            return redirect('reset_password_confirm',uidb64=uidb64, token=token)
            return JsonResponse({"error": "❌ الرابط غير صالح أو منتهي"}, status=400)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return JsonResponse({"error": "❌ خطأ في الرابط"}, status=400)


@login_required(login_url='signin')
@ratelimit(key='user_or_ip', rate='100/m')
@allowedUsers(allowedGroups=['staff','groadmin','hr','adminCastomar'])
def orfactrory(request):
    group = Group.objects.get(name='factory')
    user = UserProfile.objects.filter(user__groups=group)
    context = {
      'user':user  
    }
    return render(request, 'accounts/orfactrory.html',context)

@login_required(login_url='signin')
@ratelimit(key='user_or_ip', rate='100/m')
@allowedUsers(allowedGroups=['staff','groadmin','hr','adminCastomar'])
def Shipping_companies(request):
    group = Group.objects.get(name='Shippingcompanies')
    user = UserProfile.objects.filter(user__groups=group)
    context = {
      'user':user  
    }
    return render(request, 'accounts/dShippingcompanies.html',context)

@ratelimit(key='user_or_ip', rate='50/m')
@login_required(login_url='signin')
@allowedUsers(allowedGroups=['staff','groadmin','hr','adminCastomar'])
@transaction.atomic
def or_shipping(request,email):
    # nm = Namepartener.objects.get(email=request.user.email)
    r =  Reportpartener.objects.filter(ramepartener__email=email)
    
    return render(request, 'accounts/orshipping.html',{'r':r})

@login_required(login_url='signin')
@ratelimit(key='user_or_ip', rate='100/m')
@allowedUsers(allowedGroups=['staff','groadmin','hr','adminCastomar'])
def prodects__factrory__se(request,email):
    v =  Gx.objects.filter(email=email).exists()
    ssd = None
    if v:
        gr =  Gx.objects.get(email=email)
        ssd = gr.email
    
    events = Product.objects.filter(gx__email=ssd).annotate(
        pro_dahte = F('pro_date') + timezone.timedelta(minutes=10) ,
        
       
    )
   

   
    if request.method == "POST"  or 'p' in request.POST:
          
            try:
               namel =request.POST.get('namel')
               lg =request.POST.get('lg')
               ls =request.POST.get('ls')
               name =request.POST.get('name')
               number =request.POST.get('number')
               facat =request.POST.get('facat')
               gx =request.POST.get('gx')
               id =request.POST.get('id')
               uuid =request.POST.get('uuid')

               if name:
                   events = events.filter(name__icontains = name )
               if id:
                   events = events.filter(id__icontains = id)
               if uuid:
                   events = events.filter(uuid__icontains = uuid)
               if number:
                   events = events.filter(gx__number__icontains = number)
               if facat:
                   events = events.filter(facat__icontains = facat)
               if gx:
                   events = events.filter(gx__gx__icontains = gx)
        
               if lg and ls:
                   events = events.filter(publish_date__range = (lg, ls ))
               elif lg:
                   events = events.filter(publish_date__gte = lg)
               elif ls:
                   events = events.filter(publish_date__lte = ls)

             
    #            f = product.filter(
    #                  publish_date__range = [
    #                  lg,
    #                  ls
            
    #                  ],
                  
    #                 #  namel__icontains = namel,
    #                  name__icontains = name,
    #                  id__icontains = id,

    #                  gx__number__icontains = number,
    #                  facat__icontains = facat,
    #                  gx__gx__icontains = gx,

    #            ).annotate(
    #     pro_dahte = F('pro_date') + timezone.timedelta(minutes=10) ,
       
    # )
               context ={
                  'Product': events,
                #   'g':g
               } 
               messages.success(request, 'عملية بحث ناجحة')
               return render(request, 'accounts/dorfactrory.html' , context)
            except:
                context ={
                  'Product': events,
                } 
                
                messages.error(request, '  عملية بحث غير ناجحة  ')
                return render(request, 'accounts/dorfactrory.html' , context)

    else:
         
      
         context = {
           'Product': events,
             'from':Productfrm(),
           'all':Product.objects.all().count(),
           'formcat': Categoryform(),
           'category':Category.objects.all(),
           
           'category':Category.objects.all(),
        #    'g':g
         
             }

         return render(request, 'accounts/dorfactrory.html' , context)



# Create your views here.
# @ratelimit(key='user_or_ip', rate='10/m')
# def live(request,id):
    
#     video = Video.objects.get(id=id)
#     session_key ='view_topic_{}'.format(video.pk)
#     if not request.session.get(session_key,False):
#         video.views +=1
#         video.save()
#         request.session[session_key] = True
#     return redirect('video')
@ratelimit(key='user_or_ip', rate='10/m')
def live(request,id):
    
    video = Video.objects.get(id=id)
    if request.user in video.like.all():
        video.like.remove(request.user)
    else:
        video.like.add(request.user)
    return redirect('video')

# def live(request,id):
#     if request.user.is_authenticated:
#         video = Video.objects.get(id=id)
#         session_key ='view_topic_{}'.format(video.pk)
#         # cookies = request.COOKIES[session_key]
#         if not  request.COOKIES.get('view_topic_{}'.format(video.pk)):
#             video.views +=1
#             video.save()
#             rr = render(request,'accounts/video.html')
    
#             rr.set_cookie('view_topic_{}'.format(video.pk),'view_topic_{}'.format(video.pk) ) 
    
#             return rr ,render(request,'accounts/video.html')

     

      

#     return redirect('video')

@ratelimit(key='ip', rate='10000/m')
def video(request):
    video = Video.objects.all()
    return render(request, 'accounts/video.html',{'video':video})
@ratelimit(key='user_or_ip', rate='80/m')
def posts(request,id):
    
    userprofile = UserProfile.objects.get(user=request.user)
    videos = Video.objects.get(id=id)
    postss  = Post.objects.filter(video=videos)

    
         
    if request.method =='POST' :
          if 'post' in request.POST: 
               post = request.POST['post']
          else: 
              return redirect('posts' ,id=videos.pk)
          post = request.POST['post']
          nnnn =Post.objects.create(
             massage=  post,
             video =videos, 
             created_UserProfile = request.user ,
             img = userprofile.userimg

          )
          messages.success(request, _('تم اضافة تعليق'))
          return redirect('posts' ,id=videos.pk)
    context={'postss':postss,'userimg':userprofile.userimg,'category':Category.objects.all(),}
    return render(request, 'post.html',context)
@ratelimit(key='ip', rate='10000/m')
def signin(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:

        if request.method =='POST' and 'btnsignin' in request.POST:
           
           username = request.POST['username']
           password = request.POST['passS']
          
           user =em.authenticate(username=username ,password=password)
     
           
           if user is not None:
                recaptcha_response = request.POST.get("g-recaptcha-response")
                data={
                                     'secret':settings.GOOGLE_RACAPTCHA_SECRET_KEY,
                                     'response':recaptcha_response,
    
                                 }
                r = requests.post('https://www.google.com/recaptcha/api/siteverify',data=data)
                result = r.json()
                if result['success']:
                   auth.login(request, user ,backend='django.contrib.auth.backends.ModelBackend')
        
                   messages.success(request, 'تم التسجل بنجاح')
        
                   return redirect('/')
                else:
                                     messages.error(request, _('  انا لست برنامج روبوت '))
                                     return redirect('signin')
            
           else:
                messages.error(request, _(' خطا فى التسجيل'))
    
                return redirect('signin')
        else:
           
   
           return render(request, 'accounts/signin.html',{'category':Category.objects.all(),})


def signins(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:

        if request.method =='POST' and 'btnsignin' in request.POST:
           
           username = request.POST['username']
           password = request.POST['passS']
          
           user = auth.authenticate(username=username ,password=password)
           if user is not None:
                recaptcha_response = request.POST.get("g-recaptcha-response")
                data={
                                     'secret':settings.GOOGLE_RACAPTCHA_SECRET_KEY,
                                     'response':recaptcha_response,
    
                                 }
                r = requests.post('https://www.google.com/recaptcha/api/siteverify',data=data)
                result = r.json()
                if result['success']:
     
           
         
              
                   auth.login(request, user )
        
                   messages.success(request, 'تم التسجل بنجاح')
        
                   return redirect('/')
                else:
                                     messages.error(request, _('  انا لست برنامج روبوت '))
                                     return redirect('signin')
            
           else:
                messages.error(request, _(' خطا فى التسجيل'))
    
                return redirect('signins')
        else:
           
   
           return render(request, 'accounts/signin.html',{'category':Category.objects.all(),})



@ratelimit(key='ip', rate='10000/m')
def Shippingcompanies(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:

        if request.method =='POST' and 'btnsignup' in request.POST:
             fname=None
             lname=None
             address=None
           
             zip_number=None
             email=None
             username=None
             password=None
             tarms=None
    
             if 'fname' in request.POST:
                 fname = request.POST['fname']
             else: messages.error(request, 'error in frest name')
    
             if 'address' in request.POST: address = request.POST['address']
             else: messages.error(request, 'error in address')
    
             if 'zip_number' in request.POST: zip_number= request.POST['zip_number']
             else: messages.error(request, 'error in zip')
    
             if len(request.POST['zip_number'] ) !=  int(11) :
                messages.error(request, _('يجب ان يكون رقم الهاتف  مكون من 11 رقم'))
                return redirect('Shippingcompanies')
        
       
             if 'email' in request.POST: email = request.POST['email']
             else: messages.error(request, 'error in email')
       
             if 'passS' in request.POST: password = request.POST['passS']
             else: messages.error(request, 'error in pass')
       
             if  'tarms' in request.POST:  tarms = request.POST['tarms']
             if not  request.POST['zip_number'].startswith('010') and not request.POST['zip_number'].startswith('011')  and not request.POST['zip_number'].startswith('012') and not request.POST['zip_number'].startswith('015') :
                    messages.error(request, _('رقم الهاتف ليس صالح'))
                    return redirect('Shippingcompanies')
             elif fname  and address   and zip_number and email  and password   :
                if tarms == 'on':
                    if User.objects.filter(username=username).exists():
                     messages.error(request, _(' هذا الحساب موجود مسبقا'))
                     return redirect('Shippingcompanies')
    
                    else:
                        if User.objects.filter(email=email).exists():
                           messages.error(request, _(' هذا الحساب موجود مسبقا'))
                           return redirect('Shippingcompanies')
                        else:
                            if len(request.POST['zip_number'] ) !=  int(11) :
                             messages.error(request, _('يجب ان يكون رقم الهاتف  مكون من 11 رقم'))
                             return redirect('Shippingcompanies')
    
                            else:
                                 recaptcha_response = request.POST.get("g-recaptcha-response")
                                 data={
                                     'secret':settings.GOOGLE_RACAPTCHA_SECRET_KEY,
                                     'response':recaptcha_response,
    
                                 }
                                 r = requests.post('https://www.google.com/recaptcha/api/siteverify',data=data)
                                 result = r.json()
                                 if result['success']:
                             
                                    user = User.objects.create_user(
                                    first_name = fname,
                               
                                    email=email,
                                    password=password,
                                    username=email,
                                    
                                    )
                                    
                                    user.save()
                                    userprofile = UserProfile(
                                         user=user,
                                         address=address,
                                     
                                         zip_number= zip_number,
                                     )
                                    userprofile.save()
                                    groupss = Group.objects.get(name='Shippingcompanies')
                                    user.groups.add(groupss)
                                
                                    messages.success(request, _('تم انشاء حساب مسوق'))
                                    return redirect("verify_email",username=request.POST['email'])
                                 else:
                                     messages.error(request, _(' انا لست برنامج روبوت '))
                                     return redirect('Shippingcompanies')
        
                else:       
                     messages.error(request,_( "برجاء الموافقة على سياسات الموقع"))
                     return redirect('Shippingcompanies')
           
             else:
                 messages.error(request, _('يوجد مربع فارغ'))
                 return redirect('Shippingcompanies')
        
        else:
    
    
            return render(request, 'accounts/Shippingcompanies.html',
                #  {'category':Category.objects.all(),}        
            # 'fname': fname,
            {
                'category':Category.objects.all(),
            #     'lname': lname,
            # 'email':email,
            # 'passS':password,
            # 'username':username,
            # 'address':address,
            
            # 'zip_number': zip_number
            }
            )



def Shipping__companies(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:

        if request.method =='POST' and 'btnsignup' in request.POST:
             fname=None
             lname=None
             address=None
           
             zip_number=None
             email=None
             username=None
             password=None
             tarms=None
    
             if 'fname' in request.POST:
                 fname = request.POST['fname']
             else: messages.error(request, 'error in frest name')
    
             if 'address' in request.POST: address = request.POST['address']
             else: messages.error(request, 'error in address')
    
             if 'zip_number' in request.POST: zip_number= request.POST['zip_number']
             else: messages.error(request, 'error in zip')
    
             if len(request.POST['zip_number'] ) !=  int(11) :
                messages.error(request, _('يجب ان يكون رقم الهاتف  مكون من 11 رقم'))
                return redirect('Shippingcompanies')
        
       
             if 'email' in request.POST: email = request.POST['email']
             else: messages.error(request, 'error in email')
       
             if 'passS' in request.POST: password = request.POST['passS']
             else: messages.error(request, 'error in pass')
       
             if  'tarms' in request.POST:  tarms = request.POST['tarms']
             if not  request.POST['zip_number'].startswith('010') and not request.POST['zip_number'].startswith('011')  and not request.POST['zip_number'].startswith('012') and not request.POST['zip_number'].startswith('015') :
                    messages.error(request, _('رقم الهاتف ليس صالح'))
                    return redirect('Shippingcompanies')
             elif fname  and address   and zip_number and email  and password   :
                if tarms == 'on':
                    if User.objects.filter(username=username).exists():
                     messages.error(request, _(' هذا الحساب موجود مسبقا'))
                     return redirect('Shippingcompanies')
    
                    else:
                        if User.objects.filter(email=email).exists():
                           messages.error(request, _(' هذا الحساب موجود مسبقا'))
                           return redirect('Shippingcompanies')
                        else:
                            if len(request.POST['zip_number'] ) !=  int(11) :
                             messages.error(request, _('رقم الهاتف ليس صالح'))
                             return redirect('Shippingcompanies')
    
                            else:
                                 recaptcha_response = request.POST.get("g-recaptcha-response")
                                 data={
                                     'secret':settings.GOOGLE_RACAPTCHA_SECRET_KEY,
                                     'response':recaptcha_response,
    
                                 }
                                 r = requests.post('https://www.google.com/recaptcha/api/siteverify',data=data)
                                 result = r.json()
                                 if result['success']:
                             
                                    user = User.objects.create_user(
                                    first_name = fname,
                               
                                    email=email,
                                    password=password,
                                    username=email,
                                    
                                    )
                                    
                                    user.save()
                                    userprofile = UserProfile(
                                         user=user,
                                         address=address,
                                     
                                         zip_number= zip_number,
                                     )
                                    userprofile.save()
                                    groupss = Group.objects.get(name='Shippingcompanies')
                                    user.groups.add(groupss)
                                
                                    messages.success(request, _('تم انشاء حساب مسوق'))
                                    return redirect("verify_email",username=request.POST['email'])
                                 else:
                                     messages.error(request, _(' انا لست برنامج روبوت '))
                                     return redirect('Shippingcompanies')
        
                else:       
                     messages.error(request,_( "برجاء الموافقة على سياسات الموقع"))
                     return redirect('Shippingcompanies')
           
             else:
                 messages.error(request, _('يوجد مربع فارغ'))
                 return redirect('Shippingcompanies')
        
        else:
    
    
            return render(request, 'accounts/Shippingcompanies.html',
                #  {'category':Category.objects.all(),}        
            # 'fname': fname,
            {
                'category':Category.objects.all(),
            #     'lname': lname,
            # 'email':email,
            # 'passS':password,
            # 'username':username,
            # 'address':address,
            
            # 'zip_number': zip_number
            }
            )





@login_required(login_url='signin')
@allowedUsers(allowedGroups=['staff','Shippingcompanies'])
@transaction.atomic
def shipping(request):
    sd = 0
    if Namepartener.objects.filter(email=request.user.email).exists():
         namepartener = Namepartener.objects.get(email=request.user.email)
         sd = Deportpartener.objects.filter(ramepartener=namepartener.id).aggregate(Sum('uus'))['uus__sum']
  
    s = 0
    z = 0
    x = 0
    kj = 0
    r =  Reportpartener.objects.filter(ramepartener__email=request.user.email)
    for re in r:
        x += re.uus
        order = Order.objects.filter(Orderpartener=re).annotate(
        totalsb = Sum(F('orders__uus')  ),
        total = Sum(F('orderss__copping') * F('orderss__price')),

        )
        orders= Order.objects.filter(Orderpartener=re,user_group__name='castomar').annotate(
          total__ba = Sum(F('orderss__copping') * F('details__qus')),
        )
     
        for xd in orders:
             kj += int(xd.total__ba)
            
        for i in order:
            s += i.total
    h  =  x - s
   
    return render(request, 'pages/shipping.html',{'r':r,"s":s,'z':h,"sd":sd,'kj':kj})
@ratelimit(key='user_or_ip', rate='50/m')
@login_required(login_url='signin')
@allowedUsers(allowedGroups=['staff','Shippingcompanies'])
@transaction.atomic
def order__shipping(request,id):
    order = Order.objects.get(id=id)
    all_orders = OrderDetails.objects.filter(order=order)
    v = Order.objects.filter(pk=id).prefetch_related('orderss')\
    .annotate(total= F("orderss__quantity") * F("orderss__price"),
              pr = F("orderss__price")  )\
    .aggregate(Sum('total'))['total__sum']
    order = Order.objects.get(pk=id)
    quset = OrderDetails.objects.filter(order=order)
    # y = quset.order.user_group.name 
    group = Group.objects.get(name='castomar')
    qusetbbb = OrderDetails.objects.filter(order=order ,order__user_group=group)
    return render(request, 'pages/order__shipping.html',{'all_orders':all_orders,'totals':v,
        'group' : qusetbbb,
        'order':order,})


@ratelimit(key='ip', rate='10000/m')
@transaction.atomic
def factory(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:

        if request.method =='POST' and 'btnsignup' in request.POST:
             fname=None
             lname=None
             address=None
           
             zip_number=None
             email=None
             username=None
             password=None
             tarms=None
    
             if 'fname' in request.POST:
                 fname = request.POST['fname']
             else: messages.error(request, 'error in frest name')
    
             if 'address' in request.POST: address = request.POST['address']
             else: messages.error(request, 'error in address')
    
             if 'zip_number' in request.POST: zip_number= request.POST['zip_number']
             else: messages.error(request, 'error in zip')
    
             if len(request.POST['zip_number'] ) !=  int(11) :
                messages.error(request, _('يجب ان يكون رقم الهاتف  مكون من 11 رقم'))
                return redirect('factory')
        
       
             if 'email' in request.POST: email = request.POST['email']
             else: messages.error(request, 'error in email')
       
             if 'passS' in request.POST: password = request.POST['passS']
             else: messages.error(request, 'error in pass')
       
             if  'tarms' in request.POST:  tarms = request.POST['tarms']
             if not  request.POST['zip_number'].startswith('010') and not request.POST['zip_number'].startswith('011')  and not request.POST['zip_number'].startswith('012') and not request.POST['zip_number'].startswith('015') :
                    messages.error(request, _('رقم الهاتف ليس صالح'))
                    return redirect('factory')
             elif fname  and address   and zip_number and email  and password   :
                if tarms == 'on':
                    if User.objects.filter(username=username).exists():
                     messages.error(request, _(' هذا الحساب موجود مسبقا'))
                     return redirect('factory')
    
                    else:
                        if User.objects.filter(email=email).exists():
                           messages.error(request, _(' هذا الحساب موجود مسبقا'))
                           return redirect('factory')
                        else:
                            if len(request.POST['zip_number'] ) !=  int(11) :
                             messages.error(request, _('يجب ان يكون رقم الهاتف  مكون من 11 رقم'))
                             return redirect('factory')
    
                            else:
                                 recaptcha_response = request.POST.get("g-recaptcha-response")
                                 data={
                                     'secret':settings.GOOGLE_RACAPTCHA_SECRET_KEY,
                                     'response':recaptcha_response,
    
                                 }
                                 r = requests.post('https://www.google.com/recaptcha/api/siteverify',data=data)
                                 result = r.json()
                                 if result['success']:
                             
                                    user = User.objects.create_user(
                                    first_name = fname,
                               
                                    email=email,
                                    password=password,
                                    username=email,
                                    
                                    )
                                    
                                    user.save()
                                    userprofile = UserProfile(
                                         user=user,
                                         address=address,
                                     
                                         zip_number= zip_number,
                                     )
                                    userprofile.save()
                                    groupss = Group.objects.get(name='factory')
                                    user.groups.add(groupss)
                                
                                    messages.success(request, _('تم انشاء حساب مسوق'))
                                    return redirect("verify_email",username=request.POST['email'])
                                 else:
                                     messages.error(request, _(' انا لست برنامج روبوت '))
                                     return redirect('factory')
        
                else:       
                     messages.error(request,_( "برجاء الموافقة على سياسات الموقع"))
                     return redirect('factory')
           
             else:
                 messages.error(request, _('يوجد مربع فارغ'))
                 return redirect('factory')
        
        else:
    
    
            return render(request, 'accounts/factory.html',
                #  {'category':Category.objects.all(),}        
            # 'fname': fname,
            {
                'category':Category.objects.all(),
            #     'lname': lname,
            # 'email':email,
            # 'passS':password,
            # 'username':username,
            # 'address':address,
            
            # 'zip_number': zip_number
            }
            )

        
     
    

@ratelimit(key='ip', rate='10000/m')
@transaction.atomic

def signupcastomar(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:

        if request.method =='POST' and 'btnsignup' in request.POST:
             fname=None
             lname=None
             address=None
           
             zip_number=None
             email=None
             username=None
             password=None
             tarms=None
    
             if 'fname' in request.POST:
                 fname = request.POST['fname']
             else: messages.error(request, 'error in frest name')
    
             if 'address' in request.POST: address = request.POST['address']
             else: messages.error(request, 'error in address')
    
             if 'zip_number' in request.POST: zip_number= request.POST['zip_number']
             else: messages.error(request, 'error in zip')
    
             if len(request.POST['zip_number'] ) !=  int(11) :
                messages.error(request, _('يجب ان يكون رقم الهاتف  مكون من 11 رقم'))
                return redirect('signupcastomar')
        
       
             if 'email' in request.POST: email = request.POST['email']
             else: messages.error(request, 'error in email')
       
             if 'passS' in request.POST: password = request.POST['passS']
             else: messages.error(request, 'error in pass')
       
             if  'tarms' in request.POST:  tarms = request.POST['tarms']
             if not  request.POST['zip_number'].startswith('010') and not request.POST['zip_number'].startswith('011')  and not request.POST['zip_number'].startswith('012') and not request.POST['zip_number'].startswith('015') :
                    messages.error(request, _('رقم الهاتف ليس صالح'))
                    return redirect('signupcastomar')
             elif fname  and address   and zip_number and email  and password   :
                if tarms == 'on':
                    if User.objects.filter(username=username).exists():
                     messages.error(request, _(' هذا الحساب موجود مسبقا'))
                     return redirect('signupcastomar')
    
                    else:
                        if User.objects.filter(email=email).exists():
                           messages.error(request, _(' هذا الحساب موجود مسبقا'))
                           return redirect('signupcastomar')
                        else:
                            if len(request.POST['zip_number'] ) !=  int(11) :
                             messages.error(request, _('يجب ان يكون رقم الهاتف  مكون من 11 رقم'))
                             return redirect('signupcastomar')
    
                            else:
                                 recaptcha_response = request.POST.get("g-recaptcha-response")
                                 data={
                                     'secret':settings.GOOGLE_RACAPTCHA_SECRET_KEY,
                                     'response':recaptcha_response,
    
                                 }
                                 r = requests.post('https://www.google.com/recaptcha/api/siteverify',data=data)
                                 result = r.json()
                                 if result['success']:
                             
                                    user = User.objects.create_user(
                                    first_name = fname,
                               
                                    email=email,
                                    password=password,
                                    username=email,
                                    
                                    )
                                    
                                    user.save()
                                    userprofile = UserProfile(
                                         user=user,
                                         address=address,
                                     
                                         zip_number= zip_number,
                                     )
                                    userprofile.save()
                                    groupss = Group.objects.get(name='castomar')
                                    user.groups.add(groupss)
                                
                                    messages.success(request, _('تم انشاء حساب مسوق'))
                                    return redirect("verify_email",username=request.POST['email'])
                                 else:
                                     messages.error(request, _(' انا لست برنامج روبوت '))
                                     return redirect('signupcastomar')
        
                else:       
                     messages.error(request,_( "برجاء الموافقة على سياسات الموقع"))
                     return redirect('signupcastomar')
           
             else:
                 messages.error(request, _('يوجد مربع فارغ'))
                 return redirect('signupcastomar')
        
        else:
    
    
            return render(request, 'accounts/castomar.html',
                #  {'category':Category.objects.all(),}        
            # 'fname': fname,
            {
                'category':Category.objects.all(),
            #     'lname': lname,
            # 'email':email,
            # 'passS':password,
            # 'username':username,
            # 'address':address,
            
            # 'zip_number': zip_number
            }
            )

        
     
          
    
@ratelimit(key='ip', rate='500/m')
@transaction.atomic

def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
    

   
        if request.method =='POST' and 'btnsignup' in request.POST:
             fname=None
             lname=None
             address=None
            
             zip_number=None
             email=None
             username=None
             password=None
             tarms=None
    
             if 'fname' in request.POST: fname = request.POST['fname']
             else: messages.error(request, 'error in frest name')
    
    
            #  if 'lname' in request.POST: lname = request.POST['lname']
            #  else: messages.error(request, 'error in lname name')
       
       
             if 'address' in request.POST: address = request.POST['address']
             else: messages.error(request, 'error in address')
    
            #  if 'address2' in request.POST: address2 = request.POST['address2']
            #  else: messages.error(request, 'error in address2')
       
            #  if 'city' in request.POST: city = request.POST['city']
            #  else: messages.error(request, 'error in city')
       
             if 'zip_number' in request.POST: zip_number= request.POST['zip_number']
             else: messages.error(request, 'error in zip')
       
             if 'email' in request.POST: email = request.POST['email']
             else: messages.error(request, 'error in email')
       
            #  if 'user' in request.POST: username = request.POST['user']
            #  else: messages.error(request, 'error in user')
       
             if 'passS' in request.POST: password = request.POST['passS']
             else: messages.error(request, 'error in pass')
       
             if  'tarms' in request.POST:  tarms = request.POST['tarms']

             if not  request.POST['zip_number'].startswith('010') and not request.POST['zip_number'].startswith('011')  and not request.POST['zip_number'].startswith('012') and not request.POST['zip_number'].startswith('015') :
                    messages.error(request,_( 'رقم الهاتف ليس صالح'))
                    return redirect('signup')
    
             elif fname and  address  and  zip_number and email and password  :
                if tarms == 'on':
                    if User.objects.filter(username=username).exists():
                     messages.error(request, _('اليوزر موجود '))
                     return redirect('signup')
    
                    else:
                        if User.objects.filter(email=email).exists():
                           messages.error(request, _('الاميل موجود'))
                           return redirect('signup')
                        
    
    
                        else:
                           
                            if len(request.POST['zip_number'] ) !=  int(11) :
                             messages.error(request, _('يجب ان يكون رقم الهاتف  مكون من 11 رقم'))
                             return redirect('signup')
    
                            else:
                                 recaptcha_response = request.POST.get("g-recaptcha-response")
                                 data={
                                     'secret':settings.GOOGLE_RACAPTCHA_SECRET_KEY,
                                     'response':recaptcha_response,
    
                                 }
                                 r = requests.post('https://www.google.com/recaptcha/api/siteverify',data=data)
                                 result = r.json()
                                 if result['success']:
                         
                                    user = User.objects.create_user(
                                    first_name = fname,
                             
                                    email=email,
                                    password=password,
                                    username=email,
                                    
                                    )
                                 
                                    user.save()
                                    userprofile = UserProfile(
                                         user=user,
                                         address=address,
                                     
                                         zip_number= zip_number,
                                     )
                                    userprofile.save()
                                    group = Group.objects.get(name='admin')
                                    user.groups.add(group)
                               
                                    messages.success(request,_("تم انشاء حساب عميل"))
                                    return redirect("verify_email",username=request.POST['email'])
                                 else:
                                     messages.error(request, _('  انا لست برنامج روبوت '))
                                     return redirect('signup')
                                     
    
                else:       
                     messages.error(request, _("برجاء الموافقة على سياسات الموقع"))
                     return redirect('signup')
           
             else:
                 messages.error(request, _('يوجد فيلد فارغ'))
                 return redirect('signup')
        
        else:
    
    
             return render(request, 'accounts/signup.html',
                         
            {   
                'category':Category.objects.all(),
            #     'fname': fname,
            # 'lname': lname,
            # 'email':email,
            # 'passS':password,
            # 'username':username,
            # 'address':address,
      
            # 'zip_number': zip_number
            }
            )




@transaction.atomic

def signupsignin(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
    

   
        if request.method =='POST' and 'btnsignup' in request.POST:
             fname=None
             lname=None
             address=None
            
             zip_number=None
             email=None
             username=None
             password=None
             tarms=None
    
             if 'fname' in request.POST: fname = request.POST['fname']
             else: messages.error(request, 'error in frest name')
    
    
            #  if 'lname' in request.POST: lname = request.POST['lname']
            #  else: messages.error(request, 'error in lname name')
       
       
             if 'address' in request.POST: address = request.POST['address']
             else: messages.error(request, 'error in address')
    
            #  if 'address2' in request.POST: address2 = request.POST['address2']
            #  else: messages.error(request, 'error in address2')
       
            #  if 'city' in request.POST: city = request.POST['city']
            #  else: messages.error(request, 'error in city')
       
             if 'zip_number' in request.POST: zip_number= request.POST['zip_number']
             else: messages.error(request, 'error in zip')
       
             if 'email' in request.POST: email = request.POST['email']
             else: messages.error(request, 'error in email')
       
            #  if 'user' in request.POST: username = request.POST['user']
            #  else: messages.error(request, 'error in user')
       
             if 'passS' in request.POST: password = request.POST['passS']
             else: messages.error(request, 'error in pass')
       
             if  'tarms' in request.POST:  tarms = request.POST['tarms']

             if not  request.POST['zip_number'].startswith('010') and not request.POST['zip_number'].startswith('011')  and not request.POST['zip_number'].startswith('012') and not request.POST['zip_number'].startswith('015') :
                    messages.error(request,_( 'رقم الهاتف ليس صالح'))
                    return redirect('signup')
    
             elif fname and  address  and  zip_number and email and password  :
                if tarms == 'on':
                    if User.objects.filter(username=username).exists():
                     messages.error(request, _('اليوزر موجود '))
                     return redirect('signup')
    
                    else:
                        if User.objects.filter(email=email).exists():
                           messages.error(request, _('الاميل موجود'))
                           return redirect('signup')
                        
    
    
                        else:
                           
                            if len(request.POST['zip_number'] ) !=  int(11) :
                             messages.error(request, _('يجب ان يكون رقم الهاتف  مكون من 11 رقم'))
                             return redirect('signup')
    
                            else:
                                 recaptcha_response = request.POST.get("g-recaptcha-response")
                                 data={
                                     'secret':settings.GOOGLE_RACAPTCHA_SECRET_KEY,
                                     'response':recaptcha_response,
    
                                 }
                                 r = requests.post('https://www.google.com/recaptcha/api/siteverify',data=data)
                                 result = r.json()
                                 if result['success']:
                         
                                    user = User.objects.create_user(
                                    first_name = fname,
                             
                                    email=email,
                                    password=password,
                                    username=email,
                                    
                                    )
                                    user.is_active = True
                                    
                                 
                                    user.save()
                                    userprofile = UserProfile(
                                         user=user,
                                         address=address,
                                     
                                         zip_number= zip_number,
                                     )
                                    userprofile.save()
                                    group = Group.objects.get(name='admin')
                                    user.groups.add(group)
                               
                                    messages.success(request,_("تم انشاء حساب عميل"))
                                    return redirect("signin",)
                                 else:
                                     messages.error(request, _('  انا لست برنامج روبوت '))
                                     return redirect('signup')
                                     
    
                else:       
                     messages.error(request, _("برجاء الموافقة على سياسات الموقع"))
                     return redirect('signup')
           
             else:
                 messages.error(request, _('يوجد فيلد فارغ'))
                 return redirect('signup')
        
        else:
    
             return render(request, 'accounts/signup.html',
                         
            {   
                'category':Category.objects.all(),
      
            }
            )



def signupsignincastomar(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
    

   
        if request.method =='POST' and 'btnsignup' in request.POST:
             fname=None
             lname=None
             address=None
            
             zip_number=None
             email=None
             username=None
             password=None
             tarms=None
    
             if 'fname' in request.POST: fname = request.POST['fname']
             else: messages.error(request, 'error in frest name')
    
    
            #  if 'lname' in request.POST: lname = request.POST['lname']
            #  else: messages.error(request, 'error in lname name')
       
       
             if 'address' in request.POST: address = request.POST['address']
             else: messages.error(request, 'error in address')
    
            #  if 'address2' in request.POST: address2 = request.POST['address2']
            #  else: messages.error(request, 'error in address2')
       
            #  if 'city' in request.POST: city = request.POST['city']
            #  else: messages.error(request, 'error in city')
       
             if 'zip_number' in request.POST: zip_number= request.POST['zip_number']
             else: messages.error(request, 'error in zip')
       
             if 'email' in request.POST: email = request.POST['email']
             else: messages.error(request, 'error in email')
       
            #  if 'user' in request.POST: username = request.POST['user']
            #  else: messages.error(request, 'error in user')
       
             if 'passS' in request.POST: password = request.POST['passS']
             else: messages.error(request, 'error in pass')
       
             if  'tarms' in request.POST:  tarms = request.POST['tarms']

             if not  request.POST['zip_number'].startswith('010') and not request.POST['zip_number'].startswith('011')  and not request.POST['zip_number'].startswith('012') and not request.POST['zip_number'].startswith('015') :
                    messages.error(request,_( 'رقم الهاتف ليس صالح'))
                    return redirect('signup')
    
             elif fname and  address  and  zip_number and email and password  :
                if tarms == 'on':
                    if User.objects.filter(username=username).exists():
                     messages.error(request, _('اليوزر موجود '))
                     return redirect('signup')
    
                    else:
                        if User.objects.filter(email=email).exists():
                           messages.error(request, _('الاميل موجود'))
                           return redirect('signup')
                        
    
    
                        else:
                           
                            if len(request.POST['zip_number'] ) !=  int(11) :
                             messages.error(request, _('يجب ان يكون رقم الهاتف  مكون من 11 رقم'))
                             return redirect('signup')
    
                            else:
                                 recaptcha_response = request.POST.get("g-recaptcha-response")
                                 data={
                                     'secret':settings.GOOGLE_RACAPTCHA_SECRET_KEY,
                                     'response':recaptcha_response,
    
                                 }
                                 r = requests.post('https://www.google.com/recaptcha/api/siteverify',data=data)
                                 result = r.json()
                                 if result['success']:
                         
                                    user = User.objects.create_user(
                                    first_name = fname,
                             
                                    email=email,
                                    password=password,
                                    username=email,
                                    
                                    )
                                    user.is_active = True
                                    
                                 
                                    user.save()
                                    userprofile = UserProfile(
                                         user=user,
                                         address=address,
                                     
                                         zip_number= zip_number,
                                     )
                                    userprofile.save()
                                    group = Group.objects.get(name='castomar')
                                    user.groups.add(group)
                               
                                    messages.success(request,_("تم انشاء حساب عميل"))
                                    return redirect("signin",)
                                 else:
                                     messages.error(request, _('  انا لست برنامج روبوت '))
                                     return redirect('signup')
                                     
    
                else:       
                     messages.error(request, _("برجاء الموافقة على سياسات الموقع"))
                     return redirect('signup')
           
             else:
                 messages.error(request, _('يوجد فيلد فارغ'))
                 return redirect('signup')
        
        else:
    
             return render(request, 'accounts/signup.html',
                         
            {   
                'category':Category.objects.all(),
      
            }
            )
    
@ratelimit(key='ip', rate='10000/m')
def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('/')
        


@ratelimit(key='ip', rate='500/m')
@transaction.atomic

def profile(request):
    if request.method == 'POST' and 'btnsavee' in request.POST:
        phone = request.POST['zip_number'] 
        if len(request.POST['zip_number'] ) !=  int(11) :
            messages.error(request, _('يجب ان يكون رقم الهاتف  مكون من 11 رقم'))
            return redirect('profile')
        elif not  request.POST['zip_number'].startswith('010') and not request.POST['zip_number'].startswith('011')  and not request.POST['zip_number'].startswith('012') and not request.POST['zip_number'].startswith('015') :
                    messages.error(request, _('رقم الهاتف ليس صحيح'))
                    return redirect('profile')
        elif request.user is not None and  request.user.id != None:
            userprofile = UserProfile.objects.get(user=request.user)
            
            request.user.first_name = request.POST['fname']
          
            # request.user.username = request.POST['fname']
            userprofile =UserProfile.objects.get(user=request.user)
            if request.FILES.get('userimg') :
                userprofile.userimg = request.FILES['userimg']
            else:
 
               userprofile.userimg = userprofile.userimg
            
            userprofile.address = request.POST['address']
           
            userprofile.zip_number = request.POST['zip_number']
            # if not request.POST['passS'].startswith('pbkdf2_sha256$'):
            #     request.user.set_password(request.POST['passS'])
            request.user.save()
            userprofile.save()
            auth.login(request,request.user,backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, _("تم حفظ التغير"))
            return redirect('profile')

  

        return redirect('profile')
    else:
        if request.user is not None:
            
           
            context = None
            if not request.user.is_anonymous:
                userprofile =UserProfile.objects.get(user=request.user)
                context = {
                    'fname':request.user.first_name ,
                
                    'email':request.user.email ,
                    'user':request.user.username ,
                    'passS':request.user.password,
                 
                    'address':userprofile.address ,
                    'userimg':userprofile.userimg ,

               
                    'zip_number':userprofile.zip_number 
                    ,'category':Category.objects.all(),
                }
                
                    
                
                
            return render(request , 'accounts/profile.html' , context)
        else:
            return redirect('profile')
@ratelimit(key='user_or_ip', rate='10/m') 
def prodect_favorite(request,uuid):
    if request.user.is_authenticated and not request.user.is_anonymous and uuid:
        pro_fav = Product.objects.get(uuid=uuid)
        if UserProfile.objects.filter(user=request.user,Product_favorites=pro_fav).exists():
            messages.success(request,_( 'هذا  المنتج موجود فى المفضلة'))
            return redirect('/')
      
        else:
            userprofile = UserProfile.objects.get(user=request.user)
            userprofile.Product_favorites.add(pro_fav)
            messages.success(request ,_('تم اضافة المنتج فى المفضلة'))
            return redirect('/')
            

    else:
        messages.error(request ,_('سجل اولا'))
        return redirect('signin')


     
    return redirect('prodects' )

@ratelimit(key='user_or_ip', rate='10/m')
def show_prodect_favorite(request):

    context = None
    if request.user.is_authenticated and not request.user.is_anonymous:
        userInfo = UserProfile.objects.get(user=request.user)
        pro = userInfo.Product_favorites.all() 
        context = {'Product':pro,'category':Category.objects.all(),}


    return render(request ,'prodects/prodects.html', context)






    # if request.method =='POST' and 'btnsignup' in request.POST:
    #      fname=None
    #      lname=None
    #      address=None
    #      address2=None
    #      city=None
    #      state=None
    #      zip_number=None
    #      email=None
    #      username=None
    #      password=None
    #      tarms=None

    #      if 'fname' in request.POST: fname = request.POST['fname']
    #      else: messages.error(request, 'error in frest name')


    #      if 'lname' in request.POST: lname = request.POST['lname']
    #      else: messages.error(request, 'error in lname name')
   
   
    #      if 'address' in request.POST: address = request.POST['address']
    #      else: messages.error(request, 'error in address')

    #      if 'address2' in request.POST: address2 = request.POST['address2']
    #      else: messages.error(request, 'error in address2')
   
    #      if 'city' in request.POST: city = request.POST['city']
    #      else: messages.error(request, 'error in city')
   
    #      if 'zip' in request.POST: zip_number= request.POST['zip']
    #      else: messages.error(request, 'error in zip')
   
    #      if 'email' in request.POST: email = request.POST['email']
    #      else: messages.error(request, 'error in email')
   
    #      if 'user' in request.POST: username = request.POST['user']
    #      else: messages.error(request, 'error in user')
   
    #      if 'pass' in request.POST: passWord = request.POST['pass']
    #      else: messages.error(request, 'error in pass')
   
    #      if  'tarms' in request.POST:  tarms = request.POST['tarms']
        
         

    #      if fname and lname and address and address2 and  city and zip_number and email and username and password :
    #         if tarms == 'on':
    #            if User.objects.filter(username=username).exists():
    #             messages.error(request, 'this username is taken ')

    #            else:
    #                 if User.objects.filter(email=email).exists():
    #                    messages.error(request, 'this email is taken ')

    #                 else:
    #                     patt = "^\w+([-+,']\w+)*@\W+([-.]\w+)*\.\w+([-.]\w+)*$"
    #                 if re.match(patt,email):
    #                    user = User.objects.create_user(
    #                       first_name = fname,
    #                       last_name = lname,
    #                       email=email,
    #                       password=password,
    #                       username=username,
    #                    )
    #                    user.save()
    #                    userprofile = UserProfile(
    # #                       user=user,
    # #                       address=address,
    # #                       address2=address2,
    # #                       city=city,
    # #                       state=state,
    # #                      zip_number= zip_number,
    # #                    )
    # #                    userprofile.save()
    # #                    messages.success(request, 'your account is created ')
    # #                 else:
    # #                      messages.error(request, 'invalid email ')


                           
                       
          
               
               
    #         else:       
    #              messages.error(request, 'you must agree to the terms')
       
    #      else:
    #          messages.error(request, 'Check empty fileds')
    



    #          return render(request, 'accounts/signup.html',{
                     
    #         'fname' : fname,
    #         'lname': lname,
    #         'email':email,
    #         'pass':password,
    #         'username':username,
    #         'address':address,
    #         'address2':address2,
    #         'city':city,
    #         'state':state,
    #         'zip': zip_number
    #               })
@login_required(login_url='signin')
@allowedUsers(allowedGroups=['adminCastomar','groadmin'])
@transaction.atomic

@ratelimit(key='user_or_ip', rate='10/m')
def p(request):
    f = UserProfile.objects.all()
    username =request.POST.get('username')
    email =request.POST.get('email')
    zip_number =request.POST.get('zip_number')


    if request.method =="POST":
         quset = f.filter(
              
         user__first_name__icontains = username,
         user__email__icontains = email,
         zip_number__icontains = zip_number,

        )
         
    else:
        quset = UserProfile.objects.all()

    context ={
        'userprofile':quset,
       

        
    }
    return render(request,'reqqer/p.html',context)
@ratelimit(key='user_or_ip', rate='10/m')
@login_required(login_url='signin')
@allowedUsers(allowedGroups=['adminCastomar','groadmin'])
def orderuser(request,id):
    orderuser = User.objects.get(pk=id)
    context = None
    all_orders = None
    orderdetails = None
    if  request.user.is_authenticated and not request.user.is_anonymous:
        all_orders = Order.objects.all().filter(user=orderuser)
        if all_orders:
            for x in all_orders:
               order = Order.objects.get(id=x.id)
               orderdetails = OrderDetails.objects.all().filter(order=order)
               total = 0
               for  sub in orderdetails:
                  total += sub.price * sub.quantity
               x.totle = total
               x.items_count= orderdetails.count
               x.items_counts= sub.product.name
 
    context = {
        'all_orders':all_orders,
      
'category':Category.objects.all(),
        }


    return render(request,'reqqer/orderuser.html',context)


from django.db.models import Sum,F,Count
from .forms import puserFromss
from django.db.models import OuterRef,Subquery,Exists
from django_ratelimit.decorators import ratelimit

@allowedusershr(allowGroupshr =["staff",'hr'])
@transaction.atomic

@ratelimit(key='user_or_ip', rate='25/m')
@login_required(login_url='signin')
def totals(request,id):
    v = Order.objects.filter(pk=id).prefetch_related('orderss')\
    .annotate(total= F("orderss__quantity") * F("orderss__price"),
              pr = F("orderss__price")  )\
    .aggregate(Sum('total'))['total__sum']
    order = Order.objects.get(pk=id)
    print(order.order_updated)
    quset = OrderDetails.objects.filter(order=order)
    # y = quset.order.user_group.name 
    group = Group.objects.get(name='castomar')
    qusetbbb = OrderDetails.objects.filter(order=order ,order__user_group=group)
    # ----------------------------------
    # orservvv = Order.objects.all()
    # g = OrderDetails.objects.filter(order=OuterRef('pk')).order_by('pk')
    # orserrr = orservvv.annotate(
    #     price= Subquery(g.values('price')[:1]),
    #     quantity= Subquery(g.values('quantity')[:1]),
    #     ll = F("quantity") * F("price")

    # )
 
    # for v in orserrr:
    #     print(f"{v.pk} -   {v.price} - {v.quantity} -{v.ll}")
    # re = Order.objects.filter(status__in=['sold'])
    # se = OrderDetails.objects.filter(order__in=Subquery(re.values('pk')))
    # print(re)
    # # print(se)
    # print(len(se))
    # rer  = Order.objects.filter(
    #     Exists(OrderDetails.objects.filter(order=OuterRef('pk'),price=900))
    # )
    # print(rer.count())
    # for i in rer:
    #      print(i.order_date)
   
   
    context = {
        'all_orders':quset,
      
        'totals':v,
        'group' : qusetbbb,
        'order':order,
      
       
        
        }
    
    return render(request,'reqqer/totals.html',context)
from .forms import *
from product.models import *

@ratelimit(key='user_or_ip', rate='60/m')
@allowedusershr(allowGroupshr =["groadmin"])
@login_required(login_url='signin')
@transaction.atomic

def prodects_id_user(request ,id):
    pro = Product.objects.get(pk=id)
 
    fi = Fintion.objects.filter(fintion=pro.pk)
    sad = 0
    v = Fintion.objects.filter(fintion=pro.id, order_idsid__statusu='completed')
    for i in v:
       sad += int(i.usus ) * int(i.fintion.pricels)
    sa = 0 
    b = Fintion.objects.filter(fintion=pro.id, ).exclude(order_idsid__statusu ='completed')
    for isd in b:
       sa = int(isd.usus )* int(isd.fintion.pricels)
   
    return render(request,'prodects/fintion.html',{'gx':fi,'sa':sa,'sad':sad})

@ratelimit(key='user_or_ip', rate='60/m')
@allowedusershr(allowGroupshr =["staff",'hr'])
@transaction.atomic

@login_required(login_url='signin')
def updateOrderDetailss(request ,order_id,OrderDetails_id):
    order = get_object_or_404(OrderDetails,order__pk=order_id,pk=OrderDetails_id)
    book_id = Order.objects.get(id=order_id)
    jjj = Product.objects.get(pk=order.product.pk)
    o = order.s

  
    if request.user.groups.filter(name='hr') :
        if book_id.order_updated is not None:
             if book_id.order_updated <  timezone.now() :
                 messages.error(request, _('  تم انتهاء مدة التعديل '))
                 return redirect('orderOrder') 
    if request.method =='POST':
        
        if  book_id.statusu == 'completed' :
         messages.error(request, _(' الطلب اكتمل ولا يمكن التعديل عليه '))
         return redirect('updateOrderDetailss',order_id=order_id,OrderDetails_id=OrderDetails_id) 

        if book_id.is_finished == True: 
          vuu = request.POST.get('s')
          order = get_object_or_404(OrderDetails,order__pk=order_id,pk=OrderDetails_id)
        
          book_save = OrderdetelsFromdd(request.POST, request.FILES, instance=order)
          if book_save.is_valid():
               book_save.save()
               orderx = get_object_or_404(OrderDetails,order__pk=order_id,pk=OrderDetails_id)
               vuu = request.POST.get('s')
               jm = OrderDetails.objects.filter(order__pk=order_id ,order__status=Order.Typechoices.b)

               gf = OrderDetails.objects.filter(order__pk=order_id ).exclude(order__status=Order.Typechoices.a)
               htl = OrderDetails.objects.get(order__pk=order_id,pk=OrderDetails_id)
              
               order = get_object_or_404(OrderDetails,order__pk=order_id,pk=OrderDetails_id)  
               if  book_id.statusu == 'completed' :
                      messages.error(request, _(' الطلب اكتمل ولا يمكن التعديل عليه '))
                      return redirect('updateOrderDetailss',order_id=order_id,OrderDetails_id=OrderDetails_id) 
               elif    not gf :
                  messages.error(request, _("يجب ان تختار حاله"))
                  return redirect('updateOrderDetailss',order_id=order_id,OrderDetails_id=OrderDetails_id)  
               elif htl.order.status == None :
                  messages.error(request,_( "يجب ان تختار حاله"))
                  return redirect('updateOrderDetailss',order_id=order_id,OrderDetails_id=OrderDetails_id)  
               elif not request.user.groups.filter(name='staff') and not book_id.user_updete == request.user   :



                  messages.error(request,_( "  انت لست اليوزر الى اخترت الحاله ولا يمكن التعديل على الطلب "))
                  return redirect('updateOrderDetailss',order_id=order_id,OrderDetails_id=OrderDetails_id)  
               
               elif not int(orderx.quantity) >=  int(vuu) :
                  messages.error(request, _('عملية خاطئة'))
                  return redirect('updateOrderDetailss',order_id=order_id,OrderDetails_id=OrderDetails_id) 
               elif int(vuu) < 0 :
                  messages.error(request, _('عملية خاطئة'))
                  return redirect('updateOrderDetailss',order_id=order_id,OrderDetails_id=OrderDetails_id) 
               
               elif jm :
                  messages.error(request, _('  تم تاكيد الطلب ولا يمكن التعديل عليه'))
                  return redirect('updateOrderDetailss',order_id=order_id,OrderDetails_id=OrderDetails_id) 
               
               
                  
               elif Product.objects.filter(id=order.product.pk,facat=True ,boonimg=False) :

                  try:
                      jjj = Product.objects.get(pk=order.product.pk)
                      colorr = Color.objects.get(productcolor_id=jjj,name=orderx.colar)
                      sizes = Sise.objects.get(productsise__name=colorr,sisel=orderx.size)
                      order = get_object_or_404(OrderDetails,order__pk=order_id,pk=OrderDetails_id)
                      vuu = request.POST.get('s')
                      if order.quantity >= int(vuu) :
                  
                         colorr.qucolor  -= int(order.testing)
                         
                         colorr.save()
                         sizes.qusise -= int(order.testing)
                      
                         sizes.save()
                         jjj.qu  -= int(order.testing)
                         
                         jjj.save()

                         ddf = Fintion.objects.filter(order_detils = orderx.pk,fintion=jjj, order_idsid=book_id.pk)
                         if ddf:
                            Fintion.objects.filter(order_detils = orderx.pk,fintion=jjj, order_idsid=book_id.pk).update(usus = int(vuu))
                         else:
                            Fintion.objects.create(
                                fintion=jjj,
                                order_idsid=book_id,
                                usus = int(vuu),
                                order_detils = orderx.pk,

                             )
                        
                         order.testing = int(order.quantity) -  int(vuu)
                        
                         order.ba = int(order.quantity) - int(order.testing )
                  
                 
                         order.save()
            
            
                         jjj.qu  += int(order.testing)
                     
                         jjj.save()
                 
                         colorr = Color.objects.get(productcolor_id=jjj,name=orderx.colar)
                         colorr.qucolor += int(order.testing)
                     
                     
                         colorr.save()
                     
                         sizes = Sise.objects.get(productsise__name=colorr,sisel=orderx.size)
                         
                         sizes.qusise += int(order.testing)
                 
                         sizes.save()
                         book_id.user_updete = request.user
                         book_id.save()
                         
                         messages.success(request,_("عملية ناجحه"))
                         return redirect('totals',id=order_id)
                      else:
                        messages.error(request,_("    الكميه اكبر من القيمه المطلوبه"))

                        return redirect('totals',id=order_id)
                  except:
                    messages.error(request,_("  هناك خطْأ ما"))
                    return redirect('totals',id=order_id)
                  
               elif Product.objects.filter(id=order.product.pk,facat=False,boonimg=False):
                  try:
                  
                    jjj = Product.objects.get(pk=order.product.pk)
                    vuu = request.POST.get('s')
                    if order.quantity >= int(vuu):
                        jjj.qu  -= int(order.testing)
                        jjj.save()
                        hdhd = Order.objects.get(id=order_id)
                        ddf = Fintion.objects.filter(order_detils = orderx.pk,fintion=jjj, order_idsid=book_id.pk)
                        if ddf:
                            Fintion.objects.filter(order_detils = orderx.pk,fintion=jjj, order_idsid=book_id.pk).update(usus = int(vuu))
                        else:
                            Fintion.objects.create(
                                fintion=jjj,
                                order_idsid=hdhd,
                                usus = int(vuu),
                                order_detils = orderx.pk,

                             )
                        
                        order.testing = int(order.quantity) -  int(vuu)
                       
                        order.ba = int(order.quantity) - int(order.testing )
                 
                        order.save()
               
                        jjj.qu  += int(order.testing)
                    
                        jjj.save()
                        book_id.user_updete = request.user
                        book_id.save()
                        messages.success(request,_("عملية ناجحه"))
                        return redirect('totals',id=order_id)
                    else:
                        messages.error(request,_("الكميه اكبر من القيمه المطلوبه"))

                        return redirect('totals',id=order_id)
                  except:
                    messages.error(request,_("  هناك خطأ ما"))
                    return redirect('totals',id=order_id)
               elif Product.objects.filter(id=order.product.pk,facat=False,boonimg=True):
                  try:
                    jjj = Product.objects.get(pk=order.product.pk)
                    img = Img.objects.get(i_id=jjj,name=orderx.nameimg)
                    vuu = request.POST.get('s')
                    if order.quantity >= int(vuu):
                        jjj.qu  -= int(order.testing)
                        ddf = Fintion.objects.filter(order_detils = orderx.pk,fintion=jjj, order_idsid=book_id.pk)
                        if ddf:
                            Fintion.objects.filter(order_detils = orderx.pk,fintion=jjj, order_idsid=book_id.pk).update(usus = int(vuu))
                        else:
                            Fintion.objects.create(
                                fintion=jjj,
                                order_idsid=book_id,
                                usus = int(vuu),
                                order_detils = orderx.pk,

                             )
                        
                     
                        jjj.save()
                        s = Img.objects.get(i_id=jjj,name=orderx.nameimg)
                        s.quimg -= int(order.testing)
                      
                        s.save()
                        order.testing = int(order.quantity) -  int(vuu)
                       
                        order.ba = int(order.quantity) - int(order.testing )
                 
                        order.save()
               
               
                        jjj.qu  += int(order.testing)
                    
                        jjj.save()
                        c = Img.objects.get(i_id=jjj,name=orderx.nameimg)
                        c.quimg += int(order.testing)
                     
                     
                        c.save()
                        book_id.user_updete = request.user
                        book_id.save()
                        messages.success(request,_("عملية ناجحه"))
                        return redirect('totals',id=order_id)
                    else:
                        messages.error(request,_("الكميه اكبر من القيمه المطلوبه"))
                        return redirect('totals',id=order_id)
                  except:
                    messages.error(request,_("هناك خطأ ما"))
                    return redirect('totals',id=order_id)
        else:
           
            messages.error(request, _("الطلب لم يتم التاكيد"))
            return render(request,'pages/update.html')
    
    else:
         tr= None
         t= None
         hrr= None

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
             
         book_save = OrderdetelsFromdd(instance=order)
         context ={
              'form':book_save,
               'hrr':hrr,
               'tr':tr,
               't':t,
               'category':Category.objects.all(),
               

         }
         return render(request,'pages/update.html',context)


@ratelimit(key='user_or_ip', rate='20/m')
@allowedusershr(allowGroupshr =["staff"])
@transaction.atomic

@login_required(login_url='signin')
def fanth(request,id):
    if request.method == 'POST':
        statusu = request.POST.get('statusu')

        order = get_object_or_404(Order,pk=id)
        orderDetails = OrderDetails.objects.all().filter(order=order)
        
        d= 0
        for i in orderDetails:
           
            d += i.ba

        # if d == 0:
        #     messages.error(request, _('يجب العمل فى الطلب اولا'))
        #     return redirect('fanth', id=id)
        if statusu == None:
            messages.error(request, _('مربع الحاله فارغ'))
            return redirect('fanth', id=id)
        
        else:
            book_save = BookFrom(request.POST, request.FILES, instance=order)
            if book_save.is_valid():
               book_save.save(),
               messages.success(request, _('عملية ناجحه'))
               return redirect('orderOrder') 
            
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
    order = get_object_or_404(Order,pk=id)
    context = {
        'hrr':hrr,
       'tr':tr,
       't':t,
       'form' : BookFrom(instance=order)
        }
    
    return render(request,'orders/fanth.html',context)
        
# def orderOrder(request):
@ratelimit(key='user_or_ip', rate='100/m')
@allowedusershr(allowGroupshr =["staff","hr"])
@login_required(login_url='signin')
@transaction.atomic

def updatecoun(request,id):
    book_id = Order.objects.get(id=id)
    if request.user.groups.filter(name='hr') :
        if book_id.order_updated is not None:
             if book_id.order_updated <  timezone.now() :
                 messages.error(request, _('  تم انتهاء مدة التعديل '))
                 return redirect('orderOrder',)
           
 
    if request.method == 'POST':
        order = get_object_or_404(Order,pk=id)
        coin = request.POST.get('coin')
        orderDetails = OrderDetails.objects.all().filter(order=order)
        d= 0
        for i in orderDetails:
            d += i.ba
        gf = OrderDetails.objects.filter(order=order).exclude(order__status=Order.Typechoices.a).exclude(order__status=None)
        if not gf :
                  messages.error(request, _("يجب ان تختار حاله"))
                  return redirect('updatecoun', id=id)
        if coin == '':
            messages.error(request, _('مربع الوصول فارغ'))
            return redirect('updatecoun', id=id)
        
        if d == 0:
            messages.error(request, _('يجب العمل فى الطلب اولا'))
            return redirect('updatecoun', id=id)
      
    
        elif not int(coin) >= 0 :
            messages.error(request, _('عملية خطأه'))
            return redirect('updatecoun', id=id)
        
        elif not order.user_group.name == 'castomar' :
            messages.error(request, _(' ليس مسوق'))
            return redirect('updatecoun', id=id)
        elif  order.statusu == 'completed' :
            messages.error(request, _(' الطلب اكتمل ولا يمكن التعديل عليه '))
            return redirect('updatecoun', id=id)
        else:
           l = 0
           order = get_object_or_404(Order,pk=id)

           orderDetails = OrderDetails.objects.all().filter(order=order)
           y = 0
           d= 0
           for i in orderDetails:
               y += i.ba * i.product.qus
               d += i.ba

           if d == 0:
               messages.error(request, _(' العمل فى الطلب اولا'))
               return redirect('updatecoun', id=id)

           elif  int(y) >= int(coin):
                order.coin = coin
                order.save()
                messages.success(request, _('عملية ناجحه'))
                return redirect('orderOrder') 
           else:
               messages.error(request,_( 'الكمية الواصله اكبر من قيمة المسوق'))
               return redirect('updatecoun', id=id)
               
    if request.user.groups.filter(name='adminCastomar'):
        tr = True
        t = True
    else:
        tr = False
        t = False

    if request.user.groups.filter(name='hr')  or request.user.groups.filter(name='staff'):
        hrr = True
   
    else:
        hrr = False
    order = get_object_or_404(Order,pk=id)
    i = 0
    tj = OrderDetails.objects.filter(order=order)
    for x in tj:
            i += x.ba * x.product.qus
    print(i)
    context = {
        'hrr':hrr,
       'tr':tr,
       't':t,
       'tj':i
        }
    return render(request,'orders/coun.html',context)
import csv
import xlsxwriter
from django.http import HttpResponse
from tablib import Dataset

@ratelimit(key='user_or_ip', rate='10/m')
@allowedusershr(allowGroupshr =["hr","staff"])
@login_required(login_url='signin')
def Ordercsv(request):
    response = HttpResponse(content_type='text/xlsx')
    # response['Content-Disposition'] = "attachment; filename=v.xlsx" 
    response['Content-Disposition'] = "attachment; filename=speedfuthur.csv" 

    writer = csv.writer(response)
    writer.writerow(['id_order','OrderDetails_id','تاريخ الطلب','بوسطه','شركات الشحن','حالة الطلب','حالة عمل الطلب','انتهاء الطلب','العموله','السعر','الكميه','المقاس','الون','اسم الون','اسم المنتج','الكميه الحاليه','اسعر البيع للمنتج','سعرالحقيقى',])
    
    # quantity_d = None
    order = Order.objects.all().annotate(
        ffff = Sum(F('orderss__price') *  F('orderss__quantity')),
        ffffd = Sum(F('orderss__ba') *  F('details__qus')),
        ba = Sum(F('orderss__ba')),
        pks = Sum(F('orderss__pk')),
        a = F('is_finished'),
        s = F('posta'),
        ffr = F('status')
    )
  
    for i in order:
        print(int(i.ffff))
        writer.writerow([i.pk ,i.ffff,i.pks ,i.order_date,i.posta,i.is_Orderpartener,i.status ,i.statusu,i.is_finished,i.ba,])
    return response

import datetime
from django.db.models import Sum,F,Count
from django.db.models import Sum, IntegerField
from django.db.models.functions import Cast


@ratelimit(key='user_or_ip', rate='100/m')
@allowedusershr(allowGroupshr =["hr","staff"])
@login_required(login_url='signin')
@transaction.atomic

def order__now(request):
    r = Order.objects.all().filter(status=Order.Typechoices.a)
    ordersds = Order.objects.all()
    m=0
    ns = Ma.objects.all()
    for x in ns:
        m += int(x.qu)
    mtds = Ma.objects.all()
    nasaref = 0
    for ibv in mtds:
        nasaref += int(ibv.qu)
    orser = Order.objects.all().filter(status=Order.Typechoices.a).annotate(
        ffff = Sum(F('orderss__price') *  F('orderss__quantity')),
        ffffd = Sum(F('orderss__ba') *  F('details__qus')),
        ba = Sum(F('orderss__ba')),
        a = F('is_finished'),
        s = F('posta'),
        ffr = F('status')
    )
    print(orser)

    form = puserFromss(request.POST or None)
  
    context ={
         "form":form,
         "orser":orser,
       
       
       "jm" : Order.objects.filter(status=Order.Typechoices.b),
       'ma':m,
    'nasaref':nasaref
         
         }
    
    if request.method =="POST":
          try:
               fc = Order.objects.filter(user_group__name='admin')
               events = Order.objects.all().filter(status=Order.Typechoices.a).annotate(
        ffff = Sum(F('orderss__price') *  F('orderss__quantity')),
        ffffd = Sum(F('orderss__ba') *  F('details__qus')),
        ba = Sum(F('orderss__ba')),

        a = F('is_finished'),
        s = F('posta'),
        ffr = F('status')
    )
         
               user_updete =request.POST.get('user_updete')
               users =request.POST.get('user')
               groups =request.POST.get('groups')
               idgroups =request.POST.get('idgroups')
               status =request.POST.get('status')
               statusu =request.POST.get('statusu')
               start_data =request.POST.get('start_data')
               end_data =request.POST.get('end_data')
               phonenapber =request.POST.get('phonenapber')
               status_pay =request.POST.get('status_pay')

               mtds = Ma.objects.all()
               if status_pay:
                   events = events.filter(status_pay__icontains = status_pay)
               if statusu:
                   events = events.filter(statusu__icontains = statusu)
               if phonenapber:
                   events = events.filter(Payments__shipment_phone__icontains = phonenapber)
               if idgroups:
                   events = events.filter(id__icontains = idgroups)
               if users:
                   events = events.filter(user__username__icontains = users)
               if user_updete:
                   events = events.filter(user_updete__username__icontains = user_updete)
               if status:
                   events = events.filter(status__icontains = status)
               if groups:
                   events = events.filter(user_group__name__icontains  = groups)
               if start_data and end_data:
                   events = events.filter(order_date__range = (start_data, end_data ))
                   mtds = mtds.filter(publish_date__range = (start_data, end_data ))
                   
               elif start_data:
                   events = events.filter(order_date__gte = start_data)
                   mtds = mtds.filter(publish_date__gte = start_data)

               elif end_data:
                   events = events.filter(order_date__lte = end_data)
                   mtds = mtds.filter(publish_date__gte = start_data)

               nasaref = 0
               for ibv in mtds:
                   nasaref += int(ibv.qu)
               context ={
                   'orser':events,
                   "form":form,
                   'category':Category.objects.all(),
                   "jm" : Order.objects.filter(status=Order.Typechoices.b),
                   'ma':m,
                   'nasaref':nasaref
               } 
               messages.success(request, _('عملية بحث ناجحه'))
               return render(request, 'reqqer/order__now.html', context) 
          
          except:
                messages.error(request, _('عملية بحث فاشله '))
                orserd = Order.objects.all().filter(status=Order.Typechoices.a).annotate(
        ffff = Sum(F('orderss__price') *  F('orderss__quantity')),
        ffffd = Sum(F('orderss__ba') *  F('details__qus')),
        ba = Sum(F('orderss__ba')),

        a = F('is_finished'),
        s = F('posta'),
        ffr = F('status')
    )
                context ={
                 "form":form,
                   'orser':orserd,
                   'category':Category.objects.all(),
                   "jm" : Order.objects.filter(status=Order.Typechoices.b),
                   'ma':m,
                   'nasaref':nasaref
               } 
                return render(request, 'reqqer/order__now.html', context) 
    else:
       
        context ={
         "form":form,
          "orser":orser,
       
       'category':Category.objects.all(),
       "jm" : Order.objects.filter(status=Order.Typechoices.b),
       'ma':m,
       'nasaref':nasaref
         } 
        return render(request,'reqqer/order__now.html',context)
   
          





@ratelimit(key='user_or_ip', rate='100/m')
@allowedusershr(allowGroupshr =["hr","staff"])
@login_required(login_url='signin')
@transaction.atomic

def orderOrdertoday(request):
    r = Order.objects.all().filter(order_date= datetime.date.today()  )
    print(r)

    ordersds = Order.objects.all()
    m=0
    ns = Ma.objects.all()
    for x in ns:
        m += int(x.qu)
    mtds = Ma.objects.all()
    nasaref = 0
    for ibv in mtds:
        nasaref += int(ibv.qu)
    orser = Order.objects.all().filter(order_date= datetime.date.today()  ).annotate(
        ffff = Sum(F('orderss__price') *  F('orderss__quantity')),
        ffffd = Sum(F('orderss__ba') *  F('details__qus')),
        ba = Sum(F('orderss__ba')),

        a = F('is_finished'),
        s = F('posta'),
        ffr = F('status')
    )

    form = puserFromss(request.POST or None)
  
    context ={
         "form":form,
         "orser":orser,
       
       
       "jm" : Order.objects.filter(status=Order.Typechoices.b),
       'ma':m,
       'nasaref':nasaref
    
         
         }
    
    if request.method =="POST":
          try:
               fc = Order.objects.filter(user_group__name='admin')
               events = Order.objects.all().filter(order_date= datetime.date.today()  ).annotate(
        ffff = Sum(F('orderss__price') *  F('orderss__quantity')),
        ffffd = Sum(F('orderss__ba') *  F('details__qus')),
        ba = Sum(F('orderss__ba')),

        a = F('is_finished'),
        s = F('posta'),
        ffr = F('status')
    )
         
               user_updete =request.POST.get('user_updete')
               users =request.POST.get('user')
               groups =request.POST.get('groups')
               idgroups =request.POST.get('idgroups')
               status =request.POST.get('status')
               statusu =request.POST.get('statusu')
               start_data =request.POST.get('start_data')
               end_data =request.POST.get('end_data')
               phonenapber =request.POST.get('phonenapber')
               status_pay =request.POST.get('status_pay')

               mtds = Ma.objects.all()
               if status_pay:
                   events = events.filter(status_pay__icontains = status_pay)
               if statusu:
                   events = events.filter(statusu__icontains = statusu)
               if phonenapber:
                   events = events.filter(Payments__shipment_phone__icontains = phonenapber)
               if idgroups:
                   events = events.filter(id__icontains = idgroups)
               if users:
                   events = events.filter(user__username__icontains = users)
               if user_updete:
                   events = events.filter(user_updete__username__icontains = user_updete)
               if status:
                   events = events.filter(status__icontains = status)
               if groups:
                   events = events.filter(user_group__name__icontains  = groups)
               if start_data and end_data:
                   events = events.filter(order_date__range = (start_data, end_data ))
                   mtds = mtds.filter(publish_date__range = (start_data, end_data ))
                   
               elif start_data:
                   events = events.filter(order_date__gte = start_data)
                   mtds = mtds.filter(publish_date__gte = start_data)

               elif end_data:
                   events = events.filter(order_date__lte = end_data)
                   mtds = mtds.filter(publish_date__gte = start_data)

               nasaref = 0
               for ibv in mtds:
                   nasaref += int(ibv.qu)
               

               context ={
                   'orser':events,
                   "form":form,
                   'category':Category.objects.all(),
                   "jm" : Order.objects.filter(status=Order.Typechoices.b),
                   'ma':m,
                   'nasaref':nasaref
               } 
               messages.success(request, _('عملية بحث ناجحه'))
               return render(request, 'reqqer/ordercompleted.html', context) 
          
          except:
                messages.error(request, _('عملية بحث فاشله '))
                orserd = Order.objects.all().filter(order_date= datetime.date.today()  ).annotate(
        ffff = Sum(F('orderss__price') *  F('orderss__quantity')),
        ffffd = Sum(F('orderss__ba') *  F('details__qus')),
        ba = Sum(F('orderss__ba')),

        a = F('is_finished'),
        s = F('posta'),
        ffr = F('status')
    )
                context ={
                 "form":form,
                   'orser':orserd,
                   'category':Category.objects.all(),
                   "jm" : Order.objects.filter(status=Order.Typechoices.b),
                   'ma':m,
                   'nasaref':nasaref
               } 
                return render(request, 'reqqer/ordercompleted.html', context) 
    else:
       
        context ={
         "form":form,
          "orser":orser,
       
       'category':Category.objects.all(),
       "jm" : Order.objects.filter(status=Order.Typechoices.b),
       'ma':m,
       'nasaref':nasaref
         } 
        return render(request,'reqqer/ordertoday.html',context)
   
          


from django.db.models import Sum,F,Count
@ratelimit(key='user_or_ip', rate='100/m')
@allowedusershr(allowGroupshr =["hr","staff"])
@login_required(login_url='signin')
@transaction.atomic

def orderOrdercolected(request):
    ordersds = Order.objects.all()
    m = 0
    ns = Ma.objects.all()
    for x in ns:
        m += int(x.qu)

    mtds = Ma.objects.all()
    nasaref = 0
    for ibv in mtds:
        nasaref += int(ibv.qu)
    orser = Order.objects.all().annotate(
        ffff = Sum(F('orderss__price') *  F('orderss__quantity')),
        ffffd = Sum(F('orderss__ba') *  F('details__qus')),
        ba = Sum(F('orderss__ba')),
        # coppings = Sum(F('orderss__copping')),
        a = F('is_finished'),
        s = F('posta'),
        ffr = F('status')
    )

    form = puserFromss(request.POST or None)
  
    context ={
         "form":form,
         "orser":orser,
       
       'category':Category.objects.all(),
       "jm" : Order.objects.filter(status=Order.Typechoices.b),
       'ma':m
    #    'a':a
         
         }
    
    if request.method =="POST":
          try:
               fc = Order.objects.filter(user_group__name='admin')
               events = Order.objects.all().annotate(
        ffff = Sum(F('orderss__price') *  F('orderss__quantity')),
        ffffd = Sum(F('orderss__ba') *  F('details__qus')),
        ba = Sum(F('orderss__ba')),
        # coppings = Sum(F('orderss__copping')),
        a = F('is_finished'),
        s = F('posta'),
        ffr = F('status')
    )
         

               users =request.POST.get('user')
               user_updete =request.POST.get('user_updete')

               groups =request.POST.get('groups')
               idgroups =request.POST.get('idgroups')
               status =request.POST.get('status')
               statusu =request.POST.get('statusu')
               start_data =request.POST.get('start_data')
               end_data =request.POST.get('end_data')
               phonenapber =request.POST.get('phonenapber')
               status_pay =request.POST.get('status_pay')

               mtds = Ma.objects.all()
               if status_pay:
                   events = events.filter(status_pay__icontains = status_pay)
               if statusu:
                   events = events.filter(statusu__icontains = statusu)
               if phonenapber:
                   events = events.filter(Payments__shipment_phone__icontains = phonenapber)
               if idgroups:
                   events = events.filter(id__icontains = idgroups)
               if users:
                   events = events.filter(user__username__icontains = users)
               if user_updete:
                   events = events.filter(user_updete__username__icontains = user_updete)
               if status:
                   events = events.filter(status__icontains = status)
               if groups:
                   events = events.filter(user_group__name__icontains  = groups)
               if start_data and end_data:
                   events = events.filter(order_date__range = (start_data, end_data ))
                   mtds = mtds.filter(publish_date__range = (start_data, end_data ))
                   
               elif start_data:
                   events = events.filter(order_date__gte = start_data)
                   mtds = mtds.filter(publish_date__gte = start_data)

               elif end_data:
                   events = events.filter(order_date__lte = end_data)
                   mtds = mtds.filter(publish_date__gte = start_data)

               nasaref = 0
               for ibv in mtds:
                   nasaref += int(ibv.qu)
               

               context ={
                   'orser':events,
                   "form":form,
                   'category':Category.objects.all(),
                   "jm" : Order.objects.filter(status=Order.Typechoices.b),
                   'ma':m,
                   'nasaref':nasaref
               } 
               messages.success(request, _('عملية بحث ناجحه'))
               return render(request, 'reqqer/ordercompleted.html', context) 
          
          except:
                messages.error(request, _('عملية بحث فاشله '))
                orserd = Order.objects.all().annotate(
        ffff = Sum(F('orderss__price') *  F('orderss__quantity')),
        ffffd = Sum(F('orderss__ba') *  F('details__qus')),
        ba = Sum(F('orderss__ba')),
        # coppings = Sum(F('orderss__copping')),
        a = F('is_finished'),
        s = F('posta'),
        ffr = F('status')
    )
                context ={
                 "form":form,
                   'orser':orserd,
                   'category':Category.objects.all(),
                   "jm" : Order.objects.filter(status=Order.Typechoices.b),
                   'ma':m,
                   'nasaref':nasaref

               } 
                return render(request, 'reqqer/ordercompleted.html', context) 
    else:
       
        context ={
         "form":form,
          "orser":orser,
       
         'category':Category.objects.all(),
        "jm" : Order.objects.filter(status=Order.Typechoices.b),
         'ma':m,
         'nasaref':nasaref
         } 
        return render(request,'reqqer/ordercompleted.html',context)


@ratelimit(key='user_or_ip', rate='100/m')
@allowedusershr(allowGroupshr =["hr","staff"])
@login_required(login_url='signin')
def orderOrdercompleted(request):
    ordersds = Order.objects.all()
    m=0
    ns = Ma.objects.all()
    for x in ns:
        m += int(x.qu)
    mtds = Ma.objects.all()
    nasaref = 0
    for ibv in mtds:
        nasaref += int(ibv.qu)

    orser = Order.objects.all().filter(statusu='completed').annotate(
        ffff = Sum(F('orderss__price') *  F('orderss__quantity')),
        ffffd = Sum(F('orderss__ba') *  F('details__qus')),
        ba = Sum(F('orderss__ba')),
        # coppings = Sum(F('orderss__copping')),
        a = F('is_finished'),
        s = F('posta'),
        ffr = F('status')
    )

    form = puserFromss(request.POST or None)
  
    context ={
         "form":form,
         "orser":orser,
       
       'category':Category.objects.all(),
       "jm" : Order.objects.filter(status=Order.Typechoices.b),
       'ma':m,
       'nasaref':nasaref
         
         }
    
    if request.method =="POST":
          try:
               fc = Order.objects.filter(user_group__name='admin')
               events = Order.objects.all().filter(statusu='completed').annotate(
        ffff = Sum(F('orderss__price') *  F('orderss__quantity')),
        ffffd = Sum(F('orderss__ba') *  F('details__qus')),
        ba = Sum(F('orderss__ba')),
        # coppings = Sum(F('orderss__copping')),
        a = F('is_finished'),
        s = F('posta'),
        ffr = F('status')
    )
         

               users =request.POST.get('user')
               groups =request.POST.get('groups')
               idgroups =request.POST.get('idgroups')
               status =request.POST.get('status')
               statusu =request.POST.get('statusu')
               start_data =request.POST.get('start_data')
               end_data =request.POST.get('end_data')
               phonenapber =request.POST.get('phonenapber')
               user_updete =request.POST.get('user_updete')
               status_pay =request.POST.get('status_pay')

               mtds = Ma.objects.all()
               if status_pay:
                   events = events.filter(status_pay__icontains = status_pay)
               if statusu:
                   events = events.filter(statusu__icontains = statusu)
               if phonenapber:
                   events = events.filter(Payments__shipment_phone__icontains = phonenapber)
               if idgroups:
                   events = events.filter(id__icontains = idgroups)
               if users:
                   events = events.filter(user__username__icontains = users)
               if user_updete:
                   events = events.filter(user_updete__username__icontains = user_updete)
               if status:
                   events = events.filter(status__icontains = status)
               if groups:
                   events = events.filter(user_group__name__icontains  = groups)
               if start_data and end_data:
                   events = events.filter(order_date__range = (start_data, end_data ))
                   mtds = mtds.filter(publish_date__range = (start_data, end_data ))
                   
               elif start_data:
                   events = events.filter(order_date__gte = start_data)
                   mtds = mtds.filter(publish_date__gte = start_data)

               elif end_data:
                   events = events.filter(order_date__lte = end_data)
                   mtds = mtds.filter(publish_date__gte = start_data)

               nasaref = 0
               for ibv in mtds:
                   nasaref += int(ibv.qu)

              
               context ={
                   'orser':events,
                   "form":form,
                   'category':Category.objects.all(),
                   "jm" : Order.objects.filter(status=Order.Typechoices.b),
                   'ma':m,
                   'nasaref':nasaref
               } 
               messages.success(request, _('عملية بحث ناجحه'))
               return render(request, 'reqqer/ordercompleted.html', context) 
          
          except:
                messages.error(request, _('عملية بحث فاشله '))
                orserd = Order.objects.all().filter(statusu='completed').annotate(
        ffff = Sum(F('orderss__price') *  F('orderss__quantity')),
        ffffd = Sum(F('orderss__ba') *  F('details__qus')),
        ba = Sum(F('orderss__ba')),
        # coppings = Sum(F('orderss__copping')),
        a = F('is_finished'),
        s = F('posta'),
        ffr = F('status')
    )
                context ={
                 "form":form,
                   'orser':orserd,
                   'category':Category.objects.all(),
                   "jm" : Order.objects.filter(status=Order.Typechoices.b),
                   'ma':m,
                   'nasaref':nasaref
               } 
                return render(request, 'reqqer/ordercompleted.html', context) 
    else:
       
        context ={
         "form":form,
          "orser":orser,
          'nasaref':nasaref,
       
       'category':Category.objects.all(),
       "jm" : Order.objects.filter(status=Order.Typechoices.b),
       'ma':m
         } 
        return render(request,'reqqer/ordercompleted.html',context)



@ratelimit(key='user_or_ip', rate='100/m')
@allowedusershr(allowGroupshr =["hr","staff"])
@login_required(login_url='signin')
def orderOrder(request):
    context = None
    ordersds = Order.objects.all()
    m = 0
    ns = Ma.objects.all()
    for x in ns:
        m += int(x.qu)
    mtds = Ma.objects.all()
    nasaref = 0
    for ibv in mtds:
        nasaref += int(ibv.qu)
   
    
    orser = Order.objects.all().exclude(statusu='completed').annotate(
        a = F('is_finished'),
        s = F('posta'),
        ffr = F('status'),
        ffff = Sum(F('orderss__price') *  F('orderss__quantity')),
        ffffd = Sum(F('orderss__ba') *  F('details__qus')),
        tatalsds__quantitys = Sum(F('details__qus') *  F('orderss__quantity')),
        ba = Sum(F('orderss__ba')),
    )
    
    
    form = puserFromss(request.POST or None)
  
    context ={
         "form":form,
         "orser":orser,
       
        'category':Category.objects.all(),
        "jm" : Order.objects.filter(status=Order.Typechoices.b),
        'ma':m
    #    'a':a
         
         }
    
    if request.method =="POST":
          try:
               fc = Order.objects.filter(user_group__name='admin')
               events = Order.objects.all().exclude(statusu='completed').annotate(
                    ffff = Sum(F('orderss__price') *  F('orderss__quantity')),
        ffffd = Sum(F('orderss__ba') *  F('details__qus')),
        ba = Sum(F('orderss__ba')),
        # tatalsds__quantitys = Sum(F('details__qus') *  F('orderss__quantity')),
        a = F('is_finished'),
        s = F('posta'),
        ffr = F('status')
    )
 
               users =request.POST.get('user')
               groups =request.POST.get('groups')
               idgroups =request.POST.get('idgroups')
               status =request.POST.get('status')
               statusu =request.POST.get('statusu')
               start_data =request.POST.get('start_data')
               end_data =request.POST.get('end_data')
               phonenapber =request.POST.get('phonenapber')
               user_updete =request.POST.get('user_updete')
               status_pay =request.POST.get('status_pay')

               mtds = Ma.objects.all()
               if status_pay:
                   events = events.filter(status_pay__icontains = status_pay)
               if statusu:
                   events = events.filter(statusu__icontains = statusu)
               if phonenapber:
                   events = events.filter(Payments__shipment_phone__icontains = phonenapber)
               if idgroups:
                   events = events.filter(id__icontains = idgroups)
               if users:
                   events = events.filter(user__username__icontains = users)
               if user_updete:
                   events = events.filter(user_updete__username__icontains = user_updete)
               if status:
                   events = events.filter(status__icontains = status)
               if groups:
                   events = events.filter(user_group__name__icontains  = groups)
               if start_data and end_data:
                   events = events.filter(order_date__range = (start_data, end_data ))
                   mtds = mtds.filter(publish_date__range = (start_data, end_data ))
                   
               elif start_data:
                   events = events.filter(order_date__gte = start_data)
                   mtds = mtds.filter(publish_date__gte = start_data)

               elif end_data:
                   events = events.filter(order_date__lte = end_data)
                   mtds = mtds.filter(publish_date__gte = start_data)

               nasaref = 0
               for ibv in mtds:
                   nasaref += int(ibv.qu)
               context ={
                   'orser':events,
                   "form":form,
                   'category':Category.objects.all(),
                   "jm" : Order.objects.filter(status=Order.Typechoices.b),
               'ma':m,
               'nasaref':nasaref
               } 
               messages.success(request, _('عملية بحث ناجحه'))
               return render(request, 'reqqer/orderOrder.html', context) 
          
          except:
                messages.error(request, _('عملية بحث فاشله '))
                orserd = Order.objects.all().exclude(statusu='completed').annotate(
        ffff = Sum(F('orderss__price') *  F('orderss__quantity')),
        ffffd = Sum(F('orderss__ba') *  F('details__qus')),
        ba = Sum(F('orderss__ba')),
        tatalsds__quantitys = Sum(F('details__qus') *  F('orderss__quantity')),
        a = F('is_finished'),
        s = F('posta'),
        ffr = F('status')
    )
                context ={
                 "form":form,
                   'orser':orserd,
                   'category':Category.objects.all(),
                   "jm" : Order.objects.filter(status=Order.Typechoices.b),
               'ma':m,
               'nasaref':nasaref
               } 
                return render(request, 'reqqer/orderOrder.html', context) 
    else:
      
        context ={
          "form":form,
          "orser":orser,
          'category':Category.objects.all(),
          "jm" : Order.objects.filter(status=Order.Typechoices.b),
   'ma':m,
   'nasaref':nasaref
         } 
        return render(request,'reqqer/orderOrder.html',context)



 
@ratelimit(key='user_or_ip', rate='100/m')
@allowedusershr(allowGroupshr =["staff",'hr'])
@login_required(login_url='signin')
def updateorder(request ,id):
     book_id = Order.objects.get(id=id)
     if request.user.groups.filter(name='hr') :
        if book_id.order_updated is not None:
             if book_id.order_updated <  timezone.now() :
                 messages.error(request, _('  تم انتهاء مدة التعديل '))
                 return redirect('orderOrder') 

     if request.method =='POST':
        if   book_id.user_updete == None :
            if  book_id.is_finished == True:
                 book_save = OrderFrom(request.POST, request.FILES, instance=book_id)
                 if  book_id.statusu == 'completed' :
                     messages.error(request, _(' الطلب اكتمل ولا يمكن التعديل عليه '))
                     return redirect('orderOrder') 
                 elif  request.POST['status']== '' :
                     messages.error(request, _(' مربع الحاله فارغ '))
                     return redirect('orderOrder') 
                 elif  request.POST['status']== 'اوردر جديد' :
                     messages.error(request, _(' يجب ان تختار حالة شحن غير اوردر جديد'))
                     return redirect('orderOrder') 
     
                 
                 elif book_save.is_valid():
                      book_save.save(),
                      book_id.user_updete = request.user
                      book_id.save()
                 return redirect('orderOrder') 
            else:
                messages.error(request, "الاردر لم يتم التاكيد")
                return redirect('orderOrder') 
        else:
            if  book_id.is_finished == True:
                 book_save = OrderFrom(request.POST, request.FILES, instance=book_id)
                 if  book_id.statusu == 'completed' :
                     messages.error(request, _(' الطلب اكتمل ولا يمكن التعديل عليه '))
                     return redirect('orderOrder') 
                 elif  request.POST['status']== '' :
                     messages.error(request, _(' مربع الحاله فارغ '))
                     return redirect('orderOrder') 
                 elif  request.POST['status']== 'اوردر جديد' :
                     messages.error(request, _(' يجب ان تختار حالة شحن غير اوردر جديد'))
                     return redirect('orderOrder') 
     
                 
                 elif book_save.is_valid():
                      book_save.save(),
                      book_id.user_updete = request.user
                      book_id.order_updated = timezone.now()  + timezone.timedelta(minutes=3*60)
                      book_id.save()
                      messages.success(request, _(' تم اختيار حالة '))

                 return redirect('orderOrder') 
            else:
                messages.error(request, "الاردر لم يتم التاكيد")
                return redirect('orderOrder') 
          
     else:
         book_save = OrderFrom(instance=book_id)
       
         context ={
              'form':book_save,
           
       'category':Category.objects.all(),

         }
     return render(request,'pages/update.html',context)
@ratelimit(key='user_or_ip', rate='10/m')
@allowedusershr(allowGroupshr =["staff"])
@login_required(login_url='signin')
def deleteorder(request, id):
     book_delete =get_object_or_404(Order, id=id)
     order = Order.objects.filter(id=id).filter(status=Order.Typechoices.sold)
     if order:
        if request.method =='POST':
           if book_delete.is_finished == True:
               book_delete.delete()
               return redirect('orderOrder') 
           else:
            messages.error(request,_("لم يتم تاكيدالطلب"))
            return render(request,'pages/delete.html')
           
     else:
         messages.error(request, 'error in soll')
         return redirect('orderOrder') 
     if request.user.groups.filter(name='adminCastomar'):
        tr = True
        t = True
     else:
         tr = False
         t = False
 
     if request.user.groups.filter(name='hr') or request.user.groups.filter(name='staff'):
         hrr = True
    
     else:
         hrr = False
     return render(request,'pages/delete.html',{ 'hrr':hrr,
       'tr':tr,
       't':t,
       'category':Category.objects.all(),
       })

@ratelimit(key='user_or_ip', rate='10/m')
@allowedUsers(allowedGroups=['adminCastomar','groadmin'])
@login_required(login_url='signin')
def orderOrderDetails(request,id):
   
    orderdetails = OrderDetails.objects.all()
         
    if request.method =="POST":
        
               f = OrderDetails.objects.all()
               price= request.POST.get('price')
               quantity = request.POST.get('quantity')

               quset = f.filter(
                   
                     price__icontains= price,
                    
                     )


    else:
        quset =  OrderDetails.objects.all()

    context = {
        'all_orders':quset,
      'category':Category.objects.all(),
        
        }


    return render(request,'reqqer/OrderDetails.html',context)

@ratelimit(key='user_or_ip', rate='10/m')
@allowedUsers(allowedGroups=['adminCastomar','groadmin'])
@login_required(login_url='signin')
def orderOrderUser(request,user_id,):
   
    context = None
    all_orders = None
    orderdetails = None
    if  request.user.is_authenticated and not request.user.is_anonymous:
        all_orders = Order.objects.all().filter(user=user_id)
        if all_orders:
            for x in all_orders:
               order = Order.objects.get(id=x.id)
               orderdetails = OrderDetails.objects.all().filter(order=order)
               total = 0
               for  sub in orderdetails:
                  total += sub.price * sub.quantity
               x.totle = total
               x.items_count= orderdetails.count
       
              
    if request.user.groups.filter(name='adminCastomar'):
        tr = True
        t = True
    else:
        tr = False
        t = False

    if request.user.groups.filter(name='hr') or request.user.groups.filter(name='staff'):
        hrr = True
   
    else:
        hrr = False
    context = {
        'all_orders':all_orders,
         'hrr':hrr,
       'tr':tr,
       't':t,
       'category':Category.objects.all(),
        }

    
    return render(request, 'orders/show_orders_user.html',context )
@ratelimit(key='user_or_ip', rate='10/m')
@allowedUsers(allowedGroups=['adminCastomar','groadmin'])
@login_required(login_url='signin')
def orderOrderDetails(request,user_id,order_id):
   
    order = get_object_or_404(Order,user__pk=user_id,pk=order_id)
    quset = OrderDetails.objects.all().filter(order=order)
    
    if request.user.groups.filter(name='adminCastomar'):
        tr = True
        t = True
    else:
        tr = False
        t = False

    if request.user.groups.filter(name='hr') or request.user.groups.filter(name='staff'):
        hrr = True
   
    else:
        hrr = False
    context = {
        'all_orders':quset,
         'hrr':hrr,
       'tr':tr,
       't':t,
       'category':Category.objects.all(),
       }

    return render(request,'reqqer/OrderDetails.html',context)


import random
import http.client
from django.conf import settings

@ratelimit(key='user_or_ip', rate='10/m')
@allowedUsers(allowedGroups=['adminCastomar'])
def send_otp(mobile,otp):
    conn = http.client.HTTPSConnection("api.msg91.com")
    # authkey = settings.authkey
    headers ={'content-type': "application/json"}
    url = 'https://control.msg91.com/api/v5/otp?mobile='+mobile
    url = "http://control.msg91.com/api/v5/otp="+otp+'&sender=ABC&message='+'Your otp is'+otp+'&mobile='+mobile+'&counytry=91'
    conn.request("GET",url,headers=headers)
    res = conn.getresponse()
    data = res.read()
    return None  

@ratelimit(key='user_or_ip', rate='10/m')
def register(request):
    if request.method == 'POST':   
        email = request.POST.get("email")
        name = request.POST.get("name")
        mobile = request.POST.get("mobile")
        check_user = User.objects.filter(email=email).first()
        check_profile = Profile.objects.filter(mobile=mobile).first()
        if check_user or  check_profile:
           messages.error(request, 'email exets')
           return render(request,"register.html") 
        user = User(email=email,username=name)
        user.save()
       
        otp = str(random.randint(1000,9999))
        profile = Profile(user=user,mobile=mobile,otp=otp) 
        profile.save() 
        send_otp(mobile,otp)  
        request.session['mobile'] = mobile
        messages.success(request, 'email exets')
        return redirect('otp') 
    return render(request,"register.html") 
@ratelimit(key='user_or_ip', rate='10/m')
def otp(request):
       mobile = request.session['mobile']
       context = {'mobile':mobile}
       if request.method == 'POST':   
           otp = request.POST.get("otp")
           profile = Profile.objects.filter(mobile=mobile).first()
           if otp == profile.otp:
              return redirect('')
           else:
               return redirect('register') 
                
               
               
        
       return render(request,"otp.html",context) 


       



# def ressend_otp(request):
#     if request.method == 'POST':  
#         form = EmailPostForm(request.POST)
#         if form.is_valid():
            
#             # user_email = request.POST["otp_email"]
#             user_email = form.cleaned_data.get('tos')
#             if  User.objects.filter(email=user_email).exists():
#                  user = User.objects.get(email=user_email)
#                  otp = OtpToken.objects.create(user=user,opt_expires_at=timezone.now()+timezone.timedelta(minutes=5))
#                  message = "Email verification"
#                  cd = form.cleaned_data 
#             # messages ='lkjkljlkj'
#             #  f"""
#             # # Hi{user.username},here is your opp{otp.osp_code}
#             # # http://127.0.01:8000/verify-email/{user.username}
#             # # """
            
#                  sender = 'abdozxcvbnmapi@gmail.com'
#                 #  send_sms()
#                 #  print(otp.osp_code)
     
                 
#                  send_mail(message,sender,'abdoapiss@gmail.com',recipient_list=message)
      
#                  return redirect("verify_email",username=request.POST['username'])
#         else:
#              messages.warning(request, 'Accomnt email is_active')
#              return redirect("signupp",) 

#     else:
#           form = EmailPostForm()  

#     context ={
#         'form':form,
#     } 
#     return render(request,"resend_otp.html",context)  


from django.contrib.auth.forms import AuthenticationForm
@ratelimit(key='user_or_ip', rate='10/m')
def auth_view(request):
    form = AuthenticationForm
    if request.method =='POST' :
       
       username = request.POST['username']
       password = request.POST['password']
      
       user =auth.authenticate(username=username ,password=password)
 

       if user is not None:
        #    auth.login(request, user)
           request.seccion['pk'] = user.pk

     
           messages.success(request, 'you are now logged in')
    
           return redirect('verify-view')
        
       else:
            messages.error(request, 'username')

            return redirect('auth_view')
    else:
           
   
       return render(request, 'accounts/auth.html',{'from':form})
from .forms import Codeform   
@ratelimit(key='user_or_ip', rate='10/m')
def verify_view(request):
    form = Codeform(request.POST or None)
    if request.method =='POST' :
           pk = request.seccion.get('pk') 
           if pk:
               user = User.objects.get(pk=pk)
               code = user.code
               code_user = f"{user.username}:{user.code}"

               if not request.POST:
                   pass
               if form.is_valid():
                    num = form.cleaned_data.get('number')
                    if str(code) == num:
                       auth.login(request, user)
               

     
                       messages.success(request, _('you are now logged in'))
    
                       return redirect('verify-view')
        
                    else:
                       messages.error(request, 'username')

                       return redirect('auth_view')
  
           
   
    return render(request, 'verify.html',{'from':form})

@allowedUsers(allowedGroups=['groadmin'])

@login_required(login_url='signin')
@ratelimit(key='user_or_ip', rate='50/m')
def postvido(request):

    if request.method == 'POST':
        book_save = Videoform(request.POST, request.FILES )
        if book_save.is_valid():
            book_save.save()
            return redirect('index')

    else:
            book_save =Videoform()
    context ={
            'form':book_save,
        }
    return render(request, 'pages/update.html',context)

@aminnUsers(adminGroups=['groadmin'])

@login_required(login_url='signin')
@ratelimit(key='user_or_ip', rate='50/m')
def updateviev(request, id):
    book_id = Video.objects.get(id=id)


    if request.method == 'POST':
        book_save = Videoform(request.POST, request.FILES ,instance=book_id)
        if book_save.is_valid():
            book_save.save()
            return redirect('Videoss')

    else:
            book_save =Videoform(instance=book_id)
    context ={
            'form':book_save,
        }
    return render(request, 'pages/update.html',context)


@aminnUsers(adminGroups=['groadmin'])
@login_required(login_url='signin')
@ratelimit(key='user_or_ip', rate='50/m')
def deletevideo(request,id):
     pro_delete =get_object_or_404(Video, id=id)
     if request.method == 'POST':
          pro_delete.delete()
          return redirect('Videoss')

     else:
         return render(request,'pages/delete.html')
     
@aminnUsers(adminGroups=['groadmin'])

@login_required(login_url='signin')
@ratelimit(key='user_or_ip', rate='50/m')
def Videoss(request):
    pro_delete = Video.objects.all()

    if request.method =="POST":
     
                try: 
                    username = request.POST.get('username')
                    lg =request.POST.get('lg')
                    ls =request.POST.get('ls') 
                    pro_delete = pro_delete.filter(
                    tp_created_at__range = [
                           lg,
                            ls,

                     ],

                     captaion__icontains = username,
                    )
                    messages.success(request,_('عملية ناجه'))
                    return render(request,'Videoss.html',{'pro_delete':pro_delete})
                    
                except:
                    messages.error(request, _('عملية خاظاءه'))
                    return redirect('Videoss')

    else:
         pro_deletet = pro_delete

    return render(request,'Videoss.html',{'pro_delete':pro_deletet})







#     server {
#     listen 80;
#     server_name example.com www.example.com;

#     location / {
       

#         # تحسين التخزين المؤقت
#         proxy_cache STATIC_CACHE;
#         proxy_cache_valid 200 30m;
#         proxy_cache_use_stale error timeout updating;

#         # تحسين الأداء
#         proxy_buffering on;
#         proxy_buffers 16 16k;
#         proxy_busy_buffers_size 64k;
#         proxy_read_timeout 300;
#     }

#     location /static/ {
#         alias /home/user/django_project/static/;
#         expires max;
#         log_not_found off;
#     }

#     location /media/ {
#         alias /home/user/django_project/media/;
#     }

#     client_max_body_size 100M;
# }

# server {
#     listen 80;
#     server_name 64.23.197.169;

#     location = /favicon.ico { access_log off; log_not_found off; }
#     location /static/ {
#         root /home/boards_user/blog;
#     }

#     location / {
#         include proxy_params;
#         proxy_pass http://unix:/run/gunicorn.sock;
#     }
#     client_max_body_size 100M;
# }
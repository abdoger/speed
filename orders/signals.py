from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from accounts.models import OtpToken
from django.core.mail import send_mail
from django.utils import timezone
from .models import *
from django.contrib.auth.models import User
from django.template.loader import render_to_string
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from django.conf import settings
from django.http import JsonResponse

# @receiver(post_save,sender=Order)
# def j(sender,instance,created,**kwargs):
#     if created:
     
#             Payment.objects.create(order=instance,shipment_address='nnn')
from celery import shared_task
@shared_task           
@receiver(post_save,sender=User)
def create_token(sender,instance,created,**kwargs,):
    if created:
        if instance.is_superuser:
            pass
        else:
            OtpToken.objects.create(user=instance,opt_expires_at=timezone.now() + timezone.timedelta(minutes=9))
            instance.is_active=False
            instance.save()

        opt = OtpToken.objects.filter(user=instance).last()
        print(opt.osp_code)
        
        from_email =settings.EMAIL_HOST_USER
        subject = 'التحقق من الحساب'
        receiver =[instance.email,] 
        m = f"""
        http://64.23.197.169/ar/orders/verify_email/{instance.username}
        """
        messages = f"""
        انقر على هذا الرابط  الذى امامك واكتب رمز  التفعيل
        http://64.23.197.169/ar/orders/verify_email/{instance.username}
        """
        to = receiver
        html_content  = render_to_string('main_temp.html',{'m':m,'t':messages,'otp':opt.osp_code ,'user':instance.username})
        
        from_email = settings.EMAIL_HOST_USER
    
        messages = " فاتوره من المستقبل السريع"
                            
        
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = "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"
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
        email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": instance.email }],
            sender={"email": settings.DEFAULT_FROM_EMAIL},
            subject=subject,
            html_content=html_content ,
           
        )
        try:
            api_instance.send_transac_email(email)
            return JsonResponse({"message": "تم إرسال البريد بنجاح!"})
        except ApiException as e:
            return JsonResponse({"error": f"خطأ في إرسال البريد: {e}"}, status=500)
       





# def send_email_via_brevo(request,order):


#     from_email = settings.EMAIL_HOST_USER
#     subject = f'order__{order.id}'
#     to = [request.user.email]
#     messages = " فاطوره من المستقبل السريع"
                        
    
#     configuration = sib_api_v3_sdk.Configuration()
#     configuration.api_key['api-key'] = "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"

#     api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
#     email = sib_api_v3_sdk.SendSmtpEmail(
#         to=[{"email": request.user.email}],
#         sender={"email": settings.DEFAULT_FROM_EMAIL},
#         subject=messages,
#         html_content=html_content ,
       
#     )

#     try:
#         api_instance.send_transac_email(email)
#         return JsonResponse({"message": "تم إرسال البريد بنجاح!"})
#     except ApiException as e:
#         return JsonResponse({"error": f"خطأ في إرسال البريد: {e}"}, status=500)

        
    
from accounts.models import Code
from django.contrib.auth.models import User

# from defapp.models import CustomUser
from django.db.models.signals import post_save
from django.dispatch import receiver

# @receiver(post_save,sender=User)
# def post_save_generate_code(sender,instance,created,*args,**kwargs):
#     if created:
#         Code.objects.create(user=instance)
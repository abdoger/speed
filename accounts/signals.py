from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from .models import OtpToken
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth.models import User



@receiver(post_save,sender=User)
def create_token(sender,instance,created,**kwargs):
    if created:
        if instance.is_superuser:
            pass
        else:
            OtpToken.objects.create(user=instance,opt_expires_at=timezone.now() + timezone.timedelta(minutes=9))
            instance.is_active=False
            instance.save()

        opt = OtpToken.objects.filter(user=instance).last()
        print({opt.osp_code})
        from_email =settings.EMAIL_HOST_USER
        subject = 'Email verification'
        receiver =[instance.email,] 
        messages = f"""
          Hi{instance.username},here is your opp <h1>{opt.osp_code}</h1> 
          http://127.0.01:8000/verify-email/{instance.username}
        """
      
        to = receiver
        # send_mail(
        #        subject,
        #        messages,
        #        from_email,
        #        to,
        #        fail_silently=False
        #    )
    
from accounts.models import Code
from django.contrib.auth.models import User

# from defapp.models import CustomUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.dispatch import receiver
from accounts.models import OtpToken
from django.core.mail import send_mail
from django.utils import timezone
from orders.models import *
from django.contrib.auth.models import User


# @receiver(post_save,sender=Order)
# def j(request,sender,instance,created,**kwargs):
#     if created:
#         if  request.user.is_authenticated and not request.user.is_anonymous:
#             if Order.objects.all().filter(user=request.user, is_finished=False):
#                  order = Order.objects.get(user=request.user, is_finished=False)
     
#                  Payment.objects.create(order=order)

@receiver(post_save,sender=User)
def post_save_generate_code(sender,instance,created,*args,**kwargs):
    if created:
        Code.objects.create(user=instance)
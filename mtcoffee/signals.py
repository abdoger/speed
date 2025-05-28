
    
from accounts.models import Code
from django.contrib.auth.models import User

# from defapp.models import CustomUser
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save,sender=User)
def post_save_generate_code(sender,instance,created,*args,**kwargs):
    if created:
        Code.objects.create(user=instance)
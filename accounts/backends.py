from django.shortcuts import render,redirect
def allowedusers(allowGroups=[]):
    def decoratar(view_func):
        def wrapper_func(request,*args,**kwargs):
            group = None
            if request.user.groups.exists():
               group = request.user.groups.all()[0].name
            if group in allowGroups:
                return view_func(request,*args,**kwargs)
            else:
                return redirect('t404')
        return wrapper_func
    return decoratar


from django.contrib.auth import get_user_model 
from django.core.exceptions import ValidationError

UserModel = get_user_model()
from django.contrib.auth.models import User
class EmailBackend(object):
    def authenticate(username=None,password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
            
        except (User.DoesNotExist,User.MultipleObjectsReturned):
            return None
  
            
        except (User.DoesNotExist,User.MultipleObjectsReturned):
            return None
    
        
        
    def get_user(self,user_id):

        try:
            return  User.objects.get(pk=user_id)
   
        except User.DoesNotExist:
            return None

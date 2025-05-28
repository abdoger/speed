from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login
from accounts.forms import Codeform
from django.contrib.auth.models import User


from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib import messages



def handel404(request,exception):
    return render(request,'404.html',status=404)

def handel405(request):
    return render(request,'405.html',status=405)

@login_required
def home_view(request):
    return render(request,'main.html')


def auth_view(request):
    form = AuthenticationForm()
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            request.session['pk'] = user.pk
            return redirect('verify-view')
   
    return render(request,'auth.html',{'form':form})



def verify_view(request):
    form = Codeform(request.POST or None)
    pk = request.session.get('pk')
    if pk:

        user = User.objects.get(pk=pk)
        code = user.code
        last_name = user.last_name
        email = user.email
        code_user = f"{user.username}:{user.code}"
        if not request.POST:
              maseegs = 'kkkkkkkk'
        #    send_mail(maseegs,'abdozxcvbnmapi@gmail.com','abdoapiss@gmail.com')
      
              
            #   send_mail(maseegs,'abdozxcvbnmapi@gmail.com','abdoapiss@gmail.com')
            #   send_sms(code_user,)
              print(code)
              
              response = HttpResponse("Here's the text of the web page.")
              messages.success(request, 'invalid racaptcha plae') 
              return redirect('verify-view')
         
            #    response = HttpResponse("Here's the text of the web page.")
            #    messages.error(request, 'invalid racaptcha plae') 
            #    return redirect('login-view')
        print(code_user)
           
           
        if form.is_valid():
             num = form.cleaned_data.get('number')
             if str(code) == num:
                 code.save()
                 user = User.objects.get(pk=pk)
                 login(request,user,)
                 from django.contrib import auth
                 
                 login(request,user)
                 return redirect('index')
             else:
                 return redirect('login-view') 
                
    return render(request,'verify.html',{'form':form})


              
           

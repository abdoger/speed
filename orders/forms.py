from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from product.models import *
from .models import *
from orders.models import Order
class Namepartenerform(forms.ModelForm):
    class Meta:
        model = Namepartener
        fields =['name','tital','number','email']
        widgets ={
             'name': forms.TextInput(attrs={'class':'form-control'}),
             'tital': forms.TextInput(attrs={'class':'form-control'}),

             'number':forms.NumberInput(attrs={'class':'form-control'}),
             'email':forms.EmailInput(attrs={'class':'form-control'}),
             
          
        }

class Reportpartenerform(forms.ModelForm):
    class Meta:
        model = Reportpartener
        fields =['ramepartener','is_finished']
        widgets ={
            'ramepartener': forms.Select(attrs={'class':'form-control'}),
           

             'uus':forms.NumberInput(attrs={'class':'form-control'}),
          
        }
class Status_payform(forms.ModelForm):
    class Meta:
        model = Order
        fields =['status_pay',]
        widgets ={
            'status_pay': forms.Select(attrs={'class':'form-control'}),
           
        }

class Deportpartenerform(forms.ModelForm):
    class Meta:
        model = Deportpartener
        
        fields =['uus','is_finished']
        widgets ={
            'ramepartener': forms.Select(attrs={'class':'form-control'}),
           

             'uus':forms.NumberInput(attrs={'class':'form-control'}),
          
        }
       
  
class Reportpostasform(forms.ModelForm):
    class Meta:
        model = Reportpostas
        fields =['name','uus','is_finished',]
        widgets ={
             'name': forms.TextInput(attrs={'class':'form-control'}),
             'uus':forms.NumberInput(attrs={'class':'form-control'}),
          
        }
class Paymentform(forms.ModelForm):
    class Meta:
        model = Payment
        fields =['name','shipment_address','shipment_phone','mo','mr']
        widgets ={
             'name': forms.TextInput(attrs={'class':'form-control'}),
             'shipment_address':forms.TextInput(attrs={'class':'form-control'}),
             'shipment_phone': forms.NumberInput(attrs={'class':'form-control'}),
             'mo':forms.TextInput(attrs={'class':'form-control'}),
             'mr':forms.TextInput(attrs={'class':'form-control'}),
            #  '':forms.TextInput(attrs={'class':'form-control'}),

           
  
        }
class EmailPostForm(forms.Form):
    email = forms.EmailField(required=False,)
   
    tos = forms.EmailField()
class RrgisterForm(forms.ModelForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={"placeholder":"Enter email-address","class":"form-control"}))
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Enter email-address","class":"form-control"}))
    password1 = forms.CharField(label="password1" , widget=forms.PasswordInput(attrs={"placeholder":"Enter email-address","class":"form-control"}))
    password2 = forms.CharField(label="password Confirm",widget=forms.PasswordInput(attrs={"placeholder":"Enter email-address","class":"form-control"}))

    class Meta:
        model = User
        fields = ["email","username","password1","password2"]



class Colorform(forms.ModelForm):
    class Meta:
        model = Color
        fields =[
           'name',
           'qucolor',
           'color',

        ]
        widgets ={
             'name': forms.TextInput(attrs={'class':'form-control'}),
             'qucolor': forms.NumberInput(attrs={'class':'form-control'}),
             'color': forms.FileInput(attrs={'class':'form-control'}),
        
        }

class Sizeform(forms.ModelForm):
    class Meta:
        model = Sise
        fields =[
           'sisel',
           'qusise',
       

        ]
        widgets ={
             'qusise': forms.NumberInput(attrs={'class':'form-control'}),
             'sisel': forms.NumberInput(attrs={'class':'form-control'}),
         
        
        }

class Moform(forms.ModelForm):
    class Meta:
        model = Mo
        fields =[
           'mo',
           'na',
       
        ]
        widgets ={
             'mo': forms.TextInput(attrs={'class':'form-control'}),
             'na': forms.TextInput(attrs={'class':'form-control'}),

        }

class Mrform(forms.ModelForm):
    class Meta:
        model = Mr
        fields =[
           'mr',

        ]
        widgets ={
             'mr': forms.TextInput(attrs={'class':'form-control'}),
     
        }

class Coppingform(forms.ModelForm):
    class Meta:
        model = OrderDetails
        fields =[
           'copping',

        ]
        widgets ={
             'copping': forms.TextInput(attrs={'class':'form-control'}),
     
        }

class ordercomform(forms.ModelForm):
    class Meta:
        model = Order
        fields =[
           'is_st',

        ]
       
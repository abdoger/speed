from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .models import *
from orders.models import *
from orders.models import *




# # # from .models import Product,FF,Category
class Videoform(forms.ModelForm):
  
    class Meta:
        model = Video
        fields = ('video','phone','prise','captaion')
        widgets ={
       
            'captaion': forms.TextInput(attrs={'class':'form-control'}),
             'video': forms.FileInput(attrs={'class':'form-control'}),
          
             'phone': forms.NumberInput(attrs={'class':'form-control'}),
             'prise': forms.NumberInput(attrs={'class':'form-control'}),


             
      


        } 

class Codeform(forms.ModelForm):
    number = forms.CharField(label='code',help_text='Enter SMS verificse')
    class Meta:
        model =Code
        fields = ('number',) 

class EmailPostForm(forms.Form):
    email = forms.EmailField(required=False,)
   
    tos = forms.EmailField()


class OrderdetelsFromdd(forms.ModelForm):
    class Meta:
        model = OrderDetails
        fields =[
    
            
            's'
         
            
            
        ]
        widgets ={
       
          
             's': forms.NumberInput(attrs={'class':'form-control'}),

             
      


        }



class OrderFrom(forms.ModelForm):
    class Meta:
        model = Order
        fields =[
    
            'status',
            # 's'
         
            
            
        ]
        widgets ={
       
             'status': forms.Select(attrs={'class':'form-control'}),
            #  's': forms.NumberInput(attrs={'class':'form-control'}),

             
      


        }


class puserFromss(forms.ModelForm):
    start_data = forms.CharField(required=False)
    end_data = forms.CharField(required=False)

    class Meta:
        model = Order
        fields =[
         
            #   "user" ,
            #   "prosh"  ,
            #   "sels"  ,
            #   "ms",
             
           
            
            
        ]
        widgets ={
            #  "s":forms.NumberInput(attrs={'class':'form-control w-100'}) , 
            #   "t" :forms.NumberInput(attrs={'class':'form-control w-100'}) ,
            #   "ms" :forms.NumberInput(attrs={'class':'form-control w-100'}) ,
            #   "name_lo":forms.TextInput(attrs={'class':'form-control w-100'}) ,
            #   "prosh" :forms.NumberInput(attrs={'class':'form-control w-100'}) ,
            #   "sels" :forms.NumberInput(attrs={'class':'form-control w-100'}) ,
              "start_data" :forms.NumberInput(attrs={'class':'form-control w-100'}) ,

         

  
        }





class BookFrom(forms.ModelForm):
    class Meta:
        model = Order
        fields =[
   
            'statusu',
      
        ]
        widgets ={
            
             'statusu': forms.Select(attrs={'class':'form-control'}),
          
        }
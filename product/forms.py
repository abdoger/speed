from django import forms
from .models import *

class Maform(forms.ModelForm):
    class Meta:
        model = Ma
        fields =['qu','name','nots',]
        widgets ={
             'qu': forms.NumberInput(attrs={'class':'form-control'}),
             'name': forms.TextInput(attrs={'class':'form-control'}),

             'nots':forms.TextInput(attrs={'class':'form-control'}),
        }


class Photosform(forms.ModelForm):
    class Meta:
        model =Img
        fields =['name','asname','quimg','photos',]
        widgets ={
             'quimg' : forms.NumberInput(attrs={'class':'form-control'}),
             'name' : forms.TextInput(attrs={'class':'form-control'}),
             'asname' : forms.TextInput(attrs={'class':'form-control'}),
             'photos': forms.FileInput(attrs={'class':'form-control'}),


           
  
        }

class Gxquform(forms.ModelForm):
    class Meta:
        model =Gxqu
        fields =['qu',]
        widgets ={
             'qu': forms.NumberInput(attrs={'class':'form-control'}),
          
        }

class Gxform(forms.ModelForm):
    class Meta:
        model =Gx
        fields =['gx', 'title','number','email']
        widgets ={
             'gx': forms.TextInput(attrs={'class':'form-control','required':'required'}),
             'title': forms.TextInput(attrs={'class':'form-control','required':'required'}),
             'number': forms.NumberInput(attrs={'class':'form-control','required':'required'}),
             'email': forms.EmailInput(attrs={'class':'form-control','required':'required'}),


         
        }

class Productform_is_active(forms.ModelForm):
    class Meta:
        model = Product
        fields =[
           
            'is_active',

        ]
     



class Productfrm(forms.ModelForm):
    class Meta:
        model = Product
        fields =[
           'name',
           "asname" ,
           'asdescription',
           'description',
           'pricels',
            'price',
            'price_decint',
            'qu',
            'qur',
            'total',
            'photo',
            'photos',
            'category',
            'gx',
           
            'qus',
            'facat',
           
            # 'desconts',
            # 'qudesconts',
            'boonimg',
         

        ]
        widgets ={
            'qus': forms.NumberInput(attrs={'class':'form-control','required':'required'}),
            'qur': forms.NumberInput(attrs={'class':'form-control','required':'required'}),
            'price_decint': forms.NumberInput(attrs={'class':'form-control','required':'required'}),
            'number': forms.NumberInput(attrs={'class':'form-control','required':'required'}),
            "asdescription" : forms.TextInput(attrs={'class':'form-control','required':'required'}),
            "asname" : forms.TextInput(attrs={'class':'form-control','required':'required'}),

             'name': forms.TextInput(attrs={'class':'form-control','required':'required'}),
             'namel': forms.TextInput(attrs={'class':'form-control','required':'required'}),
             'description': forms.TextInput(attrs={'class':'form-control','required':'required'}),
             'photo': forms.FileInput(attrs={'class':'form-control'}),
             'photos': forms.FileInput(attrs={'class':'form-control'}),

             'pages': forms.NumberInput(attrs={'class':'form-control'}),
             'price': forms.NumberInput(attrs={'class':'form-control','id':'price','required':'required'}),
             'pricels': forms.NumberInput(attrs={'class':'form-control','id':'price','required':'required'}),
            #  'qudesconts': forms.NumberInput(attrs={'class':'form-control'}),
             'qu': forms.NumberInput(attrs={'class':'form-control','id':'qu','required':'required'}),
             'total': forms.NumberInput(attrs={'class':'form-control','id':'total','required':'required'}),
             'status': forms.Select(attrs={'class':'form-control'}),
             'gx': forms.Select(attrs={'class':'form-control','required':'required','label':'jjjjj'}),

             'category': forms.Select(attrs={'class':'form-control','required':'required'}),
             'user_updete': forms.Select(attrs={'class':'form-control','id':'user_updete'}),

        }





class FF(forms.ModelForm):
    class Meta:
        model = FF
        fields = '__all__'


class Categoryform(forms.ModelForm):
    class Meta:
        model =Category
        fields =['name']
        widgets ={
             'name': forms.TextInput(attrs={'class':'form-control','required':'required'}),
           
  
        }


class Productfactoryform(forms.ModelForm):
    class Meta:
        model = Product
        fields =[
           'name',
           "asname" ,
           'asdescription',
           'description',
           'pricels',
            # 'price',
            # 'price_decint',
            # 'qu',
            'qur',
            # 'total',
            'photo',
            'photos',
            'category',
            'gx',
            # 'is_active',
            # 'qus',
            'facat',
            # 'number',
            # 'namel',
            # 'desconts',
            # 'qudesconts',
            'boonimg',
            # 'is_active'
           

        ]
        widgets ={
            'qus': forms.NumberInput(attrs={'class':'form-control'}),
            'qur': forms.NumberInput(attrs={'class':'form-control','required':'required'}),
            'price_decint': forms.NumberInput(attrs={'class':'form-control'}),
            'number': forms.NumberInput(attrs={'class':'form-control'}),
            "asdescription" : forms.TextInput(attrs={'class':'form-control','required':'required'}),
            "asname" : forms.TextInput(attrs={'class':'form-control','required':'required'}),

             'name': forms.TextInput(attrs={'class':'form-control','required':'required'}),
             'namel': forms.TextInput(attrs={'class':'form-control'}),
             'description': forms.TextInput(attrs={'class':'form-control','required':'required'}),
             'photo': forms.FileInput(attrs={'class':'form-control'}),
             'photos': forms.FileInput(attrs={'class':'form-control'}),

             'pages': forms.NumberInput(attrs={'class':'form-control'}),
             'price': forms.NumberInput(attrs={'class':'form-control','id':'price'}),
             'pricels': forms.NumberInput(attrs={'class':'form-control','id':'price','required':'required'}),
             'qudesconts': forms.NumberInput(attrs={'class':'form-control'}),
             'qu': forms.NumberInput(attrs={'class':'form-control','id':'qu','required':'required'}),
             'total': forms.NumberInput(attrs={'class':'form-control','id':'total'}),
             'status': forms.Select(attrs={'class':'form-control'}),
             'gx': forms.Select(attrs={'class':'form-control','required':'required'}),

             'category': forms.Select(attrs={'class':'form-control','required':'required'}),
             'user_updete': forms.Select(attrs={'class':'form-control','id':'user_updete'}),

        }




class Searchform(forms.Form):
    query = forms.CharField()

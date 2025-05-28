# from orders.models import *
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import RegexValidator,MaxValueValidator,MinValueValidator
import secrets
import uuid
import random

class Cat(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=50,unique=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name= "الاصناف"



class Gx(models.Model):
     gx = models.CharField('اسم التاجر',max_length=150,blank=True , null=True,unique=True)
     title = models.CharField('العنوان وتفاصيل التاجر',max_length=150,null=True, blank=True,) #validators=[MaxValueValidator(11),MinValueValidator(11)]
     number = models.CharField('رقم الهاتف',max_length=150,null=True, blank=True) #validators=[MaxValueValidator(11),MinValueValidator(11)]
     email = models.CharField(max_length=150,blank=True , null=True,unique=True)
     gx_date = models.DateTimeField(default=datetime.now)

     def __str__(self):
        return self.gx
     class Meta:
        verbose_name= "اضافة تاجر"

class Gxqu(models.Model):
     qu = models.CharField(' القيمه الواصله',max_length=150,blank=True , null=True,default='0')
     publish_date = models.DateTimeField(default=datetime.now)
     gx = models.ForeignKey(Gx, on_delete=models.PROTECT,null=True, blank=True)
     name = models.ForeignKey(User, on_delete=models.PROTECT,null=True, blank=True)

     def __str__(self):
        return str(self.gx.gx)
    #  class Meta:
    #     verbose_name= "القيمه الواصله الى التاجر"

class Ma(models.Model):
     qu = models.CharField(' القيمه الواصله',max_length=150,blank=True , null=True,default='0')
     publish_date = models.DateTimeField(default=datetime.now)
     name = models.CharField(' اسم الصارف',max_length=150,blank=True , null=True,)
     nots = models.CharField('  ملحوظة الصارف',max_length=150,blank=True , null=True,)
     user = models.ForeignKey(User, on_delete=models.PROTECT,null=True, blank=True)
     def __str__(self):
        return str(self.user.username)
     class Meta:
       
        verbose_name = 'المصارف'






class Product(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name  = models.CharField('اسم المنتج',max_length=150,null=True, blank=True)
    asname = models.CharField(' اسم المنتج بالانجليزى',max_length=150,null=True, blank=True)
    description = models.TextField('الوصف')
    asdescription = models.TextField('الوصف بالانجليزى')
    price = models.IntegerField('سعر البيع',null=True, blank=True)
    price_decint = models.IntegerField('سعر الوهمي',null=True, blank=True)
    pricels = models.IntegerField('السعر الحقيقى للتاجر',null=True, blank=True)
    total = models.IntegerField('المجموع',null=True, blank=True)
    qus = models.IntegerField('قيمة الموسوق',max_length=150,null=True, blank=True,default='1')
    # number = models.CharField('رقم الهاتف',max_length=150,null=False, blank=False,) #validators=[MaxValueValidator(11),MinValueValidator(11)]
    qu = models.IntegerField('الكمية',null=True, blank=True,)
    qur = models.IntegerField('الكميه الصلية',null=True, blank=True,)
    statusu = models.CharField(max_length=50,null=True, blank=True,default='none')
    photo = models.ImageField('صورة المنتج',upload_to=' photo/%Y/%m/%d/',null=True, blank=True,)
    photos = models.ImageField(' صورة للمنتج اضافيه',upload_to=' photos/%Y/%m/%d/',null=True, blank=True,)
    is_active = models.BooleanField('التفعيل',default=False)
    facat = models.BooleanField('تفعيل الفقات المتعدده',default=False)
    desconts = models.BooleanField('منتجات خصم',default=False)
    qudesconts = models.IntegerField('قيمة الخصم',max_length=150,null=True, blank=True,)
    pro_date = models.DateTimeField('تريخ بداية المنتج',auto_now_add=True )
    publish_date = models.DateTimeField('تريخ بداية المنتج',default=timezone.now() )
    update_pro = models.DateTimeField(null=True, blank=True,)
    category = models.ForeignKey(Category, on_delete=models.PROTECT,null=True, blank=True,verbose_name=" التصنيف")
    gx = models.ForeignKey(Gx, on_delete=models.PROTECT,null=True, blank=True,verbose_name="اسم التاجر")
    # namel = models.CharField('اسم صاحب  المنتج',max_length=150,null=False, blank=False)
    user_updete = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True,related_name='prouser',)
    user_create = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True,related_name='updte',)
    boonimg = models.BooleanField('الوان اضافيه',default=False)
    
    def nd(self):
        return  Fintion.objects.filter(fintion=self).exclude(order_idsid__statusu='completed')

    def nsd(self):
        return  Fintion.objects.filter(fintion=self).filter(order_idsid__statusu='completed')
    # @property

    

    def __str__(self):
        return str(self.name)
    
    
    class Meta:
        ordering =['-publish_date']
        verbose_name = 'المنتجات'
        
    def get_absolute_url(self):
        return f'/{self.name}'
    

    
class Img(models.Model):
    photos = models.ImageField('صورة المنتج',upload_to='photosi/%Y/%m/%d/',null=False, blank=False,)
    i =  models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True,related_name='Img',)
    quimg = models.IntegerField('الكميه',null=False, blank=False,)
    name = models.CharField('اسم المنتج',max_length=150,null=False, blank=False)
    asname = models.CharField(' اسم المنتج بالانجليزى',max_length=150,null=False, blank=False)

    def __str__(self):
        return self.name 
    class Meta:
        
        verbose_name = 'اضافة صور'
    
class Color(models.Model):
    asname = models.CharField(' اسم اللون بالانجليزى',max_length=150,null=False, blank=False)

    name = models.CharField('اسم اللون',max_length=150,null=False, blank=False)
    color = models.ImageField('صورة المنتج',upload_to='color/%Y/%m/%d/')
    qucolor = models.IntegerField('الكميه',null=True, blank=True,)
    productcolor = models.ForeignKey(Product, on_delete=models.CASCADE,null=True, blank=True,related_name='productcolors')
    def __str__(self):
        return str(self.name)
    class Meta:
      
        verbose_name = 'اضافة الوان'

class Sise(models.Model):
    sisel = models.IntegerField('المقاس',null=True, blank=True,)
    
    qusise = models.IntegerField('الكميه',null=True, blank=True,)
    productsise = models.ForeignKey(Color, on_delete=models.CASCADE,null=True, blank=True,related_name="productsises")

    
    def __str__(self):
        return str(self.sisel)
    class Meta:
     
        verbose_name = 'اضافة المقاسات'
    



class FF(models.Model):
    name = models.CharField(max_length=150)




from orders.models import *

class Fintion(models.Model):
    fintion = models.ForeignKey(Product, on_delete=models.PROTECT,null=True, blank=True,related_name='fintion')
    order_idsid = models.ForeignKey(Order, on_delete=models.SET_NULL,null=True, blank=True,related_name='fintion_order')
    usus = models.CharField(default=0,max_length=200,blank=True , null=True)
    order_detils = models.CharField(default=0,max_length=200,blank=True , null=True)
    class Meta:
       
        verbose_name = 'متبعة للمنتج'
  
  

    def __str__(self):
        return str(self.usus)
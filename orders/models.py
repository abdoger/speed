from django.db import models
from django.contrib.auth.models import User
from product.models import Product
from django.db.models import F ,Q
from django.urls import reverse
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.db.models import Sum,F,Count
from django.conf import settings
from django.dispatch import receiver
import uuid 
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth.models import User

from io import BytesIO
from django.core.files import File
# from PIL import Image , ImageDraw

# from creditcards.models import CardNumberFild , CardExpirdField,SecurityCodeField 
class Clint(models.Model):
    name = models.CharField('اسم ',max_length=150,blank=True , null=True)
    tital = models.CharField('العنوان ',max_length=150,blank=True , null=True)
    number = models.CharField('رقم الهاتف  ',max_length=11,blank=True , null=True,)
    def __str__(self):
        return str(self.name)
    class Meta:
        # ordering =('name')
        indexes = [
            models.Index(fields=['-name'])
        ]
        
        verbose_name= "المصاريف"


class Namepartener(models.Model):
    name = models.CharField('اسم الشركه',max_length=150,blank=True , null=True)
    tital = models.CharField('العنوان ',max_length=150,blank=True , null=True)
    email  = models.EmailField(' الاميل ',blank=True , null=True,)

    number = models.IntegerField('رقم الهاتف  ',blank=True , null=True,)
    def __str__(self):
        return str(self.name)
    class Meta:
        verbose_name= "شركات الشكن"
  


class Statas_order(models.TextChoices):
   
       a= ' تم الدفع  ',' تم الدفع  '
       b =' لم يتم الدفع ',' لم يتم الدفع '


class Paymentstatus(models.TextChoices):
   
       COD = 'COD',' COD '
       CAARD ='  CAARD  ','CAARD'
class Order(models.Model):

    class Typechoices(models.TextChoices):
   
       a= 'اوردر جديد','اوردر جديد'
       b ='تم التاكيد','تم التاكيد'
       c= 'تم التوصيل','تم التوصيل'
       d ='اوردر ملغى','اوردر ملغى'
       f= 'عدم رد', 'عدم رد'
       g ='اتشحن','اتشحن'
       h= ' مرتج', 'مرتج'
       m ='فى التوصيل','فى التوصيل'

       sold ='sold','sold'

   

 
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
   

    user_group = models.ForeignKey(Group, on_delete=models.PROTECT, null=True, blank=True) 
    order_date = models.DateField(blank=True,null=True,default=timezone.now())
    order_delete = models.DateTimeField(auto_now_add=True)
    order_updated = models.DateTimeField(null=True, blank=True)

    order_update = models.DateTimeField(auto_now=True)
    status_copping = models.CharField(blank=True , null=True,max_length=50,verbose_name=" حالة شركة الشحن ")
    details = models.ManyToManyField(Product, through='OrderDetails',related_name='orderDetails')
    is_finished = models.BooleanField()
    is_st = models.BooleanField(default=False,verbose_name=" هل تممة على طلب شركة الشحن")

    posta = models.BooleanField(null=True, blank=True,verbose_name="تفعيل بوسطه")
    statusu = models.CharField(max_length=50,null=True, blank=True,default='none',verbose_name="حالة عمل الطاب" )
    # qr_code = models.ImageField(upload_to='qr_codes',blank=True )
    coin = models.IntegerField(blank=True , null=True,default='0',verbose_name="العموله")
    status = models.CharField(max_length=50,choices=Typechoices.choices,null=True, blank=True,default=Typechoices.a,verbose_name="حالة الطلب")
    status_pay = models.CharField(max_length=50,choices=Statas_order.choices,null=True, blank=True,default=Statas_order.b,verbose_name="حالة الدفع")
    Payment_status = models.CharField(max_length=50,choices=Paymentstatus.choices,null=True, blank=True,default=Paymentstatus.CAARD,verbose_name="خيار الدفع")
    user_updete = models.ForeignKey(User, on_delete=models.SET_NULL,max_length=77, null=True, blank=True,related_name='user_updetes')
    Orderpartener = models.ForeignKey('Reportpartener' , on_delete=models.CASCADE ,blank=True , null=True,related_name='Orderpartener',verbose_name="تابع لى شركة الشحن")
    is_Orderpartener = models.BooleanField(default=False,verbose_name="تفعيل شركات الشحن")
    total_pasta = models.IntegerField(blank=True , null=True,default='0',verbose_name="وصل بوصته")
    
    total = 0
    items_count = 0
    items_counts = 0

  
   
    def na(self):
        return  Payment.objects.filter(order=self).aggregate(s = Sum(F('na')))['s']
    # @property
    # def getsgets(self):
    #     return  OrderDetails.objects.filter(order=self).aggregate(t = Sum(F('products__qus') * F('quantity')) )['t'] or 0
    def getshhr(self):
        return  OrderDetails.objects.filter(order=self).aggregate(t = Sum(F('product__qus') * F('ba')) + Sum(F('ba') * F('price'))  )['t'] or 0
    # def tatalsds__quantitys(self):
    #     return  OrderDetails.objects.filter(order=self).aggregate(t = Sum(F('product__qus') * F('quantity'))  )['t'] or 0
    def gets(self):
        return  OrderDetails.objects.filter(order=self).aggregate(t = Sum(F('ba') * F('price')) )['t'] or 0
    def price__quantity(self):
        return  OrderDetails.objects.filter(order=self).aggregate(price__quantity = Sum(F('price') * F('quantity')) )['price__quantity'] or 0
    
 
 
    # @property

    def ns(self):
        return  Payment.objects.get(order=self)
    
    
  
    def __str__(self):
        return str(self.id)
    
    class Meta:
        ordering=['-id']
       
        verbose_name= "الطلبات"


  

class Reportpartener(models.Model):
    ramepartener = models.ForeignKey(Namepartener , on_delete=models.SET_NULL ,blank=True , null=True,related_name='reportparteners',verbose_name="شركة الشحن")
    uus = models.IntegerField('قيمة  الواصل',blank=True , null=True,)
    user_add = models.ForeignKey(User, on_delete=models.SET_NULL,max_length=77, null=True, blank=True,)
    id_order =  models.ForeignKey(Order , on_delete=models.CASCADE ,blank=True , null=True,related_name='orders',)
    reportpostas_date = models.DateTimeField(blank=True,null=True,default=timezone.now())
    is_finished = models.BooleanField("انتهاء")
    def gr(self):
        return Order.objects.filter(Orderpartener=self).aggregate(total = Sum((F("orderss__product__price") * F("orderss__ba")) + F("Payments__na")))
    def grs(self):
        return Order.objects.filter(Orderpartener=self).aggregate(jx = Sum( (F("orderss__product__price") * F("orderss__ba")) + F("Payments__na")  + F("details__qus") *  F("orderss__ba")))
    def grsds(self):
        return Order.objects.get(Orderpartener=self)
   




    
    # @property
    def __str__(self):
        return str(self.ramepartener.name)
    class Meta:
        verbose_name= "واصل شركات الشحن"

class Deportpartener(models.Model):
    ramepartener = models.ForeignKey(Namepartener , on_delete=models.CASCADE ,blank=True , null=True,verbose_name="اختر شركة شحن")
    uus = models.IntegerField('قيمة  الواصل',blank=True , null=True,)
    reportpostas_date = models.DateTimeField(blank=True,null=True,default=timezone.now())
    user_add = models.ForeignKey(User, on_delete=models.SET_NULL,max_length=77, null=True, blank=True,)
    is_finished = models.BooleanField("انتهاء")
    def __str__(self):
        return str(self.ramepartener.name)
    class Meta:
        verbose_name= "راجع شركات الشحن"



class OrderDetails(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE ,blank=True , null=True,related_name='products' ,verbose_name="المنتج")
    order = models.ForeignKey(Order, on_delete=models.CASCADE ,blank=True , null=True,related_name='orderss' ,verbose_name="الطلب")
    price = models.DecimalField(max_digits=6 , decimal_places=2,verbose_name="السعر")
    quantity = models.IntegerField(verbose_name="الكميه")
    s = models.IntegerField("الواصل",blank=True , null=True)
    testing = models.IntegerField(blank=True , null=True,default='0',verbose_name="setion")
    ba = models.IntegerField(blank=True , null=True,default='0',verbose_name="الكميه المستلمه")
    size = models.IntegerField(blank=True , null=True,default='0',verbose_name="المقاس")
    colar = models.CharField(blank=True , null=True,max_length=50,verbose_name="الون")
    nameimg = models.CharField(blank=True , null=True,max_length=50,verbose_name=" تفعيل لى صوره اضافيه")
    copping = models.IntegerField(blank=True , null=True,max_length=50, default='0',verbose_name=" الكميه الراجعه ")
    str = models.IntegerField(default='5')
    persent = models.IntegerField(default='100')
    imgf = models.CharField(max_length=250,null=True, blank=True)
    OrderDetailsimg = models.ImageField(upload_to='OrderDetails/%Y/%m/%d/',verbose_name=" الون اضافيه")


    def __str__(self):
        return self.product.name

   

    class Meta:
        ordering=['-order__id']
    class Meta:
        verbose_name= "الفواتير"

 

    
    # def __str__(self):
    #     return self.email


class Payment(models.Model):

    order = models.ForeignKey(Order , on_delete=models.CASCADE ,blank=True , null=True,related_name='Payments')
    shipment_address = models.CharField('العنوان',max_length=150,default='لايوجد',blank=True , null=True,)
    shipment_phone = models.CharField('رقم الهاتف',max_length=50,default='لايوجد',blank=True , null=True,)
    shipment_phone_to = models.CharField('رقم هاتف اخر',max_length=50,default='لايوجد',blank=True , null=True,)
    districtid = models.CharField('تفاصيل اكثر',max_length=50,default='لايوجد',blank=True , null=True,)
    name = models.CharField('الاسم',max_length=50,default='لايوجد',blank=True , null=True,)
    mo = models.CharField('المحافظه',max_length=150,blank=True , null=True,)
    na = models.IntegerField('قيمة شحن المحافظه',blank=True , null=True,)
    mr = models.CharField('المركز',max_length=150,blank=True , null=True,)
    momr = models.CharField('الملحوظات',max_length=150,blank=True , null=True,)


    def __str__(self):
        return str(self.order)
    class Meta:
        verbose_name= "الدفع"
        


    # card_number = CardNumberFild()
    # expire = CardExpirdField()
    # security_code = SecurityCodeField()

class Mo(models.Model):

    mo = models.CharField('المحافظه',max_length=150,blank=True , null=True)
    na = models.IntegerField('قيمة شحن المحافظه',blank=True , null=True,)
    def __str__(self):
        return self.mo
    class Meta:
        verbose_name= "المحافطه"
    
class Mr(models.Model):
    mo = models.ForeignKey(Mo , on_delete=models.CASCADE ,blank=True , null=True,related_name='mos')
    
    mr = models.CharField('المركز',max_length=150,blank=True , null=True,)
   
    def __str__(self):
        return self.mr
    class Meta:
        verbose_name= "المراكز"

class Tp(Mr):
    class Meta:
        proxy = True

    class Manager(models.Manager):
        def get_queryset(self) -> models.QuerySet:
            return super().get_queryset().filter(mr='ssh')
    def save(self,*args,**kwargs):
            if self._state.adding:
                self.mr = 'kkkkkkkk'
            super().save(*args,**kwargs)

    objects = Manager()
from django.db import models
from django.contrib.auth.models import User
class OTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp_secret = models.CharField(max_length=16)
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    def __str__(self):
        return self.email
from django.contrib import admin
admin.site.register(OTP)


# @receiver(post_save,sender=Order)
# def j(sender,instance,created,**kwargs):
#     if created:
     
#             Payment.objects.create(order=instance,shipment_address='nnn')

    
class Reportpostas(models.Model):
    name = models.CharField('اسم الواصل',max_length=150,blank=True , null=True)
    uus = models.IntegerField('قيمة  الواصل',blank=True , null=True,)
    reportpostas_date = models.DateTimeField(blank=True,null=True,default=timezone.now())
    is_finished = models.BooleanField()
    def __str__(self):
        return self.id
    class Meta:
        verbose_name= "تقرير بوسطه"



















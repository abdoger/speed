from django.db import models
from django.contrib.auth.models import User
from product.models import Product
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.conf import settings
import secrets
import random
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator,MaxValueValidator,MinValueValidator
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,blank=True , null=True,related_name='usersd')
    Product_favorites = models.ManyToManyField(Product)
    address = models.CharField(max_length=150,blank=True , null=True)
    userimg = models.ImageField('صورة اليوزر',blank=True , null=True,upload_to=' photo/%Y/%m/%d/',)
    zip_number = models.TextField(max_length=150,blank=True , null=True)
    def __str__(self):
        return self.user.username
    

    class Meta:
       ordering =['user']

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,blank=True , null=True)
    mobile = models.CharField(max_length=20,blank=True , null=True)
    otp = models.CharField(max_length=6,blank=True , null=True,)
 
class OtpToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='otps')
    osp_code = models.CharField(max_length=6,default=secrets.token_hex(3))
    tp_created_at = models.DateTimeField(auto_now_add = True)
    opt_expires_at = models.DateTimeField(blank=True , null=True)
    def __str__(self):
        return self.user.username
    # from django.db import models
# from defapp.models import CustomUser
import random
class Code(models.Model):
    number = models.CharField(max_length=5,blank=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.number)
    def save(self,*args,**kwargs):
        number_list = [x for x in range(10)]
        code_items =[]
        for i in range(5):
            num = random.choice(number_list)
            code_items.append(num)
        code_string = "".join(str(item) for item in code_items)
        self.number = code_string
        super().save(*args,**kwargs) 
    

class Video(models.Model):
    captaion =models.CharField('اسم المعلن',max_length=200,blank=True)
    views = models.PositiveBigIntegerField(default='0')
    prise = models.IntegerField('السعر',blank=True,null=True,)
    tp_created_at = models.DateTimeField(auto_now_add = True)
    like = models.ManyToManyField(User, blank=True,null=True,)

    phone = models.IntegerField('تليفون ',max_length=11,blank=True)
    video = models.FileField('الفيديو',upload_to="video/%y")
    def __str__(self):
        return str(self.captaion)


    


 







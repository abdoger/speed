from django.db import models
from accounts.models import Video,UserProfile
from django.contrib.auth.models import User



class Post(models.Model):
    massage=models.TextField(max_length=4000)
    video = models.ForeignKey(Video,related_name='videos',on_delete=models.CASCADE)
    img = models.ImageField(upload_to='post',blank=True,null=True,default='')
    created_UserProfile = models.ForeignKey(User,related_name='UserProfiles',on_delete=models.CASCADE)
    created_dt = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return str(self.massage)
    class Meta:
        verbose_name= " التعليقات "

class Lists(models.Model):
    massages =models.TextField(max_length=4000)
   
    created_dt = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return str(self.created_dt)


# Create your models here.

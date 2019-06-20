from django.db import models

# Create your models here.



#表名称：user_register_userinfo
class userInfo(models.Model):

    uname = models.CharField(max_length=20)
    upassword = models.CharField(max_length=100)
    uemail = models.CharField(max_length=100)
    #收货地址
    ushouAddress = models.CharField(max_length=200,default="")
    #居住地址
    uaddress = models.CharField(max_length=200,default="")
    #邮编
    upostcode = models.CharField(max_length=6,default="")
    #电话
    uphone = models.CharField(max_length=11,default="")
    # 用户等级
    ulevel = models.IntegerField(null=True)


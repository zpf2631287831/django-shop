from django.db import models
from tinymce.models import HTMLField

# Create your models here.
class TypeInfo(models.Model):
    #类型
    ttitle=models.CharField(max_length=20)#类型
    isDelete=models.BooleanField(default=False)#是否删除
    def __str__(self):
        return self.ttitle

class GoodsInfo(models.Model):
    gtitle=models.CharField(max_length=20)
    gpic=models.ImageField(upload_to='goods')#商品图片
    gprice=models.DecimalField(max_digits=5,decimal_places=2)#价格
    isDelete=models.BooleanField(default=False)#是否删除
    gunit=models.CharField(max_length=20,default='500g')#单位（重量）
    gclick=models.IntegerField()#购买数量
    gintroduce=models.CharField(max_length=200)#产品简介
    gstock=models.IntegerField()#库存
    gdetailcontent=HTMLField()#详细介绍
    gtype=models.ForeignKey(TypeInfo,on_delete=models.CASCADE)
    # gadv=models.BooleanField(default=False)
    def __str__(self):
        return self.gtitle

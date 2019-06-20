from django.conf.urls import url
from . import views
app_name = "shop"

urlpatterns = [


    url(r'^list/(\d+)/(\d+)/(\d+)/$', views.list,name='list'),
    url(r'^/(\d+)/$', views.goods_detail,name='detail'),
    url(r'^$', views.index, name='index'),

]
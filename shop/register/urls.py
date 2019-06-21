from django.conf.urls import url
from . import views
app_name = "user"

urlpatterns = [

    url(r'^register/$', views.register,name='register'),
    url(r'^register_headle/$', views.register_headle,name='register_headle'),
    url(r'^login/$', views.login,name='login'),
    url(r'^login_headle/$', views.login_headle,name='login_headle'),
    url(r'^userInfoCenter/$', views.userInfoCenter,name='userInfoCenter'),
    url(r'^user_center_order/$', views.user_center_order,name='user_center_order'),
    url(r'^user_center_site/$', views.user_center_site,name='user_center_site'),

]
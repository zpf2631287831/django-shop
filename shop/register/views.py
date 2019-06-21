from django.shortcuts import render, redirect
from hashlib import sha1
from .models import *
from django.http import HttpResponseRedirect,JsonResponse
from . import login_decorator
from z_goods.models import  *

# Create your views here.

# -----------------注册模块--------------------------
def register(request):
    contxt = {"title": "注册"}
    return render(request, "user_register/register.html", contxt)


def register_headle(request):
    post_obj = request.POST
    # 密码
    password = post_obj.get("pwd")
    # 确认密码
    passwordagain = post_obj.get("cpwd")
    # 用户名
    username = post_obj.get("user_name")
    # 邮箱
    email = post_obj.get("email")

    if password != passwordagain:
        # 提示密码不正确(这里js已经帮处理过了，不然可以携带参数回调做判断) 返回到注册界面
        return redirect("/user/register/")

    # 到这里来就表示 密码一致，可以加密存到数据库了

    # 对密码进行加密处理
    s1 = sha1()
    s1.update(password.encode())
    encryption = s1.hexdigest()

    # 创建用户模型对象
    user_obj = userInfo()
    user_obj.uname = username
    user_obj.upassword = encryption
    user_obj.uemail = email
    # 保存
    user_obj.save()

    # 跳转到登录界面
    return redirect("/user/login/")


# -----------------登录模块--------------------------
# 上面的重定向来这里做跳转登录模板界面
def login(request):
    return render(request, "user_register/login.html")


def login_headle(request):
    # 获取用户输入的账号密码 并加密
    post_obj = request.POST
    username = post_obj.get("username")
    password = post_obj.get("pwd")
    remember = post_obj.get("remember", 0)
    s1 = sha1()
    s1.update(password.encode())
    encryption = s1.hexdigest()

    # 获取数据库已经加密好的密码做对比
    user_obj_set = userInfo.objects.filter(uname=username)
    print(len(user_obj_set))
    # 根据账号查到了一条记录
    if len(user_obj_set) == 1:
        if user_obj_set[0].upassword == encryption:  # 密码正确
            # 构建重定向对象跳转到 从哪里来 往哪里去， 如果没有值，就跳转到/:index
            url = request.COOKIES.get("url","/")
            redirect_obj = HttpResponseRedirect(url)
            if remember != 0:
                # 使用cookie记住账号 key为：username
                redirect_obj.set_cookie("username", username)
            else:
                # 不记住 设置一个空的 而且立马失效
                redirect_obj.set_cookie("username", "", max_age=-1)
            # 把用户id 和用户名称使用session存起来 方便后面使用
            request.session["user_id"] = user_obj_set[0].id
            request.session["user_name"] = user_obj_set[0].uname
            # 跳转到用户信息中心模块
            return redirect_obj
        else:  # 密码错误
            context = {"title": "用户登录", "error_username": "0", "error_password": "1", "username": username,
                       "password": password}
            return render(request, "register/login.html", context)
    else:  # 账号出错
        context = {"title": "用户登录", "error_username": "1", "error_password": "0", "username": username,
                   "password": password}
        return render(request, "register/login.html", context)

@login_decorator.login
def userInfoCenter(request):
    # 根据session获取用户id进而获去用户信息
    user_obj_set = userInfo.objects.filter(id=request.session["user_id"])
    # 用户名
    username = user_obj_set[0].uname
    # 电话号码
    phone = "18520340803"
    # 邮箱地址
    email = user_obj_set[0].uemail
    # 标题
    title = "用户中心"
    #查询出cookie
    goodsID_list_str = request.COOKIES.get("goodsId_list","")
    goodsID_list = goodsID_list_str.split(",")
    print('++++++++++')
    # goods_list = []
    # for goodsID in goodsID_list:

        # #查询出商品
        # goods = GoodsInfo.objects.get(id=goodsID)
        # goods_list.append(goods)
        # "goods_list": goods_list
    context = {"user_flag":1,"title": title, "username": username, "phone": phone, "email": email,}

    return render(request, 'user_register/user_center_info.html', context)

@login_decorator.login
def user_center_order(request):
    context = {"title": "用户中心","user_flag":1}
    return render(request, "user_register/user_center_order.html", context)

@login_decorator.login
def user_center_site(request):
    context = {"title": "用户中心", "user_flag": 1}
    return render(request, "user_register/user_center_site.html",context)


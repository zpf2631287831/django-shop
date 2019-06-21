from django.http import  HttpResponseRedirect
#是否保持登录的装饰器
def login(func):

    def innerFunc_login(request,*args,**kwargs):

        if "user_id" in request.session:
            return func(request,*args,**kwargs)
        else:
            #跳转到登录页面
            redirect_obj = HttpResponseRedirect("/user/login/")
            redirect_obj.set_cookie("url",request.get_full_path())
            return redirect_obj
    return innerFunc_login


''''
>cookie:
1.HttpResponse的对象或者子类对象才能 set_cookie
2.request对象的COOKIES属性能获取到存入的cookie

>session:
1.而session是服务器的，所以就可以根据request对象赋值和取值
2.request.session["key"] = "value"

eg: http://127.0.0.1:8000/user/?id=100
#获取全路径
request.get_full_path() 获取到:/user/?id=100
#表示当前路径
request.path()  获取到： /user/
'''
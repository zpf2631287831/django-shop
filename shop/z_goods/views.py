
from django.shortcuts import render
from .models import *
from django.core.paginator import  Paginator,Page

# Create your views here.
#跳转到首页
def index(request):
    # 查找数据，4条最新的，4条最热的
    typeList = TypeInfo.objects.all()
    fruits_new = typeList[1].goodsinfo_set.order_by("-id")[0:4]
    fruits_hot = typeList[1].goodsinfo_set.order_by("-gclick")[0:4]

    seafood_new = typeList[2].goodsinfo_set.order_by("-id")[0:4]
    seafood_hot = typeList[2].goodsinfo_set.order_by("-gclick")[0:4]

    meat_new = typeList[0].goodsinfo_set.order_by("-id")[0:4]
    meat_hot = typeList[0].goodsinfo_set.order_by("-gclick")[0:4]

    eggs_new = typeList[3].goodsinfo_set.order_by("-id")[0:4]
    eggs_hot = typeList[3].goodsinfo_set.order_by("-gclick")[0:4]

    vegetable_new = typeList[4].goodsinfo_set.order_by("-id")[0:4]
    vegetable_hot = typeList[4].goodsinfo_set.order_by("-gclick")[0:4]

    freeze_new = typeList[5].goodsinfo_set.order_by("-id")[0:4]
    freeze_hot = typeList[5].goodsinfo_set.order_by("-gclick")[0:4]

    context = {
        "title": "首页",
        "shopcar": 1,
        "fruits_new": fruits_new,
        "fruits_hot": fruits_hot,
        "seafood_new": seafood_new,
        "seafood_hot": seafood_hot,
        "meat_new": meat_new,
        "meat_hot": meat_hot,
        "eggs_new": eggs_new,
        "eggs_hot": eggs_hot,
        "vegetable_new": vegetable_new,
        "vegetable_hot": vegetable_hot,
        "freeze_new": freeze_new,
        "freeze_hot": freeze_hot
    }

    return render(request, "df_goods/index.html", context)

#跳转到商品列表页
def list(request,typeId,pageNumber,sortId):

    typeId = int(typeId)
    pageNumber = int(pageNumber)
    sortId = int(sortId)

    #根据typeId获取该商品种类的商品列表
    goodsType = TypeInfo.objects.get(id=typeId)
    #根据商品类型拿最新2条推荐数据
    goodsNew = goodsType.goodsinfo_set.order_by("-id")[0:2]

    if sortId == 1:#默认排序
        print("默认排序")
        goods_list = GoodsInfo.objects.filter(gtype__id=typeId).order_by("-id")
    elif sortId == 2:#价格排序
        print("价格排序")
        goods_list = GoodsInfo.objects.filter(gtype__id=typeId).order_by("-gprice")
    elif sortId == 3:#点击量排序
        print("点击量排序")
        goods_list = GoodsInfo.objects.filter(gtype__id=typeId).order_by("-gclick")
    #分页器和分页属性
    pagenator = Paginator(goods_list,10)
    page = pagenator.page(pageNumber)

    title = goodsType.ttitle
    #控制上面的购物车 搜索框显示和影藏
    shopcar = 1


    return render(request,"df_goods/list.html",locals())


def goods_detail(request,id):

    #根据id查询出商品
    goods = GoodsInfo.objects.get(id=id)
    #累加点击量
    goods.gclick = goods.gclick+2
    goods.save()

    #查询2条新品推荐
    goods_new = goods.gtype.goodsinfo_set.order_by("-id")[0:2]


    #构建标题
    title = goods.gtype.ttitle
    # 控制上面的购物车 搜索框显示和影藏
    shopcar = 1
    httpResponse = render(request, "df_goods/detail.html", locals())
    #获取COOKIES中的数据
    goodsID_list_str = request.COOKIES.get("goodsId_list","")
    #把id变成字符串
    goodsID = "%d"%goods.id
    if goodsID_list_str != "":
        #拆分字符串成数组
        goodsID_list = goodsID_list_str.split(',')
        #如果id已经存在 就删除，重新添加到最前面
        if goodsID_list.count(goodsID) >=1:
            goodsID_list.remove(goodsID)
        #注意！！有坑，不是修改goodsID_list[0] 而是插入一个id到0的位置
        goodsID_list.insert(0,goodsID)
        #如果数组长度大于5 移除最后一个
        if len(goodsID_list)>5:
            del goodsID_list[5]
        #最后再拼成字符串
        goodsID_list_str = ','.join(goodsID_list)
    else:
        #直接添加
        goodsID_list_str = goodsID

    #最后写入cookie
    httpResponse.set_cookie("goodsId_list",goodsID_list_str)


    return httpResponse
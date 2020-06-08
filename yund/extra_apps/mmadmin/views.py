from django.shortcuts import render
from shops.models import *
from shops.serializers import *
# Create your views here.

def Login(request):
    if request.method == "POST":
        name='123456@qq.com'
        password='123'
        request_data=request.POST
        if request_data.get('name') == name and request_data.get('password') == password:
            return render(request, 'admins/index.html')
        else:
            return HttpResponse('账号密码错误')

    return render(request, 'admins/login.html')


def Goodsinfo(request):
    g_data=Goods.objects.all()
    g_ser=GoodsSerializer(g_data,many=True)
    return render(request, 'admins/goods-info.html',{'data':g_ser.data})

def Cateringinfo(request):
    c_data=Catering_goods.objects.all()
    c_ser=Catering_goodsModelSerializers(c_data,many=True)
    return render(request, 'admins/catering-info.html',{'data':c_ser.data})



"""
接受
查数据

"""

def isHtmls(request):
    """
    接受数据 渲染html
    """
    datas=[
        '1.购买时间是否要花钱',
        '2.购买时间是否要花钱',
        '3.购买时间是否要花钱'
    ]
    return render(request, 'admins/ishtmls.html',{'data':datas,'title':'我是一个头'})
    



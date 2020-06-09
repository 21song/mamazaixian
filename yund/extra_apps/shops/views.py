from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from .models import *
from home.models import *
from django.views import View
from django.db.models import Q
import json
from datetime import datetime
import time
from django.contrib.auth.hashers import make_password,check_password
from yund import settings
import os
from rest_framework.response import Response
from .serializers import *
from rest_framework.views import APIView
import json
import random
import http.client
import urllib
from AgentLogin import AgentLogin
import requests
import sys
import ssl
from urllib import request,parse
from .utilsd import *

class Addimg(APIView):
    """上传图片
    {'img':}
    """
    def post(self,request):
        img = request.FILES.get('img')
        upload_allimg(img)
        return Response('ok')

class Fixed_position(APIView):
    """位置定位(no)
    """
    def get(self,request):
        mes={}
        url="http://api.map.baidu.com/location/ip?ak=bMpFLIrqygYl8h5DbVBuX61wVKyuqIN2&coor=bd09ll"
        response=requests.get(url)
        result=json.loads(response.text)

        mes["code"]=200
        mes["data"]=result
        return Response(mes)

class Wqw_Login(APIView):
    """
    第三方登陆url
    data: {type:0微博1QQ2微信,app_url:app填的回调url}
    
    返回：url
    """
    def post(self,request):
        mes={}
        type=request.POST.get("type")
        if type == 0: # 微博
            url=AgentLogin.weibo_url("APPID", "app填的回调url" )
        elif type == 1: # QQ
            url=AgentLogin.qq_url("APPID", "app填的回调url" )
        elif type == 2: # 微信
            url=AgentLogin.weixin_url("APPID", "app填的回调url" )
        mes['code']="200" 
        mes['data']=url
        return Response(mes)

"""
第三方登陆成功
code: 用户授权登录回调参数code client_id:腾讯开放平台上app的APPID名 client_secret: 腾讯开放平台上app的secret名 redirect_uri: 腾讯开放平台上app的回调url user: 返回qq的用户名
weibo_name =AgentLogin.weibo(client_id, client_secret, redirect_uri, code)
qq_name=AgentLogin.qq(client_id, client_secret, redirect_uri, code)
weixin_name=AgentLogin.weixin(client_id, client_secret, code)
"""

class Send_s(APIView):
    """发送短信验证码
    {
        tep: 电话号码
    }
    
    """
    def post(self,request):
        mes={}
        tep=request.POST.get('tep')
        str=sends(tep)
        mes['code']="200" 
        mes['str']=str
        mes['data']="发送成功"
        return Response(mes)

class Login(APIView):
    """1-登陆
    {
        tep:电话号码,
        name:mm账号,
        password:密码
    }
    """
    authentication_classes = []
    def post(self,request):
        mes={}
        name=request.POST.get('name')
        pwd=request.POST.get('password')
        tep=request.POST.get('tep')
        try:
            if tep:
                user_tep=Users.objects.filter(tep=tep).first()
                if user_tep:
                    str=sends(tep)
                    mes['code']="200"
                    mes['data']=str
                else:
                    mes['code']="1" 
                    mes['data']="该手机号未注册"
            elif name:
                user_obj=Users.objects.filter(mmh=name).first()
                if pwd:
                    pwd_v=check_password(pwd,user_obj.password)
                    if pwd_v == True:
                        payload = {
                            "id": user_obj.id,
                            "name": user_obj.name,
                        }
                        token = get_token(payload,5)
                        mes['code']="200"
                        mes['data']=token
                    else:
                        mes['code']="1"
                        mes['data']="密码错误"
                else:
                    mes['code']="1"
                    mes['data']="密码不能为空"
            else:
                mes['code']="1"
                mes['data']="不能为空"
        except:
            mes['code']=0
            mes['msg']='服务异常'
        return Response(mes)

class Register(APIView):
    """3-注册
    {
        tep: 电话号,
        pwd: 密码
    }
    """
    authentication_classes = []
    def post(self,request):
        mes={}
        tep=request.POST.get('tep')
        pwd=request.POST.get('pwd')
        try:
            if tep and pwd:
                user_tep=Users.objects.filter(tep=tep).first()
                if user_tep:
                    mes['code']="1" 
                    mes['data']="用户已存在"
                else:
                    pwd=make_password(pwd)
                    num=ninthnum()
                    Users.objects.create(tep=tep,password=pwd,mmh=num,name=tep).save()
                    mes['code']="200"
                    mes['data']="注册成功"
            else:
                mes['code']="1" 
                mes['data']="不能为空"
        except:
            mes['code']=0
            mes['msg']='服务异常'
        return Response(mes)

class Upwd(APIView):
    """6-设置新密码
    {
        uid: 用户id,
        pwd: 密码,
        pwd2: 密码2
    }
    """
    def post(self,request):
        mes={}
        uid=request.POST.get('uid')
        pwd=request.POST.get('pwd')
        pwd2=request.POST.get('pwd2')
        try:
            if pwd == pwd2:
                Users.objects.filter(id=uid).update(password=make_password(pwd))
                mes['code']="200" 
                mes['data']="修改成功"
            else:
                mes['code']="1" 
                mes['data']="密码不一致"
        except:
            mes['code']=0
            mes['msg']='服务异常'
        return Response(mes)


# 1-定位(no)

class Address_list(APIView):
    """1-选择定位(用户地址信息)
    {
        uid:用户id
    }
    """
    def get(self,request):
        mes={}
        uid=request.GET.get("uid")
        try:
            if uid:
                a_list=Users_address.objects.filter(user_id=uid).all()
                Address_serializer=Address_listModelSerializer(a_list,many=True)
                mes['code']=200
                mes['data']=Address_serializer.data
            else:
                mes['code']=1
                mes['data']="用户id?"
        except:
            mes['code']=0
            mes['msg']='服务异常'
        return Response(mes)

class Type_move(APIView):
    """3-个人入驻(入驻分类信息)
    """
    def get(self,request):
        mes={}
        assemble_t_list=Assemble_type.objects.all()
        assemble_tserializer=Assemble_typeModelSerializer(assemble_t_list,many=True)
        mes['code']=200
        mes['data']=shop_tserializer.data
        return Response(mes)   

class Add_move(APIView):
    """3-个人入驻(添加)
    {
        uid: 用户id,
        name: 入驻人姓名,
        idcard: 身份证号,
        age: 年龄,
        tep: 手机号,
        address: 地址,
        emil: 邮箱,
        t_id: 入驻类型id,
        cname:公司名称,
        cpic:公司头像,
        ccontent:公司简介
    }
    3
    """
    def post(self,request):
        mes={}
        datas=request.POST
        uid=request.POST.get('uid')
        name=request.POST.get('name')
        idcard=request.POST.get('idcard')
        age=request.POST.get('age')
        tep=request.POST.get('tep')
        address=request.POST.get('address')
        emil=request.POST.get('emil')
        t_id=request.POST.get('t_id')
        cname=datas.get('cname')
        cpic=datas.get('cpic')
        ccontent=datas.get('ccontent')
        
        if len(datas) >= 11:
            try:
                Move_into.objects.create(
                    user_id=uid,
                    name=name,
                    idcard=idcard,
                    age=age,
                    tep=tep,
                    address=address,
                    emil=emil,
                    t_id=t_id,
                    status=0
                ).save()

                Company.objects.create(
                    user_id=uid,
                    name=cname,
                    pic=cpic,
                    details=ccontent,
                    t_id=t_id
                ).save()
                mes['code']=200
                mes['data']="添加成功"
            except:
                mes['code']=0
                mes['msg']='服务异常'
        else:
            mes['code']=1
            mes['data']="有未填参数"
        return Response(mes)

# 3-个人入驻-人脸识别(no)

class Add_moves(APIView):
    """4-企业入驻(添加)
    {
        uid: 用户id,
        name: 法人姓名,
        idcard: 法人身份证号,
        age: 年龄,
        pwd: 密码,
        tep: 手机号,
        address: 公司地址,
        emil: 邮箱,
        t_id: 公司类别id,
        cname: 公司名称,
        cpic:公司头像,
        ccontent:公司简介
    }
    
    """
    def post(self,request):
        mes={}
        datas=request.POST
        user_id=request.POST.get('uid')
        name=request.POST.get('name')
        names=request.POST.get('cname')
        idcard=request.POST.get('idcard')
        age=request.POST.get('age')
        pwd=request.POST.get('pwd')
        tep=request.POST.get('tep')
        address=request.POST.get('address')
        emil=request.POST.get('emil')
        t_id=request.POST.get('t_id')
        cpic=datas.get('cpic')
        ccontent=datas.get('ccontent')

        if len(datas) >= 13:
            try:
                Move_intos.objects.create(
                    user_id=uid,
                    name=name,
                    idcard=idcard,
                    names=names,
                    age=age,
                    tep=tep,
                    address=address,
                    emil=emil,
                    t_id=t_id,
                    pwd=pwd,
                    status=0
                ).save()

                Company.objects.create(
                    user_id=uid,
                    name=cname,
                    pic=cpic,
                    details=ccontent,
                    t_id=t_id
                ).save()

                num=ninthnum()
                Users.objects.create(tep=tep,password=pwd,mmh=num,name=tep).save()

                mes['code']=200
                mes['data']="添加成功"
            except:
                mes['code']=0
                mes['msg']='服务异常'
        else:
            mes['code']=1
            mes['data']="有未填参数"
        return Response(mes)

# 审核状态
class Examines(APIView):
    """查看审核状态
    {
        type: 0个人入驻 1企业入驻,
        id: 入驻id    
    }
    """
    def post(self,request):
        mes={}
        type=request.POST.get('type')
        id=request.POST.get('id')
        try:
            if int(type) == 0:
                status=Move_into.objects.filter(id=id).values("status")
                if status[0]['status'] == 2:
                    e_id=Move_into.objects.filter(id=id).values("e_id")
                    e_id=e_id[0]['e_id'].split(",")
                    e_list=[]
                    for i in e_id:
                        e_list.append(Examine.objects.filter(id=i).values("name"))
                    mes['code']=1
                    mes['data']="审核未通过"
                    mes['datas']=e_list
                elif status[0]['status'] == 1:
                    mes['code']=200
                    mes['data']="通过审核"
                else:
                    mes['code']=2
                    mes['data']="审核中"

            elif int(type) == 1:
                status=Move_intos.objects.filter(id=id).values("status")
                if status[0]['status'] == 2:
                    e_id=Move_intos.objects.filter(id=id).values("e_id")
                    e_id=e_id[0]['e_id'].split(",")
                    e_list=[]
                    for i in e_id:
                        e_list.append(Examine.objects.filter(id=i).values("name"))
                    mes['code']=1
                    mes['data']="审核未通过"
                    mes['datas']=e_list
                elif status[0]['status'] == 1:
                    mes['code']=200
                    mes['data']="通过审核"
                else:
                    mes['code']=2
                    mes['data']="审核中"
        except:
            mes['code']=0
            mes['msg']='服务异常'
        
        return Response(mes)


# 扫描二维码(no)

# 主页-介绍(15-主页-联系方案二))
class Recommend(APIView):
    """主页-介绍
    """
    def get(self,request):
        mes={}
        try:
            gcompany_list=Gcompany.objects.all()
            gcompany_list_tserializer=Gcompany_listModelSerializer(gcompany_list,many=True)
            mes['code']=200
            mes['data']=gcompany_list_tserializer.data
        except:
            mes['code']=0
            mes['msg']='服务异常'
        return Response(mes)

class Announcements(APIView):
    """8-公告"""
    def get(self,request):
        mes={}
        try:
            announcement_list=Announcement.objects.all()
            Announcement_list_tserializer=Announcement_listModelSerializer(announcement_list,many=True)
            mes['code']=200
            mes['data']=Announcement_list_tserializer.data
        except:
            mes['code']=0
            mes['msg']='服务异常'
        return Response(mes)

class Announcementsinfo(APIView):
    """9-公告详情
    {
        id: 公告id
    }
    
    """
    def post(self,request):
        id=request.POST.get('id')
        mes={}
        try:
            announcement_list=Announcement.objects.filter(id=id)
            announcement_list_tserializer=Announcement_listModelSerializer(announcement_list,many=True)
            mes['code']=200
            assert Announcement_list_tserializer.data != []
            mes['data']=announcement_list_tserializer.data
        except:
            mes['code']=0
            mes['msg']='服务异常'
        return Response(mes)

class Clauseinfo(APIView):
    """10-条款"""
    def get(self,request):
        mes={}
        try:
            clause_list=Clause.objects.all()
            clause_list_tserializer=Clause_listModelSerializer(clause_list,many=True)
            mes['code']=200
            mes['data']=clause_list_tserializer.data
        except:
            mes['code']=0
            mes['msg']='服务异常'
        return Response(mes)

class Helplist(APIView):
    """11-帮助"""
    def get(self,request):
        mes={}
        try:
            help_list=Help.objects.all()
            help_list_tserializer=HelpModelSerializer(help_list,many=True)
            mes['code']=200
            mes['data']=help_list_tserializer.data
        except:
            mes['code']=0
            mes['msg']='服务异常'
        return Response(mes)

class Helpinfo(APIView):
    """12-帮助详情
    {
        id: 帮助id
    }
    """
    def post(self,request):
        id=request.POST.get('id',None)
        mes={}
        try:
            help_list=Help.objects.filter(id=id)
            help_list_tserializer=HelpModelSerializer(help_list,many=True)
            mes['code']=200
            assert help_list_tserializer.data != []
            mes['data']=help_list_tserializer.data
        except:
            mes['code']=0
            mes['msg']='服务异常'
        return Response(mes)

class Qfeedbackcreate(APIView):
    """13-问题反馈
    {
        name: 留言
        tep: 电话
    }
    
    """
    def post(self,request):
        name=request.POST.get('name',None)
        tep=request.POST.get('tep',None)
        mes={}
        try:
            Qfeedback.objects.create(tep=tep,details=name).save()
            mes['code']=200
            mes['data']="添加成功"
        except:
            mes['code']=0
            mes['msg']='服务异常'
        return Response(mes)

# 14-主页-聊天(no)


class Searchs(APIView):
    """1-搜索
    {
        'uid':用户id
        'name': 搜索内容
    }
    """
    def get(self,request):
        mes={}
        name=request.GET.get('name')
        uid=request.GET.get('uid')
        try:
            num=1
            Search_take_notes.objects.create(name=name,uid=uid).save()
            st_data=Search_take_notes.objects.filter(name=name).order_by('id').first()
            num+=int(st_data.nums)
            Search_take_notes.objects.filter(name=name).update(nums=num)

            goods_data=Goods.objects.filter(Q(name__icontains=name),Q(is_del=0))
            goods_ser=GoodsModelSerializer(goods_data,many=True)
            goods_datas=tags(goods_ser.data)
            mes['code']=200
            mes['data']=goods_datas
        except:
            mes['code']=0
            mes['msg']='服务异常'

        return Response(mes)

class Search_takeinfo(APIView):
    """1-搜索历史信息
    {
        uid: 用户id
    }
    
    """
    def get(self,request):
        mes={}
        uid=request.GET.get("uid")
        try:
            search_take_notes_list=Search_take_notes.objects.filter(uid=uid)
            search_take_notes_list_tserializer=Search_take_notesModelSerializer(search_take_notes_list,many=True)
            mes['code']=200
            assert search_take_notes_list_tserializer.data != []
            mes['data']=search_take_notes_list_tserializer.data
        except:
            mes['code']=0
            mes['msg']='服务异常'

        return Response(mes)

class Search_takedelete(APIView):
    """1-搜索历史清空
    {
        uid: 用户id,
        sid: 记录id
    }

    """
    def post(self,request):
        mes={}
        uid=request.POST.get("uid")
        sid=request.POST.get("sid")
        if sid:
            try:
                Search_take_notes.objects.filter(uid=uid,id=sid).delete()
                mes['code']=200
                mes['data']="删除成功"
            except:
                mes['code']=0
                mes['msg']='服务异常'
        else:
            try:
                Search_take_notes.objects.filter(uid=uid).delete()
                mes['code']=200
                mes['data']="清空成功"
            except:
                mes['code']=0
                mes['msg']='服务异常'

        return Response(mes)

class Search_lenovo(APIView):
    """2-搜索联想
    {
        'name':搜索字
    }
    """
    def get(self,request):
        mes={}
        name=request.GET.get('name')
        try:
            st_data=Search_take_notes.objects.filter(name__istartswith=name).order_by('-nums').values('name').distinct()[:5]
            mes['code']=200
            mes['data']=st_data
        except:
            mes['code']=0
            mes['msg']='服务异常'    
        return Response(mes)


class Userinfo(APIView):
    """5-我的-设置-个人资料
    {
       'uid': 用户id 
    }
    """
    def get(self,request):
        mes={}
        uid=request.GET.get("uid")
        try:
            userinfo=Users.objects.filter(id=uid)
            userinfo_ser=UserinfoModelSerializer(userinfo,many=True)          
            mes['code']=200
            mes['data']=userinfo_ser.data
        except:
            mes['code']=0
            mes['msg']='服务异常'

        return Response(mes)

class Users_address_info(APIView):
    """5-我的-设置-管理收货地址
    {
       'uid': 用户id 
    }
    """
    def get(self,request):
        mes={}
        uid=request.GET.get('uid')
        try:
            ua_data=Users_address.objects.filter(user_id=uid)
            ua_ser=Users_addressModelSerializer(ua_data,many=True)          
            mes['code']=200
            mes['data']=ua_ser.data
        except:
            mes['code']=0
            mes['msg']='服务异常'

        return Response(mes)

class Users_address_add(APIView):
    """5-我的-设置-地址添加修改
    {
        'user_id':用户id,
        'name':收货人姓名,
        'tep':电话,
        'address':收货地址,
        'details':详细地址,
        'type':是否默认0否1是,
        'id':地址id有为编辑,无为新增
    }
    """
    def post(self,request):
        mes={}
        request_data=request.data
        aid=request_data.get('id')
        try:
            if aid:
                try:
                    Users_address.objects.filter(id=aid).update(
                        user_id=request_data.get('user_id'),
                        name=request_data.get('name'),
                        tep=request_data.get('tep'),
                        address=request_data.get('address'),
                        details=request_data.get('details'),
                        type=request_data.get('type')
                    )
                    mes['code']=200
                    mes['msg']='修改成功'
                except:
                    mes['code']=0
                    mes['msg']='修改异常'
            else:
                ua_ser=Users_addressSerializer(data=request_data)
                if ua_ser.is_valid():
                    user_obj=ua_ser.save()
                    mes['code']=200
                    mes['msg']='成功'
                else:
                    mes['code']=1
                    mes['msg']=ua_ser.errors
        except:
            mes['code']=0
            mes['msg']='修改异常'
        return Response(mes)

class Users_address_delete(APIView):
    """5-我的-设置-收货地址-删除
    {
        'aid':地址id
    }
    """
    def post(self,request):
        mes={}
        aid=request.POST.get('aid')
        try:
            Users_address.objects.filter(id=aid).delete()
            mes['code']=200
            mes['data']='成功'
        except:
            mes['code']=1
            mes['msg']='服务异常'
        return Response(mes)

class Users_address_type(APIView):
    """5-我的-设置-设为默认地址
    {
        'aid':地址id,
        'user_id':用户id
    }
    """
    def post(self,request):
        mes={}
        aid=request.POST.get('aid')
        user_id=request.POST.get('user_id')
        try:
            Users_address.objects.filter(type=1,user_id=user_id).update(type=0)
            Users_address.objects.filter(id=aid).update(type=1)
            mes['code']=200
            mes['data']='成功'
        except:
            mes['code']=1
            mes['msg']='服务异常'
        return Response(mes)

class User_utep(APIView):
    """我的-设置-修改手机号
    {
        'user_id':用户id,
        'tep':手机号
    }
    """
    def post(self,request):
        mes={}
        request_data=request.data
        user_id=request_data.get('user_id')
        tep=request_data.get('tep')
        try:
            Users.objects.filter(_id=user_id).update(tep=tep)
            mes['code']=200
            mes['data']='成功'
        except:
            mes['code']=1
            mes['msg']='服务异常'
        return Response(mes)


# 我的-设置-修改支付密码(no)


class Goods_info(APIView):
    """搜索-商品
     {'name':名称}
     """
    def get(self,request):
        mes={}
        name=request.GET.get('name')
        print(name)
        if name:
            try:
                goods_data=Goods.objects.filter(Q(name__icontains=name),Q(is_del=0))
                goods_ser=GoodsModelSerializer(goods_data,many=True)
                goods_datas=tags(goods_ser.data)
                mes['code']=200
                mes['data']=goods_datas
            except:
                mes['code']=1
                mes['msg']='服务异常'
        else:
            try:
                goods_data=Goods.objects.filter(is_del=0)
                goods_ser=GoodsModelSerializer(goods_data,many=True)
                goods_datas=tags(goods_ser.data)
                mes['code']=200
                mes['data']=goods_datas
                mes['msg']='未找到'
            except:
                mes['code']=1
                mes['msg']='服务异常'
        return Response(mes)

class Goods_list(APIView):
    """搜索-商品/筛选
    {
        'brand':品牌(0否1是),
        'old_new':0旧1新,
        'type':1私人2公司,
        'city':市
    }
    """
    def post(self,request):
        mes={}
        requset_data = request.data
        q=dfilter(requset_data)
        print(q)

        citylist=requset_data.get('city')
        # citylist=citylist.split(',')
        # print(citylist)
        goods_val=Goods.objects.filter(q)
        goods_ser=GoodsModelSerializer(goods_val,many=True)
        goods_datas=tags(goods_ser.data)
        mes['code']=200
        mes['data']=goods_datas
        return Response(mes)

class Goods_sort(APIView):# 距离排序(no)
    """搜索-商品/级别排序.
    {
        'name':名称,
        'star':星,
        'drills':钻,
        'crowns':冠,
        'sales_volume':销量,
        'price':价格,
        'status':0正序1倒序
    }
    """
    def post(self,request):
        mes={}
        requset_data = request.data
        status = requset_data.get('status')
        name = requset_data.get('name')
        strs = ''
        try:
            for i in requset_data:
                strs = i
                break
            if int(status) == 1:
                goods_val=Goods.objects.filter(Q(name__icontains=name),Q(is_del=0)).order_by('-'+strs)
            else:
                goods_val=Goods.objects.filter(is_del=0).order_by(strs)
            goods_ser=GoodsModelSerializer(goods_val,many=True)
            tag=tags(goods_ser.data)
            mes['code']=200
            mes['data']=tag
        except:
            mes['code']=0
            mes['msg']='服务异常'
        return Response(mes)



class Goods_details(APIView):
    """1-首页-搜索-商品详情
    {
        'g_id':商品id,
        'u_id':用户id
    }return:
    {
        'goods':当前商品信息,
        'is_collection':是否收藏,
        'comment':商品评价,
        'qa':问答,
        'recommend':推荐商品信息,
        'company':公司信息
    }
    """
    def get(self,request):
        mes={}
        gid=request.GET.get('g_id')
        uid=request.GET.get('u_id')
        try:
            g_list=Goods.objects.filter(id=gid)
            g_serializer=GoodsModelSerializer(g_list,many=True)

            co_data=Company.objects.filter(id=g_list[0].company_id).first()
            is_collection='未收藏'
            uc_data=User_collection.objects.filter(uid=uid,tid=co_data.t_id,g_id=gid)
            if uc_data:
                is_collection='收藏'
            
            s_c_list=Goods_comment_types.objects.filter(g_id=gid).values_list('t_id','type_count')
            s_c_lists=[]
            for i in s_c_list:
                s_c_dict={}
                name=Comment_type.objects.filter(id=i[0]).values("name")
                s_c_dict['name']=name[0]['name']
                s_c_dict['t_id']=i[0]
                s_c_dict['count']=i[1]
                s_c_lists.append(s_c_dict)

            qa=QA.objects.filter(g_id=gid).values('id','questions','answers')
            qa_list=[]
            if qa:
                for j in qa:
                    qa_dict={}
                    qa_dict['questions']=qa[0]['questions']
                    qa_dict['answers']=qa[0]['answers']
                    qa_list.append(qa_dict)
            else:
                mes['msg']='无问答信息'

            c_id=Goods.objects.filter(id=gid).values('company_id')
            s_t_list=Goods.objects.filter(Q(company_id=c_id[0]['company_id']),Q(is_del=0)).order_by('-sales_volume')[:3]
            s_t_ser=GoodsModelSerializer(s_t_list,many=True)

            c_data=Company.objects.filter(id=c_id[0]['company_id'])
            c_data_ser=CompanyModelSerializer(c_data,many=True)
            
            datas={
                'goods':g_serializer.data,
                'is_collection':is_collection,
                'comment':s_c_lists,
                'qa':qa_list,
                'recommend':s_t_ser.data,
                'company':c_data_ser.data
            }
            mes['code']=200
            mes['data']=datas
        except:
            mes['code']=0
            mes['msg']='服务异常'
        return Response(mes)

class Goods_collection(APIView):
    """1-首页-搜索-商品详情-收藏
    {
        'uid':用户id,
        'tid':总分类id,
        'g_id':商品id
    }
    """
    def post(self,request):
        mes={}
        try:
            request_data=request.data
            uc_ser=UcSerializer(data=request_data)
            if uc_ser.is_valid():
                user_obj=uc_ser.save()
                mes['code']=200
                mes['msg']="成功"
            else:
                mes['code']=1
                mes['msg']=uc_ser.errors
        except:
            mes['code']=0
            mes['msg']="服务异常"
        return Response(mes)

class Goods_collection_delete(APIView):
    """1-首页-搜索-商品详情-取消收藏
    {
        'uid':用户id,
        'g_id':商品id
    }
    """
    def post(self,request):
        mes={}
        try:
            request_data=request.data
            uid=request_data.get('uid')
            g_id=request_data.get('g_id')
            User_collection.objects.filter(uid=uid,g_id=g_id).delete()
            mes['code']=200
            mes['msg']="成功"
        except:
            mes['code']=0
            mes['msg']="服务异常"
        return Response(mes)

class Goods_reports(APIView):
    """1-首页-搜索-商品详情(举报)
    {
        'g_id':商品id,
        'name':举报内容,
        'uid':用户id
    }
    """
    def post(self,request):
        mes={}
        request_data=request.data
        greports_ser=GreportsSerializer(data=request_data)
        if greports_ser.is_valid():
            reports_obj=greports_ser.save()
            mes['code']=200
            mes['msg']='成功'
        else:
            mes['code']=1
            mes['msg']=greports_ser.errors

        return Response(mes)

class Goods_norms_data(APIView):
    """1-首页-搜索-商品详情(规格数据)
    {'g_id':商品id}
    """
    def get(self,request):
        mes={}
        gid=request.GET.get('g_id')
        try:
            goods_data=Goods_attribute_definition.objects.filter(g_id=gid).values_list('id','name')
            gdlist=[]
            for i in goods_data:
                gdict={}
                ga_data=Goods_attribute.objects.filter(type=i[0]).values('name')
                gdict[i[1]]=ga_data
                gdlist.append(gdict)
            gn_data=Goods_norms.objects.filter(g_id=gid)
            gn_list=[]
            for i in gn_data:
                gn_lis=[]
                ids=i.a_id.split(',')
                ga_data1=Goods_attribute.objects.filter(id=ids[0]).values('name')
                ga_data2=Goods_attribute.objects.filter(id=ids[1]).values('name')
                gn_lis.append(ga_data1[0]['name'])
                gn_lis.append(ga_data2[0]['name'])
                gn_lis.append(i.price)
                gn_lis.append(i.stock)
                gn_list.append(gn_lis)
                # {颜色:{尺码:31,吃码:32}}
                # is[[颜色,吃码,价格,库存],[颜色,吃码,价格,库存],[颜色,吃码,价格,库存]]
            datas={
                'data':gdlist,
                'norms':gn_list
            }
            mes['code']=200
            mes['data']=datas
        except:
            mes['code']=0
            mes['msg']='服务异常'
        return Response(mes)

class Goods_add_cart(APIView):
    """1-首页-商品详情-加入购物车
    {
        'user_id':用户id,
        'gid':商品id,
        'nums':数量,
        'gn_id':尺寸id  
    }
    """
    def post(self,requset):
        mes={}
        request_data=requset.data
        uid=request_data.get('user_id')
        count=request_data.get('nums')
        gn_id=request_data.get('gn_id')
        gid=request_data.get('gid')

        goods_data=Goods.objects.filter(id=gid)
        name=goods_data[0].name
        pics=goods_data[0].pics
        cid=goods_data[0].company_id

        c_data=Company.objects.filter(id=cid)
        cname=c_data[0].name

        gn_data=Goods_norms.objects.filter(id=gn_id)
        price=gn_data[0].price

        datas={
            'uid':uid,
            'name':name,
            'count':count,
            'price':price,
            'gn_id':gn_id,
            'pics':pics,
            'cid':cid,
            'cname':cname,
        }

        g_ser=Goods_cartSerializer(data=datas)
        if g_ser.is_valid():
            reports_obj=g_ser.save()
            mes['code']=200
            mes['msg']='成功'
        else:
            mes['code']=1
            mes['msg']=g_ser.errors
        return Response(mes)

class Goods_details_comment(APIView):
    """1-首页-商品详情-评价
    {'g_id':商品id}
    """
    def get(self,request):
        mes={}
        gid=request.GET.get('g_id')

        c_date=Comment.objects.filter(g_id=gid).values('rank')
        num=0
        for i in c_date:
            num+=int(i['rank'])
        nums=num/len(c_date)
        nums=round(nums)

        s_c_list=Goods_comment_types.objects.filter(g_id=gid).values_list('t_id','type_count')
        s_c_lists=[]
        for i in s_c_list:
            s_c_dict={}
            name=Comment_type.objects.filter(id=i[0]).values("name")
            s_c_dict['name']=name[0]['name']
            s_c_dict['t_id']=i[0]
            s_c_dict['count']=i[1]
            s_c_lists.append(s_c_dict)
        
        c_dateinfo=Comment.objects.filter(g_id=gid).order_by('-rank')[:10]
        c_dlist=[]
        for i in c_dateinfo:
            c_ddict={}
            u_data=Users.objects.filter(id=i.com_users_id).values('name','pic')
            c_ddict['name']=u_data[0]['name']
            c_ddict['pic']=u_data[0]['pic']
            c_ddict['rank']=i.rank
            c_ddict['content']=i.comments
            c_dlist.append(c_ddict)

        datas={
            'rank':nums,
            'comment':s_c_lists,
            'data':c_dlist

        }
        mes['code']=200
        mes['data']=datas
        return Response(mes)

class Goods_details_typeinfo(APIView):
    """1-首页-商品详情-评价(分类切换)
    {'g_id':商品id,
    't_id':分类id}
    """
    def get(self,request):
        mes={}
        gid=request.GET.get('g_id')
        tid=request.GET.get('t_id')
        try:
            c_dateinfo=Comment.objects.filter(g_id=gid,t_id=tid).order_by('-rank')
            c_dlist=[]
            for i in c_dateinfo:
                c_ddict={}
                u_data=Users.objects.filter(id=i.com_users_id).values('name','pic')
                c_ddict['name']=u_data[0]['name']
                c_ddict['pic']=u_data[0]['pic']
                c_ddict['rank']=i.rank
                c_ddict['content']=i.comments
                c_dlist.append(c_ddict)

            mes['code']=200
            mes['data']=c_dlist
        except:
            mes['code']=0
            mes['msg']='服务异常'
        return Response(mes)

class Goods_details_qainfo(APIView):
    """1-首页-商品详情-商品问答
    {'g_id':商品id}
    """
    def get(self,request):
        mes={}
        gid=request.GET.get('g_id')
        try:
            qa_data=QA.objects.filter(g_id=gid)
            qa_ser=QAModelSerializer(qa_data,many=True)
            mes['code']=200
            mes['data']=qa_ser.data
        except:
            mes['code']=0
            mes['msg']='服务异常'
        return Response(mes)

class Address_status(APIView):
    """1-首页-提交订单-默认收获地址信息
    {
        'user_id':用户id
    }
    """
    def get(self,request):
        mes={}
        uid=request.GET.get('user_id')
        gid=request.GET.get('gid')
        try:
            ua_val=Users_address.objects.filter(user_id=uid,type=1)
            ua_ser=Users_addressSerializer(ua_val,many=True)
            mes['code']=200
            mes['data']=ua_ser.data
        except:
            mes['code']=0
            mes['msg']='服务异常'

        return Response(mes)

class Submit_order_info(APIView):
    """1-首页-提交订单
    {
        'user_id':用户id,
        'gid':商品id,
        'nums':数量,
        'gn_id':尺寸id
    }
    """
    def post(self,request):
        mes={}
        request_data=request.data
        user_id=request_data.get('user_id')
        gid=request_data.get('gid')
        # 默认地址
        # 商品id
        # 商品数量
        # 商品金额
        # 邮费

        
        ua_val=Users_address.objects.filter(user_id=uid,type=1)
        ua_ser=Users_addressSerializer(ua_val,many=True)
        
        gid=gid.split(',')
        for i in gid:
            Goods.objects.filter(id=i).values('name','pics',)

        

        return Response(mes)

class Goods_infos(APIView):
    """7-前台管理-商品管理
    {'uid':用户id}
    """
    def post(self,request):
        mes={}
        uid=request.POST.get('uid')
        try:
            goods_val=Goods.objects.filter(Q(user_id=uid),Q(is_del=0))
            goods_ser=GoodsbfSerializer(goods_val,many=True)
            mes['code']=200
            mes['data']=goods_ser.data
        except:
            mes['code']=0
            mes['msg']='服务异常'
        return Response(mes)

class Goods_is_status(APIView):
    """7-商品上下架
    {'gid':商品id,
    'status':0下架1上架}
    """
    def post(self,request):
        mes={}
        gid=request.POST.get('gid')
        status_value=request.POST.get('status')
        try:
            Goods.objects.filter(id=gid).update(status=status_value)
            mes['code']=200
            mes['data']='成功'
        except:
            mes['code']=1
            mes['msg']='服务异常'
        return Response(mes)

class Goods_delete(APIView):
    """7-商品删除
    {'gid':商品id}
    """
    def post(self,request):
        mes={}
        gid=request.POST.get('gid')
        try:
            Goods.objects.filter(id=gid).update(is_del=1)
            mes['code']=200
            mes['data']='成功'
        except:
            mes['code']=1
            mes['msg']='服务异常'
        return Response(mes)

# 7-商品预览(no)商品详情页

class Goods_add(APIView):
    """7-前台管理-商品管理-添加修改商品
    {'name': 标题,
    'pics': 图片,
    'normsid':一级规格id,
    'norms_priceid':规格价格id,
    'qaid': 问答id,
    'prices': 运费,
    'sales_volume':销量,
    'old_new':新旧(旧0新1),
    'brand':品牌(0否1是),
    'place':发货地,
    's_details':详情,   
    'user_id':用户id,
    'type':1个人入驻2企业入驻,
    'id':商品id有为编辑,无为新增}
    """
    def post(self,request):
        mes={}
        request_data=request.data
        gid=request_data.get('id')
        user_id=request_data.get('user_id')
        normsid=request_data.get('normsid')
        if len(normsid) != 1:
            normsid=normsid.split(',')
        else:
            normsid=[normsid]
        norms_priceid=request_data.get('norms_priceid')
        if len(norms_priceid) != 1:
            norms_priceid=norms_priceid.split(',')
        else:
            norms_priceid=[norms_priceid]
        qaid=request_data.get('qaid')
        if len(qaid) != 1:
            qaid=qaid.split(',')
        else:
            qaid=[qaid]
        place=request_data.get('place')
        place=place.split(',')
        drill,crown,tid=0,0,0
        try:
            c_data=Company.objects.filter(user_id=user_id)
            if int(request_data.get('type')) == 1:
                drill=Move_into.objects.filter(user_id=user_id).values('drill')[0]['drill']
                crown=Move_into.objects.filter(user_id=user_id).values('crown')[0]['crown']
                tid=Move_into.objects.filter(user_id=user_id).values('t_id')[0]['t_id']
            elif int(request_data.get('type')) == 2:
                drill=Move_intos.objects.filter(user_id=user_id).values('drill')[0]['drill']
                crown=Move_intos.objects.filter(user_id=user_id).values('crown')[0]['crown']
                tid=Move_intos.objects.filter(user_id=user_id).values('t_id')[0]['t_id']
            else:
                mes['code']=0
                mes['msg']='type参数没有'
            pdict={'province':place[0],'city':place[1],'county':place[2],'drill':drill,'crown':crown,'company_id':c_data[0].id,'tid':tid}
            for i in request_data:
                rdict={}
                if type(request_data[i]) == str:
                    rdict[i]=request_data[i]
                else:
                    rdict[i]=request_data[i][0]
                request_data=dict(request_data,**rdict)
            request_data=dict(request_data,**pdict)
            if gid:
                try:
                    Goods.objects.filter(id=gid).update(
                        name=request_data.get('name'),
                        pics=request_data.get('pics'),
                        price=request_data.get('price'),
                        prices=request_data.get('prices'),
                        sales_volume=request_data.get('sales_volume'),
                        old_new=request_data.get('old_new'),
                        brand=request_data.get('brand'),
                        s_details=request_data.get('s_details'),
                        user_id=request_data.get('user_id'),
                        type=request_data.get('type'),
                        province=place[0],
                        city=place[1],
                        county=place[2]
                    )
                    mes['code']=200
                    mes['msg']='成功'
                except:
                    mes['code']=0
                    mes['msg']='服务修改异常'
            else:
                goods_ser=GoodsSerializer(data=request_data)
                if goods_ser.is_valid():
                    user_obj=goods_ser.save()
                    for i in normsid:
                        Goods_attribute_definition.objects.filter(id=i).update(g_id=user_obj.id)
                    for i in norms_priceid:
                        Goods_norms.objects.filter(id=i).update(g_id=user_obj.id)
                    for i in qaid:
                        QA.objects.filter(id=i).update(g_id=user_obj.id)
                    mes['code']=200
                    mes['msg']='成功'
                else:
                    mes['code']=1
                    mes['msg']=goods_ser.errors 
        except:
            mes['code']=0
            mes['msg']="服务异常"
        return Response(mes)

class Goods_qa_add(APIView):
    """7-前台管理-商品管理-问答添加
    {
        'questions':问题,
        'answers':答案
    }
    """
    def post(self,request):
        mes={}
        try:
            request_data=request.data
            goodsqa_ser=QaSerializer(data=request_data)
            if goodsqa_ser.is_valid():
                user_obj=goodsqa_ser.save()
                mes['code']=200
                mes['msg']=user_obj.id
            else:
                mes['code']=1
                mes['msg']=goodsqa_ser.errors 
        except:
            mes['code']=0
            mes['msg']="服务异常"
        return Response(mes)

class Goods_qa_info(APIView):
    """7-前台管理-商品管理-问答列表
    {
        'qaid':问答id
    }
    """
    def get(self,request):
        mes={}
        try:
            qaid=request.GET.get('qaid')
            if len(qaid) != 1:
                qaid=qaid.split(',')
            else:
                qaid=[qaid]
            qa_data=[]
            for i in qaid:
                qa_da=QA.objects.filter(id=i)
                qa_ser=QaSerializer(qa_da,many=True)
                qa_data.append(qa_ser.data)
            mes['code']=200
            mes['data']=qa_data
        except:
            mes['code']=0
            mes['msg']="服务异常"
        return Response(mes)

class Goods_qa_delete(APIView):
    """7-前台管理-商品管理-问答删除
    {
        'qid':问答id
    }
    """
    def post(self,request):
        mes={}  
        qid=request.POST.get('qid')
        try:
            QA.objects.filter(id=qid).delete()
            mes['code']=200
            mes['data']='成功'
        except:
            mes['code']=0
            mes['msg']='服务异常'
        return Response(mes)

class Goods_attribute_definition_add(APIView):
    """7-前台管理-商品管理-一级规格添加
    {
        'name':名称
    }
    """
    def post(self,request):
        mes={}
        try:
            request_data=request.data
            gad_ser=GadSerializer(data=request_data)
            if gad_ser.is_valid():
                user_obj=gad_ser.save()
                mes['code']=200
                mes['data']=user_obj.id
            else:
                mes['code']=1
                mes['msg']=gad_ser.errors 
        except:
            mes['code']=0
            mes['msg']="服务异常"
        return Response(mes)

class Goods_attribute_add(APIView):
    """7-前台管理-商品管理-二级规格添加
    {   
        'tid':一级规格id,
        'name':名称
    }
    """
    def post(self,request):
        mes={}
        try:
            request_data=request.data
            gad_ser=GaSerializer(data=request_data)
            if gad_ser.is_valid():
                user_obj=gad_ser.save()
                mes['code']=200
                mes['data']='OK'
            else:
                mes['code']=1
                mes['msg']=gad_ser.errors 
        except:
            mes['code']=0
            mes['msg']="服务异常"
        return Response(mes)

class Goods_attribute_info(APIView):    
    """7-前台管理-商品管理-规格列表
    {
        'tid':一级规格id
    }
    """
    def get(self,request):
        mes={}
        try:
            tid=request.GET.get('tid')
            if not tid:
                return Response({'mes':'tid呢?'})
            if len(tid) != 1:
                tid=tid.split(',')
            else:
                tid=[tid]
            tidlist=[]
            for i in tid:
                gad_da=Goods_attribute_definition.objects.filter(id=i).values('id','name','g_id')
                if not gad_da:
                    return Response({'code':200,'mes':'暂无数据'})
                gad_ser=GadSerializer(gad_da,many=True)
                gad_data=gad_ser.data
                ga_da=Goods_attribute.objects.filter(tid=i).values('id','name','tid')
                ga_ser=GaSerializer(ga_da,many=True)
                gad_data[0]['list']=ga_ser.data

                tidlist.append(gad_data)
            mes['code']=200
            mes['data']=tidlist
        except:
            mes['code']=0
            mes['msg']="服务异常"
        return Response(mes)

class Goods_attribute_definition_delete(APIView):
    """7-前台管理-商品管理-一级规格删除
    {
        'tid':一级规格id
    }
    """
    def post(self,request):
        mes={}  
        tid=request.POST.get('tid')
        try:
            Goods_attribute_definition.objects.filter(id=tid).delete()
            Goods_attribute.objects.filter(tid=tid).delete()
            mes['code']=200
            mes['data']='成功'
        except:
            mes['code']=0
            mes['msg']='服务异常'
        return Response(mes)

class Goods_attribute_delete(APIView):
    """7-前台管理-商品管理-二级规格删除
    {
        'tid':二级规格id
    }
    """
    def post(self,request):
        mes={}  
        tid=request.POST.get('tid')
        try:
            Goods_attribute.objects.filter(id=tid).delete()
            mes['code']=200
            mes['data']='成功'
        except:
            mes['code']=0
            mes['msg']='服务异常'
        return Response(mes)

class Goods_norms_add(APIView):
    """7-前台管理-商品管理-规格价格添加
    {
        'a_id':二级规格id,
        'price':价格,
        'stock':库存
    }
    """
    def post(self,request):
        mes={}
        try:
            request_data=request.data
            gn_ser=GnSerializer(data=request_data)
            if gn_ser.is_valid():
                user_obj=gn_ser.save()
                mes['code']=200
                mes['data']=user_obj.id
            else:
                mes['code']=1
                mes['msg']=gn_ser.errors 
        except:
            mes['code']=0
            mes['msg']="服务异常"

        return Response(mes)

class Goods_norms_delete(APIView):
    """7-前台管理-商品管理-规格价格删除
    {
        'nid':id(规格价格)
    }
    """
    def post(self,request):
        mes={}  
        nid=request.POST.get('nid')
        try:
            Goods_norms.objects.filter(id=nid).delete()
            mes['code']=200
            mes['data']='成功'
        except:
            mes['code']=0
            mes['msg']='服务异常'
        return Response(mes)




class Catering_info(APIView):
    """7-前台-餐饮简介
    {
        'uid':用户id,
        'type':1个人入驻2企业入驻
    }
    """
    def get(self,request):
        mes={}
        uid=request.GET.get('uid')
        type=request.GET.get('type')
        try: 
            c_data=Catering_shop.objects.filter(uid=uid,type=type)
            if c_data:
                c_ser=Catering_shopModelSerializers(c_data,many=True)
                mes['code']=200
                mes['data']=c_ser.data
            else:
                mes['code']=1
                mes['msg']="无数据"
        except:
            mes['code']=0
            mes['msg']="服务异常"
        return Response(mes)

class Catering_info_add(APIView):
    """7-前台-餐饮管理-简介添加修改
    {
    'uid':用户id,
    'place':餐厅地址,
    'tep':电话,
    'business_hours':营业时间,
    'details':详情,
    'type':1个人入驻2企业入驻,
    'id':店铺id有为编辑,无为新增
    }
    """
    def post(self,request):
        mes={}
        request_data=request.data
        uid=request_data.get('uid')
        cid=request_data.get('id')
        drill,crown=0,0
        if int(request_data.get('type')) == 1:
            drill=Move_into.objects.filter(user_id=uid).values('drill')[0]['drill']
            crown=Move_into.objects.filter(user_id=uid).values('crown')[0]['crown']
        elif int(request_data.get('type')) == 2:
            drill=Move_intos.objects.filter(user_id=uid).values('drill')[0]['drill']
            crown=Move_intos.objects.filter(user_id=uid).values('crown')[0]['crown']
        
        pdict={'drill':drill,'crown':crown}
        for i in request_data:
            rdict={}
            if type(request_data[i]) == str:
                rdict[i]=request_data[i]
            else:
                rdict[i]=request_data[i][0]
            request_data=dict(request_data,**rdict)
        request_data=dict(request_data,**pdict)
        if cid:
            try:
                Catering_shop.objects.filter(id=cid).update(
                    place=request_data['place'],
                    crown=crown,
                    drill=drill,
                    tep=request_data['tep'],
                    business_hours=request_data['business_hours'],
                    details=request_data['details'],
                    uid=request_data['uid'],
                    type=request_data['type']
                )
                mes['code']=200
                mes['msg']='修改成功'
            except:
                mes['code']=0
                mes['msg']='修改异常'
        else:
            catering_ser=Catering_shopSerializer(data=request_data)
            if catering_ser.is_valid():
                user_obj=catering_ser.save()
                mes['code']=200
                mes['msg']='添加成功'
            else:
                mes['code']=1
                mes['msg']=catering_ser.errors

        return Response(mes)

class Catering_type_info(APIView):
    """7-前台-餐饮管理-类别管理
    {
        'cid':店铺id
    }
    """
    def get(self,request):
        mes={}
        cid=request.GET.get('cid')
        try:
            ct_data=Catering_type.objects.filter(cid=cid)
            if ct_data:
                ct_ser=Catering_typeModelSerializers(ct_data,many=True)
                mes['code']=200
                mes['data']=ct_ser.data
            else:
                mes['code']=1
                mes['msg']="无数据"
        except:
            mes['code']=0
            mes['msg']="服务异常"
        return Response(mes)

class Catering_type_add(APIView):
    """7-前台-餐饮管理-类别管理添加
    {
        'cid':店铺id,
        'name':类别名称
    }
    """
    def post(self,request):
        mes={}
        request_data=request.data
        ct_ser=Catering_typeSerializer(data=request_data)
        if ct_ser.is_valid():
            user_obj=ct_ser.save()
            mes['code']=200
            mes['msg']='成功'
        else:
            mes['code']=1
            mes['msg']=ct_ser.errors


        return Response(mes)

class Catering_type_delete(APIView):
    """7-前台-餐饮管理-类别管理删除
    {
        'tid':类别id,
        'cid':店铺id
    }
    """
    def post(self,request):
        mes={}
        cid=request.POST.get('cid')
        tid=request.POST.get('tid')
        try:
            Catering_type.objects.filter(cid=cid,id=tid).delete()
            mes['code']=200
            mes['data']='成功'
        except:
            mes['code']=1
            mes['msg']='服务异常'
        return Response(mes)

class Catering_goods_info(APIView):
    """7-前台-餐饮管理
    {
        'cid':店铺id
    }
    """
    def get(self,request):
        mes={}
        cid=request.GET.get('cid')
        try:
            c_data=Catering_goods.objects.filter(Q(cid=cid),Q(is_del=0))
            if c_data:
                c_ser=Catering_goodsModelSerializers(c_data,many=True)
                mes['code']=200
                mes['data']=c_ser.data
            else:
                mes['code']=1
                mes['msg']="无数据"
        except:
            mes['code']=0
            mes['msg']="服务异常"
        return Response(mes)

class Catering_goods_delete(APIView):
    """7-前台-餐饮管理-餐饮删除
    {
        'gid':餐饮id,
        'cid':店铺id
    }
    """
    def post(self,request):
        mes={}
        gid=request.POST.get('gid')
        cid=request.POST.get('cid')
        try:
            Catering_goods.objects.filter(id=gid,cid=cid).update(is_del=1)
            mes['code']=200
            mes['data']='成功'
        except:
            mes['code']=1
            mes['msg']='服务异常'
        return Response(mes)

class Catering_goods_add(APIView):
    """7-前台-餐饮管理-添加编辑餐品
    {
        'cid':店铺id,
        'name':餐品名称,
        'pic':图片,
        'price':价格,
        'c_tid' 类别id,
        'id':餐饮商品id有为编辑,无为新增
    }
    """
    def post(self,request):
        mes={}
        request_data=request.data
        gid=request_data.get('id')
        cid=request_data.get('cid')
        drill,crown=0,0
        try:
            drill=Catering_shop.objects.filter(id=cid).values('drill')[0]['drill']
            crown=Catering_shop.objects.filter(id=cid).values('crown')[0]['crown']
            pdict={'drill':drill,'crown':crown}
            for i in request_data:
                rdict={}
                if type(request_data[i]) == str:
                    rdict[i]=request_data[i]
                else:
                    rdict[i]=request_data[i][0]
                request_data=dict(request_data,**rdict)
            request_data=dict(request_data,**pdict)

            if gid:
                try:
                    Catering_goods.objects.filter(id=gid).update(
                        cid=cid,
                        crown=crown,
                        drill=drill,
                        name=request_data['name'],
                        pic=request_data['pic'],
                        price=request_data['price'],
                        c_tid=request_data['c_tid']
                    )
                    mes['code']=200
                    mes['msg']='修改成功'
                except:
                    mes['code']=0
                    mes['msg']='修改异常'
            else:
                cg_ser=Catering_goodsSerializer(data=request_data)
                if cg_ser.is_valid():
                    user_obj=cg_ser.save()
                    mes['code']=200
                    mes['msg']='添加成功'
                else:
                    mes['code']=1
                    mes['msg']=cg_ser.errors
        except:
            mes['code']=1
            mes['msg']='服务异常'
        return Response(mes)


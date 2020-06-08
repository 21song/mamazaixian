from django.contrib import admin
from django.urls import path,re_path
from .views import *
#导入类视图模板模块
from django.views.generic import TemplateView


urlpatterns = [
    # # 发送验证码
    # path('send_s',Send_s.as_view()),
    # # 位置定位
    # path('fixed_position',Fixed_position.as_view()),

    # # 1-登陆
    # path('login',Login.as_view()),
    # # 3-注册
    # path('register',Register.as_view()),
    # # 第三方登陆url
    # path('wqw_Login',Wqw_Login.as_view()),
    # # 6-设置新密码
    # path('upwd',Upwd.as_view()),

    # # 添加规格信息
    # path('goodsnadd',Goodsnadd.as_view()),

    # # 1-选择定位(用户地址信息)
    # path('address_list',Address_list.as_view()),
    # # 3-个人入驻(入驻分类信息)
    # path('type_move',Type_move.as_view()),
    # # 3-个人入驻(添加)
    # path('add_move',Add_move.as_view()),
    # # 4-企业入驻(添加)
    # path('add_moves',Add_moves.as_view()),
    
    # # 查看审核状态
    # path('examines',Examines.as_view()),
    # # app介绍
    # path('recommend',Recommend.as_view()),
    # # 公告信息
    # path('announcements',Announcements.as_view()),

    # # 公告详情
    # path('anouncementsinfo',Announcementsinfo.as_view()),
    # # 条款信息
    # path('clauseinfo',Clauseinfo.as_view()),
    # # 帮助信息
    # path('helplist',Helplist.as_view()),
    # # 帮助详情
    # path('helpinfo',Helpinfo.as_view()),
    # # 添加反馈信息
    # path('qfeedbackcreate',Qfeedbackcreate.as_view()),

    # # 1-搜索
    # path('searchs',Searchs.as_view()),
    # # 1-搜索历史信息
    # path('search_takeinfo',Search_takeinfo.as_view()),
    # # 1-删除搜索历史
    # path('search_takedelete',Search_takedelete.as_view()),
    # # 1-搜索联想
    # path('search_lenovo',Search_lenovo.as_view()),

    # 搜索-商品
    path('goods_info',Goods_info.as_view()),
    # 搜索-商品/筛选    
    path('goods_list',Goods_list.as_view()),
    # 搜索-商品/级别排序
    path('goods_sort',Goods_sort.as_view()),

    # 1-首页-搜索-商品详情
    path('goods_details',Goods_details.as_view()),
    # 1-首页-搜索-商品详情(举报)
    path('goods_reports',Goods_reports.as_view()),
    # 1-首页-搜索-商品详情(规格数据)
    path('goods_norm_data',Goods_norms_data.as_view()),
    # 1-首页-商品详情-加入购物车
    path('goods_add_cart',Goods_add_cart.as_view()),
    # 1-首页-商品详情-评价
    path('goods_details_comment',Goods_details_comment.as_view()),
    # 1-首页-商品详情-评价(分类切换)
    path('goods_details_typeinfo',Goods_details_typeinfo.as_view()),
    # 1-首页-商品详情-商品问答
    path('goods_details_qainfo',Goods_details_qainfo.as_view()),
    # 1-首页-提交订单-默认收获地址信息
    path('address_status',Address_status.as_view()),
    # 1-首页



    # 5-我的-设置-个人资料
    path('userinfo',Userinfo.as_view()),
    # 5-我的-设置-管理收货地址
    path('users_address_info',Users_address_info.as_view()),
    # 5-我的-设置-地址添加修改
    path('users_address_add',Users_address_add.as_view()),
    # 5-我的-设置-地址删除
    path('users_address_delete',Users_address_delete.as_view()),
    # 5-我的-设置-设为默认地址
    path('users_address_type',Users_address_type.as_view()),
    # 我的-设置-修改手机号
    path('user_utep',User_utep.as_view()),



    # 7-前台管理-商品管理
    path('goods_infos',Goods_infos.as_view()),
    # 7-商品上下架
    path('goods_is_status',Goods_is_status.as_view()),
    # 7-商品删除
    path('goods_delete',Goods_delete.as_view()),
    # 7-前台管理-商品管理-商品添加修改
    path('goods_add',Goods_add.as_view()),

    # # 7-前台-餐饮管理简介
    # path('catering_info',Catering_info.as_view()),
    # # 7-前台-餐饮管理-简介添加修改
    # path('catering_info_add',Catering_info_add.as_view()),
    # # 7-前台-餐饮管理-类别管理
    # path('catering_type_info',Catering_type_info.as_view()),
    # # 7-前台-餐饮管理-类别管理添加
    # path('catering_type_add',Catering_type_add.as_view()),
    # # 7-前台-餐饮管理-类别管理删除
    # path('catering_type_delete',Catering_type_delete.as_view()),
    # # 7-前台-餐饮管理
    # path('catering_goods_info',Catering_goods_info.as_view()),
    # # 7-前台-餐饮管理-餐饮删除
    # path('catering_goods_delete',Catering_goods_delete.as_view()),
    # # 7-前台-餐饮管理-餐品添加编辑
    # path('catering_goods_add',Catering_goods_add.as_view()),

    

    # # 上传图片
    # path('addimg',Addimg.as_view()),

]
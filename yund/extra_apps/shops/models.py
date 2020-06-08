from django.db import models

# Create your models here.

from django.utils.html import format_html
from yund.settings import URL

class BaseModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        
        abstract = True


class Comment(BaseModel,models.Model):
    """商品评价详情表"""
    id = models.AutoField(primary_key=True)
    g_id = models.IntegerField(default=0,verbose_name='商品id')
    rank = models.IntegerField(default=0,verbose_name='评论星数')
    comments = models.CharField(max_length=255,verbose_name='评论内容')
    com_type_id = models.IntegerField(default=0,verbose_name='评论类别id')
    com_users_id = models.IntegerField(default=0,verbose_name='评论用户id')
    t_id = models.IntegerField(verbose_name='总分类id')
    # type = models.IntegerField(verbose_name='0商品评论1服务评论')

    class Meta: 
        db_table = "comment"
        verbose_name = "商品评价详情"
        verbose_name_plural = "商品评价详情"





class Comment_type(BaseModel,models.Model):
    """商品评价分类表"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255,verbose_name='分类名称')
    status = models.IntegerField(default=0,verbose_name='上架1下架0')
    sort = models.IntegerField(default=0,verbose_name='排序')

    class Meta: 
        db_table = "comment_type"
        verbose_name = "商品评价分类"
        verbose_name_plural = "商品评价分类"

class Goods(BaseModel,models.Model):
    """商品表"""
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(verbose_name='用户id')
    name = models.CharField(max_length=30,verbose_name='名称')
    status = models.IntegerField(default=1,verbose_name='上1下0架')
    star = models.IntegerField(default=0,verbose_name='星')
    drill = models.IntegerField(default=0,verbose_name='钻')
    crown = models.IntegerField(default=0,verbose_name='冠')
    price = models.DecimalField(max_digits=8, decimal_places=2,verbose_name='价格')
    color = models.CharField(max_length=255,verbose_name='颜色')
    size = models.CharField(max_length=255,verbose_name='尺寸')
    pic = models.CharField(max_length=255,verbose_name='图片',null=True, blank=True)
    pics = models.CharField(max_length=255,verbose_name='相册',null=True, blank=True)
    sales_volume = models.IntegerField(default=0,verbose_name='销量')
    prices = models.DecimalField(max_digits=8, decimal_places=2,verbose_name='运费')
    brand = models.CharField(max_length=255,verbose_name='品牌(0否1是)')
    old_new = models.IntegerField(default=1,verbose_name='旧0新1')
    company_id = models.IntegerField(default=0,verbose_name='公司id')
    province = models.CharField(max_length=30,verbose_name='省')
    city = models.CharField(max_length=30,verbose_name='市')
    county = models.CharField(max_length=30,verbose_name='县')
    comment_count = models.IntegerField(default=0,verbose_name='评价总数')
    s_details = models.CharField(max_length=255,verbose_name='详情')
    type = models.IntegerField(default=1,verbose_name='1个人入驻2企业入驻')
    is_del = models.IntegerField(default=0,verbose_name='0未删除1已删除')

    class Meta: 
        db_table = "goods"
        verbose_name = "商品"
        verbose_name_plural = "商品"

    def to_dict(self):
        dicts = {
            'id': self.id,
            'name':self.name,
            'status':self.status,
            'star':self.star,
            'drill':self.drill,
            'crown':self.crown,
            'price':self.price,
            'color':self.color,
            'size':self.size,
            'sales_volume':self.sales_volume,
            'brand':self.brand,
            'old_new':self.old_new,
            'company_id':self.company_id,
            'public_private':self.public_private,
            's_type_id':self.s_type_id,
            'comment_count':self.comment_count}
        return dicts


class Goods_comment_types(BaseModel,models.Model):
    """商品评价分类关联表"""
    id = models.AutoField(primary_key=True)
    t_id = models.IntegerField(default=0,verbose_name='评价分类id')
    g_id = models.IntegerField(default=0,verbose_name='商品id')
    type_count = models.IntegerField(default=0,verbose_name='分类评价总数')
    z_tid = models.IntegerField(default=0,verbose_name='总分类id')

    class Meta: 
        db_table = "goods_comment_types"
        verbose_name = "商品评价分类关联"
        verbose_name_plural = "商品评价分类关联"

class QA(BaseModel,models.Model):
    """商品问答表"""
    id = models.AutoField(primary_key=True)
    g_id = models.IntegerField(default=0,verbose_name='商品id')
    questions = models.CharField(max_length=255,verbose_name='问题')
    answers = models.CharField(max_length=255,verbose_name='答案')
    t_id = models.IntegerField(verbose_name='总分类id')

    class Meta: 
        db_table = "qa"
        verbose_name = "商品问答"
        verbose_name_plural = "商品问答"

class Goods_type(BaseModel,models.Model):
    """商品分类表"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30,verbose_name='分类名称')
    status = models.IntegerField(default=0,verbose_name='上架1下架0')

    class Meta: 
        db_table = "goods_type"
        verbose_name = "商品分类"
        verbose_name_plural = "商品分类"

class Goods_attribute(BaseModel,models.Model):
    """商品属性表"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30,verbose_name='属性名称')
    type = models.IntegerField(verbose_name='属性分类id')

    class Meta:
        db_table = "goods_attribute"

class Goods_norms(BaseModel,models.Model):
    """商品规格表"""
    id = models.AutoField(primary_key=True)
    g_id = models.IntegerField(verbose_name='商品id')
    a_id = models.CharField(max_length=255,verbose_name='属性id')
    price = models.DecimalField(max_digits=8, decimal_places=2,verbose_name='价格')
    stock = models.IntegerField(verbose_name='库存')
    
    class Meta:
        db_table = "goods_norms"

class Goods_attribute_definition(BaseModel,models.Model):
    """商品属性分类表"""
    id = models.AutoField(primary_key=True)
    g_id = models.IntegerField(verbose_name='商品id')
    name = models.CharField(max_length=255,verbose_name='属性分类名称')

    class Meta:
        db_table = "goods_attribute_definition"

class Goods_report_content(BaseModel,models.Model):
    """商品举报内容表"""
    id = models.AutoField(primary_key=True)
    uid = models.IntegerField(verbose_name='用户id')
    name = models.CharField(max_length=255,verbose_name="内容")
    g_id = models.IntegerField(verbose_name="商品id")

    class Meta:
        db_table = "goods_report_content"
        verbose_name = "商品举报内容"
        verbose_name_plural = "商品举报内容"

class Goods_cart(BaseModel,models.Model):
    """商品购物车"""
    id = models.AutoField(primary_key=True)
    uid = models.IntegerField(verbose_name='用户id')
    name = models.CharField(max_length=255,verbose_name="商品名称")
    count = models.IntegerField(verbose_name="商品数量")
    price = models.DecimalField(max_digits=8, decimal_places=2,verbose_name='价格')
    gn_id = models.IntegerField(verbose_name='商品规格id')
    pics = models.CharField(max_length=255,verbose_name="图片",null=True, blank=True)
    cid = models.IntegerField(verbose_name='公司id')
    cname = models.CharField(max_length=255,verbose_name="公司名称")

    class Meta:
        db_table = "goods_cart"
        verbose_name = "商品购物车"
        verbose_name_plural = "商品购物车"


class Goods_order(BaseModel,models.Model):
    """商品订单表"""
    id = models.AutoField(primary_key=True)
    uid = models.IntegerField(verbose_name='用户id')
    ono = models.CharField(max_length=255,verbose_name="订单编号")
    aid = models.IntegerField(verbose_name="收货地址id")
    content = models.CharField(max_length=255,verbose_name="订单备注")
    price = models.DecimalField(max_digits=8, decimal_places=2,verbose_name='订单总价')
    status =  models.IntegerField(verbose_name="订单状态(0待付款1待发货2待收货3已完成4退款中5退款成功)")
    pays = models.IntegerField(verbose_name="支付方式(0贡献值1微信支付)")
    logostics_no = models.CharField(max_length=255,verbose_name="物流单号")

    class Meta:
        db_table = "goods_order"
        verbose_name = "商品订单"
        verbose_name_plural = "商品订单"

class Goods_order_details(BaseModel,models.Model):
    """商品订单详情表"""
    id = models.AutoField(primary_key=True)
    oid = models.IntegerField(verbose_name='订单id')
    gc_name = models.CharField(max_length=255,verbose_name="商品公司名称")
    g_id = models.IntegerField(verbose_name="商品id")
    name = models.CharField(max_length=255,verbose_name="商品名称")
    pic = models.CharField(max_length=255,verbose_name="商品图片",null=True, blank=True)
    nums = models.IntegerField(verbose_name='数量')
    gn_id =  models.IntegerField(verbose_name="商品规格id")

    class Meta:
        db_table = "goods_order_details"
        verbose_name = "商品订单详情"
        verbose_name_plural = "商品订单详情"
    
class Goods_order_remove(BaseModel,models.Model):
    """商品订单退订表"""
    id = models.AutoField(primary_key=True)
    oid = models.IntegerField(verbose_name='订单id')
    uid = models.IntegerField(verbose_name='用户id')
    ono = models.CharField(max_length=255,verbose_name="订单编号")
    content = models.CharField(max_length=255,verbose_name="退款原因")
    price = models.DecimalField(max_digits=8, decimal_places=2,verbose_name='退款金额')
    pic = models.CharField(max_length=255,verbose_name="退款凭证")
    

    class Meta:
        db_table = "goods_order_remove"
        verbose_name = "商品订单退订"
        verbose_name_plural = "商品订单退订"


class Catering_shop(BaseModel,models.Model):
    """餐饮店铺表"""
    id = models.AutoField(primary_key=True)
    uid = models.IntegerField(verbose_name='用户id')
    place = models.CharField(max_length=255,verbose_name="餐厅地址")
    tep = models.CharField(max_length=255,verbose_name="电话")
    business_hours = models.CharField(max_length=255,verbose_name="营业时间")
    details = models.CharField(max_length=255,verbose_name="详情")
    star = models.IntegerField(default=0,verbose_name='星')
    drill = models.IntegerField(default=0,verbose_name='钻')
    crown = models.IntegerField(default=0,verbose_name='冠')
    type = models.IntegerField(default=1,verbose_name='1个人入驻2企业入驻')
    status = models.IntegerField(default=1,verbose_name='上1下0架')

    class Meta:
        db_table = "catering_shop"
        verbose_name = "餐饮店铺"
        verbose_name_plural = "餐饮店铺"

class Catering_type(BaseModel,models.Model):
    """餐饮分类表"""
    id = models.AutoField(primary_key=True)
    cid = models.IntegerField(verbose_name='店铺id')
    name = models.CharField(max_length=255,verbose_name="分类名称")
    status = models.IntegerField(default=1,verbose_name='上1下0架')

    class Meta:
        db_table = "catering_type"
        verbose_name = "餐饮分类"
        verbose_name_plural = "餐饮分类"

class Catering_goods(BaseModel,models.Model):
    """餐饮商品表"""
    id = models.AutoField(primary_key=True)
    cid = models.IntegerField(verbose_name='店铺id')
    name = models.CharField(max_length=255,verbose_name="餐品名称")
    pic = models.CharField(max_length=255,verbose_name='图片',null=True, blank=True)
    star = models.IntegerField(default=0,verbose_name='星')
    drill = models.IntegerField(default=0,verbose_name='钻')
    crown = models.IntegerField(default=0,verbose_name='冠')
    price = models.DecimalField(max_digits=8, decimal_places=2,verbose_name="餐品价格")
    c_tid = models.IntegerField(verbose_name="餐品分类id")
    is_del = models.IntegerField(default=0,verbose_name='0未删除1已删除')

    class Meta:
        db_table = "catering_goods"
        verbose_name = "餐饮商品"
        verbose_name_plural = "餐饮商品"


class Rotation_chart(BaseModel,models.Model):
    """轮播图"""
    id = models.AutoField(primary_key=True)
    pic = models.CharField(max_length=255,verbose_name='图片',default=0)
    sort = models.IntegerField(default=0,verbose_name='排序')

    def image_data(self):
        return format_html(
            '<img src="{}" style="width:80px;height:40px;"/>',
            URL+self.pic.url,
        )
    image_data.short_description = "图片"

    class Meta:  
        db_table = "rotation_chart"
        verbose_name = "轮播图"
        verbose_name_plural = "轮播图"

class Goods_t(models.Model):
    """xadmin自定义html"""
    class Meta:
        verbose_name = "商品规格设置"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.Meta.verbose_name

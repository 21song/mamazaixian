
#导包 导入序列化库
from rest_framework import serializers
#导入数据库 类
from .models import *
from home.models import *
from django.contrib.auth.models import Group

class UserGroupsSerializer(serializers.ModelSerializer):
    """
    用户组序列化类
    """
    class Meta:
        model = Group
        fields = "__all__"

#商品添加
class GoodsSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    name = serializers.CharField(max_length=30, error_messages={'max_length': '太长'})
    status = serializers.IntegerField(required=False)
    star = serializers.IntegerField(required=False)
    crown = serializers.IntegerField(required=False)
    price = serializers.DecimalField(max_digits=8, decimal_places=2,required=False)
    color = serializers.CharField(required=False)
    size = serializers.CharField(required=False)
    pic = serializers.CharField(required=False)
    pics = serializers.CharField(required=False)
    sales_volume = serializers.IntegerField(required=False)
    prices = serializers.DecimalField(max_digits=8, decimal_places=2,required=False)
    brand = serializers.CharField(max_length=255,required=False)
    old_new = serializers.IntegerField(required=False)
    company_id = serializers.IntegerField(required=False)
    public_private = serializers.IntegerField(required=False)#公0私1
    province = serializers.CharField(max_length=30,required=False)# 省
    city = serializers.CharField(max_length=30,required=False)# 市
    county = serializers.CharField(max_length=30,required=False)# 县
    comment_count = serializers.IntegerField(required=False) # 评价总数
    s_details = serializers.CharField(required=False)
    is_qa = serializers.IntegerField(required=False)# 是否问答
    type = serializers.IntegerField(required=False)#是否上线


    def validate(self, attrs):
        # 将qa信息添加到qa表
        if attrs.get('qa'):
            qa = attrs.pop('qa')
            # print()
        return attrs
    
    def create(self, validated_data):
        return Goods.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     instance.r_id = validated_data.get('r_id', instance.r_id)
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.status = validated_data.get('status', instance.status)
    #     instance.star = validated_data.get('star', instance.star)
    #     instance.crown = validated_data.get('crown', instance.crown)
    #     instance.price = validated_data.get('price', instance.price)
    #     instance.color = validated_data.get('color', instance.color)
    #     instance.size = validated_data.get('size', instance.size)
    #     instance.pic = validated_data.get('pic', instance.pic)
    #     instance.sales_volume = validated_data.get('sales_volume', instance.sales_volume)
    #     instance.prices = validated_data.get('prices', instance.prices)
    #     instance.brand = validated_data.get('brand', instance.brand)
    #     instance.old_new = validated_data.get('old_new', instance.old_new)
    #     instance.company_id = validated_data.get('company_id', instance.company_id)
    #     instance.public_private = validated_data.get('public_private', instance.public_private)
    #     instance.s_place_id = validated_data.get('s_place_id', instance.s_place_id)
    #     instance.comment_count = validated_data.get('comment_count', instance.comment_count)
    #     instance.s_details = validated_data.get('s_details', instance.s_details)
    #     instance.is_qa = validated_data.get('is_qa', instance.is_qa)
    #     instance.type = validated_data.get('type', instance.type)
    #     instance.save()
    #     return instance

    class Meta:
        model = Goods
        fields = '__all__'

#商品地址
class Users_addressSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=255,required=False)
    tep = serializers.CharField(max_length=30,required=False)
    address = serializers.CharField(max_length=255,required=False)
    details = serializers.CharField(max_length=255,required=False)
    type = serializers.IntegerField(default=0,required=False)

    def validate(self, attrs):
        return attrs
    
    def create(self, validated_data):
        return Users_address.objects.create(**validated_data)

    class Meta:
        model = Users_address
        fields = '__all__'


#商品问答表
class QaSerializer(serializers.ModelSerializer):
    questions = serializers.CharField(max_length=255,required=False)#问题
    answers = serializers.CharField(max_length=255,required=False)#答案

    def validate(self, attrs):
        return attrs
    
    def create(self, validated_data):
        return QA.objects.create(**validated_data)

    class Meta:
        model = QA
        fields = '__all__'

#商品属性分类
class GadSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255,required=False)#属性分类名称

    def validate(self, attrs):
        return attrs
    
    def create(self, validated_data):
        return Goods_attribute_definition.objects.create(**validated_data)
    class Meta:
        model = Goods_attribute_definition
        fields = '__all__'
    
#商品属性
class GaSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255,required=False)#属性分类名称
    tid = serializers.IntegerField(default=0,required=False)

    def validate(self, attrs):
        return attrs
    
    def create(self, validated_data):
        return Goods_attribute.objects.create(**validated_data)
    class Meta:
        model = Goods_attribute
        fields = '__all__'

            
#商品规格
class GnSerializer(serializers.ModelSerializer):
    a_id = serializers.CharField(max_length=255,required=False)
    price = serializers.DecimalField(max_digits=8, decimal_places=2,required=False)
    stock = serializers.IntegerField(default=0,required=False)

    def validate(self, attrs):
        return attrs
    
    def create(self, validated_data):
        return Goods_norms.objects.create(**validated_data)
    class Meta:
        model = Goods_norms
        fields = '__all__'


# 商品举报表
class GreportsSerializer(serializers.ModelSerializer):
    uid = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=255,required=False)
    g_id = serializers.IntegerField(required=False)
    def validate(self, attrs):
        return attrs
    
    def create(self, validated_data):
        return Goods_report_content.objects.create(**validated_data)

    class Meta:
        model = Goods_report_content
        fields = '__all__'

# 收藏表
class UcSerializer(serializers.ModelSerializer):
    uid = serializers.IntegerField(required=False)
    tid = serializers.IntegerField(required=False)
    g_id = serializers.IntegerField(required=False)
    def validate(self, attrs):
        return attrs
    
    def create(self, validated_data):
        return User_collection.objects.create(**validated_data)

    class Meta:
        model = User_collection
        fields = '__all__'



# 餐饮店铺
class Catering_shopSerializer(serializers.ModelSerializer):
    uid = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=255,required=False)
    g_id = serializers.IntegerField(required=False)
    rid = serializers.IntegerField(required=False)
    place = serializers.CharField(max_length=255,required=False)
    tep = serializers.CharField(max_length=255,required=False)
    business_hours = serializers.CharField(max_length=255,required=False)
    details = serializers.CharField(max_length=255,required=False)
    star = serializers.IntegerField(default=0,required=False)
    drill = serializers.IntegerField(default=0,required=False)
    crown = serializers.IntegerField(default=0,required=False)
    type = serializers.IntegerField(default=1,required=False)
    status = serializers.IntegerField(default=1,required=False)
    def validate(self, attrs):
        return attrs
    
    def create(self, validated_data):
        return Catering_shop.objects.create(**validated_data)

    class Meta:
        model = Catering_shop
        fields = '__all__'


# 餐饮分类
class Catering_typeSerializer(serializers.ModelSerializer):
    cid = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=255,required=False)
    def validate(self, attrs):
        return attrs
    
    def create(self, validated_data):
        return Catering_type.objects.create(**validated_data)

    class Meta:
        model = Catering_type
        fields = '__all__'

# 餐饮信息
class Catering_goodsSerializer(serializers.ModelSerializer):
    cid = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=255,required=False)
    pic = serializers.CharField(max_length=255,required=False)
    star = serializers.IntegerField(default=0,required=False)
    drill = serializers.IntegerField(default=0,required=False)
    crown = serializers.IntegerField(default=0,required=False)
    price = serializers.DecimalField(max_digits=8, decimal_places=2,required=False)
    c_tid = serializers.IntegerField(required=False)
    
    def validate(self, attrs):
        return attrs
    
    def create(self, validated_data):
        return Catering_goods.objects.create(**validated_data)

    class Meta:
        model = Catering_goods
        fields = '__all__'


# 公司信息
class CompanySerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(required=False)
    pic = serializers.CharField(max_length=255,required=False)
    name = serializers.CharField(max_length=30,required=False)
    title = serializers.CharField(max_length=255,required=False)
    details = serializers.CharField(max_length=255,required=False)
    sort = serializers.IntegerField(default=0,required=False)
    status = serializers.IntegerField(default=1,required=False)
    t_id = serializers.CharField(max_length=255,default=0,required=False)


    def validate(self, attrs):
        return attrs
    
    def create(self, validated_data):
        return Company.objects.create(**validated_data)

    class Meta:
        model = Company
        fields = '__all__'

# 商品购物车
class Goods_cartSerializer(serializers.ModelSerializer):
    uid = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=255,required=False)
    count = serializers.IntegerField(required=False)
    price = serializers.DecimalField(max_digits=8, decimal_places=2,required=False)
    gn_id = serializers.IntegerField(required=False)
    pics = serializers.CharField(max_length=255,required=False)
    cid = serializers.IntegerField(required=False)
    cname = serializers.CharField(max_length=255,required=False)

    def validate(self, attrs):
        return attrs
    
    def create(self, validated_data):
        return Goods_cart.objects.create(**validated_data)

    class Meta:
        model = Goods_cart
        fields = '__all__'

#---


#商品所有信息
class GoodsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = '__all__'

# 商品部分信息
class GoodsbfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = ('pic','name','price','id')

#分类评价数量
class Goods_comment_typeseModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods_comment_types
        
        fields = ('id','t_id','s_id','type_count')

# 商品分类
class GoodsTyprModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods_type
        
        fields = ('id','name')

# 公司信息
class CompanyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        
        fields = '__all__'

# 规格信息
class NormsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods_norms
        
        fields = '__all__'

# 用户地址
class Address_listModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users_address
        
        fields = '__all__'

# 官方表
class Gcompany_listModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gcompany
        
        fields = '__all__'

# 公告信息
class Announcement_listModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        
        fields = '__all__'

# 总分类
class Assemble_typeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assemble_type
        
        fields = '__all__'

# 轮播图
class Rotation_chart_listModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rotation_chart
        
        fields = '__all__'

# 条款
class Clause_listModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clause
        
        fields = '__all__'

# 帮助
class HelpModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Help
        
        fields = '__all__'

# 搜索记录
class Search_take_notesModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Search_take_notes
        
        fields = '__all__'

# 用户表
class UserinfoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        
        fields = ('name','login_time','star','drill','crown','pic','tep','mmh','wxh','wbh','qqh')
        
# 地址表
class Users_addressModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users_address
        
        fields = '__all__'

#商品所有信息
class QAModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = QA
        fields = '__all__'

#搜索历史表
class Search_take_notesModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Search_take_notes
        fields = '__all__'


# 餐饮店铺表
class Catering_shopModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Catering_shop
        fields = '__all__'

# 餐饮分类
class Catering_typeModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Catering_type
        fields = '__all__'

# 餐品信息
class Catering_goodsModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Catering_goods
        fields = '__all__'
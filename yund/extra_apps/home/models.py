from django.db import models

# Create your models here.
class BaseModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        
        abstract = True

class Users(BaseModel,models.Model):
    """用户表"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30,verbose_name='name')
    password = models.CharField(max_length=255,verbose_name='密码')
    login_time = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=1,verbose_name='状态')
    star = models.IntegerField(default=0,verbose_name='星')
    drill = models.IntegerField(default=0,verbose_name='钻')
    crown = models.IntegerField(default=0,verbose_name='冠')
    pic = models.CharField(max_length=1000,verbose_name='头像', null=True, blank=True)
    tep = models.CharField(max_length=30,verbose_name='电话号码')
    mmh = models.CharField(max_length=30,verbose_name='MM账号')
    wxh = models.CharField(max_length=30,verbose_name='微信号')
    wbh = models.CharField(max_length=30,verbose_name='微博号')
    qqh = models.CharField(max_length=30,verbose_name='qq号')
    type = models.IntegerField(default=0,verbose_name='0普通用户1个人入驻2企业入驻')

    class Meta:  
        db_table = "users"
        verbose_name = "用户"
        verbose_name_plural = "用户"

class Users_details(BaseModel,models.Model):
    """用户详细信息表"""
    id = models.AutoField(primary_key=True)
    u_id = models.ForeignKey(Users,verbose_name='用户id',related_name='u_details',on_delete=models.CASCADE)
    remaining_sum = models.IntegerField(default=0,verbose_name='贡献值')
    pwd = models.CharField(max_length=255,verbose_name='支付密码')

    class Meta: 
        db_table = "users_details"
        verbose_name = "用户详细信息"
        verbose_name_plural = "用户详细信息"

class Users_address(BaseModel,models.Model):
    """用户收获地址表"""
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(verbose_name='用户id')
    name = models.CharField(max_length=255,verbose_name='收件人')
    tep = models.CharField(max_length=30,verbose_name='电话号')
    address = models.CharField(max_length=255,verbose_name='地址名称')
    details = models.CharField(max_length=255,verbose_name='详情地址')
    type = models.IntegerField(default=0,verbose_name='是否默认0否1是')

    class Meta:
        db_table = "users_address"
        verbose_name = "用户收获地址"
        verbose_name_plural = "用户收获地址"

class Move_into(BaseModel,models.Model):
    """个人入驻表"""
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(verbose_name='用户id')
    name = models.CharField(max_length=255,verbose_name="入驻人姓名")
    idcard = models.CharField(max_length=255,verbose_name='身份证号')
    age = models.CharField(max_length=30,verbose_name='年龄')
    tep = models.CharField(max_length=30,verbose_name='电话号')
    address = models.CharField(max_length=255,verbose_name='地址名称')
    emil = models.CharField(max_length=255,verbose_name='邮箱')
    t_id = models.IntegerField(verbose_name='类型id')
    status = models.IntegerField(default=0,verbose_name='状态') #0审核中 1以通过 2未通过
    e_id = models.CharField(max_length=255,default=0,verbose_name='审核id')
    star = models.IntegerField(default=0,verbose_name='星')
    drill = models.IntegerField(default=0,verbose_name='钻')
    crown = models.IntegerField(default=0,verbose_name='冠')
    business_scope = models.CharField(max_length=255,default=0,verbose_name='经营范围')
    main_business = models.CharField(max_length=255,default=0,verbose_name='主营业务')
    after_sale_service = models.CharField(max_length=255,default=0,verbose_name='售后服务')
    service_info = models.CharField(max_length=255,default=0,verbose_name='服务介绍')

    class Meta:
        db_table = "move_into"
        verbose_name = "个人入驻"
        verbose_name_plural = "个人入驻"

class Move_intos(BaseModel,models.Model):
    """企业入驻表"""
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(verbose_name='用户id')
    name = models.CharField(max_length=255,verbose_name="法人姓名")
    idcard = models.CharField(max_length=255,verbose_name='法人身份证号')
    age = models.CharField(max_length=30,verbose_name='年龄')
    tep = models.CharField(max_length=30,verbose_name='电话号')
    emil = models.CharField(max_length=255,verbose_name='邮箱')
    names = models.CharField(max_length=255,verbose_name="企业名称")
    address = models.CharField(max_length=255,verbose_name='公司地址')
    t_id = models.CharField(max_length=255,verbose_name='类型id')
    pwd = models.CharField(max_length=255,verbose_name='密码')
    status = models.IntegerField(default=0,verbose_name='状态') #0审核中 1以通过 2未通过
    e_id = models.CharField(max_length=255,default=0,verbose_name='审核id')
    pic = models.CharField(max_length=255,verbose_name='图片',null=True, blank=True)
    star = models.IntegerField(default=0,verbose_name='星')
    drill = models.IntegerField(default=0,verbose_name='钻')
    crown = models.IntegerField(default=0,verbose_name='冠')
    business_scope = models.CharField(max_length=255,default=0,verbose_name='经营范围')
    main_business = models.CharField(max_length=255,default=0,verbose_name='主营业务')
    after_sale_service = models.CharField(max_length=255,default=0,verbose_name='售后服务')
    service_info = models.CharField(max_length=255,default=0,verbose_name='服务介绍')

    class Meta:
        db_table = "move_intos"
        verbose_name = "企业入驻"
        verbose_name_plural = "企业入驻"

class Company(BaseModel,models.Model):
    """公司表"""
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(verbose_name='用户id')
    pic = models.CharField(max_length=255,verbose_name='头像')
    name = models.CharField(max_length=30,verbose_name='名称')
    title = models.CharField(max_length=255,verbose_name='副标题')
    details = models.CharField(max_length=255,verbose_name='简介')
    sort = models.IntegerField(default=0,verbose_name='排序')
    status = models.IntegerField(default=1,verbose_name='上1下0架')
    t_id = models.CharField(max_length=255,default=0,verbose_name='分类id')

    class Meta: 
        db_table = "company"
        verbose_name = "公司"
        verbose_name_plural = "公司"

class Company_type(BaseModel,models.Model):
    """公司分类表"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30,verbose_name='分类名称')
    status = models.IntegerField(default=0,verbose_name='上架1下架0')

    class Meta: 
        db_table = "company_type"
        verbose_name = "公司分类"
        verbose_name_plural = "公司分类"



# class Examine(BaseModel,models.Model):
#     """审核类型表"""
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=255,verbose_name="审核内容")

#     class Meta:
#         db_table = "examine"
#         verbose_name = "审核信息"
#         verbose_name_plural = "审核信息"

class Gcompany(BaseModel,models.Model):
    """官方表"""
    id = models.AutoField(primary_key=True)
    weixin = models.CharField(max_length=255,verbose_name="官方微信")
    tep = models.CharField(max_length=30,verbose_name='客服电话')
    emil = models.CharField(max_length=255,verbose_name='公司邮箱')
    address = models.CharField(max_length=255,verbose_name='地址')
    details = models.CharField(max_length=255,verbose_name='平台介绍')

    class Meta:
        db_table = "gcompany"
        verbose_name = "官方信息"
        verbose_name_plural = "官方信息"

class Announcement(BaseModel,models.Model):
    """公告表"""
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255,verbose_name="公告标题")
    detail = models.CharField(max_length=255,verbose_name='副标题')
    details = models.CharField(max_length=255,verbose_name='详情')

    class Meta:
        db_table = "announcement"
        verbose_name = "公告信息"
        verbose_name_plural = "公告信息"

class Clause(BaseModel,models.Model):
    """条款表"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255,verbose_name="条款内容")

    class Meta:
        db_table = "clause"
        verbose_name = "条款信息"
        verbose_name_plural = "条款信息"

class Help(BaseModel,models.Model):
    """帮助表"""
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255,verbose_name="帮助问题")
    details = models.CharField(max_length=255,verbose_name="解决方法")

    class Meta:
        db_table = "help"
        verbose_name = "帮助"
        verbose_name_plural = "帮助"

class Qfeedback(BaseModel,models.Model):
    """问题反馈"""
    id = models.AutoField(primary_key=True)
    details = models.CharField(max_length=255,verbose_name="留言")
    tep = models.CharField(max_length=30,verbose_name='联系电话')

    class Meta:
        db_table = "qfeedback"
        verbose_name = "问题反馈"
        verbose_name_plural = "问题反馈"

class Search_take_notes(BaseModel,models.Model):
    """用户搜索记录"""
    id = models.AutoField(primary_key=True)
    uid = models.IntegerField(verbose_name='用户id')
    name = models.CharField(max_length=255,verbose_name="搜索记录")
    nums = models.IntegerField(default=0,verbose_name='搜索次数')

    class Meta:
        db_table = "search_take_notes"
        verbose_name = "用户搜索记录"
        verbose_name_plural = "用户搜索记录"

class User_collection(BaseModel,models.Model):
    """用户收藏表"""
    id = models.AutoField(primary_key=True)
    uid = models.IntegerField(verbose_name='用户id')
    tid = models.IntegerField(verbose_name='总分类id')
    g_id = models.IntegerField(verbose_name="商品id")

    class Meta:
        db_table = "user_collection"
        verbose_name = "用户收藏"
        verbose_name_plural = "用户收藏"

class Assemble_type(BaseModel,models.Model):
    """总分类表"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255,verbose_name='分类名称')#分类名称
    sort = models.IntegerField(default=0,verbose_name='排序')
    status = models.IntegerField(default=0,verbose_name='0下架1上架')

    class Meta: 
        db_table = "assemble_type"
        verbose_name = "总分类"
        verbose_name_plural = "总分类"



class QA(BaseModel,models.Model):
    """问答表"""
    id = models.AutoField(primary_key=True)
    g_id = models.IntegerField(default=0,verbose_name='商品id',null=True, blank=True)
    questions = models.CharField(max_length=255,verbose_name='问题')
    answers = models.CharField(max_length=255,verbose_name='答案')
    t_id = models.IntegerField(verbose_name='总分类id',null=True, blank=True,default=0)

    class Meta: 
        db_table = "qa"
        verbose_name = "问答"
        verbose_name_plural = "问答"


class Comment(BaseModel,models.Model):
    """评价详情表"""    
    id = models.AutoField(primary_key=True)
    g_id = models.IntegerField(default=0,verbose_name='商品id')
    rank = models.IntegerField(default=0,verbose_name='评论星数')
    comments = models.CharField(max_length=255,verbose_name='评论内容')
    com_type_id = models.IntegerField(default=0,verbose_name='评论类别id')
    com_users_id = models.IntegerField(default=0,verbose_name='评论用户id')
    t_id = models.IntegerField(verbose_name='总分类id')

    class Meta: 
        db_table = "comment"
        verbose_name = "评价详情"
        verbose_name_plural = "评价详情"





class Comment_type(BaseModel,models.Model):
    """评价分类表"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255,verbose_name='分类名称')
    status = models.IntegerField(default=0,verbose_name='上架1下架0')
    sort = models.IntegerField(default=0,verbose_name='排序')

    class Meta: 
        db_table = "comment_type"
        verbose_name = "评价分类"
        verbose_name_plural = "评价分类"


class Goods_comment_types(BaseModel,models.Model):
    """评价分类关联表"""
    id = models.AutoField(primary_key=True)
    t_id = models.IntegerField(default=0,verbose_name='评价分类id')
    g_id = models.IntegerField(default=0,verbose_name='商品id')
    type_count = models.IntegerField(default=0,verbose_name='分类评价总数')
    z_tid = models.IntegerField(default=0,verbose_name='总分类id')

    class Meta: 
        db_table = "goods_comment_types"
        verbose_name = "评价分类关联"
        verbose_name_plural = "评价分类关联"


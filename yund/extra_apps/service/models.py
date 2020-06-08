from django.db import models

class Service(models.Model):
    """
    服务表。
    """
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(verbose_name='用户ID')
    type = models.IntegerField(verbose_name='0普通or1个人or2企业')    # 0普通用户1个人入驻2企业入驻
    star = models.IntegerField(default=0, verbose_name='星')
    drill = models.IntegerField(default=0, verbose_name='钻')
    crown = models.IntegerField(default=0, verbose_name='冠')
    pics = models.TextField(verbose_name='相册',blank=True, null=True)
    title = models.CharField(max_length=60, verbose_name='服务标题')
    price = models.DecimalField(max_digits=15,decimal_places=2,verbose_name='服务价格')
    cost = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='上门费用')
    sales_volume = models.IntegerField(default=50,verbose_name='销量')
    ondoor = models.IntegerField(verbose_name='到店0or上门1or均可2')  # 1上门;0到店;2均可
    brand = models.IntegerField(verbose_name='品牌1or否0')    #是否品牌(1是；0否)
    place = models.CharField(max_length=128, verbose_name='服务地点')
    details = models.CharField(max_length=255, verbose_name='服务详情')
    status = models.IntegerField(verbose_name='上架1or下架0',default=1)   #是否上架(1上架；0下架)
    t_id = models.IntegerField(verbose_name='功能模块分类ID',default=2)  # 2就是服务；1是商品
    suspend_status = models.IntegerField(verbose_name='正常1or停用0',default=1)   # 正常1，假删0

    class Meta:
        db_table = "Service"
        verbose_name = verbose_name_plural = "服务表"

    def __str__(self):
        return str(self.title)


class ServiceStaff(models.Model):
    """
    服务团队人员表
    """
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(verbose_name='用户id')
    name = models.CharField(max_length=16, verbose_name='姓名')
    pic = models.CharField(max_length=64, verbose_name='头像')
    details = models.TextField(blank=True, null=True,verbose_name='成员描述')
    status = models.IntegerField(verbose_name='状态',default=1)  # 正常1；异常0


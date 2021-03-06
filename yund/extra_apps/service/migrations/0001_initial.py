# Generated by Django 2.0.4 on 2020-06-08 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.IntegerField(verbose_name='用户ID')),
                ('type', models.IntegerField(verbose_name='个人0or企业1')),
                ('star', models.IntegerField(default=0, verbose_name='星')),
                ('drill', models.IntegerField(default=0, verbose_name='钻')),
                ('crown', models.IntegerField(default=0, verbose_name='冠')),
                ('pics', models.TextField(blank=True, null=True, verbose_name='相册')),
                ('title', models.CharField(max_length=60, verbose_name='服务标题')),
                ('price', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='服务价格')),
                ('cost', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='上门费用')),
                ('sales_volume', models.IntegerField(default=50, verbose_name='销量')),
                ('ondoor', models.IntegerField(verbose_name='到店0or上门1or均可2')),
                ('brand', models.IntegerField(verbose_name='品牌1or否0')),
                ('place', models.CharField(max_length=128, verbose_name='服务地点')),
                ('details', models.CharField(max_length=255, verbose_name='服务详情')),
                ('status', models.IntegerField(default=1, verbose_name='上架1or下架0')),
                ('t_id', models.IntegerField(default=2, verbose_name='功能模块分类ID')),
                ('suspend_status', models.IntegerField(default=1, verbose_name='正常1or停用0')),
            ],
            options={
                'verbose_name': '服务表',
                'verbose_name_plural': '服务表',
                'db_table': 'Service',
            },
        ),
        migrations.CreateModel(
            name='ServiceStaff',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.IntegerField(verbose_name='用户id')),
                ('name', models.CharField(max_length=16, verbose_name='姓名')),
                ('pic', models.CharField(max_length=64, verbose_name='头像')),
                ('details', models.TextField(blank=True, null=True, verbose_name='成员描述')),
                ('status', models.IntegerField(default=1, verbose_name='状态')),
            ],
        ),
    ]

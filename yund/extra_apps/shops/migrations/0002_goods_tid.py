# Generated by Django 2.0.4 on 2020-06-08 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='goods',
            name='tid',
            field=models.IntegerField(default=0, verbose_name='总分类id'),
        ),
    ]

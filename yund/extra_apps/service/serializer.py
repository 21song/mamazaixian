from rest_framework import serializers
from .models import Service, ServiceStaff


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"


class ServiceSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = (
            "id",
            "title",
            "price",
            "pics",
            "star",
            "drill",
            "crown",
            "ondoor",
            "type",
            "brand",
        )

    # 对 序列化后的结果进行「自定义过滤」
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        pics = ret.pop("pics")
        pic = pics.split(',')[0]
        ret['pic'] = pic

        ondoor = ret.pop("ondoor")
        type = ret.pop("type")
        brand = ret.pop("brand")
        label_list = []
        if ondoor == 1:
            label_list.append('上门')
        elif ondoor == 2:
            label_list.extend(['上门', '到店'])
        else:
            label_list.append('到店')
        if type == 2:
            label_list.append('公司')
        else:
            label_list.append('个人')
        if brand == 1:
            label_list.append('品牌')
        ret['label_list'] = label_list
        return ret


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceStaff
        fields = "__all__"

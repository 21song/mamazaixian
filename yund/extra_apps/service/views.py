from django.shortcuts import render
from django.db.models import Q
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Service as ModelService
from .models import ServiceStaff as ModelServiceStaff
from .utils.pic_upload import upload,delete_img
from home.models import Users as ModelUsers
from home.models import QA as ModelQA
from home.models import Goods_comment_types, Comment_type, Comment
from .serializer import *

class Service(APIView):

    def get(self,request:Request):
        """
        查看某一服务
        需要参数：service_id
        """
        service_id = request.query_params.get('service_id')
        service = ModelService.objects.filter(id=service_id,is_del=0).first()
        service_data = ServiceSerializer(service).data

        context = {
            "msg": "查看服务成功",
            "service": service_data
        }
        return Response(context)

    def post(self,request:Request):
        """
        添加或修改服务；
        如果有service_id参数，则是修改；如果没有service_id参数，则是添加服务
        需要参数：user_id、title、pics、price、cost、ondoor、brand、place、details
        修改的话，还需要service_id参数
        """
        service_id = request.data.get('service_id')
        service = ModelService.objects.filter(id=service_id).first()

        user_id = request.data.get('user_id')
        type = ModelUsers.objects.filter(id=user_id).first().type
        title = request.data.get('title')
        pics = request.data.get('pics')
        price = request.data.get('price')
        cost = request.data.get('cost')
        ondoor = request.data.get('ondoor')
        brand = request.data.get('brand')
        place = request.data.get('place')
        details = request.data.get('details')

        if service:
            service.user_id = user_id
            service.type = type
            service.title = title
            service.pics = pics
            service.price = price
            service.cost = cost
            service.ondoor = ondoor
            service.brand = brand
            service.place = place
            service.details = details
            service.save()
        else:
            service = ModelService.objects.create(
                user_id = user_id,
                type = type,
                title = title,
                pics = pics,
                price = price,
                cost = cost,
                ondoor = ondoor,
                brand = brand,
                place = place,
                details = details,
            )

        service_data = ServiceSerializer(service).data

        context = {
            "msg": "添加或修改服务成功",
            "service":service_data
        }
        return Response(context)



class ServiceManage(APIView):
    def get(self, request: Request):
        """
        查看本人的服务，出售中or已下架
        需要参数：user_id、status(1上架，0下架)
        """
        user_id = request.query_params.get('user_id')
        status = request.query_params.get('status')
        services = ModelService.objects.filter(user_id=user_id,status=status,is_del=0).all()

        services_data = ServiceSimpleSerializer(services,many=True).data

        context = {
            "msg": "查看本人的服务成功",
            "user_id":user_id,
            "service status":status,
            "data": services_data
        }
        return Response(context)

    def put(self, request: Request):
        """
        上架或下架操作
        需要参数：service_id、status(1上架，0下架)(表单中提交)
        """
        service_id = request.data.get('service_id')
        status = request.data.get('status')
        service = ModelService.objects.filter(id=service_id,is_del=0).first()
        service.status = status
        service.save()
        context = {
            "msg": "上架或下架操作成功",
            "service_id": service_id,
            "service":service.title,
            "current status": status,
        }
        return Response(context)

    def delete(self,request:Request):
        """
        删除服务
        需要参数：service_id(body中表单提交)
        """
        service_id = request.data.get('service_id')
        service = ModelService.objects.filter(id=service_id).first()
        service_title = service.title
        service.is_del = 1  # 设置状态为已删除
        service.save()

        context = {
            "msg": "删除服务成功",
            "deleted service": service_title
        }
        return Response(context)


class StaffManage(APIView):
    def get(self,request:Request):
        """
        查看整体团队
        需要参数：user_id
        """
        user_id = request.query_params.get('user_id')
        staff = ModelServiceStaff.objects.filter(user_id=user_id).all()
        staff_data = StaffSerializer(staff,many=True).data
        context = {
            "msg": "查看团队成功",
            "user_id":user_id,
            "staff":staff_data
        }
        return Response(context)

class StaffMember(APIView):
    def get(self,request:Request):
        """
        查看团队某个成员信息
        需要参数：staff_id
        """
        staff_id = request.query_params.get('staff_id')
        staff = ModelServiceStaff.objects.filter(id=staff_id).first()
        staff_data = StaffSerializer(staff).data
        context = {
            "msg": "查看团队某成员成功",
            "staff": staff_data
        }
        return Response(context)

    def post(self,request:Request):
        """
        增加或修改团队成员，一次增加或修改一个
        需要参数：user_id、name、pic、details
        如果是修改，还需要参数：staff_id
        """
        staff_id = request.data.get('staff_id')
        staff = ModelServiceStaff.objects.filter(id=staff_id).first()

        user_id = request.data.get('user_id')
        name = request.data.get('name')
        pic = request.data.get('pic')
        details = request.data.get('details')
        if staff:
            staff.name = name
            staff.pic = pic
            staff.details = details
            staff.save()
        else:
            staff = ModelServiceStaff.objects.create(
                user_id = user_id,
                name = name,
                pic = pic,
                details = details
            )
        staff_data = StaffSerializer(staff).data

        context = {
            "msg": "添加或修改团队成员成功",
            "service": staff_data
        }
        return Response(context)

    def delete(self,request:Request):
        """
        删除团队某个成员信息
        需要参数：staff_id(body中表单提交)
        """
        staff_id = request.data.get('staff_id')
        staff = ModelServiceStaff.objects.filter(id=staff_id).first()
        staff_name = staff.name
        staff.delete()
        context = {
            "msg": "删除团队成员成功",
            "deleted staff": staff_name
        }
        return Response(context)


class Picture(APIView):

    def post(self, request: Request):
        """
        上传图片
        需要字段：img(文件类型)
        """
        img = request.FILES.get('img')
        url = upload(img)  # upload方法在utils.pic_upload写了
        context = {"img_url": url}
        return Response(context)

    def delete(self, request: Request):
        """
        删除图片
        需要字段：img_url
        """
        img_url = request.data.get('img_url')
        delete_img(img_url)
        info = f"{img_url}已删除"
        context = {"del_info": info}
        return Response(context)


class ServiceSearch(APIView):
    def get(self,request:Request):
        """
        输入搜索词，找到所有相关服务；如果没有搜索词，则返回所有服务;
        还可排序
        参数（均为可选）：keyword、
        order_by(star、drill、crown、sales_volume、price_des、price_asc六选一)
        """
        keyword = request.query_params.get('keyword')
        order_by = request.query_params.get('order_by')

        if keyword:
            if order_by == 'star':
                service = ModelService.objects.filter(
                    Q(title__contains=keyword) | Q(details__contains=keyword),
                    is_del=0).order_by('-star')
            elif order_by == 'drill':
                service = ModelService.objects.filter(
                    Q(title__contains=keyword) | Q(details__contains=keyword),
                    is_del=0).order_by('-drill')
            elif order_by == 'crown':
                service = ModelService.objects.filter(
                    Q(title__contains=keyword) | Q(details__contains=keyword),
                    is_del=0).order_by('-crown')
            elif order_by == 'sales_volume':
                service = ModelService.objects.filter(
                    Q(title__contains=keyword) | Q(details__contains=keyword),
                    is_del=0).order_by('-sales_volume')
            elif order_by == 'price_des':
                service = ModelService.objects.filter(
                    Q(title__contains=keyword) | Q(details__contains=keyword),
                    is_del=0).order_by('-price')
            elif order_by == 'price_asc':
                service = ModelService.objects.filter(
                    Q(title__contains=keyword) | Q(details__contains=keyword),
                    is_del=0).order_by('price')
            else:
                service = ModelService.objects.filter(
                    Q(title__contains=keyword) | Q(details__contains=keyword),
                    is_del=0).order_by('-id')
        else:
            if order_by == 'star':
                service = ModelService.objects.filter(is_del=0).order_by('-star')
            elif order_by == 'drill':
                service = ModelService.objects.filter(is_del=0).order_by('-drill')
            elif order_by == 'crown':
                service = ModelService.objects.filter(is_del=0).order_by('-crown')
            elif order_by == 'sales_volume':
                service = ModelService.objects.filter(is_del=0).order_by('-sales_volume')
            elif order_by == 'price_des':
                service = ModelService.objects.filter(is_del=0).order_by('-price')
            elif order_by == 'price_asc':
                service = ModelService.objects.filter(is_del=0).order_by('price')
            else:
                service = ModelService.objects.filter(is_del=0).order_by('-id')

        service_data = ServiceSimpleSerializer(service,many=True).data
        context = {
            "msg": "搜索服务并排序成功",
            "service": service_data
        }
        return Response(context)

class ServiceSelect(APIView):
    def get(self, request: Request):
        """
        输入搜索词，找到所有相关服务；如果没有搜索词，则返回所有服务;
        还可筛选
        参数（均为可选）：keyword、brand(1\0)、 ondoor(0\1\2)、type(0\1\2)
        """
        request_data = dict(request.GET)
        keyword = request.query_params.get('keyword')
        q = Q()
        if keyword:
            request_data.pop('keyword')
            for k, l in request_data.items():
                q.add(Q(**{k: l[0]}), Q.AND)
            service = ModelService.objects.filter(
                Q(title__contains=keyword) | Q(details__contains=keyword),
                q,is_del=0).order_by('-id')
        else:
            for k, l in request_data.items():
                q.add(Q(**{k: l[0]}), Q.AND)
            service = ModelService.objects.filter(q,is_del=0).order_by('-id')

        service_data = ServiceSimpleSerializer(service, many=True).data
        context = {
            "msg": "搜索服务并筛选成功",
            "service": service_data
        }
        return Response(context)


class QA(APIView):
    def get(self,request:Request):
        """
        查看本服务的问答内容，可查看所有本服务的问答(不带参数qa_id)，也可以查看单条问答（带参数qa_id）
        需要参数(二选一)：service_id，qa_id
        """
        service_id = request.query_params.get('service_id')
        qa_id = request.query_params.get('qa_id')
        if qa_id:
            qa = ModelQA.objects.filter(id=qa_id).first()
            if qa:
                qa_data = QASerializer(qa).data
            else:
                qa_data = '没有相关qa'
        elif service_id:
            qa = ModelQA.objects.filter(g_id=service_id)
            if qa:
                qa_data = QASerializer(qa,many=True).data
            else:
                qa_data = '没有相关qa'

        context = {
            "msg": "查看服务的问答成功",
            "qa": qa_data
        }
        return Response(context)

    def post(self,request:Request):
        """
        添加或修改问答，添加问答(不带参数qa_id)，修改（带参数qa_id）
        需要参数：service_id(必选)，qa_id(可选)、questions(必选)、answers(必选)
        """
        service_id = request.data.get('service_id')
        qa_id = request.data.get('qa_id')
        questions = request.data.get('questions')
        answers = request.data.get('answers')
        t_id = ModelService.objects.filter(id=service_id).first().t_id

        if qa_id:
            qa = ModelQA.objects.filter(id=qa_id).first()
            qa.questions = questions
            qa.answers = answers
            qa.save()
        else:
            qa = ModelQA.objects.create(
                g_id=service_id,
                questions=questions,
                answers=answers,
                t_id=t_id
            )
        qa_data = QASerializer(qa).data
        context = {
            "msg": "添加或修改问答成功",
            "qa": qa_data
        }
        return Response(context)

    def delete(self,request:Request):
        """
        删除问答
        需要参数：qa_id
        """
        qa_id = request.data.get('qa_id')
        qa = ModelQA.objects.filter(id=qa_id).first()
        qa_questions = qa.questions
        qa.delete()
        context = {
            "msg": "删除问答成功",
            "deleted qa": qa_questions
        }
        return Response(context)


class ServiceDetail(APIView):
    def get(self, request: Request):
        """
        普通用户看到的服务详情页面
        需要参数：service_id
        """
        # 服务信息
        service_id = request.query_params.get('service_id')
        service = ModelService.objects.filter(id=service_id,is_del=0).first()
        service_data = ServiceSerializer(service).data

        # 服务评价(评价分类数量)
        # 在评价分类关联表中定位到相应服务
        comment_type = Goods_comment_types.objects.filter(g_id=service_id)
        comment_type_count = dict()
        sum = 0
        for ct in comment_type:
            # 根据评价分类id到评价分类表中找到分类名称
            name = Comment_type.objects.filter(id=ct.t_id).first().name
            type_count = ct.type_count
            comment_type_count[name] = type_count
            sum += type_count
        comment_type_count['sum'] = sum

        # 用户问答
        qa = ModelQA.objects.filter(g_id=service_id).last()
        qa_data = QASerializer(qa).data

        # 服务团队
        user_id = service.user_id
        staff = ModelServiceStaff.objects.filter(user_id=user_id).all()[:3]
        staff_data = StaffSerializer(staff, many=True).data

        context = {
            "msg": "查看服务成功",
            "service": service_data,
            "comment_type_count":comment_type_count,
            "qa":qa_data,
            "staff": staff_data,
        }
        return Response(context)


class ServiceComment(APIView):
    def get(self, request: Request):
        """
        查看某服务的所有评价
        需要参数：service_id
        """
        service_id = request.query_params.get('service_id')
        comment = Comment.objects.filter(g_id=service_id)
        if not comment:
            return Response('暂无评论')

        # 计算综合星数overall_star
        sum_star = 0
        for c in comment:
            sum_star += c.rank
        overall_star = round(sum_star / len(comment))

        # 服务评价(评价分类数量)comment_type_count
        # 在评价分类关联表中定位到相应服务
        comment_type = Goods_comment_types.objects.filter(g_id=service_id)
        comment_type_count = dict()
        sum = 0
        for ct in comment_type:
            # 根据评价分类id到评价分类表中找到分类名称
            name = Comment_type.objects.filter(id=ct.t_id).first().name
            type_count = ct.type_count
            comment_type_count[name] = type_count
            sum += type_count
        comment_type_count['sum'] = sum

        # 某服务的若干条评价
        comment_data = CommentSerializer(comment,many=True).data

        context = {
            "msg": "查看服务的评价成功",
            "service_id": service_id,
            "overall_star":overall_star,
            "comment_type_count":comment_type_count,
            "comment_data": comment_data,
        }
        return Response(context)





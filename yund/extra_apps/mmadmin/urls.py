from django.contrib import admin
from django.urls import path,re_path
from .views import *
from django.views.generic import TemplateView

urlpatterns = [

    path('login',Login),
    path('goodsinfo',Goodsinfo),
    path('cateringinfo',Cateringinfo),
    path('ishtmls',isHtmls),
]
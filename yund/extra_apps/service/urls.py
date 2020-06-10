from django.urls import path,include
from . import views

app_name = 'service'

urlpatterns = [
    path('',views.Service.as_view()),
    path('manage/',views.ServiceManage.as_view()),
    path('staff/',views.StaffManage.as_view()),
    path('member/',views.StaffMember.as_view()),
    path('pic/',views.Picture.as_view()),
    path('search/',views.ServiceSearch.as_view()),
    path('select/',views.ServiceSelect.as_view()),
    path('detail/',views.ServiceDetail.as_view()),
    path('qa/',views.QA.as_view()),
    path('comment/',views.ServiceComment.as_view()),
]




from django.urls import path

from . import views

urlpatterns = [
    #项目urls->应用中的urls->应用views->返回html
    path('', views.index, name='index'),
    path('<str:room_name>/', views.room, name='room'),
]


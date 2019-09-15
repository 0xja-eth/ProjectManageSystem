
from django.contrib import admin
from django.urls import path
from .views import *
from utils.view_func_utils import recieveRequest

ROUTE_SETTINGS = {
	'register' : {
		# 接收POST数据（字段名，数据类型）
		'POST': [['username', 'str'], ['password', 'str'],
				['email', 'str'], ['code', 'str']],
		# 逻辑处理函数
		'func': register
	},
	'login': {
		# 接收POST数据（字段名，数据类型）
		'POST': [['username', 'str'], ['password', 'str']],
		# 逻辑处理函数
		'func': login
	},
}

urlpatterns = [
	path('register', recieveRequest, ROUTE_SETTINGS['register']),
	path('login', recieveRequest, ROUTE_SETTINGS['login'])
]
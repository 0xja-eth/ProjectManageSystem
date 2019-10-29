
from .views import DataManager
from utils.interface_manager import InterfaceManager

Interfaces = {
	'data' : {
		# 接收POST数据（字段名，数据类型）
		'params': [],
		'method': 'GET',
		# 逻辑处理函数
		'func': DataManager.getSystemData
	},
}

urlpatterns = InterfaceManager.generateUrlPatterns(Interfaces)


from .views import UserManager
from utils.interface_manager import InterfaceManager

Interfaces = {
	'register' : {
		# 接收POST数据（字段名，数据类型）
		'POST': [['un', 'str'], ['pw', 'str'],
				['email', 'str'], ['code', 'str']],
		# 逻辑处理函数
		'func': UserManager.register
	},
	'login': {
		'POST': [['un', 'str'], ['pw', 'str']],
		'func': UserManager.login
	},
	'forget': {
		'POST': [['un', 'str'], ['pw', 'str'],
				['email', 'str'], ['code', 'str']],
		'func': UserManager.forget
	},
	'code': {
		'POST': [['un', 'str'], ['email', 'str'], ['type', 'str']],
		'func': UserManager.sendCode
	},
}

urlpatterns = InterfaceManager.generateUrlPatterns(Interfaces)

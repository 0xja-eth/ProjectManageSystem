
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
	'reset_pwd': {
		'POST': [['auth', 'str'], ['old', 'str'], ['new', 'str']],
		'func': UserManager.resetPwd
	},
	'edit_info': {
		'POST': [['auth', 'str'], ['name', 'str'], ['gender', 'int'],
				['birth','str'], ['city','str'], ['edu_id','int'],
				['duty','str'], ['contact','str'], ['desc','str']],
		'func': UserManager.editInfo
	},
	'upload_avatar': {
		'POST': [['auth', 'str']], 'FILES': ['avatar'],
		'func': UserManager.uploadAvatar
	},
	'get_friends': {
		'POST': [['auth', 'str']],
		'func': UserManager.getFriends
	},
	'get_reqs': {
		'POST': [['auth', 'str'],['type', 'str']],
		'func': UserManager.getFriendReqs
	},
	'search': {
		'POST': [['auth', 'str'], ['un','str']],
		'func': UserManager.searchUser
	},
	'add_friend': {
		'POST': [['auth', 'str'], ['fuid','int']],
		'func': UserManager.addFriend
	},
	'del_friend': {
		'POST': [['auth', 'str'], ['fid','int']],
		'func': UserManager.deleteFriend
	},
}

urlpatterns = InterfaceManager.generateUrlPatterns(Interfaces)

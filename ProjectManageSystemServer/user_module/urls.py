
from .views import UserView
from utils.interface_manager import InterfaceManager

Interfaces = {
	'register' : {
		# 接收POST数据（字段名，数据类型）
		'params': [['un', 'str'], ['pw', 'str'],
				['email', 'str'], ['code', 'str']],
		# 逻辑处理函数
		'func': UserView.register
	},
	'login': {
		'params': [['un', 'str'], ['pw', 'str']],
		'func': UserView.login
	},
	'forget': {
		'params': [['un', 'str'], ['pw', 'str'],
				['email', 'str'], ['code', 'str']],
		'func': UserView.forget
	},
	'code': {
		'params': [['un', 'str'], ['email', 'str'], ['type', 'str']],
		'func': UserView.sendCode
	},
	'reset_pwd': {
		'params': [['auth', 'str'], ['old', 'str'], ['new', 'str']],
		'func': UserView.resetPwd
	},
	'edit_info': {
		'params': [['auth', 'str'], ['name', 'str'], ['gender', 'int'],
				['birth','str'], ['city','str'], ['edu_id','int'],
				['duty','str'], ['contact','str'], ['desc','str']],
		'func': UserView.editInfo
	},
	'upload_avatar': {
		'params': [['auth', 'str']], 'files': ['avatar'],
		'func': UserView.uploadAvatar
	},
	'get_friends': {
		'params': [['auth', 'str']],
		'func': UserView.getFriends
	},
	'get_reqs': {
		'params': [['auth', 'str'],['type', 'str']],
		'func': UserView.getFriendReqs
	},
	'search': {
		'params': [['auth', 'str'], ['un','str']],
		'func': UserView.searchUser
	},
	'add_friend': {
		'params': [['auth', 'str'], ['fuid','int']],
		'func': UserView.addFriend
	},
	'del_friend': {
		'params': [['auth', 'str'], ['fid','int']],
		'func': UserView.deleteFriend
	},
	'oper_req': {
		'params': [['auth', 'str'], ['fid','int'], ['accept','bopl']],
		'func': UserView.operFriendReq
	},
	'refresh_token': {
		'params': [['auth', 'str']],
		'func': UserView.refreshToken
	}
}

urlpatterns = InterfaceManager.generateUrlPatterns(Interfaces)

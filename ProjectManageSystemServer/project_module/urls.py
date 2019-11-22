
from .views import ProjectView
from utils.interface_manager import InterfaceManager

Interfaces = {
	'new' : {
		# 接收POST数据（字段名，数据类型）
		'params': [['auth', 'str'], ['name', 'str'],
				['type_id', 'int'], ['start_date', 'date'],
				['desc','str']],
		# 逻辑处理函数
		'func': ProjectView.new
	},
	'get' : {
		'params': [['auth', 'str'], ['pid', 'var']],
		'func': ProjectView.get
	},
	'edit' : {
		'params': [['auth', 'str'], ['pid', 'int'], ['name','str'],
				['type_id', 'int'], ['start_date', 'date'], ['desc','str']],
		'func': ProjectView.edit
	},
	'delete' : {
		'params': [['auth', 'str'], ['pid', 'int'], ['pw','str']],
		'func': ProjectView.delete
	},
	'get_members' : {
		'params': [['auth', 'str'], ['pid', 'int']],
		'func': ProjectView.getMembers
	},
	'add_members': {
		'params': [['auth', 'str'], ['pid', 'int'],
				['uids','int[]'], ['rids','int[][]'], ['pw','str']],
		'func': ProjectView.addMembers
	},
	'delete_members': {
		'params': [['auth', 'str'], ['pid', 'int'],
				['uids','int[]'], ['pw','str']],
		'func': ProjectView.deleteMembers
	},
	'edit_members': {
		'params': [['auth', 'str'], ['pid', 'int'],
				['uids','int[]'], ['rids','int[][]']],
		'func': ProjectView.editMembers
	},
	'change_pm': {
		'params': [['auth', 'str'], ['pid', 'int'],
				['uid','int'], ['pw','str']],
		'func': ProjectView.changeProjectManager
	},
	'get_notices': {
		'params': [['auth', 'str']],
		'func': ProjectView.getNotices
	},
	'add_notice': {
		'params': [['auth', 'str'], ['pid', 'int'],
				['title','str'], ['content','str']],
		'func': ProjectView.addNotice
	},
	'del_notices': {
		'params': [['auth', 'str'], ['pid','int'], ['nids', 'int']],
		'func': ProjectView.deleteNotices
	},
	'read_notices': {
		'params': [['auth', 'str'], ['rids', 'int']],
		'func': ProjectView.readNotices
	},
}

urlpatterns = InterfaceManager.generateUrlPatterns(Interfaces)

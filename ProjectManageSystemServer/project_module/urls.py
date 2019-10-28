
from .views import ProjectManager
from utils.interface_manager import InterfaceManager

Interfaces = {
	'new' : {
		# 接收POST数据（字段名，数据类型）
		'POST': [['auth', 'str'], ['name', 'str'],
				['type_id', 'int'], ['start_date', 'date'],
				['desc','str']],
		# 逻辑处理函数
		'func': ProjectManager.new
	},
	'get' : {
		'POST': [['auth', 'str'], ['pid', 'var']],
		'func': ProjectManager.get
	},
	'edit' : {
		'POST': [['auth', 'str'], ['pid', 'int'], ['name','str'],
				['type_id', 'int'], ['start_date', 'date'], ['desc','str']],
		'func': ProjectManager.edit
	},
	'delete' : {
		'POST': [['auth', 'str'], ['pid', 'int'], ['pw','str']],
		'func': ProjectManager.delete
	},
	'get_members' : {
		'POST': [['auth', 'str'], ['pid', 'int']],
		'func': ProjectManager.getMembers
	},
	'add_members': {
		'POST': [['auth', 'str'], ['pid', 'int'],
				['uids','int[]'], ['rids','int[][]'], ['pw','str']],
		'func': ProjectManager.addMembers
	},
	'delete_members': {
		'POST': [['auth', 'str'], ['pid', 'int'],
				['uids','int[]'], ['pw','str']],
		'func': ProjectManager.deleteMembers
	},
	'edit_members': {
		'POST': [['auth', 'str'], ['pid', 'int'],
				['uids','int[]'], ['rids','int[][]']],
		'func': ProjectManager.editMembers
	},
	'change_pm': {
		'POST': [['auth', 'str'], ['pid', 'int'],
				['uid','int'], ['pw','str']],
		'func': ProjectManager.changeProjectManager
	},
	'get_notices': {
		'POST': [['auth', 'str']],
		'func': ProjectManager.getNotices
	},
	'add_notice': {
		'POST': [['auth', 'str'], ['pid', 'int'],
				['title','str'], ['content','str']],
		'func': ProjectManager.addNotice
	},
	'del_notices': {
		'POST': [['auth', 'str'], ['pid','int'], ['nids', 'int']],
		'func': ProjectManager.deleteNotices
	},
	'read_notices': {
		'POST': [['auth', 'str'], ['rids', 'int']],
		'func': ProjectManager.readNotices
	},
}

urlpatterns = InterfaceManager.generateUrlPatterns(Interfaces)

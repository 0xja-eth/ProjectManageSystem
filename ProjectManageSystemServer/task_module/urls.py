
from .views import TaskManager
from utils.interface_manager import InterfaceManager

Interfaces = {
	'get': {
		'POST': [['auth', 'str'], ['pid', 'var']],
		'func': TaskManager.get
	},
	'add': {
		'POST': [['auth', 'str'], ['pid', 'int'], ['name', 'str'],
				['desc', 'str'], ['parent_id', 'int'], ['prev_ids', 'int[]'],
				['auto_adjust', 'bool'], ['start_date', 'date'],
				['duration', 'var'], ['end_date', 'var']],
		'func': TaskManager.add
	},
	'edit': {
		'POST': [['auth', 'str'], ['tid', 'int'], ['name', 'str'],
				['desc', 'str'], ['parent_id', 'int'], ['prev_ids', 'int[]'],
				['progress', 'int'], ['status_id', 'int'], ['auto_adjust', 'bool'],
				['start_date', 'date'], ['duration', 'var'], ['end_date', 'var']],
		'func': TaskManager.edit
	},
	'delete': {
		'POST': [['auth', 'str'], ['tid', 'int']],
		'func': TaskManager.delete
	},
	'distribute': {
		'POST': [['auth', 'str'], ['tid', 'int'], ['uids', 'int[]']],
		'func': TaskManager.distribute
	},
	'adjust': {
		'POST': [['auth', 'str'], ['pid', 'int'],
				['tids', 'int[]'], ['prevs', 'int[][]']],
		'func': TaskManager.adjust
	},
	'get_prs': {
		'POST': [['auth', 'str'], ['pid', 'var'], ['tid', 'var']],
		'func': TaskManager.getProgressReqs
	},
	'add_pr': {
		'POST': [['auth', 'str'], ['tid', 'int'],
				['progress', 'int'], ['desc', 'str']],
		'func': TaskManager.addProgressReq
	},
	'oper_pr': {
		'POST': [['auth', 'str'], ['prid', 'int'],
				['result', 'bool'], ['progress', 'val']],
		'func': TaskManager.operProgressReq
	},
}

urlpatterns = InterfaceManager.generateUrlPatterns(Interfaces)


from .views import TaskView
from utils.interface_manager import InterfaceManager

Interfaces = {
	'get': {
		'params': [['auth', 'str'], ['pid', 'var']],
		'func': TaskView.get
	},
	'add': {
		'params': [['auth', 'str'], ['pid', 'int'], ['name', 'str'],
				['desc', 'str'], ['parent_id', 'int'], ['prev_ids', 'int[]'],
				['auto_adjust', 'bool'], ['start_date', 'date'],
				['duration', 'var'], ['end_date', 'var']],
		'func': TaskView.add
	},
	'edit': {
		'params': [['auth', 'str'], ['tid', 'int'], ['name', 'str'],
				['desc', 'str'], ['parent_id', 'int'], ['prev_ids', 'int[]'],
				['progress', 'int'], ['status_id', 'int'], ['auto_adjust', 'bool'],
				['start_date', 'date'], ['duration', 'var'], ['end_date', 'var']],
		'func': TaskView.edit
	},
	'delete': {
		'params': [['auth', 'str'], ['tid', 'int']],
		'func': TaskView.delete
	},
	'distribute': {
		'params': [['auth', 'str'], ['tid', 'int'], ['uids', 'int[]']],
		'func': TaskView.distribute
	},
	'adjust': {
		'params': [['auth', 'str'], ['pid', 'int'],
				['tids', 'int[]'], ['prevs', 'int[][]']],
		'func': TaskView.adjust
	},
	'get_prs': {
		'params': [['auth', 'str'], ['pid', 'var'], ['tid', 'var']],
		'func': TaskView.getProgressReqs
	},
	'add_pr': {
		'params': [['auth', 'str'], ['tid', 'int'],
				['progress', 'int'], ['desc', 'str']],
		'func': TaskView.addProgressReq
	},
	'oper_pr': {
		'params': [['auth', 'str'], ['prid', 'int'],
				['result', 'bool'], ['progress', 'val']],
		'func': TaskView.operProgressReq
	},
}

urlpatterns = InterfaceManager.generateUrlPatterns(Interfaces)

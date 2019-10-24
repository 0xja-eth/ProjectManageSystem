
from user_module.models import *
from project_module.models import *
from task_module.models import *
from chat_module.models import *
from user_module.views import CodeDatum
from utils.view_manager import ViewManager

# Create your views here.
class DataManager:

	@classmethod
	def getSystemData(cls):

		data = {}

		data['Educations'] = cls.convertTupleToDict(User.USER_EDUCATIONS)
		data['LoginStatuses'] = cls.convertTupleToDict(User.USER_STATUSES)
		data['ProjectTypes'] = cls.convertTupleToDict(Project.PROJECT_TYPES)
		data['TaskStatuses'] = cls.convertTupleToDict(Task.TASK_STATUSES)
		data['TaskLevels'] = cls.convertTupleToDict(Task.TASK_LEVELS)

		data['Roles'] = ViewManager.getObjects(Role, return_type='dict')

		data['ProjectManagerRoleId'] = Role.ProjectManagerId
		data['BeforeStartStatusId'] = TaskStatus.Unstart.value
		data['StartedStatusId'] = TaskStatus.Started.value
		data['CompletedStatusId'] = TaskStatus.Finished.value
		data['FailedStatusId'] = TaskStatus.Failed.value
		data['PausedStatusId'] = TaskStatus.Paused.value
		data['CancelledStatusId'] = TaskStatus.Cancelled.value

		data['UnLength'] = User.UN_LEN
		data['PwdLength'] = User.PWD_LEN
		data['EmailReg'] = User.EMAIL_REG
		data['CodeLength'] = CodeDatum.CODE_LENGTH
		data['CodeSecond'] = CodeDatum.CODE_SECOND

		return data

	@classmethod
	def convertTupleToDict(cls, data):
		return {'id': data[0],'name': data[1]}

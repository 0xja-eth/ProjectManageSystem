
from user_module.models import *
from project_module.models import *
from task_module.models import *
from chat_module.models import *
from user_module.views import CodeDatum
from utils.view_manager import ViewUtils

# Create your views here.
class DataManager:

	@classmethod
	def getSystemData(cls):

		data = {}

		data['Educations'] = cls.convertTuplesToDict(User.USER_EDUCATIONS)
		data['LoginStatuses'] = cls.convertTuplesToDict(User.USER_STATUSES)
		data['ProjectTypes'] = cls.convertTuplesToDict(Project.PROJECT_TYPES)
		data['TaskStatuses'] = cls.convertTuplesToDict(Task.TASK_STATUSES)
		data['TaskLevels'] = cls.convertTuplesToDict(Task.TASK_LEVELS)

		data['Roles'] = ViewUtils.getObjects(Role, return_type='dict')

		data['ProjectManagerRoleId'] = Role.ProjectManagerId

		data['OfflineStatusID'] = UserStatus.Offline.value
		data['OnlineStatusID'] = UserStatus.Online.value

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
	def convertTuplesToDict(cls, data):
		res = []
		for d in data:
			res.append({'id': d[0],'name': d[1]})
		return res

from django.shortcuts import render
from user_module.models import User
from user_module.views import UserView
from project_module.views import ProjectView
from utils.exception import ErrorException, ErrorType
from utils.interface_manager import InterfaceManager
from utils.view_manager import ViewUtils
from .models import *
import datetime

# Create your views here.
class TaskView():

	# 获取任务
	@classmethod
	def get(cls, user: User, pid=None):
		if pid is None:
			tasks = ModelUtils.getObjectRelatedForAll(
				user.tasktake_set, 'task')
		else:
			pid = InterfaceManager.convertDataType(pid, 'int')

			proj = ProjectView.Common.getProject(id=pid)
			tasks = proj.tasks(True)

		return {
			'tasks': ModelUtils.objectsToDict(tasks, type='detail')
		}

	# 添加任务
	@classmethod
	def add(cls, user: User, pid, name, desc, parent_id, prev_ids,
			auto_adjust, start_date, duration=0, end_date=None, prev_order_id=None):

		# 参数处理
		# 如果有 end_date 参数，直接解析使用
		if end_date is not None:
			end_date = InterfaceManager.convertDataType(end_date, 'date')
		# 否则，根据 duration 计算一个 end_date
		else:
			delta = datetime.timedelta(duration)
			end_date = start_date + delta

		# 参数校验
		cls.Check.ensureNameFormat(name)
		cls.Check.ensureDescFormat(desc)
		cls.Check.ensureDurationFormat(duration)
		cls.Check.ensureEndDateFormat(start_date, end_date)

		cls.Common.ensureTaskExist(id=parent_id)

		for prev_id in prev_ids:
			cls.Common.ensureTaskExist(id=prev_id)

		ProjectView.Common.ensureProjectManager(user.id, pid)

		# 校验 & 获取必要数据
		proj = ProjectView.Common.getProject(id=pid)

		prev_order = None
		if prev_order_id is not None:
			prev_order = cls.Common.getTask(
				id=prev_order_id, project=proj)

		# 添加任务
		proj.addTask(name, desc, parent_id, prev_ids, auto_adjust,
					 start_date, end_date, prev_order)

	# 修改任务
	@classmethod
	def edit(cls, user: User, tid, name, desc, parent_id,
			 prev_ids, auto_adjust, progress, start_date,
			 duration=0, end_date=None, status_id=None, prev_order_id=None):

		# 参数处理
		# 如果有 status_id 参数，判断格式
		if status_id is not None:
			cls.Check.ensureStatusFormat(status_id)

		# 如果有 end_date 参数，直接解析使用
		if end_date is not None:
			end_date = InterfaceManager.convertDataType(end_date, 'date')
		# 否则，根据 duration 计算一个 end_date
		else:
			delta = datetime.timedelta(duration)
			end_date = start_date + delta

		# 参数校验
		cls.Check.ensureNameFormat(name)
		cls.Check.ensureDescFormat(desc)
		cls.Check.ensureDurationFormat(duration)
		cls.Check.ensureEndDateFormat(start_date, end_date)

		cls.Common.ensureTaskExist(id=parent_id)

		for prev_id in prev_ids:
			cls.Common.ensureTaskExist(id=prev_id)

		# 校验 & 获取必要数据
		task = cls.Common.getTask(id=tid)
		project = task.project

		# 确保项目经理权限
		ProjectView.Common.ensureProjectManager(user.id, project.id)

		prev_order = None
		if prev_order_id is not None:
			prev_order = cls.Common.getTask(
				id=prev_order_id, project_id=task.project_id)

		# 修改任务
		project.editTask(task, name, desc, parent_id, prev_ids, auto_adjust,
					progress, start_date, end_date, status_id, prev_order)

	# 删除任务
	@classmethod
	def delete(cls, user: User, tid):
		task = cls.Common.getTask(id=tid)
		project = task.project

		# 确保项目经理权限
		ProjectView.Common.ensureProjectManager(user.id, project.id)

		project.delete(task)

	# 分配任务
	@classmethod
	def distribute(cls, user: User, tid, uids):
		task = cls.Common.getTask(id=tid)
		pid = task.project_id

		# 确保用户存在且已加入项目中
		for uid in uids:
			ProjectView.Common.ensureParticipationExist(pid, uid)

		# 确保项目经理权限
		ProjectView.Common.ensureProjectManager(user.id, pid)

		task.distribute(uids)

	# 调整任务
	@classmethod
	def adjust(cls, user: User, pid, tids, prevs):

		# 获取项目
		project = ProjectView.Common.getProject(id=pid)

		# 确保项目经理权限
		ProjectView.Common.ensureProjectManager(user.id, project.id)

		task_data = []

		for i in range(len(tids)):
			tid = tids[i]
			prev = prevs[i]

			# 确保每个任务都在该项目内
			task = cls.Common.getTask(id=tid, project=project)

			# 确保每个前序任务都在该项目内
			for prev_id in prev:
				cls.Common.ensureTaskExist(id=prev_id, project=project)

			# 封装 task_data
			task_data.append({'task': task, 'prev_ids': prev})

		project.adjustTasks(task_data)

	# 获取任务进度请求
	@classmethod
	def getProgressReqs(cls, user: User, pid=None, tid=None):
		# 如果提供了 pid 和 tid
		if pid is not None and tid is not None:
			raise ErrorException(ErrorType.ParameterError)

		# 如果提供 pid
		if pid is not None:
			proj = ProjectView.Common.getProject(id=pid)
			return proj.convertToDict('pr')

		# 如果提供 tid
		if tid is not None:
			task = cls.Common.getTask(id=tid)
			return task.convertToDict('pr')

		raise ErrorException(ErrorType.ParameterError)

	# 获取任务进度请求
	@classmethod
	def addProgressReq(cls, user: User, tid, progress, desc):

		task = cls.Common.getTask(id=tid)

		# 确保参加任务
		cls.Common.ensureTaskTakeExist(tid, user.id)

		task.addProgressReq(user, progress, desc)

	# 评审任务进度请求
	@classmethod
	def operProgressReq(cls, user: User, prid, result, progress=None):

		# 确保 pr 存在且未评审
		pr = cls.Common.getTaskProgress(id=prid, result_time__isnull=True)

		if progress is not None:
			cls.Check.ensureProgressFormat(progress)

		proj_id = pr.task.project_id

		ProjectView.Common.ensureProjectManager(user.id, proj_id)

		pr.oper(result, progress)

	# 校验输入参数格式
	class Check:

		# 校验任务名格式
		@classmethod
		def ensureNameFormat(cls, val: str):
			if not val:
				raise ErrorException(ErrorType.InvalidTaskName)
			if len(val) > Task.NAME_LEN:
				raise ErrorException(ErrorType.InvalidTaskName)

		# 校验任务描述格式
		@classmethod
		def ensureDescFormat(cls, val: str):
			if len(val) > Task.DESC_LEN:
				raise ErrorException(ErrorType.InvalidTaskDesc)

		# 校验任务工期格式
		@classmethod
		def ensureDurationFormat(cls, val: int):
			if val < 0:
				raise ErrorException(ErrorType.InvalidTaskDuration)

		# 校验任务结束日期格式
		@classmethod
		def ensureEndDateFormat(cls, start: datetime.datetime,
								end: datetime.datetime):
			if start > end:
				raise ErrorException(ErrorType.InvalidTaskEndDate)

		# 校验任务状态格式
		@classmethod
		def ensureStatusFormat(cls, val: int):
			if val not in [
				TaskStatus.Failed.value,
				TaskStatus.Cancelled.value,
				TaskStatus.Paused.value
			]:
				raise ErrorException(ErrorType.InvalidTaskStatusId)

		# 校验任务进度格式
		@classmethod
		def ensureProgressFormat(cls, val: int):
			if not (0 <= val <= 100):
				raise ErrorException(ErrorType.InvalidTaskProgress)

	# 共享函数
	class Common:

		# 获取任务
		@classmethod
		def getTask(cls, return_type='object', **args) -> Task:
			return ViewUtils.getObject(Task, ErrorType.TaskNotExist,
									   return_type=return_type, **args)

		# 获取进度请求
		@classmethod
		def getTaskTake(cls, tid, uid, return_type='object') -> TaskTake:
			return ViewUtils.getObject(TaskTake, ErrorType.TaskTakeNotExist,
									   task_id=tid, user_id=uid,
									   return_type=return_type)

		# 获取进度请求
		@classmethod
		def getTaskProgress(cls, return_type='object', **args) -> TaskProgress:
			return ViewUtils.getObject(TaskProgress, ErrorType.ProgressReqNotExist,
									   return_type=return_type, **args)

		# 确保任务存在
		@classmethod
		def ensureTaskExist(cls, **args):
			return ViewUtils.ensureObjectExist(
				Task, ErrorType.TaskNotExist, **args)

		# 确保任务分配存在
		@classmethod
		def ensureTaskTakeExist(cls, tid, uid):
			return ViewUtils.ensureObjectExist(
				TaskTake, ErrorType.TaskTakeNotExist, task_id=tid, user_id=uid)

		# 确保进度请求存在
		@classmethod
		def ensureTaskProgressExist(cls, **args):
			return ViewUtils.ensureObjectExist(
				TaskProgress, ErrorType.ProgressReqNotExist, **args)

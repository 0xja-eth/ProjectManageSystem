from django.db import models
from utils.model_manager import ModelUtils
from utils.exception import ErrorException, ErrorType
from enum import Enum
import datetime

# Create your models here.

# ===================================================
#  任务状态枚举
# ===================================================
class TaskStatus(Enum):
	Unstart = 1 # 未开始
	Started = 2 # 进行中
	Finished = 3 # 已完成
	Failed = 4 # 未完成
	Paused = 5 # 已暂停
	Cancelled = 6 # 已取消

# ===================================================
#  任务层级枚举
# ===================================================
class TaskLevel(Enum):
	Step = 1 # 阶段
	MainTask = 2 # 主任务
	SubTask = 3 # 子任务
	Todo = 4 # 清单

# ===================================================
#  任务表
# ===================================================
class Task(models.Model):

	class Meta:

		verbose_name = verbose_name_plural = "任务"

	NAME_LEN = 24
	DESC_LEN = 128

	TASK_STATUSES = [
		(TaskStatus.Unstart.value, '未开始'),
		(TaskStatus.Started.value, '进行中'),
		(TaskStatus.Finished.value, '已完成'),
		(TaskStatus.Failed.value, '未完成'),
		(TaskStatus.Paused.value, '已暂停'),
		(TaskStatus.Cancelled.value, '已取消'),
	]

	TASK_LEVELS = [
		(TaskLevel.Step.value, '阶段'),
		(TaskLevel.MainTask.value, '主任务'),
		(TaskLevel.SubTask.value, '子任务'),
		(TaskLevel.Todo.value, '清单'),
	]

	# 后序任务（仅用于显示顺序）
	next_order = models.ForeignKey(to='self', related_name='next_order_task', null=True, on_delete=models.SET_NULL, verbose_name="后序任务")

	# 任务名
	name = models.CharField(max_length=24, verbose_name="任务名")

	# 任务描述
	description = models.CharField(blank=True, max_length=128, verbose_name="描述")

	# 项目
	project = models.ForeignKey(to='project_module.Project', on_delete=models.CASCADE, verbose_name="项目")

	# 父任务
	parent = models.ForeignKey(to='self', related_name='parent_task', null=True, on_delete=models.CASCADE, verbose_name="父任务")

	# 创建时间
	create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

	# 开始日期
	start_date = models.DateField(null=True, blank=True, verbose_name="开始日期")

	# 结束日期
	end_date = models.DateField(null=True, blank=True, verbose_name="结束日期")

	# 任务状态
	status = models.PositiveSmallIntegerField(default=0, choices=TASK_STATUSES, verbose_name="任务状态")

	# 任务层级
	level = models.PositiveSmallIntegerField(default=0, choices=TASK_LEVELS, verbose_name="任务层级")

	# 任务进度
	progress = models.PositiveSmallIntegerField(default=0, verbose_name="任务进度")

	# 自动调整
	auto_adjust = models.BooleanField(default=True, verbose_name="自动调整")

	# 删除标志
	is_deleted = models.BooleanField(default=False, verbose_name="删除标志")

	def __str__(self):
		return "%s(%s)" % (self.name, self.project)

	def convertToDict(self, type=None):

		start_date = ModelUtils.timeToStr(self.start_date)
		end_date = ModelUtils.timeToStr(self.end_date)

		if type == "pr":
			prs = self.progressReqs()

			return {
				'task_name': self.name,
				'prs': ModelUtils.objectsToDict(prs)
			}

		if type == "project":
			return {
				'id': self.id,
				'name': self.name,
				'progress': self.progress,
				'level': self.level,
				'status_id': self.status,
				'start_date': start_date,
				'end_date': end_date,
			}

		if type == "detail":
			return self.convertToDict()

		create_time = ModelUtils.timeToStr(self.create_time)

		return {
			'id': self.id,
			'name': self.name,
			'description': self.description,
			'project_id': self.project.id,
			'project_name': self.project.name,
			'parent_id': self.parent.id,
			'parent_name': self.parent.name,
			'status_id': self.status,
			'level': self.level,
			'progress': self.progress,
			'auto_adjust': self.auto_adjust,
			'create_time': create_time,
			'start_date': start_date,
			'end_date': end_date,
		}


	# 任务分配情况
	# 获取当前任务分配集
	def taskTakes(self):
		return self.tasktake_set.all()

	# 分配任务角色
	def distribute(self, uids):

		takes = self.taskTakes()

		# 对于每一个用户ID
		for uid in uids:
			# 如果该任务分配数据存在再数据库中
			if takes.filter(user_id=uid).exists():
				# 减去该任务分配数据
				takes = takes.exclude(user_id=uid)
			else:
				# 否则增加任务分配0
				self.addTaskTake(uid)

		# 对于剩下的任务分配，删除
		for take in takes: take.delete()

	# 增加任务分配
	def addTaskTake(self, uid):
		take = TaskTake()
		take.task = self
		take.user_id = uid
		take.save()

	# 前置任务
	# 获取前置任务集
	def prevTasks(self):
		return PrevTask.objects.filter(task=self)

	# 设置前置任务集
	def setPrevTasks(self, prev_ids):

		prevs = self.prevTasks()

		# 对于每一个前置任务ID
		for prev_id in prev_ids:
			# 如果该前置任务存在再数据库中
			if prevs.filter(prev_id=prev_id).exists():
				# 减去该前置任务数据
				prevs = prevs.exclude(prev_id=prev_id)
			else:
				# 否则增加前置任务
				self.addPrevTask(prev_id)

		# 对于剩下的前序任务，删除
		for prev in prevs: prev.delete()

	# 添加一个前置任务
	# 确保了无环
	def addPrevTask(self, prev_id):

		# 确保前置任务不造成回路
		self.ensureLoopNotExist(prev_id)

		prev = PrevTask()
		prev.task = self
		prev.prev_id = prev_id
		prev.save()

	# 确保新的前置关系不会造成回路
	def ensureLoopNotExist(self, prev_id):
		if self.checkIfLoop(prev_id):
			raise ErrorException(ErrorType.LoopPrevTask)

	# 检查新的前置关系是否造成回路
	def checkIfLoop(self, prev_id):

		next_tasks = PrevTask.objects.filter(prev=self)

		# 循环判断每一个后置任务
		for next_task in next_tasks:
			task = next_task.task
			# 如果要添加前置关系的前置任务ID == 循环到的某个后置任务ID
			# 则该边添加后将会造成回路，返回 True
			if prev_id == task.id: return True
			# 如果判断到某个后置任务会造成回路，返回 True
			if task.checkIfLoop(prev_id):
				return True

		return False

	# 进度请求
	# 新增一个进度请求
	def addProgressReq(self, user, progress, desc):

		req = TaskProgress()
		req.progress = progress
		req.description = desc
		req.user = user
		req.task = self
		req.save()

	# 获取任务的全部进度请求（unresulted 为是否考虑未审阅过的请求）
	def progressReqs(self, unresulted=True):
		reqs = self.taskprogress_set
		if unresulted: return reqs.all()
		# 获取 result_time 不是 null 的请求（即审阅过）
		return reqs.filter(result_time__isnull=False)

	# 获取未审阅过的请求（只能有一个）
	def unresultedProgressReq(self):
		req = self.progressReqs().filter(result_time__isnull=True)
		if req.exists(): return req[0]
		return None

	# 改变进度
	def changeProgress(self, progress):

		self.progress = progress
		self._refreshStatus()

	# 刷新状态
	def _refreshStatus(self):

		now = datetime.datetime.now()

		self.progress = max(min(self.progress, 100), 0)

		if self.progress >= 100:
			self.status = TaskStatus.Finished.value
		elif now >= self.start_date:
			self.status = TaskStatus.Started.value
		else:
			self.status = TaskStatus.Unstart.value

		self.save()

	# 向前推导，更新自己的开始结束时间
	def deduction(self):
		self.visited = True
		if not self.auto_adjust: return

		duration = self.end_date-self.start_date

		# 获取前置任务组
		prev_tasks = self.prevTasks()

		# 如果前一个任务不存在
		if not prev_tasks.exists() and \
				self.start_date<self.project.start_date:
			self.start_date = self.project.start_date

		else: # 否则
			for prev_task in prev_tasks:
				# 推导一个前置任务
				task = prev_task.prev
				if not task.visited: task.deduction()
				# 调整开始/结束时间
				self.start_date = max(task.end_date, self.start_date)

		self.end_date = self.start_date+duration

# ===================================================
#  前置任务表
# ===================================================
class PrevTask(models.Model):

	class Meta:

		verbose_name = verbose_name_plural = "前置任务"

	# 本任务
	task = models.ForeignKey(to='Task', related_name='currtask', on_delete=models.CASCADE, verbose_name="本任务")

	# 前置任务
	prev = models.ForeignKey(to='Task', related_name='prevtask', on_delete=models.CASCADE, verbose_name="前置任务")

	def __str__(self):
		return "%s->%s" % (self.prev, self.task)

# ===================================================
#  任务参与关系表
# ===================================================
class TaskTake(models.Model):

	class Meta:

		verbose_name = verbose_name_plural = "任务参与关系"

	# 用户
	user = models.ForeignKey(to='user_module.User', on_delete=models.CASCADE, verbose_name="用户")

	# 任务
	task = models.ForeignKey(to='Task', on_delete=models.CASCADE, verbose_name="任务")

	def __str__(self):
		return "%s-%s" % (self.user, self.task)

# ===================================================
#  任务进度请求表
# ===================================================
class TaskProgress(models.Model):

	class Meta:

		verbose_name = verbose_name_plural = "任务进度请求"

	# 发起者
	user = models.ForeignKey(to='user_module.User', on_delete=models.CASCADE, verbose_name="发起用户")

	# 任务
	task = models.ForeignKey(to='Task', on_delete=models.CASCADE, verbose_name="任务")

	# 目标进度
	progress = models.PositiveSmallIntegerField(default=0, verbose_name="目标进度")

	# 进度说明
	description = models.CharField(blank=True, max_length=128, verbose_name="进度说明")

	# 评审结果
	result = models.BooleanField(default=False, verbose_name="评审结果")

	# 创建时间
	create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

	# 评审时间
	result_time = models.DateTimeField(null=True, blank=True, verbose_name="评审时间")

	def __str__(self):
		return "%s-%s(%d%%)" % (self.user, self.task, self.progress)

	def converToDict(self, type=None):

		create_time = ModelUtils.timeToStr(self.create_time)
		result_time = ModelUtils.timeToStr(self.result_time, None)

		result = {
			'id': self.id,
			'creator_id': self.user_id,
			'creator_name': self.user.name,
			'task_id': self.task_id,
			'progress': self.progress,
			'desc': self.description,
			'create_time': create_time,
		}

		if result_time:
			result['result'] = self.result
			result['result_time'] = result_time

		return result

	# 审阅
	def oper(self, result, progress=None):

		self.result = result
		self.result_time = datetime.datetime.now()

		if result:
			if progress is not None: self.progress = progress
			self.task.changeProgress(self.progress)

		self.save()


from django.db import models
from django.db.models import Count, Sum
from user_module.models import User
from task_module.models import Task, TaskStatus, PrevTask, TaskTake
from utils.model_manager import ModelManager
from enum import Enum
import datetime

# Create your models here.

# ===================================================
#  项目类型枚举
# ===================================================
class ProjectType(Enum):
	Internet = 1 # 互联网
	Finance = 2 # 金融
	Commerce = 3 # 电商
	Education = 4 # 教育
	Game = 5 # 游戏
	Science = 6 # 科学
	Industry = 7 # 工业
	Welfare = 8 # 公益
	Government = 9 # 政府
	Other = 10 # 其他

# ===================================================
#  项目表
# ===================================================
class Project(models.Model):

	class Meta:

		verbose_name = verbose_name_plural = "项目"

	NAME_LEN = 16
	DESC_LEN = 256

	# 项目类型
	PROJECT_TYPES = [
		(ProjectType.Internet.value, '互联网'),
		(ProjectType.Finance.value, '金融'),
		(ProjectType.Commerce.value, '电商'),
		(ProjectType.Education.value, '教育'),
		(ProjectType.Game.value, '游戏'),
		(ProjectType.Science.value, '科学'),
		(ProjectType.Industry.value, '工业'),
		(ProjectType.Welfare.value, '公益'),
		(ProjectType.Government.value, '政府'),
		(ProjectType.Other.value, '其他'),
	]

	# 项目名
	name = models.CharField(max_length=16, verbose_name="项目名")

	# 项目类型
	type = models.PositiveSmallIntegerField(default=0, choices=PROJECT_TYPES, verbose_name="项目类型")

	# 聊天室
	chat = models.OneToOneField('chat_module.Chat', null=True, on_delete=models.CASCADE, verbose_name="聊天室")

	# 描述
	description = models.CharField(blank=True, max_length=256, verbose_name="描述")

	# 创建时间
	create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

	# 开始日期
	start_date = models.DateField(null=True, blank=True, verbose_name="开始日期")

	# 结束日期
	end_date = models.DateField(null=True, blank=True, verbose_name="结束日期")

	# 首位任务（仅用于显示顺序）
	first_task = models.OneToOneField(to='task_module.Task', related_name='task_project',
								   null=True, on_delete=models.SET_NULL, verbose_name="首位任务")

	# 删除标志
	is_deleted = models.BooleanField(default=False, verbose_name="删除标志")

	def __str__(self):
		return "%s(%s)" % (self.name, self._creatorName())

	def _creatorName(self):
		user = self.creator()
		if user: return str(user)
		return '未知'

	def convertToDict(self, type=None):

		# 获取索引信息
		if type == "index":
			return {
				'id': self.id,
				'name': self.name,
			}

		if type == "pr":
			tasks = self.tasks()
			return {'tasks': ModelManager.objectsToDict(tasks, type='pr')}

		# 汇总信息
		if type == "total":

			sum_tasks, unstart_tasks, started_tasks, \
				finished_tasks, progress = self.analayTasks()

			return {
				'name': "汇总",
				'sum_tasks': sum_tasks,
				'unstart_tasks': unstart_tasks,
				'started_tasks': started_tasks,
				'finished_tasks': finished_tasks,
				'progress': progress/sum_tasks,
				'total': True
			}

		if type == "notices":
			notices = self.notice_set.all()
			creator = self.creator()
			return {
				'id': self.id,
				'name': self.name,
				'creator_id': creator.id,
				'creator_name': creator.name,
				'notices': ModelManager.objectsToDict(notices)
			}

		# 获取成员视图数据
		if type == "members":

			ann = self.tasks().annotate(req_cnt=Count(
				'taskprogress__id', distinct=True))
			agg = ann.aggregate(req_cnt=Sum('req_cnt'))

			members = self.members()

			member_info = ModelManager.objectsToDict(
				members, type="member_info", proj=self)
			member_task = ModelManager.objectsToDict(
				members, type="member_task", proj=self)

			for i in range(members.count()):
				# 玩家是否处于空闲状态 = 进行中的任务数是否为 0
				member_info[i]['is_free'] = \
					member_task[i]['started_tasks'] == 0
				member_task[i]['rids'] = member_info[i]['rids']

			member_task.append(self.convertToDict('total'))

			return {
				'req_cnt': agg['req_cnt'],
				'member_info': member_info,
				'member_task': member_task,
			}

		chat_id = ModelManager.objectToId(self.chat)
		create_time = ModelManager.timeToStr(self.create_time)
		start_date = ModelManager.timeToStr(self.start_date)
		end_date = ModelManager.timeToStr(self.end_date)

		res = {
			'id': self.id,
			'name': self.name,
			'type_id': self.type,
			'description': self.description,
			'create_time': create_time,
			'start_date': start_date,
			'end_date': end_date,
			'chat_id': chat_id
		}

		# 获取详情信息（用于详情页展示）
		if type == "detail":

			members = ModelManager.objectsToDict(
				self.members(), type="member", proj=self)
			tasks = ModelManager.objectsToDict(
				self.tasks(True), type="project")

			res['members'] = members
			res['tasks'] = tasks

		return res

	# 成员操作
	# 获取创建人（返回 User）
	def creator(self):
		part = self.participation_set.filter(
			participationrole__role_id=Role.ProjectManagerId)
		if part.exists(): return part[0].user
		return None

	# 获取成员数组（返回 User[]）
	def members(self):
		return ModelManager.getObjectRelatedForAll(
			self.participation_set, 'user')

	# 增加（多个）成员
	# member_data: {uid, rids}
	def addMembers(self, member_data):

		for data in member_data:
			uid = data['uid']
			rids = data['rids']
			self.addMember(uid, rids)

	# 增加一个成员
	def addMember(self, uid, rids):

		part = Participation()
		part.user_id = uid
		part.project = self
		part.save()

		for rid in rids:
			self.addParticipateRole(part, rid)

	# 修改（多个）成员角色
	# member_data: {uid, rids}
	def editMembers(self, member_data):

		for data in member_data:
			uid = data['uid']
			rids = data['rids']
			self.editMember(uid, rids)

	# 修改一个成员角色
	def editMember(self, uid, rids):

		from .views import ProjectManager

		part = ProjectManager.Common.getParticipation(uid, self.id)
		roles = self.getRoles(uid=uid)

		# 对于每一个角色ID
		for rid in rids:
			# 如果该角色关系数据存在再数据库中
			if roles.filter(role_id=rid).exists():
				# 减去该角色关系
				roles = roles.exclude(role_id=rid)
			else:
				self.addParticipateRole(part, rid)

		# 对于剩下的角色关系，删除
		for role in roles: role.delete()

	# 增加一个参与角色
	def addParticipateRole(self, part, rid):

		role = ParticipationRole()
		role.participation = part
		role.role_id = rid
		role.save()

	# 删除（多个）成员
	# member_data: {uid, rids}
	def deleteMembers(self, uids):

		from .views import ProjectManager

		for uid in uids:
			part = ProjectManager.Common.getParticipation(uid, self.id)
			part.delete()

	# 角色操作
	# 获取某角色参与该项目中的角色数组（返回 Role[]）
	def getRoles(self, user: User=None, uid=None):

		from .views import ProjectManager

		if user is not None: uid = user.id

		part = ProjectManager.Common.getParticipation(uid, self.id)

		return ModelManager.getObjectRelatedForAll(
			part.participationrole_set, 'role', True)

	# 获取某角色参与该项目中的角色ID数组（返回 int[]）
	def getRoleIds(self, user: User, uid=None):
		result = []
		roles = self.getRoles(user, uid)
		for r in roles: result.append(r.id)

		return result

	def changeProjectManager(self, creator: User, uid):

		from .views import ProjectManager

		cpart = ProjectManager.Common.getParticipation(creator.id, self.id)
		mpart = ProjectManager.Common.getParticipation(uid, self.id)

		role = cpart.participationrole_set.filter(role_id=Role.ProjectManagerId)
		if not role.exists(): return
		role.participation = mpart
		role.save()



	# 任务操作
	# 获取任务数组（返回 Task[]）
	def tasks(self, ordered=False, include_deleted=False):
		if self.first_task is None: return []
		if not ordered: return self._tasks(include_deleted)
		else: return self._orderedTasks(include_deleted)

	def _tasks(self, include_deleted=False):
		if include_deleted: return self.task_set.all()
		return self.task_set.filter(is_deleted=False)

	def _orderedTasks(self, include_deleted=False):
		task = self.first_task
		tasks = [task]
		while task.next_order:
			task = task.next_order
			# 如果包含删除 或 删除标记为 False
			if include_deleted or not task.is_deleted:
				tasks.append(task)

		return tasks

	# 最后一个任务
	def lastTask(self):
		if self.first_task is None: return None
		temp = self.tasks().filter(next_order__isnull=True)
		if temp.exists(): return temp.first()
		return None

	# 前一个任务
	def prevOrderTask(self, task):
		if self.first_task is None: return None
		temp = self.tasks().filter(next_order=task)
		if temp.exists(): return temp.first()
		return None

	# 获取某角色参与该项目中的任务数组（返回 Task 的 QuerySet）
	def getMemberTasks(self, user: User, status=None):
		if status is None:
			return ModelManager.getObjectRelatedForFilter(
				user.tasktake_set, 'task', task_project=self)
		else:
			return ModelManager.getObjectRelatedForFilter(
				user.tasktake_set, 'task',
				task__project=self, task__status=status)

	# 分析任务情况
	def analayTasks(self, tasks=None):

		from task_module.models import TaskStatus

		if tasks is None: tasks = self.tasks(True)

		unstart_tasks = started_tasks = finished_tasks = 0
		sum_tasks = len(tasks)
		progress = 0.0

		for i in range(sum_tasks):
			status = tasks[i].status
			progress += tasks[i].progress

			if status == TaskStatus.Unstart.value:
				unstart_tasks += 1
			if status == TaskStatus.Started.value:
				started_tasks += 1
			if status == TaskStatus.Finished.value:
				finished_tasks += 1

		return sum_tasks, unstart_tasks, started_tasks, \
			finished_tasks, progress


	# 任务调整
	# task_data: {task, prev_ids}
	def adjustTasks(self, task_data):

		for i in range(len(task_data)):
			task = task_data[i]['task']
			prev_ids = task_data[i]['prev_ids']

			# 调整任务顺序
			if i == 0: self.first_task = task
			else:
				prev_task = task_data[i-1]['task']
				prev_task.next_order = task

			task.setPrevTasks(prev_ids)

			task.save()

		self.save()

	# 增加任务
	def addTask(self, name, desc, parent_id, prev_ids, auto_adjust,
				start_date, end_date, prev_order: Task = None):

		# 设置基本信息
		task = Task()
		task.project = self

		# 调用修改信息
		self.editTask(task, name, desc, parent_id, prev_ids, auto_adjust,
					  0, start_date, end_date, None, prev_order)

	# 修改任务
	def editTask(self, task: Task, name, desc, parent_id, prev_ids, auto_adjust,
				progress, start_date, end_date, status_id=None, prev_order: Task = None):

		# 设置基本信息
		task.name = name
		task.description = desc
		task.parent_id = parent_id
		task.auto_adjust = auto_adjust
		task.progress = progress
		task.start_date = start_date
		task.end_date = end_date

		# 设置任务状态
		# 如果传了状态ID，设置状态
		if status_id: task.status = status_id
		# 否则状态改为 Unsetart (将会自动调整）
		else: task.status = TaskStatus.Unstart

		# 设置任务顺序
		# 先检查原有位置
		if task.next_order is not None:
			# 获取原来的前序任务
			prev = self.prevOrderTask(task)
			if prev is not None:
				prev.next_order = task.next_order
			else:
				self.first_task = task.next_order

		# 如果前序任务非空，插入
		if prev_order is not None:
			task.next_order = prev_order.next_order
			prev_order.next_order = task
			prev_order.save()
		# 否则从头插入
		else:
			task.next_order = self.first_task
			self.first_task = task
			self.save()

		# 设置前置任务
		task.setPrevTasks(prev_ids)

		task.save()

		self.refreshTasks()

	# 删除任务
	def deleteTask(self, task: Task):

		# 获取原来的前序任务
		prev = self.prevOrderTask(task)
		if prev is not None:
			prev.next_order = task.next_order
		else:
			self.first_task = task.next_order

		if self.first_task == task:
			self.first_task = task.next_order
		else:
			# 找到该任务的前序任务
			prev_order = self.tasks().filter(next_order=task)
			# 如果存在，设置后序任务
			if prev_order.exists():
				prev_order = prev_order[0]
				prev_order.next_order = task.next_order

		task.delete()

		self.refreshTasks()

	# 刷新任务（向前推导）
	def refreshTasks(self):

		# 找到自动调整的任务
		tasks = self.tasks().filter(auto_adjust=True)

		# 初始化 visited
		for task in tasks:
			task.visited = False

		# 每一个任务都进行一次推导
		for task in tasks:
			if not task.visited: task.deduction()

		# 更新项目起止时间
		for task in tasks:
			self.start_date = min(self.start_date, task.start_date)
			self.end_date = max(self.end_date, task.end_date)

		# 推导完毕，全部保存
		for task in tasks: task.save()

		self.save()


	# 通知操作
	# 增加通知
	def addNotice(self, title, content):

		notice = Notice()
		notice.project = self
		notice.title = title
		notice.content = content
		notice.save()

	# 删除通知
	def deleteNotices(self, nids):

		notices = self.notice_set.filter(id__in=nids)

		for notice in notices:
			notice.delete()

# ===================================================
#  角色表
# ===================================================
class Role(models.Model):

	class Meta:

		verbose_name = verbose_name_plural = "角色"

	# 项目经理角色ID
	ProjectManagerId = 1

	# 角色名
	name = models.CharField(max_length=8, verbose_name="角色名")

	# 角色描述
	description = models.CharField(blank=True, max_length=48, verbose_name="描述")

	def __str__(self):
		return self.name

	def convertToDict(self):
		return {
			'id': self.id,
			'name': self.name,
			'description': self.description
		}

# ===================================================
#  项目参与关系表
# ===================================================
class Participation(models.Model):

	class Meta:

		verbose_name = verbose_name_plural = "项目参与关系"

	# 用户
	user = models.ForeignKey(to='user_module.User', on_delete=models.CASCADE,
							 verbose_name="用户")

	# 项目
	project = models.ForeignKey(to='Project', on_delete=models.CASCADE,
								verbose_name="项目")

	# 加入时间
	join_time = models.DateTimeField(auto_now_add=True, verbose_name="加入时间")

	def __str__(self):
		return "%s-%s" % (self.user, self.project)

# ===================================================
#  参与角色表
# ===================================================
class ParticipationRole(models.Model):

	class Meta:

		verbose_name = verbose_name_plural = "参与角色"

	# 参与关系
	participation = models.ForeignKey(to='Participation', on_delete = models.CASCADE,
									verbose_name="参与关系")

	# 角色
	role = models.ForeignKey(to='Role', on_delete = models.CASCADE,
						   verbose_name="角色")

	def __str__(self):
		return "%s(%s)" % (self.participation, self.role)

# ===================================================
#  通知表
# ===================================================
class Notice(models.Model):

	class Meta:

		verbose_name = verbose_name_plural = "通知"

	# 标题
	title = models.CharField(max_length=32, verbose_name="标题")

	# 内容
	content = models.CharField(blank=True, max_length=512, verbose_name="内容")

	# 项目
	project = models.ForeignKey(to='Project', on_delete = models.CASCADE,
							  verbose_name="项目")

	# 创建时间
	create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

	# 删除标志
	is_deleted = models.BooleanField(default=False, verbose_name="删除标志")

	def __str__(self):
		return "%s(%s)" % (self.title, self.project)

	def convertToDict(self, type=None, **args):

		from .views import ProjectManager

		result = {
			'id': self.id,
			'title': self.title,
			'content': self.content,
			'create_time': self.create_time,
		}

		if type == 'receive':
			user = args['args']
			receive = ProjectManager.Common.\
				createOrGetNoticeReceive(self.id, user.id)
			receive = receive.convertToDict()

			result['rid'] = receive['id']
			if 'read_time' in receive:
				result['read_time'] = receive['read_time']

		return result

# ===================================================
#  通知接收表
# ===================================================
class NoticeReceive(models.Model):

	class Meta:

		verbose_name = verbose_name_plural = "通知接收"

	# 用户
	user = models.ForeignKey(to='user_module.User', on_delete=models.CASCADE,
						   verbose_name="用户")

	# 通知
	notice = models.ForeignKey(to='Notice', on_delete=models.CASCADE,
							 verbose_name="通知")

	# 阅读时间
	read_time = models.DateTimeField(null=True, blank=True, verbose_name="阅读时间")

	def __str__(self):
		return "%s-%s" % (self.user, self.notice)

	def convertToDict(self):

		read_time = ModelManager.timeToStr(self.read_time, None)

		if read_time is not None:
			return {
				'id': self.id,
				'read_time': read_time
			}

		return {'id': self.id}

	def read(self):
		self.read_time = datetime.datetime.now()
		self.save()
from django.db import models
from enum import Enum

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
	Step = 0 # 阶段
	MainTask = 1 # 主任务
	SubTask = 2 # 子任务
	Todo = 3 # 清单

class Task(models.Model):

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

	order = models.PositiveSmallIntegerField(null=True)
	name = models.CharField(max_length=24)
	description = models.CharField(blank=True, max_length=128)
	project = models.ForeignKey(to='project_module.Project', on_delete=models.CASCADE)
	parent = models.ForeignKey(to='self', null=True, on_delete=models.CASCADE)
	create_time = models.DateTimeField(auto_now_add=True)
	start_time = models.DateTimeField(null=True, blank=True)
	end_time = models.DateTimeField(null=True, blank=True)
	status = models.PositiveSmallIntegerField(default=0, choices=TASK_STATUSES)
	level = models.PositiveSmallIntegerField(default=0, choices=TASK_LEVELS)
	progress = models.PositiveSmallIntegerField(default=0)
	is_deleted = models.BooleanField(default=False)



class PrevTask(models.Model):
	task = models.ForeignKey(to='Task', related_name='currtask', on_delete=models.CASCADE)
	prev = models.ForeignKey(to='Task', related_name='prevtask', on_delete=models.CASCADE)


class TaskTake(models.Model):
	user = models.ForeignKey(to='user_module.User', on_delete=models.CASCADE)
	task = models.ForeignKey(to='Task', on_delete=models.CASCADE)


class TaskProgress(models.Model):
	user = models.ForeignKey(to='user_module.User', on_delete=models.CASCADE)
	task = models.ForeignKey(to='Task', on_delete=models.CASCADE)
	progress = models.SmallIntegerField(default=0)
	description = models.CharField(blank=True, max_length=128)
	result = models.BooleanField(default=False)
	create_time = models.DateTimeField(auto_now_add=True)
	result_time = models.DateTimeField(null=True, blank=True)

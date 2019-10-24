from django.db import models
from enum import Enum

# Create your models here.

# ===================================================
#  项目类型枚举
# ===================================================
class ProjectType(Enum):
	Internet = 0 # 互联网
	Finance = 1 # 金融
	Commerce = 2 # 电商
	Education = 3 # 教育
	Game = 4 # 游戏
	Science = 5 # 科学
	Industry = 6 # 工业
	Welfare = 7 # 公益
	Government = 8 # 政府
	Other = 9 # 其他

class Project(models.Model):
	# 项目类型都有哪些
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

	name = models.CharField(max_length=16)
	type = models.PositiveSmallIntegerField(default=0, choices=PROJECT_TYPES)
	chat = models.OneToOneField('chat_module.Chat', null=True, on_delete=models.CASCADE)
	description = models.CharField(blank=True, max_length=256)
	create_time = models.DateTimeField(auto_now_add=True)
	start_time = models.DateTimeField(null=True, blank=True)
	end_time = models.DateTimeField(null=True, blank=True)
	is_deleted = models.BooleanField(default=False)


class Role(models.Model):
	ProjectManagerId = 1

	name = models.CharField(max_length=8)
	description = models.CharField(blank=True, max_length=48)

	def convertToDict(self):
		return {
			'id': self.id,
			'name': self.name,
			'description': self.description
		}

class Participation(models.Model):
	user = models.ForeignKey(to='user_module.User', on_delete=models.CASCADE)
	project = models.ForeignKey(to='Project', on_delete=models.CASCADE)
	join_time = models.DateTimeField(auto_now_add=True)


class ParticipationRole(models.Model):
	participation=models.ForeignKey(to='Participation', on_delete = models.CASCADE)
	role=models.ForeignKey(to='Role', on_delete = models.CASCADE)

class Notice(models.Model):
	title=models.CharField(max_length=32)
	content=models.CharField(blank=True, max_length=512)
	project=models.ForeignKey(to='Project', on_delete = models.CASCADE)
	create_time=models.DateTimeField(auto_now_add=True)
	is_deleted=models.BooleanField(default=False)

class NoticeReceive(models.Model):
	user=models.ForeignKey(to='user_module.User', on_delete = models.CASCADE)
	notice=models.ForeignKey(to='Notice', on_delete = models.CASCADE)
	read_time=models.DateTimeField(null=True, blank=True)

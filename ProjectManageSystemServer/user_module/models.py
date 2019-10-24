from django.db import models
from utils.model_manager import ModelManager
from enum import Enum

# Create your models here.

# ===================================================
#  用户学历枚举
# ===================================================
class UserEduaction(Enum):
	PrimarySchool = 0 # 小学
	MiddleSchool = 1 # 初中
	HighSchool = 2 # 高中
	Specialty = 3 # 专科
	Undergraduate = 4 # 本科
	Master = 5 # 硕士
	Doctor = 6 # 博士
	Other = 7 # 其他

# ===================================================
#  用户状态枚举
# ===================================================
class UserStatus(Enum):
	Offline = 0 # 离线
	Online = 1 # 在线
	Other = 2 # 其他

class User(models.Model):

	PASSWORD_SALT = 'd28cb767c4272d8ab91000283c67747cb2ef7cd1'

	UN_LEN = 16
	PWD_LEN = [8,32]
	EMAIL_REG = r'^[A-Za-z0-9一-龥]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/'

	USER_EDUCATIONS = [
		(UserEduaction.PrimarySchool.value, '小学'),
		(UserEduaction.MiddleSchool.value, '初中'),
		(UserEduaction.HighSchool.value, '高中'),
		(UserEduaction.Specialty.value, '专科'),
		(UserEduaction.Undergraduate.value, '本科'),
		(UserEduaction.Master.value, '硕士'),
		(UserEduaction.Doctor.value, '博士'),
		(UserEduaction.Other.value, '其他'),
	]
	USER_STATUSES = [
		(UserStatus.Offline.value, '离线'),
		(UserStatus.Online.value, '在线'),
		(UserStatus.Other.value, '其他'),
	]

	username = models.CharField(max_length=64)
	password = models.CharField(max_length=64)
	email = models.CharField(max_length=128)
	name = models.CharField(blank=True, max_length=12)
	gender = models.BooleanField(null=True, blank=True)
	avatar = models.ImageField(null=True, blank=True)
	birth = models.DateField(null=True, blank=True)
	city = models.CharField(blank=True, max_length=16)
	education = models.PositiveSmallIntegerField(default=0, choices=USER_EDUCATIONS)
	duty = models.CharField(blank=True, max_length=16)
	contact = models.CharField(blank=True, max_length=16)
	description = models.CharField(blank=True, max_length=100)
	create_time = models.DateTimeField(auto_now_add=True)
	status = models.PositiveSmallIntegerField(default=0, choices=USER_STATUSES)
	is_deleted = models.BooleanField(default=False)

	def convertToDict(self, type=None, params=None):

		create_time = self.create_time.strftime('%Y-%m-%d %H:%M:%S')

		# 获取陌生人的资料
		if type == 'stranger':
			return {
				'id': self.id,
				'username': self.username,
				'gender': self.gender,
				'avatar': self.avatar,
				'description': self.description,
				'status_id': self.status,
			}

		# 获取好友的资料
		if type == 'friend':
			return self.convertToDict()

		# 获取好友列表
		if type == 'friends':
			return ModelManager.objectsToDict(self.getFriends())

		# 个人详细资料
		return {
			'id': self.id,
			'username': self.username,
			'email': self.email,
			'name': self.name,
			'gender': self.gender,
			'avatar': self.avatar,
			'birth': self.birth,
			'city': self.city,
			'education_id': self.education,
			'duty': self.duty,
			'contact': self.contact,
			'description': self.description,
			'create_time': create_time,
			'status_id': self.status,
		}

	def getFriends(self, accepted=True):
		return Friend.objects.filter(subject_id=self.id, accepted=accepted)

	# 登陆
	def login(self):
		self.status = UserStatus.Online.value
		self.save()

	# 登出
	def logout(self):
		self.status = UserStatus.Offline.value
		self.save()

	# 发送好友请求
	# TODO(吴宁): 该函数为实际操作的函数，不需检查重复添加
	def addFriend(self, fuid):
		pass


class Friend(models.Model):
	subject = models.ForeignKey(to='User', related_name='subject', on_delete=models.CASCADE)
	object = models.ForeignKey(to='User', related_name='object', on_delete=models.CASCADE)
	send_time = models.DateTimeField(auto_now_add=True)
	accepted = models.BooleanField(default=False)
	# accepted 后才有 chat
	chat = models.OneToOneField('chat_module.Chat', null=True, on_delete=models.CASCADE)

	def convertToDict(self):

		cid = 0
		if self.chat: cid = self.chat_id

		return {
			'sid': self.subject_id,
			'object': self.object.convertToDict('friend'),
			'cid': cid
		}




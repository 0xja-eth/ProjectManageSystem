from django.db import models
from utils.model_manager import ModelManager
from enum import Enum
import datetime

# Create your models here.

# ===================================================
#  用户学历枚举
# ===================================================
class UserEduaction(Enum):
	PrimarySchool = 1 # 小学
	MiddleSchool = 2 # 初中
	HighSchool = 3 # 高中
	Specialty = 4 # 专科
	Undergraduate = 5 # 本科
	Master = 6 # 硕士
	Doctor = 7 # 博士
	Other = 8 # 其他

# ===================================================
#  用户状态枚举
# ===================================================
class UserStatus(Enum):
	Offline = 1 # 离线
	Online = 2 # 在线
	Other = 3 # 其他

class User(models.Model):

	class Meta:

		verbose_name = verbose_name_plural = "用户"

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

	# 用户名
	username = models.CharField(max_length=64, verbose_name="用户名")

	# 密码
	password = models.CharField(max_length=64, verbose_name="密码")

	# 邮箱
	email = models.CharField(max_length=128, verbose_name="邮箱")

	# 姓名
	name = models.CharField(blank=True, max_length=12, verbose_name="姓名")

	# 性别
	gender = models.BooleanField(null=True, blank=True, verbose_name="性别")

	# 头像
	avatar = models.ImageField(null=True, blank=True, verbose_name="头像",
							   upload_to=ModelManager.PictureUpload('players'))

	# 生日
	birth = models.DateField(null=True, blank=True, verbose_name="生日")

	# 居住地
	city = models.CharField(blank=True, max_length=16, verbose_name="居住地")

	# 学历
	education = models.PositiveSmallIntegerField(default=0, choices=USER_EDUCATIONS, verbose_name="学历")

	# 职位
	duty = models.CharField(blank=True, max_length=16, verbose_name="职位")

	# 联系方式
	contact = models.CharField(blank=True, max_length=16, verbose_name="联系方式")

	# 个人介绍
	description = models.CharField(blank=True, max_length=100, verbose_name="个人介绍")

	# 注册时间
	create_time = models.DateTimeField(auto_now_add=True, verbose_name="注册时间")

	# 登录状态
	status = models.PositiveSmallIntegerField(default=0, choices=USER_STATUSES, verbose_name="登录状态")

	# 删除标志
	is_deleted = models.BooleanField(default=False, verbose_name="删除标志")

	def __str__(self):
		return "%d.%s(%s)" % (self.id, self.name, self.username)

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
			'gender': int(self.gender),
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

	class Meta:

		verbose_name = verbose_name_plural = "好友关系"

	# 发起用户
	subject = models.ForeignKey(to='User', related_name='subject', on_delete=models.CASCADE, verbose_name="发起用户")

	# 目标用户
	object = models.ForeignKey(to='User', related_name='object', on_delete=models.CASCADE, verbose_name="目标用户")

	# 发起时间（如果同意了，改为同意时间）
	send_time = models.DateTimeField(auto_now_add=True, verbose_name="发起时间")

	# 接受标志
	accepted = models.BooleanField(default=False, verbose_name="接受")

	# accepted 后才有 chat
	# 聊天室
	chat = models.OneToOneField('chat_module.Chat', null=True, on_delete=models.CASCADE, verbose_name="聊天室")

	def __str__(self):
		return "%s-%s" % (str(self.subject), str(self.object))

	def convertToDict(self):

		cid = 0
		if self.chat: cid = self.chat_id

		return {
			'sid': self.subject_id,
			'object': self.object.convertToDict('friend'),
			'cid': cid
		}

	# 操作
	def oper(self, accepted):
		if accepted: # 如果接受
			self.accepted = True
			self.send_time = datetime.datetime.now()
			self.save()

		else: # 否则删除
			self.delete()


from django.shortcuts import render
from utils.exception import ErrorException, ErrorType
from utils.view_manager import ViewManager
from utils.interface_manager import InterfaceManager
from user_module.models import User
from user_module.views import UserManager
from .models import *
import datetime, random, re, hashlib, smtplib

# Create your views here.
class ProjectManager():

	# 业务逻辑
	# 获取项目
	@classmethod
	def get(cls, user: User, pid=None):

		# 若不传 pid 参数，获取该用户所有 Project
		if pid is None: return cls._getProjects(user)

		# 否则，获取指定 pid 的 Project
		pid = InterfaceManager.convertDataType(pid, 'int')
		return cls._getProject(user, pid)

	# 获取项目列表
	@classmethod
	def _getProjects(cls, user):

		# parts = user.participation_set.all().select_related('project')
		# projs = ModelManager.getObjectRelated(parts, 'project')

		projs = ModelManager.getObjectRelatedForAll(user.participation_set, 'project')
		projs = ModelManager.objectsToDict(projs, type="index")

		return {'projects': projs}

	# 获取单个项目的详细数据
	@classmethod
	def _getProject(cls, user, pid):

		# 确保参与了该项目
		cls.Common.ensureParticipationExist(user.id, pid)
		proj = cls.Common.getProject(id=pid)

		return proj.convertToDict("detail")

	# 获取项目的成员视图数据
	@classmethod
	def getMembers(cls, user: User, pid):

		# 确保参与了该项目
		cls.Common.ensureParticipationExist(user.id, pid)
		proj = cls.Common.getProject(id=pid)

		return proj.convertToDict("members")

	# 新建项目（返回创建任务的ID）
	@classmethod
	def new(cls, user: User, name, type_id, start_date, desc):

		cls.Check.ensureNameFormat(name)
		cls.Check.ensureTypeFormat(type_id)
		cls.Check.ensureDescFormat(desc)

	@classmethod
	def _doNew(cls, user, name, type_id, start_date, desc):

		proj = Project()
		proj.name = name
		proj.type = type_id
		proj.start_date = start_date
		proj.description = desc

		proj.addMember(user.id, [Role.ProjectManagerId])

	# 修改项目信息
	@classmethod
	def edit(cls, user: User, pid, name, type_id, start_date, desc):

		cls.Common.ensureProjectManager(user.id, pid)
		proj = cls.Common.getProject(id=pid)

		proj.name = name
		proj.type = type_id
		proj.start_date = start_date
		proj.description = desc
		proj.save()

	# 删除项目
	@classmethod
	def delete(cls,user: User, pid, pw):

		# 验证密码
		UserManager.Check.ensurePasswordFormat(pw)
		UserManager.Common.ensurePasswordCorrect(user, pw)

		# 身份校验
		cls.Common.ensureProjectManager(user.id, pid)

		proj = cls.Common.getProject(id=pid)
		proj.delete()

	# 添加成员
	@classmethod
	def addMembers(cls,user: User, pid, uids, rids, pw):

		# 验证身份
		cls.Common.ensureProjectManager(user.id, pid)

		# 验证密码
		UserManager.Check.ensurePasswordFormat(pw)
		UserManager.Common.ensurePasswordCorrect(user, pw)

		member_data = []

		for i in range(len(uids)):
			uid = uids[i]
			rids_ = rids[i]

			# 确保每一个用户都存在
			UserManager.Common.ensureUserExist(id=uid)
			# 确保每一个角色都存在
			for rid in rids_:
				cls.Common.ensureRoleExist(rid)

			member_data.append({'uid': uid, 'rids': rids_})

		proj = cls.Common.getProject(id=pid)
		proj.addMembers(member_data)

	# 修改成员角色
	@classmethod
	def editMembers(cls,user: User, pid, uids, rids):

		# 验证身份
		cls.Common.ensureProjectManager(user.id, pid)

		member_data = []

		for i in range(len(uids)):
			uid = uids[i]
			rids_ = rids[i]

			# 确保每一个用户都参与本项目
			cls.Common.ensureParticipationExist(uid, pid)

			# 确保每一个角色都存在
			for rid in rids_:
				cls.Common.ensureRoleExist(rid)

			member_data.append({'uid': uid, 'rids': rids_})

		proj = cls.Common.getProject(id=pid)
		proj.editMembers(member_data)

	# 踢出成员
	@classmethod
	def deleteMembers(cls,user: User, pid, uids, pw):

		# 验证身份
		cls.Common.ensureProjectManager(user.id, pid)

		# 验证密码
		UserManager.Check.ensurePasswordFormat(pw)
		UserManager.Common.ensurePasswordCorrect(user, pw)

		proj = cls.Common.getProject(id=pid)
		proj.deleteMembers(uids)

	# 修改项目经理
	@classmethod
	def changeProjectManager(cls,user: User, pid, uid, pw):

		# 验证身份
		cls.Common.ensureProjectManager(user.id, pid)

		# 验证密码
		UserManager.Check.ensurePasswordFormat(pw)
		UserManager.Common.ensurePasswordCorrect(user, pw)

		proj = cls.Common.getProject(id=pid)
		proj.changeProjectManager(user, uid)

	# 获取通知（全部项目，按项目分组，包括详细内容）
	@classmethod
	def getNotices(cls,user: User):

		projs = cls.Common.getProjects(user)

		return {
			'proj_notices': ModelManager.objectsToDict(projs, type="notices")
		}

	# 发布通知
	@classmethod
	def addNotice(cls,user: User, pid, title, content):

		# 验证身份
		cls.Common.ensureProjectManager(user.id, pid)

		proj = cls.Common.getProject(id=pid)
		proj.addNotice(title, content)

	# 删除通知（可以删除多个）
	@classmethod
	def deleteNotices(cls,user: User, pid, nids):

		# 验证身份
		cls.Common.ensureProjectManager(user.id, pid)

		# 验证通知ID
		for nid in nids:
			cls.Common.ensureNoticeExist(project_id=pid, id=nid)

		proj = cls.Common.getProject(id=pid)
		proj.deleteNotices(nids)

	# 阅读通知（标记为已读）
	@classmethod
	def readNotices(cls,user: User, rids):

		for rid in rids:
			rec = cls.Common.getNoticeReceive(user.id, rid)
			rec.read()

	# 校验输入参数格式
	class Check:

		# 校验项目名格式
		@classmethod
		def ensureNameFormat(cls, val: str):
			if not val:
				raise ErrorException(ErrorType.InvalidProjName)
			if len(val) > Project.NAME_LEN:
				raise ErrorException(ErrorType.InvalidProjName)

		# 校验项目类型格式
		@classmethod
		def ensureTypeFormat(cls, val: int):
			ViewManager.ensureEnumData(
				val, ProjectType, ErrorType.InvalidProjTypeId)

		# 校验项目描述格式
		@classmethod
		def ensureDescFormat(cls, val: str):
			if len(val) > Project.DESC_LEN:
				raise ErrorException(ErrorType.InvalidProjDesc)

	# 共享函数
	class Common:

		# 获取参与关系
		@classmethod
		def getParticipation(cls, uid, pid, return_type='object') -> Participation:
			return ViewManager.getObject(Participation, ErrorType.DoNotParticipated,
										 return_type=return_type, user_id=uid, project_id=pid)

		# 获取项目
		@classmethod
		def getProject(cls, return_type='object', **args) -> Project:
			return ViewManager.getObject(Project, ErrorType.ProjectNotExist,
										 return_type=return_type, **args)
		# 获取用户参加的项目集
		@classmethod
		def getProjects(cls, user, return_type='object'):
			return ModelManager.getObjectRelatedForAll(
				user.participation_set, 'project')

		# 获取项目
		@classmethod
		def getRole(cls, rid, return_type='object') -> Role:
			return ViewManager.getObject(Role, ErrorType.RoleNotExist,
										 return_type=return_type, id=rid)

		# 获取通知
		@classmethod
		def getNotice(cls, return_type='object', **args) -> Notice:
			return ViewManager.getObject(Notice, ErrorType.NoticeNotExist,
										 return_type=return_type, **args)

		# 获取通知接收
		@classmethod
		def getNoticeReceive(cls, nid, uid, return_type='object') -> NoticeReceive:
			return ViewManager.getObject(NoticeReceive, ErrorType.ReceiveNotExist,
										 notice_id=nid, user_id=uid,
										 return_type=return_type)

		# 确保项目存在
		@classmethod
		def ensureProjectExist(cls, **args):
			return ViewManager.ensureObjectExist(
				Project, ErrorType.ProjectNotExist, **args)

		# 确保项目存在
		@classmethod
		def ensureRoleExist(cls, rid):
			return ViewManager.ensureObjectExist(
				Role, ErrorType.RoleNotExist, id=rid)

		# 确保用户是项目的项目经理
		@classmethod
		def ensureProjectManager(cls, uid, pid):
			part = cls.getParticipation(uid, pid)
			part_roles = part.participationrole_set.all()
			ViewManager.ensureObjectExist(
				ParticipationRole, ErrorType.NotAProjManager,
				part_roles, role_id=Role.ProjectManagerId)

		# 确保项目参与关系存在
		@classmethod
		def ensureParticipationExist(cls, uid, pid):
			return ViewManager.ensureObjectExist(
				Participation, ErrorType.DoNotParticipated,
				user_id=uid, project_id=pid)

		# 确保项目参与关系不存在
		@classmethod
		def ensureParticipationNotExist(cls, uid, pid):
			return ViewManager.ensureObjectNotExist(
				Participation, ErrorType.HaveParticipated,
				user_id=uid, project_id=pid)

		# 确保通知存在
		@classmethod
		def ensureNoticeExist(cls, **args):
			return ViewManager.ensureObjectExist(
				Notice, ErrorType.NoticeNotExist, **args)

		# 获取或创建一个通知接收数据
		@classmethod
		def createOrGetNoticeReceive(cls, nid, uid):

			notice = cls.getNotice(id=nid)
			receive = notice.noticereceive_set.filter(user_id=uid)

			if receive.exists(): return receive.first()
			receive = NoticeReceive()
			receive.notice = notice
			receive.user_id = uid
			receive.save()

			return receive

from enum import Enum


class ErrorType(Enum):

	# Common
	Success				= 0  # 成功，无错误
	InvalidRequest		= 1  # 非法的请求方法
	ParameterError		= 2  # 参数错误
	InvalidRoute		= 3  # 非法路由
	InvalidEmit			= 4  # 非法返回
	PermissionDenied	= 5  # 无权操作

	AttrNotExist		= 6  # 属性不存在

	# UserModule Common
	InvalidInfo			= 100  # 非法的信息填写
	InvalidCode			= 101  # 验证码错误
	EmailSendError		= 102  # 邮件发送错误

	# AuthManager
	InvalidToken		= 110  # 无效的令牌

	# Register
	UsernameExist		= 120  # 用户名已存在
	InvalidUsername		= 121  # 非法的用户名
	InvalidPassword		= 122  # 非法的密码
	PhoneExist			= 123  # 电话号码已存在
	InvalidPhone		= 124  # 非法的电话号码
	EmailExist			= 125  # 邮箱地址已存在
	InvalidEmail		= 126  # 非法的邮箱地址

	# Login
	UsernameNotExist	= 130  # 用户不存在
	IncorrectPassword	= 131  # 密码错误
	IncorrectLogin		= 132  # 用户不存在或密码错误
	PhoneNotExist		= 133  # 号码不存在
	EmailNotExist		= 134  # 邮箱不存在
	UserAbnormal		= 135  # 用户状态异常
	UserFrozen			= 136  # 用户被冻结

	# Forget
	IncorrectEmail		= 140  # 邮箱错误
	IncorrectPhone		= 141  # 号码错误

	# User
	InvalidName			= 150  # 非法的名称格式
	InvalidGender		= 151  # 非法的性别
	InvalidBirth		= 152  # 非法的出生日期
	InvalidCity			= 153  # 非法的居住地格式
	InvalidEduId		= 154  # 非法的学历
	InvalidDuty			= 155  # 非法的职位格式
	InvalidConnact		= 156  # 非法的联系方式格式
	InvalidDesc			= 157  # 非法的个人描述格式
	InvalidAvatar		= 158  # 非法的头像格式或大小

	# Friend
	NotAFriend			= 160  # 对方不是好友
	AlreadyAFriend		= 161  # 你们已经是好友

	# Project Info
	InvalidProjName		= 200  # 非法的名称格式
	InvalidProjTypeId	= 201  # 非法的项目类型
	InvalidProjDesc		= 202  # 非法的项目描述格式

	# Project
	ProjectNotExist		= 210  # 项目不存在
	RoleNotExist		= 211  # 角色不存在
	DoNotParticipated	= 212  # 用户没有参加此项目
	HaveParticipated	= 213  # 已经参加了此项目

	NotAProjManager		= 213  # 不是项目经理

	# Notice
	NoticeNotExist 		= 220  # 通知不存在
	ReceiveNotExist 	= 221  # 未接收到此通知

	# Task
	TaskNotExist		= 300  # 任务不存在
	TaskTakeNotExist 	= 301  # 任务分配不存在
	ProgressReqNotExist = 302  # 进度请求不存在

	# Task Info
	InvalidTaskName		= 310  # 非法的名称格式
	InvalidTaskDesc		= 311  # 非法的任务描述格式
	InvalidTaskDuration	= 312  # 非法的工期设定
	InvalidTaskEndDate	= 313  # 非法的结束日期
	InvalidTaskStatusId	= 314  # 非法的任务状态
	InvalidTaskProgress	= 315  # 非法的任务进度

	# Task Schedule
	LoopPrevTask		= 320  # 循环的任务依赖

	# TaskProgress
	UnresultProgressReq	= 330  # 该任务已经有一个未审阅的进度请求

class ErrorException(Exception):

	error_dict = {

		# Common
		ErrorType.Success:			"",
		ErrorType.InvalidRequest:	"非法的请求方法！",
		ErrorType.ParameterError:	"参数错误！",
		ErrorType.InvalidRoute:		"非法路由！",
		ErrorType.InvalidEmit:		"非法返回！",

		ErrorType.PermissionDenied:	"无权操作！",

		ErrorType.AttrNotExist:		"属性不存在！",

		# UserModule Common
		ErrorType.InvalidInfo:		"非法的信息填写！",
		ErrorType.InvalidCode:		"验证码过时或输入错误！",
		ErrorType.EmailSendError:	"邮件发送错误！",

		# AuthManager
		ErrorType.InvalidToken:		"登陆超时或尚未登录！",

		# Register
		ErrorType.UsernameExist:	"用户名已存在！",
		ErrorType.InvalidUsername:	"非法的用户名！",
		ErrorType.InvalidPassword:	"非法的密码！",
		ErrorType.PhoneExist:		"电话号码已存在！",
		ErrorType.InvalidPhone:		"非法的电话号码！",
		ErrorType.EmailExist:		"邮箱地址已存在！",
		ErrorType.InvalidEmail:		"非法的邮箱地址！",

		# Login
		ErrorType.UsernameNotExist:	"用户不存在！",
		ErrorType.IncorrectPassword:"密码错误！",
		ErrorType.IncorrectLogin:	"用户不存在或密码错误！",
		ErrorType.PhoneNotExist:	"号码不存在！",
		ErrorType.EmailNotExist:	"邮箱不存在！",
		ErrorType.UserAbnormal:		"用户状态异常！",
		ErrorType.UserFrozen:		"该用户被冻结，请联系客服！",
		
		# Forget
		ErrorType.IncorrectEmail:	"邮箱错误！",
		ErrorType.IncorrectPhone:	"号码错误！",

		# User
		ErrorType.InvalidName: 		"非法的名称格式！",
		ErrorType.InvalidGender: 	"非法的性别！",
		ErrorType.InvalidBirth: 	"非法的出生日期！",
		ErrorType.InvalidCity: 		"非法的居住地格式！",
		ErrorType.InvalidEduId: 	"非法的学历！",
		ErrorType.InvalidDuty: 		"非法的职位格式！",
		ErrorType.InvalidConnact: 	"非法的联系方式格式！",
		ErrorType.InvalidDesc: 		"非法的个人描述格式！",
		ErrorType.InvalidAvatar: 	"非法的头像格式或大小！",

		# Friend
		ErrorType.NotAFriend: 		"你与对方不是好友关系！",
		ErrorType.AlreadyAFriend: 	"你们已经是好友关系！",

		# Project Info
		ErrorType.InvalidProjName: 		"非法的名称格式！",
		ErrorType.InvalidProjTypeId: 	"非法的项目类型！",
		ErrorType.InvalidProjDesc:	 	"非法的项目描述格式！",

		# Project
		ErrorType.ProjectNotExist: 		"项目不存在！",
		ErrorType.RoleNotExist:			"角色不存在！",
		ErrorType.DoNotParticipated: 	"你没有参加此项目或项目不存在！",
		ErrorType.HaveParticipated: 	"该用户已经参加了此项目！",

		ErrorType.NotAProjManager:		"你不是项目经理，无权操作！",

		# Notice
		ErrorType.NoticeNotExist:		"通知不存在！",
		ErrorType.ReceiveNotExist:		"未接收到此通知！",

		# Task
		ErrorType.TaskNotExist:			"任务不存在！",
		ErrorType.TaskTakeNotExist:		"任务分配不存在！",
		ErrorType.ProgressReqNotExist:	"进度请求不存在！",

		# Task Schedule
		ErrorType.LoopPrevTask:			"循环的任务依赖！",

		# Task Info
		ErrorType.InvalidTaskName: 		"非法的名称格式！",
		ErrorType.InvalidTaskDesc:	 	"非法的任务描述格式！",
		ErrorType.InvalidTaskDuration: 	"非法的工期设定！",
		ErrorType.InvalidTaskEndDate: 	"非法的结束日期！",
		ErrorType.InvalidTaskStatusId: 	"非法的任务状态！",
		ErrorType.InvalidTaskProgress: 	"非法的任务进度！",

		ErrorType.UnresultProgressReq:	"该任务已经有一个未审阅的进度请求！",
	}

	def __init__(self, error_type: ErrorType):
		self.error_type = error_type
		self.msg = ErrorException.error_dict[error_type]

	def __str__(self):
		return self.msg

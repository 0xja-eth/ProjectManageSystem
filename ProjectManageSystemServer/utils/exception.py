from enum import Enum

class ErrorType(Enum):

	# Common
	Success				= 0  # 成功，无错误
	InvalidRequest		= 1  # 非法的请求方法
	ParameterError		= 2  # 参数错误
	InvalidRoute		= 3  # 非法路由
	InvalidEmit			= 4  # 非法返回
	PermissionDenied	= 5  # 无权操作

	# UserModule Common
	InvalidInfo			= 100 # 非法的信息填写
	InvalidCode			= 101 # 验证码错误
	EmailSendError		= 102 # 邮件发送错误

	# AuthManager
	InvalidToken		= 110 # 无效的令牌

	# Register
	UsernameExist		= 120 # 用户名已存在
	InvalidUsername		= 121 # 非法的用户名
	InvalidPassword		= 122 # 非法的密码
	PhoneExist			= 123 # 电话号码已存在
	InvalidPhone		= 124 # 非法的电话号码
	EmailExist			= 125 # 邮箱地址已存在
	InvalidEmail		= 126 # 非法的邮箱地址

	# Login
	UsernameNotExist	= 130 # 用户不存在
	IncorrectPassword	= 131 # 密码错误
	IncorrectLogin		= 132 # 用户不存在或密码错误
	PhoneNotExist		= 133 # 号码不存在
	EmailNotExist		= 134 # 邮箱不存在
	UserAbnormal		= 135 # 用户状态异常
	UserFrozen			= 136 # 用户被冻结

	# Forget
	IncorrectEmail		= 140 # 邮箱错误
	IncorrectPhone		= 141 # 号码错误

	# Friend
	NotAFriend			= 150 # 对方不是好友
	AlreadyAFriend		= 151 # 你们已经是好友

class ErrorException(Exception):

	error_dict = {

		# Common
		ErrorType.Success:			"",
		ErrorType.InvalidRequest:	"非法的请求方法！",
		ErrorType.ParameterError:	"参数错误！",
		ErrorType.InvalidRoute:		"非法路由！",
		ErrorType.InvalidEmit:		"非法返回！",
		ErrorType.PermissionDenied:	"无权操作！",

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

		# Friend
		ErrorType.NotAFriend: 		"你与对方不是好友关系！",
		ErrorType.AlreadyAFriend: 	"你们已经是好友关系！",

	}

	def __init__(self, error_type: ErrorType):
		self.error_type = error_type
		self.msg = ErrorException.error_dict[error_type]

	def __str__(self):
		return self.msg
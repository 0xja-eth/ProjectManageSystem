from django.conf import settings
from utils.exception import ErrorException, ErrorType
from utils.view_manager import ViewManager
from .models import *
import datetime, random, re, hashlib, smtplib

# =======================
# 登陆状态数据类
# =======================
class Authorization:

    AUTH_SECOND = 30*60 # 登陆状态有效时间（秒）
    TOKEN_LENGTH = 24 # token 位数

    def __init__(self, user: User):
        self.user = user
        self.token = ''
        self.out_time = datetime.datetime.now()

        self.refresh()

    # 刷新 Auth
    def refresh(self):
        self.token = self._generateToken()

        # token 过期时间
        now = datetime.datetime.now()
        delta = datetime.timedelta(0, self.AUTH_SECOND)
        self.out_time = now+delta

    # 生成一个 token
    def _generateToken(self):
        return ''

    def convertToDict(self):
        return {
            'uid': self.user.id,
            'token': self.token,
            'out_time': self.out_time
        }

# =======================
# 登陆状态管理类，管理授权数据
# =======================
class AuthorizationManager:

    authorizations = {}

    # 生成一个 Authorization 并存入 authorizations 中
    @classmethod
    def generateAuth(cls, user: User):
        auth = cls.getAuth(user) or Authorization(user)
        cls.authorizations[user] = auth
        return auth

    # 寻找指定的 Authorization
    @classmethod
    def getAuth(cls, user: User):
        if user in cls.authorizations:
            return cls.authorizations[user]
        return None

    # 删除指定的 Authorization
    @classmethod
    def deleteAuth(cls, user: User):
        if user in cls.authorizations:
            cls.authorizations.pop(user)
        else:
            raise ErrorException(ErrorType.InvalidUser)

    # 获取 user
    # TODO(吴宁): 先根据 token 获取 auth，
    # TODO(吴宁): 若 auth 存在且未过期，返回其 user
    # TODO(吴宁): 否则，抛出异常：ErrorType.InvalidToken
    @classmethod
    def getUser(cls, token):
        for user in cls.authorizations:
            if cls.authorizations[user].token==token:
                if datetime.datetime.now() > token.out_time:
                    raise ErrorException(ErrorType.InvalidToken)
                return user


    # 扫描 Auth，如果过期就删去
    @classmethod
    def scanAuths(cls):
        for user in cls.authorizations:
            if datetime.datetime.now() > cls.authorizations[user].token.out_time:
                cls.deleteAuth(user)

# =======================
# 验证码数据类
# =======================
class CodeDatum:

    CODE_LENGTH = 6 # 验证码位数
    CODE_SECOND = 60 # 验证码有效时间（秒）

    def __init__(self, un, email, type):
        self.un = un
        self.email = email
        self.type = type
        self.code = self.generateCode()

        # token 过期时间
        now = datetime.datetime.now()
        delta = datetime.timedelta(0, self.CODE_SECOND)
        self.out_time = now+delta

    # 生成一个 code（100000~999999）
    def generateCode(self):
        max_ = pow(10, self.CODE_LENGTH)
        return str(random.randint(max_ / 10, max_ - 1))

# =======================
# 验证码管理类，管理验证码数据，处理验证码发送
# =======================
class CodeManager:

    code_data = {}

    # 生成一个 CodeDatum 并存入 code_data 中
    @classmethod
    def generateCode(cls, un, email, type):
        code = cls.getCode(un, email, type) or CodeDatum(un, email, type)
        cls.code_data[cls.getKey(un, email, type)] = code

        return code.code

    # 获取键名
    @classmethod
    def getKey(cls, un, email, type):
        return '%s,%s,%s' % (un, email, type)

    # 寻找指定的 CodeDatum
    @classmethod
    def getCode(cls, un, email, type):
        if cls.getKey(un, email, type) in cls.code_data:
            return cls.code_data[cls.getKey(un, email, type)]
        return None

    # 删除指定的 CodeDatum
    @classmethod
    def deleteCode(cls, un, email,type):
        if (un, email) in cls.code_data:
             cls.code_data.pop(cls.getKey(un, email, type))
        else:
            raise ErrorException(ErrorType.InvalidCode)

    # 确保验证码正确，否则抛出异常：ErrorType.InvalidCode
    @classmethod
    def ensureCode(cls, un, email, code, type):
        if (un, email) in cls.code_data:
            return cls.code_data[cls.getKey(un, email, type)]==code
        else:
            raise ErrorException(ErrorType.InvalidCode)

    # 扫描 Code，如果过期就删去
    @classmethod
    def scanCodes(cls):
        for code in cls.code_data:
            if datetime.datetime.now() > cls.code_data[code].token.out_time:
                cls.code_data.pop(code)

# =======================
# 用户管理类，管理用户模块的视图函数
# =======================
class UserManager:

    # 业务逻辑
    # 注册（无返回值）
    @classmethod
    def register(cls, un, pw, email, code):
#
# <<<<<<< HEAD
# 		user = User()
# 		user.username = un
# 		user.password = pw
# 		user.email = email
# 		user.save()
#
# 	# 登陆（返回目标 user 的数据和 auth）
# 	@classmethod
# 	def login(cls, un, pw):
#
# 		cls.Check.ensureUsernameFormat(un)
# 		cls.Check.ensurePasswordFormat(pw)
#
# 		pw = cls.cryptoPassword(pw)
# 		# 获取对应的 User（程序会自动校验并报错）
# 		user = cls.Common.getUser(username=un, password=pw)
#
# 		return cls._doLogin(user)
#
# 	@classmethod
# 	def _doLogin(cls, user: User):
#
# 		user.login()
# 		auth = AuthorizationManager.generateAuth(user)
#
# 		return {
# 			'user': user.convertToDict(),
# 			'auth': auth.convertToDict()
# 		}
#
# 	# 找回密码（无返回值）
# 	# TODO(吴宁): 仿照上面的函数完成此函数（实际上和 register 差不多）
# 	@classmethod
# 	def forget(cls, un, pw, email, code):
# 		pass
#
# 	# 发送验证码（无返回值）
# 	@classmethod
# 	def sendCode(cls, un, email, type):
#
# 		conf = settings.CODE_TEXT[type]
# 		code = CodeManager.generateCode(un, email, type)
#
# 		if not (type == 'register' or type == 'forget'):
# 			raise ErrorException(ErrorType.ParameterError)
#
# 		print("sendCode to %s [%s]: %s" % (email, type, code))
# 		cls._doSendCode(un, email, code, conf)
#
# 	@classmethod
# 	def _doSendCode(cls, un, email, code, conf):
# 		try:
# 			from django.core.mail import send_mail
#
# 			send_mail(conf[0], conf[1] % (
# 					un, code, CodeDatum.CODE_SECOND
# 				), conf[2], [email])
#
# 		except smtplib.SMTPException as exception:
# 			print("ERROR in sendEmailCode: " + str(exception))
# 			raise ErrorException(ErrorType.EmailSendError)
#
# 	# 登出（无返回值）
# 	@classmethod
# 	def logout(cls, user: User):
# 		AuthorizationManager.deleteAuth(user)
# 		user.logout()
#
# 	# 获取用户详细数据（返回 user 详细数据）
# 	@classmethod
# 	def getDetail(cls, user: User):
# 		return user.convertToDict()
#
# 	# 修改用户信息（无返回值）
# 	# TODO(吴宁): 仿照上面的函数完成此函数，需要先 ensure 后再进行实际的操作
# 	@classmethod
# 	def editInfo(cls, user: User, name, gender, birth, city,
# 				 edu_id, duty, contact, desc):
# 		pass
#
# 	# 上传头像（无返回值）
# 	# TODO(吴宁): avatar 是一个从 FILES 取出的值，需要检查其大小、格式等属性并存入 user 对象
# 	@classmethod
# 	def uploadAvatar(cls, user: User, avatar):
# 		pass
#
# 	# 修改密码（无返回值）
# 	# TODO(吴宁): 校验 old 密码是否正确，正确则重置为 new 密码，注意密码加密
# 	@classmethod
# 	def resetPwd(cls, user: User, old, new):
# 		pass
#
# 	# 获取好友列表
# 	@classmethod
# 	def getFriends(cls, user: User):
# 		return user.convertToDict('friends')
#
# 	# 获取好友列表
# 	@classmethod
# 	def getFriendReqs(cls, user: User, type):
# 		# 限制 type 取值
# 		if type != 'send' and type != 'received':
# 			raise ErrorException(ErrorType.ParameterError)
# 		return user.convertToDict(type+'_reqs')
#
# 	# 搜索用户信息（un 为关键字，必须精确匹配 username 才能搜索出来）
# 	# TODO(吴宁): 搜索，注意要过滤掉已添加的好友
# 	@classmethod
# 	def searchUser(cls, user: User, un):
# 		pass
#
# 	# 发起好友请求（fuid 为添加目标的 uid）
# 	# TODO(吴宁): 检查是否重复添加，完善 User.addFriend 函数
# 	@classmethod
# 	def addFriend(cls, user: User, fuid):
# 		pass
#
# 	# 删除好友（fid 为好友关系的 id，即 Friend 表的 id，而不是 uid）
# 	# TODO(吴宁): 老规矩，先检查
# 	@classmethod
# 	def deleteFriend(cls, user: User, fid):
# 		pass
#
# 	# 操作好友请求（fid 为好友关系的 id，即 Friend 表的 id，而不是 uid，accept 为是否接受）
# 	# TODO(吴宁): 检查后更新属性即可
# 	@classmethod
# 	def operFriendReq(cls, user: User, fid, accept):
# 		pass
#
# 	# 刷新 token
# 	@classmethod
# 	def refreshToken(cls, user: User):
# 		auth = AuthorizationManager.getAuth(user)
# 		if auth is None:
# 			raise ErrorException(ErrorType.InvalidToken)
#
# 		auth.refresh()
#
# 		return {'auth': auth.convertToDict()}
#
# 	# 密码加密
# 	@classmethod
# 	def cryptoPassword(cls, value):
# 		value = User.PASSWORD_SALT + value + User.PASSWORD_SALT
# 		value = hashlib.sha1(value.encode()).hexdigest()
# 		return value
#
# 	# 校验输入参数格式
# 	class Check:
#
# 		# 校验用户名格式
# 		@classmethod
# 		def ensureUsernameFormat(cls, val: str):
# 			if not val:
# 				raise ErrorException(ErrorType.InvalidUsername)
# 			if len(val) > User.UN_LEN:
# 				raise ErrorException(ErrorType.InvalidUsername)
#
# 		# 校验密码格式
# 		@classmethod
# 		def ensurePasswordFormat(cls, val: str):
# 			if not val:
# 				raise ErrorException(ErrorType.IncorrectPassword)
# 			if not (User.PWD_LEN[0] <= len(val) <= User.PWD_LEN[1]):
# 				raise ErrorException(ErrorType.IncorrectPassword)
#
# 		# 校验邮箱格式
# 		@classmethod
# 		def ensureEmailFormat(cls, val: str):
# 			if not val:
# 				raise ErrorException(ErrorType.IncorrectEmail)
# 			if not re.compile(User.EMAIL_REG).search(val):
# 				raise ErrorException(ErrorType.IncorrectEmail)
#
# 		# TODO(吴宁): 仿照上面 ensure 函数的格式填写下面的函数内容
# 		# TODO(吴宁): 按照 需求设计文档 2.5 和 系统数据模型 1.2 完成以下校验函数
# 		# TODO(吴宁): 注意：每一个常量（比如限制的长度/正则表达式等）都需要在 User 里定义
# 		# TODO(吴宁): 这样就能减少修改带来的不便，虽然几乎不会去修改，但是这是一个好习惯
# 		# 校验名字格式
# 		@classmethod
# 		def ensureNameFormat(cls, val: str):
# 			pass
#
# 		# 校验性别格式
# 		@classmethod
# 		def ensureGenderFormat(cls, val: int):
# 			pass
#
# 		# 校验生日格式
# 		@classmethod
# 		def ensureBirthFormat(cls, val: str):
# 			pass
#
# 		# 校验城市格式
# 		@classmethod
# 		def ensureCityFormat(cls, val: str):
# 			pass
#
# 		# 校验学历ID格式
# 		@classmethod
# 		def ensureEduIdFormat(cls, val: int):
# 			pass
#
# 		# 校验职位格式
# 		@classmethod
# 		def ensureDutyFormat(cls, val: str):
# 			pass
#
# 		# 校验联系方式格式
# 		@classmethod
# 		def ensureContactFormat(cls, val: str):
# 			pass
#
# 		# 校验个人描述格式
# 		@classmethod
# 		def ensureDescFormat(cls, val: str):
# 			pass
#
# 		# 校验头像
# 		@classmethod
# 		def ensureAvatar(cls, avatar):
# 			pass
#
# 	# 共享函数
# 	# TODO(吴宁): 实现上面函数时，利用好这里的函数，不要写重复逻辑的函数了
# 	# TODO(吴宁): 如果函数不够用，可以自行添加，ErrorType 也可以自行增加
# 	class Common:
#
# 		# 获取用户
# 		@classmethod
# 		def getUser(cls, return_type='object', **args) -> User:
# 			return ViewManager.getObject(User, ErrorType.UsernameNotExist,
# 										 return_type=return_type, **args)
#
# 		# 获取好友关系
# 		@classmethod
# 		def getFriend(cls, uid, fuid, accepted=True, return_type='object') -> User:
# 			return ViewManager.getObject(Friend, ErrorType.NotAFriend, return_type=return_type,
# 										 subject=uid, object=fuid, accepted=accepted)
#
# 		# 确保密码正确
# 		@classmethod
# 		def ensurePasswordCorrect(cls, user, pw):
# 			pw = UserManager.cryptoPassword(pw)
# 			if user.password != pw:
# 				raise ErrorException(ErrorType.IncorrectPassword)
#
# 		# 确保用户存在
# 		@classmethod
# 		def ensureUserExist(cls, **args):
# 			return ViewManager.ensureObjectExist(
# 				User, ErrorType.UsernameNotExist, **args)
#
# 		# 确保用户不存在
# 		@classmethod
# 		def ensureUserNotExist(cls, **args):
# 			return ViewManager.ensureObjectNotExist(
# 				User, ErrorType.UsernameExist, **args)
#
# 		# 确保好友关系存在
# 		@classmethod
# 		def ensureFriendExist(cls, **args):
# 			return ViewManager.ensureObjectExist(
# 				Friend, ErrorType.NotAFriend, **args)
#
# 		# 确保好友关系不存在
# 		@classmethod
# 		def ensureFriendNotExist(cls, **args):
# 			return ViewManager.ensureObjectNotExist(
# 				Friend, ErrorType.AlreadyAFriend, **args)
# =======
        cls.Check.ensureUsernameFormat(un)
        cls.Check.ensurePasswordFormat(pw)
        cls.Check.ensureEmailFormat(email)

        CodeManager.ensureCode(un, code, email, 'register')

        cls._doRegister(un, pw, email)

    @classmethod
    def _doRegister(cls, un, pw, email):

        pw = cls.cryptoPassword(pw)

        user = User()
        user.username = un
        user.password = pw
        user.email = email
        user.save()

    # 登陆（返回目标 user 的数据和 auth）
    @classmethod
    def login(cls, un, pw):

        cls.Check.ensureUsernameFormat(un)
        cls.Check.ensurePasswordFormat(pw)

        pw = cls.cryptoPassword(pw)
        # 获取对应的 User（程序会自动校验并报错）
        user = cls.Common.getUser(username=un, password=pw)

        return cls._doLogin(user)

    @classmethod
    def _doLogin(cls, user: User):

        user.login()
        auth = AuthorizationManager.generateAuth(user)

        return {
            'user': user.convertToDict(),
            'auth': auth.convertToDict()
        }

    # 找回密码（无返回值）
    # TODO(吴宁): 仿照上面的函数完成此函数（实际上和 register 差不多）
    @classmethod
    def forget(cls, un, pw, email, code):
        cls.Check.ensureUsernameFormat(un)
        cls.Check.ensurePasswordFormat(pw)
        cls.Check.ensureEmailFormat(email)
        CodeManager.ensureCode(un, code, email, 'forget')
        cls._doRegister(un, pw, email)


    # 发送验证码（无返回值）
    @classmethod
    def sendCode(cls, un, email, type):

        conf = settings.CODE_TEXT[type]
        code = CodeManager.generateCode(un, email, type)

        if not (type == 'register' or type == 'forget'):
            raise ErrorException(ErrorType.ParameterError)

        print("sendCode to %s [%s]: %s" % (email, type, code))
        cls._doSendCode(un, email, code, conf)

    @classmethod
    def _doSendCode(cls, un, email, code, conf):
        try:
            from django.core.mail import send_mail

            send_mail(conf[0], conf[1] % (
                    un, code, CodeDatum.CODE_SECOND
                ), conf[2], [email])

        except smtplib.SMTPException as exception:
            print("ERROR in sendEmailCode: " + str(exception))
            raise ErrorException(ErrorType.EmailSendError)

    # 登出（无返回值）
    @classmethod
    def logout(cls, user: User):
        AuthorizationManager.deleteAuth(user)
        user.logout()

    # 获取用户详细数据（返回 user 详细数据）
    @classmethod
    def getDetail(cls, user: User):
        return user.convertToDict()

    # 修改用户信息（无返回值）
    # TODO(吴宁): 仿照上面的函数完成此函数，需要先 ensure 后再进行实际的操作
    @classmethod
    def editInfo(cls, user: User, name, gender, birth, city,
                 edu_id, duty, contact, desc):

        cls.Check.ensureUsernameFormat(name)
        cls.Check.ensureGenderFormat(gender)
        cls.Check.ensureBirthFormat(birth)
        cls.Check.ensureCityFormat(city)
        cls.Check.ensureEduIdFormat(edu_id)
        cls.Check.ensureDutyFormat(duty)
        cls.Check.ensureContactFormat(contact)
        cls.Check.ensureDescFormat(desc)

        user.name = name
        user.gender = gender
        user.birth = birth
        user.city = city
        user.education = edu_id
        user.duty = duty
        user.contact = contact
        user.description = desc
        user.save()

    # 上传头像（无返回值）
    # TODO(吴宁): avatar 是一个从 FILES 取出的值，需要检查其大小、格式等属性并存入 user 对象
    @classmethod
    def uploadAvatar(cls, user: User, avatar):
        pass

    # 修改密码（无返回值）
    # TODO(吴宁): 校验 old 密码是否正确，正确则重置为 new 密码，注意密码加密
    @classmethod
    def resetPwd(cls, user: User, old, new):

        cls.Check.ensurePasswordFormat(old)
        cls.Check.ensurePasswordFormat(new)

        if not user.password == old:
            raise ErrorException(ErrorType.InvalidPassword)

        user.password = new
        user.save()

    # 获取好友列表
    @classmethod
    def getFriends(cls, user: User):
        return user.convertToDict('friends')

    # 获取好友列表
    @classmethod
    def getFriendReqs(cls, user: User, type):
        # 限制 type 取值
        if type != 'send' and type != 'received':
            raise ErrorException(ErrorType.ParameterError)
        return user.convertToDict(type+'_reqs')

    # 搜索用户信息（un 为关键字，必须精确匹配 username 才能搜索出来）
    # TODO(吴宁): 搜索，注意要过滤掉已添加的好友
    @classmethod
    def searchUser(cls, user: User, un):
        userfind=User.objects.filter(username=un)
        if not userfind:
            raise ErrorException(ErrorType.UsernameNotExist)
        else:
            return userfind

    # 发起好友请求（fuid 为添加目标的 uid）
    # TODO(吴宁): 检查是否重复添加，完善 User.addFriend 函数
    @classmethod
    def addFriend(cls, user: User, fuid):
        friend = user.getFriends()
        for i in friend:
            if i.id==fuid:
                raise ErrorException(ErrorType.AlreadyAFriend)
        user.addFriend(fuid)
        user.save()


    # 删除好友（fid 为好友关系的 id，即 Friend 表的 id，而不是 uid）
    # TODO(吴宁): 老规矩，先检查
    @classmethod
    def deleteFriend(cls, user: User, fid):
        friends = user.getFriends()
        for friend in friends:
            if friend.id == fid:
               friend.delete()
            else:
                raise ErrorException(ErrorType.NotAFriend)

    # 操作好友请求（fid 为好友关系的 id，即 Friend 表的 id，而不是 uid，accept 为是否接受）
    # TODO(吴宁): 检查后更新属性即可
    @classmethod
    def operFriendReq(cls, user: User, fuid, accept):
        friends = user.getFriends()
        for friend in friends:
            if friend.id == fuid:
                friend.oper(accept)
            else:
                raise ErrorException(ErrorType.NotAFriend)


    # 刷新 token
    @classmethod
    def refreshToken(cls, user: User):
        auth = AuthorizationManager.getAuth(user)
        if auth is None:
            raise ErrorException(ErrorType.InvalidToken)

        auth.refresh()

        return {'auth': auth.convertToDict()}

    # 密码加密
    @classmethod
    def cryptoPassword(cls, value):
        value = User.PASSWORD_SALT + value + User.PASSWORD_SALT
        value = hashlib.sha1(value.encode()).hexdigest()
        return value

    # 校验输入参数格式
    class Check:

        # 校验用户名格式
        @classmethod
        def ensureUsernameFormat(cls, val: str):
            if not val:
                raise ErrorException(ErrorType.InvalidUsername)
            if len(val) > User.UN_LEN:
                raise ErrorException(ErrorType.InvalidUsername)

        # 校验密码格式
        @classmethod
        def ensurePasswordFormat(cls, val: str):
            if not val:
                raise ErrorException(ErrorType.IncorrectPassword)
            if not (User.PWD_LEN[0] <= len(val) <= User.PWD_LEN[1]):
                raise ErrorException(ErrorType.IncorrectPassword)

        # 校验邮箱格式
        @classmethod
        def ensureEmailFormat(cls, val: str):
            if not val:
                raise ErrorException(ErrorType.IncorrectEmail)
            if not re.compile(User.EMAIL_REG).search(val):
                raise ErrorException(ErrorType.IncorrectEmail)

        # TODO(吴宁): 仿照上面 ensure 函数的格式填写下面的函数内容
        # TODO(吴宁): 按照 需求设计文档 2.5 和 系统数据模型 1.2 完成以下校验函数
        # TODO(吴宁): 注意：每一个常量（比如限制的长度/正则表达式等）都需要在 User 里定义
        # TODO(吴宁): 这样就能减少修改带来的不便，虽然几乎不会去修改，但是这是一个好习惯
        # 校验名字格式
        @classmethod
        def ensureNameFormat(cls, val: str):
            if not val:
                raise ErrorException(ErrorType.InvalidName)
            if not len(val)<64:
                raise ErrorException(ErrorType.InvalidName)

        # 校验性别格式
        @classmethod
        def ensureGenderFormat(cls, val: str):
            if not val:
                raise ErrorException(ErrorType.InvalidGender)
            if not type(val)==bool:
                raise ErrorException(ErrorType.InvalidGender)

        # 校验生日格式
        @classmethod
        def ensureBirthFormat(cls, val: str):
            if not val:
                raise ErrorException(ErrorType.InvalidBirth)
            if not type(val)==models.DateField:
                raise ErrorException(ErrorType.InvalidBirth)

        # 校验城市格式
        @classmethod
        def ensureCityFormat(cls, val: str):
            if not val:
                raise ErrorException(ErrorType.InvalidCity)
            if not len(val)<16:
                raise ErrorException(ErrorType.InvalidCity)

        # 校验学历ID格式
        @classmethod
        def ensureEduIdFormat(cls, val: str):
            if not val:
                raise ErrorException(ErrorType.InvalidEduId)
            if not type(val)== models.PositiveSmallIntegerField:
                raise ErrorException(ErrorType.InvalidEduId)

        # 校验职位格式
        @classmethod
        def ensureDutyFormat(cls, val: str):
            if not val:
                raise ErrorException(ErrorType.InvalidDuty)
            if not len(val)<16:
                raise ErrorException(ErrorType.InvalidDuty)

        # 校验联系方式格式
        @classmethod
        def ensureContactFormat(cls, val: str):
            if not val:
                raise ErrorException(ErrorType.InvalidConnact)
            if not len(val)<16:
                raise ErrorException(ErrorType.InvalidConnact)

        # 校验个人描述格式
        @classmethod
        def ensureDescFormat(cls, val: str):
            if not val:
                raise ErrorException(ErrorType.InvalidDesc)
            if not len(val) < 100:
                raise ErrorException(ErrorType.InvalidDesc)

        # 校验头像
        @classmethod
        def ensureAvatar(cls, avatar):
            if not avatar:
                raise ErrorException(ErrorType.InvalidAvatar)
            if not type(avatar)== models.ImageField:
                raise ErrorException(ErrorType.InvalidAvatar)

    # 共享函数
    # TODO(吴宁): 实现上面函数时，利用好这里的函数，不要写重复逻辑的函数了
    # TODO(吴宁): 如果函数不够用，可以自行添加，ErrorType 也可以自行增加
    class Common:

        # 获取用户
        @classmethod
        def getUser(cls, return_type='object', **args) -> User:
            return ViewManager.getObject(User, ErrorType.UsernameNotExist,
                                         return_type=return_type, **args)

        # 获取好友关系
        @classmethod
        def getFriend(cls, uid, fuid, accepted=True, return_type='object') -> User:
            return ViewManager.getObject(Friend, ErrorType.NotAFriend, return_type=return_type,
                                         subject=uid, object=fuid, accepted=accepted)

        # 确保用户存在
        @classmethod
        def ensureUserExist(cls, **args):
            return ViewManager.ensureObjectExist(
                User, ErrorType.UsernameExist, **args)

        # 确保用户不存在
        @classmethod
        def ensureUserNotExist(cls, **args):
            return ViewManager.ensureObjectNotExist(
                User, ErrorType.UsernameNotExist, **args)

        # 确保好友关系存在
        @classmethod
        def ensureFriendExist(cls, **args):
            return ViewManager.ensureObjectExist(
                Friend, ErrorType.NotAFriend, **args)

        # 确保好友关系不存在
        @classmethod
        def ensureFriendNotExist(cls, **args):
            return ViewManager.ensureObjectNotExist(
                Friend, ErrorType.AlreadyAFriend, **args)
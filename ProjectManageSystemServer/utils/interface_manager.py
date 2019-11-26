from django.conf import settings
from django.http import JsonResponse
from django.urls import path
from utils.exception import ErrorType, ErrorException
from user_module.views import AuthorizationManager
import json, datetime, traceback

# ===============================
# 接口管理器：处理接口的检查、调用
# ===============================
class InterfaceManager:

	@classmethod
	def generateUrlPatterns(cls, interfaces):
		urlpatterns = []

		for key in interfaces:
			urlpatterns.append(path(key, cls.recieveRequest, interfaces[key]))

		return urlpatterns

	# 接收请求
	@classmethod
	def recieveRequest(cls, request, func, method='POST', params=[], files=[]):
		try:
			# 获取数据
			dict = cls.getRequestDict(request, method=method, params=params, files=files)

			# 如果传输包含 auth 数据，获取其用户
			if 'auth' in dict:
				dict['user'] = AuthorizationManager.getUser(dict['auth'])
				del dict['auth']

			res = {'data': func(**dict)}

		except ErrorException as exception:
			return cls.getErrorResponse(exception)

		return cls.getSuccessResponse(res)

	# 获取请求参数字典
	@classmethod
	def getRequestDict(cls, request, method='POST', params=[], files=[]):

		data = dict()

		if method.upper() != request.META['REQUEST_METHOD']:
			raise ErrorException(ErrorType.InvalidRequest)

		body = request.body.decode()
		if body: raw = json.loads(body)
		else: raw = {}

		for item in params:
			if item[0] in raw:
				data[item[0]] = cls.convertDataType(raw[item[0]], item[1])
			elif item[1] != 'var': # 如果该参数是必选的
				raise ErrorException(ErrorType.ParameterError)

		for key in files:
			value = request.FILES.get(key)
			if value:
				data[key] = value
			else:
				raise ErrorException(ErrorType.ParameterError)

		print(data)

		return data

	# 处理WebSocket请求
	@classmethod
	def processWebsocketRequest(cls, request, key_data=[]):
		res_data = dict()

		for data in key_data:

			key = data[0]
			type = data[1]

			if key in request:
				res_data[key] = cls.convertDataType(request[key], type)
			else:
				raise ErrorException(ErrorType.ParameterError)

		print('processWebsocketRequest: ' + str(res_data))

		return res_data

	# 转换数据类型
	@classmethod
	def convertDataType(cls, value, type='str'):
		try:
			if type == 'int':
				value = int(value)

			elif type == 'int[]':

				if not isinstance(value, list):
					value = json.loads(value)

				for i in range(len(value)):
					value[i] = int(value[i])

			elif type == 'int[][]':

				if not isinstance(value, list):
					value = json.loads(value)

				for i in range(len(value)):
					for j in range(len(value[i])):
						value[i][j] = int(value[i][j])

			elif type == 'bool':
				value = bool(value)

			elif type == 'date':
				value = datetime.datetime.strptime(value, '%Y-%m-%d')

			elif type == 'datetime':
				value = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')

			# 其他类型判断
			return value

		except:
			raise ErrorException(ErrorType.ParameterError)

	"""
	# 转换多个数据类型
	@classmethod
	def convertMultDataType(cls, data, keys, type='str'):
		for key in keys:
			data[key] = cls.convertDataType(data[key], type)
	
	# 转换数据数组中全部数据类型
	@classmethod
	def convertAllDataType(cls, data, type='str'):
		cls.convertMultDataType(data, data, type)
	"""

	# 封装成功响应数据字典
	@classmethod
	def getSuccessResponseDict(cls, dict=None):

		if dict is None: dict = {}
		dict['status'] = ErrorType.Success.value

		return dict

	# 封装Emit数据字典
	@classmethod
	def getSuccessEmitDict(cls, type, dict=None):

		if dict is None: dict = {}
		dict['type'] = type
		dict['status'] = ErrorType.Success.value

		return dict

	# 封装错误响应数据字典
	@classmethod
	def getErrorResponseDict(cls, exception: ErrorException):
		return {
			'status': exception.error_type.value,
			'errmsg': str(exception)
		}

	# 封装错误Emit数据字典
	@classmethod
	def getErrorEmitDict(cls, type, exception: ErrorException):
		return {
			'type': type,
			'status': exception.error_type.value,
			'errmsg': str(exception)
		}

	# 获取成功响应对象
	@classmethod
	def getSuccessResponse(cls, dict=None):
		dict = cls.getSuccessResponseDict(dict)

		if settings.HTML_TEST:
			# 测试代码
			response = JsonResponse(dict)
			response["X-Frame-Options"] = ''

			return response
		else:
			return JsonResponse(dict)

	# 获取失败响应对象
	@classmethod
	def getErrorResponse(cls, exception: ErrorException):
		traceback.print_exc()

		dict = cls.getErrorResponseDict(exception)

		if settings.HTML_TEST:
			# 测试代码
			response = JsonResponse(dict)
			response["X-Frame-Options"] = ''

			return response
		else:
			return JsonResponse(dict)

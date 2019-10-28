
from django.conf import settings
from django.utils.deconstruct import deconstructible
from utils.exception import ErrorType, ErrorException
import os, time, random

# ===================================================
#  图片上传处理
# ===================================================
@deconstructible
class PictureUpload:

	def __init__(self, dir):
		self.dir = dir

	def __call__(self, instance, filename):
		# 根路径
		base = os.path.join(settings.BASE_DIR, settings.STATIC_BASE)

		# 文件拓展名
		ext = os.path.splitext(filename)[1]

		# 定义文件名,用户id_年月日时分秒_随机数
		currtime = time.strftime('%H%M%S')
		filename = "pic%d_%s_%04d" % (instance.id, currtime, random.randint(0, 9999))

		# 保存路径
		path = os.path.join(base, self.dir, filename + ext)

		return path

# ============================================
# 模型管理器：处理模型函数的共有业务逻辑
# ============================================
class ModelManager:

	@classmethod
	def timeToStr(cls, time, empty=''):
		if not time: return empty
		return time.strftime('%Y-%m-%d %H:%M:%S')

	@classmethod
	def objectToId(cls, object, empty=0):
		if not object: return empty
		return object.id

	# 获取一个QuerySet的相关属性集合
	# objects: QuerySet
	@classmethod
	def getObjectRelated(cls, objects, key, unique=False):
		result = []

		for obj in objects:
			try: result.append(getattr(obj, key))
			except: raise ErrorException(ErrorType.AttrNotExist)

		if unique: result = list(set(result))
		return result

	# 通过 all() 获取一个QuerySet的相关属性
	# objects: QuerySet
	@classmethod
	def getObjectRelatedForAll(cls, objects, key, unique=False):
		temp = objects.select_related(key).all()
		return cls.getObjectRelated(temp, key, unique)

	# 通过 filter() 获取一个QuerySet的相关属性
	# objects: QuerySet
	@classmethod
	def getObjectRelatedForFilter(cls, objects, key, unique=False, **args):
		temp = objects.select_related(key).filter(**args)
		return cls.getObjectRelated(temp, key, unique)

	# 物体集转化为字典
	@classmethod
	def objectsToDict(cls, objects, **args):
		result = []

		for obj in objects:
			result.append(obj.convertToDict(**args))

		return result


from django.conf import settings
from django.utils.deconstruct import deconstructible
from utils.exception import ErrorType, ErrorException
import os, time, random

# ============================================
# 模型管理器：处理模型函数的共有业务逻辑
# ============================================
class ModelManager:

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
			filename = "pic%d_%s_%04d" % (instance.id, currtime,
										  random.randint(0, 9999))

			# 保存路径
			path = os.path.join(base, self.dir, filename + ext)

			return path

	# 物体集转化为字典
	@classmethod
	def objectsToDict(cls, objects, **args):
		result = []

		for obj in objects:
			result.append(obj.convertToDict(**args))

		return result

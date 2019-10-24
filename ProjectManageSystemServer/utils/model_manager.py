
from utils.exception import ErrorType, ErrorException

# ===============================
# 模型管理器：处理模型函数的共有业务逻辑
# ===============================
class ModelManager:

	# 物体集转化为字典
	@classmethod
	def objectsToDict(cls, objects, **args):
		result = []

		for obj in objects:
			result.append(obj.convertToDict(**args))

		return result

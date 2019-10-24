
from utils.exception import ErrorType, ErrorException

# ===============================
# 视图管理器：处理视图函数中的共有业务逻辑
# ===============================
class ViewManager:

    # 确保某模型数据对象存在
    @classmethod
    def ensureObjectExist(cls, obj_type, error, objects=None,
                          include_deleted=False, **args):
        if not cls.hasObjects(obj_type, objects, include_deleted, **args):
            raise ErrorException(error)

    # 确保某模型数据对象不存在
    @classmethod
    def ensureObjectNotExist(cls, obj_type, error, objects=None,
                             include_deleted=False, **args):
        if cls.hasObjects(obj_type, objects, include_deleted, **args):
            raise ErrorException(error)

    # 是否存在某模型数据对象
    @classmethod
    def hasObjects(cls, obj_type, objects=None, include_deleted=False, **args):

        if objects is None: objects = obj_type.objects.all()

        # 实际上执行查询的部分：
        try:
            if not include_deleted and hasattr(obj_type, 'is_deleted'):
                return objects.filter(is_deleted=False, **args).exists()
            else:
                return objects.filter(**args).exists()

        except:
            raise ErrorException(ErrorType.ParameterError)

    # 获取模型数据对象
    @classmethod
    def getObject(cls, obj_type, error, objects=None,
                  return_type='QuerySet', include_deleted=False, **args):

        if objects is None: objects = obj_type.objects.all()

        # 如果是获取 object：
        if return_type == 'object':

            query_set = cls.getObject(obj_type, error, objects,
                                  'QuerySet', include_deleted, **args)

            if query_set.exists():
                return query_set[0]

            else:
                raise ErrorException(error)

        # 如果是获取 字典 数据（通过 converToDict）：
        if return_type == 'dict':
            object = cls.getObject(obj_type, error, objects,
                               'object', include_deleted, **args)

            return object.convertToDict()

        # 实际上执行查询的部分：
        try:
            if not include_deleted and hasattr(obj_type, 'is_deleted'):
                return objects.filter(is_deleted=False, **args)
            else:
                return objects.filter(**args)

        except:
            raise ErrorException(ErrorType.ParameterError)

    # 获取模型数据对象集
    @classmethod
    def getObjects(cls, obj_type, objects=None, return_type='QuerySet',
                   include_deleted=False, **args):

        # 如果没有提供 objects，获取全部的objects：
        if objects is None: objects = obj_type.objects.all()

        # 过滤 deleted：
        if not include_deleted and hasattr(obj_type, 'is_deleted'):
            result = objects.filter(is_deleted=False)
        else:
            result = objects

        # 执行查询：
        result = result.filter(**args)

        if return_type == 'dict':
            temp = []
            for r in result:
                temp.append(r.convertToDict())
            result = temp

        return result


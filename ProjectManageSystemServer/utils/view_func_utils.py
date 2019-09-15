from django.conf import settings
from django.http import JsonResponse, HttpResponse
from utils.exception import ErrorType, ErrorException
import json, requests, datetime, traceback

# 接收请求
def recieveRequest(request, func, POST=[], GET=[], FILES=[]):

    try:
        # 获取数据
        data = getRequestDict(request, POST=POST, GET=GET, FILES=FILES)

        res = func(data)

    except ErrorException as exception:
        return getErrorResponse(exception)

    return getSuccessResponse(res)

# 获取请求参数字典
def getRequestDict(request, POST=[], GET=[], FILES=[]):
    data = dict()

    for item in POST:
        value = request.POST.get(item[0])
        if value:
            data[item[0]] = convertDataType(value, item[1])
        else:
            raise ErrorException(ErrorType.ParameterError)

    for item in GET:
        value = request.GET.get(item[0])
        if value:
            data[item[0]] = convertDataType(value, item[1])
        else:
            raise ErrorException(ErrorType.ParameterError)

    for key in FILES:
        value = request.FILES.get(key)
        if value:
            data[key] = value
        else:
            raise ErrorException(ErrorType.ParameterError)

    print(data)

    return data

# 处理WebSocket请求
def processWebsocketRequest(request, key_data=[]):
    res_data = dict()

    for data in key_data:

        key = data[0]
        type = data[1]

        if key in request:
            res_data[key] = convertDataType(request[key], type)
        else:
            raise ErrorException(ErrorType.ParameterError)

    print('request: ' + str(res_data))

    return res_data

# 转换数据类型
def convertDataType(value, type='str'):
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

        elif type == 'date':
            value = datetime.datetime.strptime(value, '%Y-%m-%d')

        elif type == 'datetime':
            value = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')

        # 其他类型判断
        return value

    except:
        raise ErrorException(ErrorType.ParameterError)

# 转换多个数据类型
def convertMultDataType(data, keys, type='str'):
    for key in keys:
        data[key] = convertDataType(data[key], type)

# 转换数据数组中全部数据类型
def convertAllDataType(data, type='str'):
    convertMultDataType(data, data, type)

# 封装成功响应数据字典
def getSuccessResponseDict(dict={}, list_encapsulate=settings.RESPONSE_LIST_ENCAP):

    dict['status'] = ErrorType.Success.value

    return dict

# 封装Emit数据字典
def getSuccessEmitDict(type, dict={}, list_encapsulate=settings.RESPONSE_LIST_ENCAP):

    dict['type'] = type
    dict['status'] = ErrorType.Success.value

    return dict

# 封装错误响应数据字典
def getErrorResponseDict(exception: ErrorException):
    return {
        'status': exception.error_type.value,
        'errmsg': str(exception)
    }

# 封装错误Emit数据字典
def getErrorEmitDict(type, exception: ErrorException):
    return {
        'type': type,
        'status': exception.error_type.value,
        'errmsg': str(exception)
    }

# 获取成功响应对象
def getSuccessResponse(dict={}):
    dict = getSuccessResponseDict(dict)

    if settings.HTML_TEST:
        # 测试代码
        response = JsonResponse(dict)
        response["X-Frame-Options"] = ''

        return response
    else:
        return JsonResponse(dict)

# 获取失败响应对象
def getErrorResponse(exception: ErrorException):
    traceback.print_exc()

    dict = getErrorResponseDict(exception)

    if settings.HTML_TEST:
        # 测试代码
        response = JsonResponse(dict)
        response["X-Frame-Options"] = ''

        return response
    else:
        return JsonResponse(dict)

# 获取模型数据对象
def getObject(obj_type, error, objects=None, id=None, name=None,
              return_type='QuerySet', include_deleted=False):

    if objects is None: objects = obj_type.objects.all()

    if return_type == 'object':

        query_set = getObject(obj_type, error, objects, id, name,
                              'QuerySet', include_deleted)

        if query_set.exists():
            return query_set[0]

        else:
            raise ErrorException(error)

    if return_type == 'dict':
        object = getObject(obj_type, error, objects, id, name,
                           'object', include_deleted)

        return object.convertToDict()

    if id:
        if not include_deleted and hasattr(obj_type, 'is_deleted'):
            return objects.filter(id=id, is_deleted=False)
        else:
            return objects.filter(id=id)

    if name:
        if not include_deleted and hasattr(obj_type, 'is_deleted'):
            return objects.filter(name=name, is_deleted=False)
        else:
            return objects.filter(name=name)

    return None

# 获取模型数据对象集
def getObjects(obj_type, objects=None, ids=None, return_type='QuerySet',
               include_deleted=False):

    if objects is None: objects = obj_type.objects.all()

    if not include_deleted and hasattr(obj_type, 'is_deleted'):

        result = objects.filter(is_deleted=False)

    else:

        result = objects

    if ids:
        result = result.filter(id__in=ids)

    if return_type == 'dict':
        temp = []
        for r in result:
            temp.append(r.convertToDict())
        result = temp

    return result


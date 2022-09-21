from flask import jsonify

from applications.common.utils.code import SUCCESS, FAIL


def success_api(msg: str="成功", data={}):
    """ 成功响应 默认值”成功“ """
    return jsonify(success=True, code=SUCCESS, msg=msg, data=data)


def fail_api(msg: str="失败", code_id: int=FAIL):
    """ 失败响应 默认值“失败” """
    return jsonify(success=False, code=code_id, msg=msg)


def table_api(msg: str="", count=0, data=None, limit=10):
    """ 动态表格渲染响应 """
    res = {
        'success': True,
        'msg': msg,
        'code': SUCCESS,
        'data': data,
        'count': count,
        'limit': limit
    }
    return jsonify(res)

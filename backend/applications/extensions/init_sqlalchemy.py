import datetime

from flask import Flask, request
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy, BaseQuery
from marshmallow import fields
from marshmallow.validate import (URL, Email, Range, Length, Equal, Regexp,
                                  Predicate, NoneOf, OneOf, ContainsOnly)

URL.default_message = '无效的链接'
Email.default_message = '无效的邮箱地址'
Range.message_min = '不能小于{min}'
Range.message_max = '不能小于{max}'
Range.message_all = '不能超过{min}和{max}这个范围'
Length.message_min = '长度不得小于{min}位'
Length.message_max = '长度不得大于{max}位'
Length.message_all = '长度不能超过{min}和{max}这个范围'
Length.message_equal = '长度必须等于{equal}位'
Equal.default_message = '必须等于{other}'
Regexp.default_message = '非法输入'
Predicate.default_message = '非法输入'
NoneOf.default_message = '非法输入'
OneOf.default_message = '无效的选择'
ContainsOnly.default_message = '一个或多个无效的选择'

fields.Field.default_error_messages = {
    "required": "缺少必要数据",
    "null": "数据不能为空",
    "validator_failed": "非法数据",
}

fields.Str.default_error_messages = {'invalid': "不是合法文本"}

fields.Int.default_error_messages = {"invalid": "不是合法整数"}

fields.Number.default_error_messages = {"invalid": "不是合法数字"}

fields.Boolean.default_error_messages = {"invalid": "不是合法布尔值"}


class Query(BaseQuery):
    def soft_delete(self):
        return self.update({"delete_at": datetime.datetime.now()})

    def logic_all(self):
        return self.filter_by(delete_at=None).all()

    def all_json(self, schema: Marshmallow().Schema):
        return schema(many=True).dump(self.all())

    def layui_paginate(self):
        limit = request.args.get('limit', type=int)
        page = request.args.get('page', type=int)
        return self.paginate(page=page, per_page=limit, error_out=False)

    def layui_paginate_json(self, schema: Marshmallow().Schema):
        """
        返回dict
        """
        _res = self.paginate(
            page=request.args.get('page', type=int),
            per_page=request.args.get('limit', type=int),
            error_out=False)
        return schema(
            many=True).dump(_res.items), _res.total, _res.page, _res.per_page

    def layui_paginate_db_json(self):
        """
        db.query(A.name).layui_paginate_db_json()
        """
        _res = self.paginate(
            page=request.args.get('page', type=int),
            per_page=request.args.get('limit', type=int),
            error_out=False)
        return [dict(i) for i in _res.items], _res.total


db = SQLAlchemy(query_class=Query)
ma = Marshmallow()


def init_databases(app: Flask):
    db.init_app(app)
    ma.init_app(app)

from marshmallow import fields

from applications.extensions import ma


class SevenDaySchema(ma.Schema):
    dates = fields.Str()
    num = fields.Integer()


class GroupSchema(ma.Schema):
    type = fields.Integer()
    num = fields.Integer()


class FunctionGroupSchema(ma.Schema):
    function = fields.Str()
    num = fields.Integer()

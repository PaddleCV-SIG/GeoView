from marshmallow import fields

from applications.extensions import ma


class AnalysisSchema(ma.Schema):
    id = fields.Integer()
    type = fields.Integer()
    before_img = fields.Str()
    before_img1 = fields.Str()
    after_img = fields.Str()
    data = fields.Dict()
    is_hole = fields.Boolean()
    create_time = fields.DateTime()

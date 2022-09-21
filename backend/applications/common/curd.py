import datetime

from marshmallow import Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from applications.extensions import db, ma


class LogicalDeleteMixin(object):
    """
    class Test(db.Model,LogicalDeleteMixin):
    __tablename__ = 'admin_test'
    id = db.Column(db.Integer, primary_key=True, comment='角色ID')

    Test.query.filter_by(id=1).soft_delete()
    Test.query.logic_all()
    """
    create_at = db.Column(
        db.DateTime, default=datetime.datetime.now, comment='创建时间')
    update_at = db.Column(
        db.DateTime,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now,
        comment='创建时间')
    delete_at = db.Column(db.DateTime, comment='删除时间')


def auto_model_jsonify(data, model: db.Model):
    """
    不需要建立schemas，直接使用orm的定义模型进行序列化
    基本功能，待完善
    示例
    power_data = curd.auto_model_jsonify(model=Dept, data=dept)
    """

    def get_model():
        return model

    class AutoSchema(SQLAlchemyAutoSchema):
        class Meta(Schema):
            model = get_model()
            include_fk = True
            include_relationships = True
            load_instance = True

    common_schema = AutoSchema(many=True)  # 用已继承ma.ModelSchema类的自定制类生成序列化类
    output = common_schema.dump(data)
    return output


def model_to_dicts(schema: ma.Schema, data):
    """
    :param schema: schema类
    :return: 返回单个查询结果
    """
    # 如果是分页器返回，需要传入model.items
    common_schema = schema(many=True)  # 用已继承ma.ModelSchema类的自定制类生成序列化类
    output = common_schema.dump(data)  # 生成可序列化对象
    return output


def get_one_by_id(model: db.Model, id):
    """
    :param model: 模型类
    :param id: id
    :return: 返回单个查询结果
    """
    return model.query.filter_by(id=id).first()


def delete_one_by_id(model: db.Model, id):
    """
    :param model: 模型类
    :param id: id
    :return: 返回单个查询结果
    """
    r = model.query.filter_by(id=id).delete()
    db.session.commit()
    return r


# 启动状态
def enable_status(model: db.Model, id):
    enable = 1
    role = model.query.filter_by(id=id).update({"enable": enable})
    if role:
        db.session.commit()
        return True
    return False


# 停用状态
def disable_status(model: db.Model, id):
    enable = 0
    role = model.query.filter_by(id=id).update({"enable": enable})
    if role:
        db.session.commit()
        return True
    return False

from flask import Blueprint, request, jsonify

from applications.common.utils import upload as upload_curd, type_utils
from applications.common.utils.http import fail_api

file_api = Blueprint('file_api', __name__, url_prefix='/api/file')


#   上传接口
@file_api.post('/upload')
def upload_api():
    if 'files' in request.files:
        type_ = request.form['type']
        to_type = type_utils.str_to_type(type_)
        photos = request.files.getlist("files")
        mime = request.files['files'].content_type
        data = list()
        for photo in photos:
            file_url, photo_id = upload_curd.upload_one(
                photo=photo, mime=mime, type_=to_type)
            data.append({
                "src": file_url,
                "filename": photo.filename,
                "photo_id": photo_id
            })
        res = {"msg": "上传成功", "code": 0, "success": True, "data": data}
        return jsonify(res)
    return fail_api()

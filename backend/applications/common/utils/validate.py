# xss过滤
from flask import abort, make_response, jsonify


def xss_escape(s: str):
    if s is None:
        return None
    else:
        return s.replace("&", "&amp;").replace(">", "&gt;").replace("<", "&lt;").replace("'", "&#39;").replace('"',
                                                                                                               "&#34;")


def check_data(schema, data):
    errors = schema.validate(data)
    for k, v in errors.items():
        for i in v:
            # print("{}{}".format(k, i))
            msg = "{}{}".format(k, i)
    if errors:
        abort(make_response(jsonify(result=False, msg=msg), 200))

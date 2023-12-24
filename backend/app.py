import traceback
from datetime import timedelta

from flask import session
from flask_migrate import Migrate

from applications import create_app
from applications.common.utils.http import fail_api
from applications.extensions import db

debug_mode = False
app = create_app()


@app.before_request
def before():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=20)


@app.errorhandler(Exception)
def error_handler(e):
    if debug_mode:
        traceback.print_exc()
    return fail_api("后端出现异常：{}".format(str(e)))


migrate = Migrate(app, db)

if __name__ == '__main__':
    import yaml
    with open('../config.yaml') as file:
        config = yaml.load(file.read(), Loader=yaml.FullLoader)
    debug_mode = bool(config.get("debug", False))
    app.run(host=config["host"]["backend"], port=config["port"]["backend"])

from datetime import timedelta

from flask import session
from flask_migrate import Migrate

from applications import create_app
from applications.common.utils.http import fail_api
from applications.extensions import db

app = create_app()


@app.before_request
def before():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=20)


@app.errorhandler(Exception)
def error_handler(e):
    return fail_api("后端出现异常：{}".format(str(e)))


migrate = Migrate(app, db)

if __name__ == '__main__':
    import yaml
    with open('../config.yaml') as file:
        config = yaml.load(file.read(), Loader=yaml.FullLoader)
    with open("../frontend/.env", 'w') as file:
        file.write(
            "VUE_APP_BACKEND_PORT = {}\nVUE_APP_BACKEND_IP = {}\nVUE_APP_BAIDU_MAP_ACCESS_KEY = {}".
            format(config["port"]["backend"], config["host"]["backend"]
                   if config["host"]["backend"] != "0.0.0.0" else "127.0.0.1",
                   config["baidu_map"]["access_key"]))
    app.run(host=config["host"]["backend"], port=config["port"]["backend"])

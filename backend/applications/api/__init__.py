from flask import Flask

from applications.api.analysis import analysis_api
from applications.api.file import file_api
from applications.api.history import history_api


def system_api(app: Flask):
    app.register_blueprint(file_api)
    app.register_blueprint(history_api)
    app.register_blueprint(analysis_api)
    pass

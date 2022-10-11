from datetime import timedelta

from flask import session
from flask_migrate import Migrate

from applications import create_app
from applications.extensions import db

app = create_app()


@app.before_request
def before():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=20)


migrate = Migrate(app, db)

if __name__ == '__main__':
    import yaml
    with open('../config.yaml') as file:
        config = yaml.load(file.read(), Loader=yaml.FullLoader)
    with open("../frontend/.env", 'w') as file:
        file.write("VUE_APP_BACKEND_PORT = {}".format(config["port"][
            "backend"]))
    app.run(host=config["host"]["backend"], port=config["port"]["backend"])

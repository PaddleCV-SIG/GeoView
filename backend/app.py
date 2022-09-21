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
    app.run(host='0.0.0.0', port="5008")

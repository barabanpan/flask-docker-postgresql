from flask import Flask
from celery import Celery
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

from .config import Config


db = SQLAlchemy()
mail = Mail()
celery = Celery(__name__,
                broker=Config.CELERY_BROKER_URL,
                backend=Config.CELERY_RESULT_BACKEND)


def create_app():
    app = Flask(__name__)

    # data in config is taken from .env
    # .env[dev or prod] is stated in docker-compose[dev or prod]
    # and we choose which docker-compose we build a container from
    app.config.from_object("project.config.Config")

    db.init_app(app)
    mail.init_app(app)

# doesn't seem to work at all
#    with app.app_context():  # WHAT IS THAT FOR???
#        @app.before_first_request
#        def create_tables():
#            db.create_all()
#            db.session.commit()

    from .views.views import main_app_bp
    app.register_blueprint(main_app_bp)

    return app

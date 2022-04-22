from flask import Flask
from app.models import db, ma

from app.routes import url_routes


def create_app():
    
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db.init_app(app)
    ma.init_app(app)
    
    app.register_blueprint(url_routes.blueprint)

    with app.app_context():
        db.create_all()

    return app

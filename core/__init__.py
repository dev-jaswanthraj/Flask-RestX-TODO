from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["JWT_SECRET_KEY"] = "1234567890"

api = Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

with app.app_context():
    from core.models import Todo, User
    db.create_all()
from core import views
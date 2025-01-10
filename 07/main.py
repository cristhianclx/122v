import datetime
from flask import Flask, request
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["JWT_SECRET_KEY"] = "python"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(days=7)

jwt = JWTManager(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

ma = Marshmallow(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    country = db.Column(db.String(10), nullable=True)
    city = db.Column(db.String(150), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return "<User: {}>".format(self.id)
    

class UserSchema(ma.Schema):
    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "age",
            "country",
            "city",
            "created_at",
        )
        datetimeformat = "%Y-%m-%d %H:%M:%S"


user_schema = UserSchema()
users_schema = UserSchema(many = True)


class UserSimpleSchema(ma.Schema):
    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
        )
        datetimeformat = "%Y-%m-%d %H:%M:%S"


user_simple_schema = UserSimpleSchema()
users_simple_schema = UserSimpleSchema(many = True)


class Message(db.Model):

    __tablename__ = "messages"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50))
    content = db.Column(db.Text)
    priority = db.Column(db.String(10)) # LOW,HIGH
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", backref="user")

    def __repr__(self):
        return "<Message: {}>".format(self.id)


class MessageSchema(ma.Schema):
    user = ma.Nested(UserSchema)
    class Meta:
        model = Message
        fields = (
            "id",
            "title",
            "content",
            "priority",
            "user",
            "created_at",
        )
        datetimeformat = "%Y-%m-%d %H:%M:%S"


message_schema = MessageSchema()
messages_schema = MessageSchema(many = True)


class MessageBasicSchema(ma.Schema):
    class Meta:
        model = Message
        fields = (
            "id",
            "title",
            "content",
            "priority",
            "created_at",
        )
        datetimeformat = "%Y-%m-%d %H:%M:%S"


message_basic_schema = MessageBasicSchema()
messages_basic_schema = MessageBasicSchema(many = True)


@app.route("/status/", methods=["GET"])
def status():
    return {
        "working": "live",
    }


@app.route("/login/", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "cristhian" or password != "test":
        return {"msg": "Bad username or password"}, 401
    access_token = create_access_token(identity=username)
    return {"access_token": access_token}


@app.route("/public/")
def public():
    return {
        "public": True,
    }


# headers: Authorization Bearer X
@app.route("/me/")
@jwt_required()
def me():
    current_user = get_jwt_identity()
    return {
        "logged_as": current_user,
    }


@app.route("/me/messages/", methods=["GET", "POST"])
@jwt_required()
def my_messages():
    if request.method == "GET":
        # return todos los mensajes asociados al usuario logueado, first_name="cristhian"
        return []
    if request.method == "POST":
        # crear un mensaje asociado al usuario first_name="cristhian"
        return {}
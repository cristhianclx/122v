from flask import Flask, request
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful_swagger_3 import Resource, Api, swagger, Schema
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

ma = Marshmallow(app)

api = Api(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    country = db.Column(db.String(10), nullable=True)
    city = db.Column(db.String(150), nullable=True)
    created_at = db.Column(
        db.DateTime(timezone=True),
        server_default=func.now(),
    )

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
users_schema = UserSchema(many=True)


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
users_simple_schema = UserSimpleSchema(many=True)


class Message(db.Model):

    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50))
    content = db.Column(db.Text)
    priority = db.Column(db.String(10))  # LOW,HIGH
    created_at = db.Column(
        db.DateTime(timezone=True),
        server_default=func.now(),
    )

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
messages_schema = MessageSchema(many=True)


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
messages_basic_schema = MessageBasicSchema(many=True)


class StatusResource(Resource):
    def get(self):
        return {"status": "live"}


class UsersPublicResource(Resource):
    def get(self):
        items = User.query.all()
        return users_simple_schema.dump(items)


class UsersResource(Resource):
    def get(self):
        items = User.query.all()
        return users_schema.dump(items)

    def post(self):
        data = request.get_json()
        item = User(**data)
        db.session.add(item)
        db.session.commit()
        return user_schema.dump(item), 201


class UserIDResource(Resource):
    def get(self, id):
        item = User.query.get_or_404(id)
        return user_schema.dump(item)

    def patch(self, id):
        item = User.query.get_or_404(id)
        data = request.get_json()
        item.first_name = data.get("first_name", item.first_name)
        item.last_name = data.get("last_name", item.last_name)
        item.age = data.get("age", item.age)
        item.country = data.get("country", item.country)
        item.city = data.get("city", item.city)
        db.session.add(item)
        db.session.commit()
        return user_schema.dump(item)

    def delete(self, id):
        item = User.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()
        return {}, 204


class MessagesResource(Resource):
    def get(self):
        items = Message.query.all()
        return messages_schema.dump(items)

    def post(self):
        data = request.get_json()
        item = Message(**data)
        db.session.add(item)
        db.session.commit()
        return message_schema.dump(item), 201


class MessageIDResource(Resource):
    def get(self, id):
        item = Message.query.get_or_404(id)
        return message_schema.dump(item)

    def patch(self, id):
        item = Message.query.get_or_404(id)
        data = request.get_json()
        item.title = data.get("title", item.title)
        item.content = data.get("content", item.content)
        item.priority = data.get("priority", item.priority)
        item.user_id = data.get("user_id", item.user_id)
        db.session.add(item)
        db.session.commit()
        return message_schema.dump(item)

    def delete(self, id):
        item = Message.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()
        return {}, 204


class UserIDMessagesResource(Resource):
    def get(self, id):
        user = User.query.get_or_404(id)
        items = Message.query.filter_by(user=user).all()
        return messages_basic_schema.dump(items)

    def post(self, id):
        user = User.query.get_or_404(id)
        data = request.get_json()
        item = Message(**data)
        item.user = user
        db.session.add(item)
        db.session.commit()
        return message_basic_schema.dump(item)


api.add_resource(StatusResource, "/status/")
api.add_resource(UsersPublicResource, "/users/public/")
api.add_resource(UsersResource, "/users/")
api.add_resource(UserIDResource, "/users/<int:id>/")
api.add_resource(MessagesResource, "/messages/")
api.add_resource(MessageIDResource, "/messages/<int:id>/")
api.add_resource(UserIDMessagesResource, "/users/<int:id>/messages/")


class EmailModel(Schema):
    type = "string"
    format = "email"


class KeysModel(Schema):
    type = "object"
    properties = {"name": {"type": "string"}}


class UserModel(Schema):
    properties = {
        "id": {
            "type": "integer",
            "format": "int64",
        },
        "name": {"type": "string"},
        "mail": EmailModel,
        "keys": KeysModel.array(),
        "user_type": {
            "type": "string",
            "enum": ["admin", "regular"],
            "nullable": True,
        },
        "password": {
            "type": "string",
            "format": "password",
            "load_only": True,
        },
    }
    required = ["name"]


class UserItemResource(Resource):
    @swagger.tags(["user"])
    @swagger.reorder_with(
        UserModel,
        description="Returns a user",
        summary="Get User",
    )
    def get(self, user_id):
        # Do some processing
        return (
            UserModel(**{"id": 1, "name": "somebody"}),
            200,
        )  # generates json response {"id": 1, "name": "somebody"}


api.add_resource(UserItemResource, "/api/users/<int:user_id>")

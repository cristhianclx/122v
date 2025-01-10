from flask import Flask, request
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Resource, Api
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


class StatusResource(Resource):
    def get(self):
        return {
            "status": "live"
        }


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


api.add_resource(StatusResource, "/status/")
api.add_resource(UsersResource, "/users/")
api.add_resource(UserIDResource, "/users/<int:id>/")
api.add_resource(MessagesResource, "/messages/")
api.add_resource(MessageIDResource, "/messages/<int:id>/")


# LABORATORIO
# EP: /users/<id>/messages/
#     GET: return all messages for a user
#     POST: create a message associated to user
#             item = Message(**data)
#             item.user = user
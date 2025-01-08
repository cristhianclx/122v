from flask import Flask, request
from flask_migrate import Migrate
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

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


class StatusResource(Resource):
    def get(self):
        return {
            "status": "live"
        }


class UsersResource(Resource):
    def get(self):
        data = User.query.all()
        items = []
        for d in data:
            items.append({
                "id": d.id,
                "first_name": d.first_name,
                "last_name": d.last_name,
                "age": d.age,
                "country": d.country,
                "city": d.city,
            })
        return items
    
    def post(self):
        data = request.get_json()
        item = User(**data)
        db.session.add(item)
        db.session.commit()
        return {
            "id": item.id,
            "first_name": item.first_name,
            "last_name": item.last_name,
            "age": item.age,
            "country": item.country,
            "city": item.city,
        }, 201


api.add_resource(StatusResource, "/status/")
api.add_resource(UsersResource, "/users/")

# LABORATORIO
# /messages/ GET, POST


# EP: /users/
# (x) GET -> [{id, first_name, last_name}, {id, first_name, last_name}], 200
# (x) POST {first_name, last_name} -> {id, first_name, last_name}, 201
# EP: /users/<id>/
# ( ) GET -> {id, first_name, last_name}, 200
# ( ) PATCH {last_name} -> {id, first_name, last_name}, 200
# ( ) DELETE -> {}, 204
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.sql import func


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    age = db.Column(db.Integer)
    country = db.Column(db.String(10))
    city = db.Column(db.String(150))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return "<User: {}>".format(self.id) # <User: 1>


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

    
@app.route("/status/")
def status():
    return {
        "status": "ok"
    }


@app.route("/users/")
def users():
    data = User.query.all()
    return render_template("users.html", items=data)


@app.route("/users/add/", methods=["GET", "POST"])
def users_add():
    if request.method == "GET":
        return render_template("users-add.html")
    if request.method == "POST":
        item = User(
            first_name=request.form["first_name"],
            last_name=request.form["last_name"],
            age=request.form["age"],
            country=request.form["country"],
            city=request.form["city"],
        )
        db.session.add(item)
        db.session.commit()
        return render_template("users-add.html", information="Your changes were saved")


# LABORATORIO
# /messages/
# /messages/add/


# R /users/<id> -> read one user
# U /users/<id>/edit/ -> edit user
# D /users/<id>/delete/ -> delete user
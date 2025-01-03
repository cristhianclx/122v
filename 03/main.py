from flask import Flask, render_template, request, redirect, url_for
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


@app.route("/users/<id>")
def users_by_id(id):
    data = User.query.get_or_404(id)
    return render_template("users-details.html", item=data)


@app.route("/users/<id>/edit/", methods=["GET", "POST"])
def users_edit_by_id(id):
    data = User.query.get_or_404(id)
    if request.method == "GET":
        return render_template("users-edit.html", item=data)
    if request.method == "POST":
        data.first_name = request.form["first_name"]
        data.last_name = request.form["last_name"]
        data.age = request.form["age"]
        data.country = request.form["country"]
        data.city = request.form["city"]
        db.session.add(data)
        db.session.commit()
        return render_template("users-edit.html", item=data, information="Your changes were saved")


@app.route("/users/<id>/delete/", methods=["GET", "POST"])
def users_delete_by_id(id):
    data = User.query.get_or_404(id)
    if request.method == "GET":
        return render_template("users-delete.html", item=data)
    if request.method == "POST":
        db.session.delete(data)
        db.session.commit() 
        return redirect(url_for('users'))


@app.route("/messages/")
def messages():
    data = Message.query.all()
    return render_template("messages.html", items=data)


@app.route("/messages/add/", methods=["GET", "POST"])
def messages_add():
    users = User.query.all()
    if request.method == "GET":
        return render_template("messages-add.html", users=users)
    if request.method == "POST":
        item = Message(
            title=request.form["title"],
            content=request.form["content"],
            priority=request.form["priority"],
            user_id=request.form["user_id"],
        )
        db.session.add(item)
        db.session.commit()
        return render_template("messages-add.html", information="Your changes were saved", users=users)
    

@app.route("/messages/<id>")
def messages_by_id(id):
    users = User.query.all()
    data = Message.query.get_or_404(id)
    return render_template("messages-details.html", item=data, users=users)


# LABORATORIO
# messages/<id>/edit
# messages/<id>/delete
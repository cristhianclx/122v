from flask import Flask, render_template
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

ma = Marshmallow(app)

socketio = SocketIO(app)


class Room(db.Model):
    __tablename__ = "rooms"

    id = db.Column(db.String, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return "<Room: {}>".format(self.id)


class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    room_id = db.Column(db.String, db.ForeignKey("rooms.id"))
    room = db.relationship("Room", backref="room")

    def __repr__(self):
        return "<Message: {}>".format(self.id)


class MessageSchema(ma.Schema):
    class Meta:
        model = Message
        fields = (
            "id",
            "user",
            "content",
            "created_at",
        )
        datetimeformat = "%Y-%m-%d %H:%M:%S"


message_schema = MessageSchema()
messages_schema = MessageSchema(many = True)


@app.route("/ping/")
def ping():
    return {
        "status": "live",
    }


@app.route("/")
def index():
    items = Room.query.all()
    return render_template("index.html", items=items)


@app.route("/rooms/<id>")
def rooms_by_id(id):
    room = Room.query.get_or_404(id)
    items = Message.query.filter_by(room = room).all()
    return render_template("messages.html", room=room, items=items)


@socketio.on("ws-messages")
def handle_ws_message(data):
    item = Message(**data)
    db.session.add(item)
    db.session.commit()
    raw = message_schema.dump(item)
    channel_id = "ws-messages-responses-{}".format(item.room.id)
    socketio.emit(channel_id, raw)


# LABORATORIO
# - create room, /rooms/create/
# - hacer visible el created_at, pero para los mensajes mayores a un dia de generados
#   poner hace mas de un dia
#      user 1: 122v (2024-01-01 05:00:00)
#      ....
#      user 1: 122v (hace mas de un dia)
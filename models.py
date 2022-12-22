from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    rooms = db.relationship('Room', backref='poster')
    messages = db.relationship('Message', backref='author')

    def __repr__(self):
        return '<User {}>'.format(self.id)

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    messages = db.relationship('Message', backref='room')
    poster_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<ChatRoom {}>'.format(self.id)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    poster_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Message {}>'.format(self.id)
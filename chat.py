from flask import Flask, request, session, url_for, redirect, render_template, abort, g, flash, _app_ctx_stack
from werkzeug.security import check_password_hash, generate_password_hash
import json

from models import Room, db, User, Message

app = Flask(__name__)

PER_PAGE = 30
DEBUG = True
SECRET_KEY = 'development key'

SQLALCHEMY_DATABASE_URI = 'sqlite:///chat.db'

app.config.from_object(__name__)
app.config.from_envvar('CHAT_SETTINGS', silent=True)

db.init_app(app)

@app.cli.command('initdb')
def initdb_command():
	db.drop_all()
	db.create_all()
	print('Initialized the database.')

@app.route('/')
def start():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user = User.query.filter_by(name=request.form['username']).first()
        if user is None:
            error = 'Invalid username/password'
        elif not check_password_hash(user.password, request.form['password']):
            error = 'Invalid username/password'
        else:
            session['id'] = user.id
            session['logged_in'] = True
            return redirect(url_for('show_main_page'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('start'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        if not request.form['username']:
            error = 'You have to enter a username'
        elif not request.form['password']:
            error = 'You have to enter a password'
        elif request.form['password'] != request.form['password2']:
            error = 'The two passwords have to match'
        else:
            db.session.add(User(name=request.form['username'], password=generate_password_hash(request.form['password'])))
            db.session.commit()
            flash('Account created successfully')
            return(redirect(url_for('login')))
    return render_template('register.html', error=error)

@app.route('/main', methods=['GET', 'POST'])
def show_main_page():
    chatRooms = Room.query.order_by(Room.id.desc()).all()
    return render_template('main.html', chatRooms=chatRooms)

@app.route('/enter/<room>')
def enter_chat_room(room):
    r = Room.query.filter_by(name=room).first()
    return render_template('chatRoom.html', room=r)

@app.route('/newroom', methods=['POST'])
def create_chat_room():
    user = User.query.filter_by(id=session['id']).first()
    new = Room(name=request.form['roomName'], poster_id=user.id)
    db.session.add(new)
    db.session.commit()
    return redirect(url_for('show_main_page'))

@app.route('/message/<room>', methods=['POST'])
def post_message(room):
    r = Room.query.filter_by(name=room).first()
    user = User.query.filter_by(id=session['id']).first()
    message = Message(content=request.form['message'], room_id=r.id, poster_id=user.id)
    db.session.add(message)
    db.session.commit()
    return redirect(url_for('enter_chat_room', room=room))

@app.route('/leave', methods=['GET'])
def leave_room():
    return redirect(url_for('show_main_page'))

@app.route('/delete/<room>')
def delete_chat_room(room):
    r = Room.query.filter_by(name=room).first()
    user = User.query.filter_by(id=session['id']).first()
    if r.poster_id == user.id:
        db.session.delete(r)
        db.session.commit()
    else:
        flash('You did not create that room')
    return redirect(url_for('show_main_page'))

@app.route('/messages')
def update():
    messages = Message.query.order_by(Message.id.desc()).all()
    return json.dumps(messages)
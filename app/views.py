from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, current_user, login_required, logout_user
from app import app, db, lm
from forms import LoginForm, SubmitEntry
from models import User, Entry, Title, ROLE_USER, ROLE_ADMIN
from datetime import datetime

@lm.user_loader
def load_user(id):
	return User.query.get(int(id))

@app.before_request
def before_request():
	g.user = current_user
	if g.user.is_authenticated():
		g.user.last_seen = datetime.utcnow()
		db.session.add(g.user)
		db.session.commit()

@app.route('/')
@app.route('/index')
def index():
	if g.user is not None and g.user.is_authenticated():
		author = g.user
	else:
		author = {'nickname': 'visitor'}
	titles = Title.query.all()
	return render_template("index.html",
		title = 'home',
		author = author,
		titles = titles)

@app.route('/register', methods = ['GET', 'POST'])
def register():
	form = LoginForm()
	if form.validate_on_submit():
		user = User()
		user.nickname = form.nickname.data
		user.password = form.password.data
		if User.query.filter_by(nickname = user.nickname).first():
			flash('username exists')
			return redirect(url_for('register'))
		db.session.add(user)
		db.session.commit()
		flash('congrulations, you become an author')
		login_user(user)
		return redirect(url_for('index'))
	return render_template('register.html',
		title = 'sign up',
		form = form)

@app.route('/author/<nickname>')
def author(nickname):
	author = User.query.filter_by(nickname = nickname).first()
	if author == None:
		flash('Author ' + nickname + ' not found.')
		return redirect(url_for('index'))
	entries = [
		{
			'title': 'eksi sozluk reloaded',
			'author': {'nickname': 'taskiner'},
			'body': 'an eksi-sozluk clone written with python and flask'
		},
		{
			'title': 'ssg',
			'author': {'nickname': 'taskiner'},
			'body': 'founder of eksi-sozluk'
		}
	] # fake entries
	return render_template('author.html',
		author = author,
		entries = entries)

@app.route('/login', methods = ['GET', 'POST'])
def login():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		nickname = form.nickname.data
		password = form.password.data
		registered_user = User.query.filter_by(nickname=nickname, password=password).first()
		if registered_user is None:
			flash('wrong username or password')
			return redirect(url_for('login'))
		login_user(registered_user)
		flash('logged in succesfully.')
		return redirect(request.args.get('next') or url_for('index'))
	return render_template('login.html',
		title = 'login',
		form = form)

@app.route('/title/<title_id>', methods = ['GET', 'POST'])
def title(title_id):
	form = SubmitEntry()
	title = Title.query.filter_by(id = title_id).first()
	entries = Entry.query.filter_by(title_id= title_id).all()
	# TODO: if title not found, let user add it.
	if form.validate_on_submit():
		entry = Entry(body = form.body.data, 
			timestamp = datetime.utcnow(), 
			user_id = current_user.id,
			title_id = title_id)
		db.session.add(entry)
		db.session.commit()
		return redirect(url_for('title', title_id = title_id))
	return render_template('title.html',
		title = title.title_name,
		ttl = title,
		entries = entries,
		form = form)

@app.route('/logout')
@login_required
def logout():
	logout_user()
	flash('logout succesfull')
	return redirect(url_for('index'))




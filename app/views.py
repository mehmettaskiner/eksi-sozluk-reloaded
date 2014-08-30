#-*- coding: utf8 -*-
from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, current_user, login_required, logout_user
from app import app, db, lm
from forms import LoginForm, SubmitEntry, SearchTitle
from models import User, Entry, Title, ROLE_USER, ROLE_ADMIN
from datetime import datetime

#############################################################
# send titles = Title.fetch_non_empty_titles() with render_template
# where you want to show left frame
#############################################################

@lm.user_loader
def load_user(id):
	return User.query.get(int(id))

@app.before_request
def before_request():
	g.user = current_user
	g.search_form = SearchTitle() # attached search form to global g user variable to make sure it is available from everywhere

# index page
@app.route('/')
@app.route('/index')
def index():
	non_empty_titles = Title.fetch_non_empty_titles(Title())
	return render_template("index.html",
		title = 'home',
		titles = non_empty_titles,
		)

# register page
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
		form = form,
		titles = Title.fetch_non_empty_titles(Title()))

# author's profiles
@app.route('/author/<nickname>')
def author(nickname):
	author = User.query.filter_by(nickname = nickname).first()
	if author == None:
		flash('Author ' + nickname + ' not found.')
		return redirect(url_for('index'))
	entries = Entry.query.filter_by(user_id = author.id)
	return render_template('author.html',
		title = author.nickname,
		author = author,
		entries = entries,
		titles = Title.fetch_non_empty_titles(Title()))

# login page
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
		registered_user.save_last_seen()
		flash('logged in succesfully.')
		return redirect(request.args.get('next') or url_for('index'))
	return render_template('login.html',
		title = 'login',
		form = form,
		titles = Title.fetch_non_empty_titles(Title()))

# title view page
@app.route('/title/<title_id>', methods = ['GET', 'POST'])
def title(title_id):
	form = SubmitEntry()
	title = Title.query.filter_by(id = title_id).first()
	entries = Entry.query.filter_by(title_id= title_id).all()
	if title == None:
		return redirect(url_for('index'))
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
		form = form,
		titles = Title.fetch_non_empty_titles(Title()))

# search function
@app.route('/search', methods = ['POST'])
def search():
	if not g.search_form.validate_on_submit():
		return redirect(url_for('index'))
	title_name = g.search_form.data['search']
	title = Title.query.filter_by(title_name = title_name).first()
	if title == None:
		title = Title(title_name = title_name)
		db.session.add(title)
		db.session.commit()
	return redirect(url_for('title', title_id = title.id))

# entry delete function
@app.route('/delete/<entry_id>', methods = ['GET', 'POST'])
@login_required
def delete(entry_id):
	entry = Entry.query.filter_by(id = entry_id).first()
	if g.user.id == entry.user_id or g.user.role == ROLE_ADMIN:
		db.session.delete(entry)
		db.session.commit()
		flash("entry deleted")
	else:
		flash('you are not allowed to do this.')
	return redirect(url_for('title', title_id = entry.title_id))

# add buddy function
@app.route('/follow/<nickname>')
@login_required
def follow(nickname):
	user = User.query.filter_by(nickname = nickname).first()
	if user == None:
		flash('Author ' + nickname + ' not found.')
		return redirect(url_for('index'))
	if user == g.user:
		flash("You can't follow yourself!")
		return redirect(url_for('index'))
	u = g.user.follow(user)
	if u is None:
		flash('Cannot follow ' + nickname + '.')
		return redirect(url_for('author', nickname = nickname))
	db.session.add(u)
	db.session.commit()
	flash(nickname + ' is your buddy now.')
	return redirect(url_for('author', nickname = nickname))

@app.route('/unfollow/<nickname>')
@login_required
def unfollow(nickname):
	user = User.query.filter_by(nickname = nickname).first()
	if user == None:
		flash('User ' + nickname + ' not found.')
		return redirect(url_for('index'))
	if user == g.user:
		flash("you can't unbuddy yourself.")
		return redirect(url_for('author', nickname = nickname))
	u = g.user.unfollow(user)
	if u is None:
		flash('Cannot unfollow ' + nickname + '.')
		return redirect(url_for('author', nickname = nickname))
	db.session.add(u)
	db.session.commit()
	flash(nickname + 'is not your buddy anymore.')
	return redirect(url_for('author', nickname = nickname))

# buddies' titles
@app.route('/buddy')
@login_required
def buddy():
	followed_entries = g.user.followed_entries().all()
	followed_titles = []
	if len(followed_entries) == 0:
		flash('you have no buddy entries.')
		return redirect(url_for('index'))
	for entry in followed_entries:
		followed_titles.append(entry.title)

	return render_template("buddy.html",
		title = 'buddy entries',
		titles = followed_entries,
		)

@app.route('/entry/<entry_id>', methods = ['GET', 'POST'])
def entry(entry_id):
	form = SubmitEntry()
	entry = Entry.query.filter_by(id = entry_id).first()
	entries = []
	entries.append(entry)
	title = Title.query.filter_by(id = entry.title_id).first()
	if form.validate_on_submit():
		new_entry = Entry(body = form.body.data, 
			timestamp = datetime.utcnow(), 
			user_id = current_user.id,
			title_id = title_id)
		db.session.add(new_entry)
		db.session.commit()
		return redirect(url_for('title', title_id = title_id))
	return render_template('title.html',
		title = title.title_name,
		ttl = title,
		entries = entries,
		form = form,
		titles = Title.fetch_non_empty_titles(Title()))

# logout
@app.route('/logout')
@login_required
def logout():
	logout_user()
	flash('logout succesfull')
	return redirect(url_for('index'))
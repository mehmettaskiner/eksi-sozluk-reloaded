from app import db
from datetime import datetime

ROLE_USER = 0
ROLE_ADMIN = 1

followers = db.Table('followers',
	db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
	db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
	)

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	nickname = db.Column(db.String(64), index = True, unique = True)
	password = db.Column(db.String(120), index = True, unique = False)
	role = db.Column(db.SmallInteger, default = ROLE_USER)
	entries = db.relationship('Entry', backref = 'author', lazy = 'dynamic')
	last_seen = db.Column(db.DateTime)
	followed = db.relationship('User',
		secondary = followers,
		primaryjoin = (followers.c.follower_id == id),
		secondaryjoin = (followers.c.followed_id == id),
		backref = db.backref('followers', lazy = 'dynamic'),
		lazy = 'dynamic')

	def followed_entries(self):
		return Entry.query.join(followers, (followers.c.followed_id == Entry.user_id)).filter(followers.c.follower_id == self.id).order_by(Entry.timestamp.desc())

	def save_last_seen(self):
		self.last_seen = datetime.utcnow()
		db.session.add(self)
		db.session.commit()

	def follow(self, user):
		if not self.is_following(user):
			self.followed.append(user)
			return self

	def unfollow(self, user):
		if self.is_following(user):
			self.followed.remove(user)
			return self

	def is_following(self, user):
		return self.followed.filter(followers.c.followed_id == user.id).count() > 0

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.id)

	def __repr__(self):
		return '<User %r>' % (self.nickname)

class Entry(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	body = db.Column(db.String(10000))
	timestamp = db.Column(db.DateTime)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	title_id = db.Column(db.Integer, db.ForeignKey('title.id'))

	def __repr__(self):
		return '<Entry %r>' % (self.body)

class Title(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	title_name = db.Column(db.String(50))
	entries = db.relationship('Entry', backref = 'title', lazy = 'dynamic')

	def fetch_non_empty_titles(self):
		return Title.query.join(Entry).filter(Entry.title_id == Title.id).order_by(Entry.timestamp.desc()).all()

	def __repr__(self):
		return '<Title %r>' % (self.title_name)
from app import db

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	nickname = db.Column(db.String(64), index = True, unique = True)
	password = db.Column(db.String(120), index = True, unique = False)
	role = db.Column(db.SmallInteger, default = ROLE_USER)
	entries = db.relationship('Entry', backref = 'author', lazy = 'dynamic')
	last_seen = db.Column(db.DateTime)

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

	def __repr__(self):
		return '<Title %r>' % (self.title_name)
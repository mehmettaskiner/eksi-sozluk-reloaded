#!flask/bin/python
from app import app, db
from app.models import Entry


def vote_fix():
    entries = Entry.query.all()
    for entry in entries:
        entry.positive_vote = 0
        entry.negative_vote = 0
        db.session.add(entry)
        db.session.commit()


def vote_fix_test():
    first_entry = Entry.query.first()
    print first_entry
    print first_entry.positive_vote
    print first_entry.negative_vote


if __name__ == '__main__':
    vote_fix()
    vote_fix_test()
from sqlalchemy import *
from migrate import *

from migrate.changeset import schema

pre_meta = MetaData()
post_meta = MetaData()
entry = Table('entry', post_meta,
              Column('id', Integer, primary_key=True, nullable=False),
              Column('body', String(length=10000)),
              Column('timestamp', DateTime),
              Column('user_id', Integer),
              Column('title_id', Integer),
              Column('positive_vote', Integer),
              Column('negative_vote', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['entry'].columns['positive_vote'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['entry'].columns['positive_vote'].drop()

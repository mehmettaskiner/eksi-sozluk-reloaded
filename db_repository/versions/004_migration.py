from sqlalchemy import *
from migrate import *

from migrate.changeset import schema

pre_meta = MetaData()
post_meta = MetaData()
entry = Table('entry', pre_meta,
              Column('id', INTEGER, primary_key=True, nullable=False),
              Column('body', VARCHAR(length=10000)),
              Column('timestamp', DATETIME),
              Column('user_id', INTEGER),
              Column('title_id', INTEGER),
              Column('negative_vote', INTEGER),
              Column('positive_vote', INTEGER),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['entry'].columns['negative_vote'].drop()
    pre_meta.tables['entry'].columns['positive_vote'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['entry'].columns['negative_vote'].create()
    pre_meta.tables['entry'].columns['positive_vote'].create()

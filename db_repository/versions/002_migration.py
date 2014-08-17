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
)

title = Table('title', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('title_name', String(length=50)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['entry'].create()
    post_meta.tables['title'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['entry'].drop()
    post_meta.tables['title'].drop()

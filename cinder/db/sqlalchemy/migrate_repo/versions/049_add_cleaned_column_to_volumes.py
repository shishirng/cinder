
from oslo_log import log as logging
from sqlalchemy import Column, MetaData, String, Table, Boolean

from cinder.i18n import _LE


def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    volumes = Table('volumes', meta, autoload=True)
    cleaned = Column('cleaned', Boolean(default=True))
    cleaner = Column('cleaner', String(264))
    try:
        volumes.create_column(cleaned)
        volumes.create_column(cleaner)
    except Exception:
        LOG.error(_LE("Adding cleaned/cleaner column to volumes table failed."))
        raise

def downgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine

    volumes = Table('volumes', meta, autoload=True)
    cleaned = volumes.columns.cleaned
    cleaner = volumes.columns.cleaner

    try:
        volumes.drop_column(cleaned)
        volumes.drop_column(cleaner)
    except Exception:
        LOG.error(_LE("Dropping cleaned/cleaner column from volumes table failed."))
        raise


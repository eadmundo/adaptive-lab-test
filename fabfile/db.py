"""
fabfile module for managing database-related tasks.
"""
from fabric.api import task
from fabric.context_managers import settings, hide
from fabric.colors import cyan, yellow
from fabric.utils import abort
from fabric.contrib.console import confirm
from fabfile.utils import do
from fabfile.virtualenv import venv_path

DB = {
    'name': 'app',
    'user': 'www-data',
}


@task
def build(db_name=None, config=None):
    """Initialise and migrate database to latest version."""
    if db_name:
        DB['name'] = db_name

    config_export = ''

    if config:
        config_export = 'FLASK_CONFIG=config/%s.py ' % config

    print(cyan('\nUpdating database...'))

    # Ensure database exists
    if not _pg_db_exists(DB['name']):
        do('createdb -O \'%(user)s\' \'%(name)s\'' % DB)

    # Ensure versions folder exists
    do('mkdir -p db/versions')

    # Run migrations
    do('%s%s/bin/alembic -c db/alembic.ini upgrade head' % (config_export, venv_path))


@task
def drop(db_name=None, warn=True):

    if not db_name:
        abort('You must provide a database name')

    if warn is True:
        print('\nYou are about to drop the database ' + yellow('%s' % db_name, bold=True))
        if not confirm('Continue?', default=False):
            abort('User aborted')

    if _pg_db_exists(db_name):
        do('dropdb %s' % db_name)


@task
def generate(message=None):
    """Generates a new Alembic revision based on DB changes."""
    args = ''
    if message:
        args = '-m "%s"' % message
    do('%s/bin/alembic -c db/alembic.ini revision --autogenerate %s' % (venv_path, args))


def _pg_db_exists(database):
    """
    Helper function to check if the postgresql database exists.
    """
    with settings(hide('running', 'warnings'), warn_only=True):
        return do('psql -tAc "SELECT 1 FROM pg_database WHERE datname = \'%s\'" postgres |grep -q 1' % database, capture=True).succeeded

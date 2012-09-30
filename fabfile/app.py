"""
fabfile module containing application-specific tasks.
"""
import os
import json

from fabric.api import env, task
from fabric.colors import cyan
from fabric.context_managers import lcd
from fabfile.utils import do
from fabfile.virtualenv import venv_path


@task
def build():
    """
    Run application build tasks.
    """
    # Ensure all base files exist
    do('mkdir -p app/static/assets/tmp')
    do('touch app/static/assets/tmp/mustache-compiled-templates.min.js')

    # Bower install
    print(cyan('\nRunning bower install...'))
    do('npm_config_loglevel=error bower install')
    do('npm_config_loglevel=error bower list --paths > app/static/assets/tmp/bower-paths.json')
    for path in json.loads(open('app/static/assets/tmp/bower-paths.json').read()).values():
        do('mkdir -p app/static/assets/%s' % os.path.dirname(path))
        do('cp %s app/static/assets/%s' % (path, path))

    # Generate static assets. Note that we always build assets with the
    # production config because dev will never point to compiled files.
    print(cyan('\nGenerating static assets...'))
    do('export FLASK_CONFIG=config/production.py && %s/bin/python manage.py mustache_compile' % venv_path)
    do('export FLASK_CONFIG=config/production.py && %s/bin/python manage.py assets clean' % venv_path)
    do('export FLASK_CONFIG=config/production.py && %s/bin/python manage.py assets -v build' % venv_path)


def run():
    """Start app in debug mode (for development)."""
    do('export FLASK_CONFIG=config/dev.py && %s/bin/python manage.py runserver' % venv_path)


def test():
    """Run unit tests"""
    print(cyan('\nRunning tests...'))
    do('export FLASK_CONFIG=config/test.py && %s/bin/nosetests --exclude-dir-file=\'.noseexclude\' --with-yanc --with-spec --spec-color -q --nocapture' % venv_path)


@task
def coverage():
    """Generate test coverage report"""
    do('export FLASK_CONFIG=config/test.py && %s/bin/nosetests --exclude-dir-file=\'.noseexclude\' --with-cov --cov=app --cov-report=html' % venv_path)


def start():
    """Start app using init."""
    do('sudo start gunicorn')


def stop():
    """Stop app using init."""
    do('sudo stop gunicorn')


def restart():
    """Restart app using init."""
    do('sudo restart gunicorn')

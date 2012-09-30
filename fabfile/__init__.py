from fabric.decorators import task
from fabric.context_managers import settings

# Load configuration
# import config

# Fabfile modules
import app
import db
import deployment as code
import puppet
import server
import virtualenv


@task
def build():
    """
    Execute build tasks.
    """
    virtualenv.build()
    app.build()
    db.build()


@task
def run():
    """
    Run app in debug mode (for development).
    """
    app.run()


@task
def test():
    """Run tests."""
    db.drop(db_name='test_app', warn=False)
    db.build(db_name='test_app', config='test')
    app.test()
    db.drop(db_name='test_app', warn=False)


#@task
def deploy():
    """
    Deploy to remote environment.

    Deploys code from the current git branch to the remote server and reloads
    services so that the new code is in effect.

    The remote server to deploy to is automatically determined based on the
    currently checked-out git branch and matched to the configuration specified
    in fabfile/deploy/config.py.
    """
    code.deploy()
    # Post-deploy tasks on the remote server
    with settings(host_string=server.remote()):
        build()
        puppet.run()
        app.restart()

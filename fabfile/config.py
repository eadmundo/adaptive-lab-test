"""
fabfile bundle config.
"""
from fabric.api import env
from fabfile.git import branch

env.branch = branch()
env.remote_path = '/srv/www/app'

env.user = env.user if env.user is 'root' else 'tobias'

env.servers = {
}

#
# Standalone manifest - for dev Vagrant box.
#
node precise64 {

  include common
  include vagrant
  include vagrant::postgresql
  include vagrant::puppet

  # Nginx
  nginx::site { 'gunicorn':
    ensure   => present,
    template => gunicorn,
    auth     => false,
  }

  # Gunicorn
  gunicorn::instance { 'gunicorn':
    ensure   => present,
    template => gunicorn,
    envs     => [
      [ 'FLASK_CONFIG' => "/srv/www/app/app/config/dev.py" ],
    ],
    # Gunicorn service in Vagrant can't start on init becuase /vagrant isn't
    # get mounted until boot is finished. Puppet will start it instead.
    startup  => false,
  }
}

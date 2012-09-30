define gunicorn::instance( $ensure = 'present', $template = $name, $startup = 'runlevel [2345]', $envs = [], $site_root = '/srv/www/app' ) {
  file { "/etc/init/${name}.conf":
    ensure  => $ensure,
    content => template("gunicorn/${template}.conf.tpl"),
    notify  => Service[$name],
  }
  file { "/etc/sudoers.d/upstart-${name}":
    mode    => 440,
    content => "fabric ALL = (root) NOPASSWD: /sbin/start ${name}, /sbin/stop ${name}, /sbin/reload ${name}, /sbin/restart ${name}\n"
  }
  service { $name:
    ensure   => running,
    provider => upstart,
    require  => [
      File["/etc/init.d/${name}"],
      File['/var/log/gunicorn.log'],
    ],
  }
  # Bug in Puppet <=2.7.14 requires symlink to exist in /etc/init.d, even for
  # upstart job
  file { "/etc/init.d/${name}":
    ensure => link,
    target => '/lib/init/upstart-job',
  }
  file { '/var/log/gunicorn.log':
    ensure => present,
    owner  => 'www-data',
    group  => 'www-data',
  }
}

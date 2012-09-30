class nginx {
  package { 'nginx':
    ensure => installed,
  }
  # Disable default nginx site
  file { '/etc/nginx/sites-enabled/default':
    ensure => absent,
    before => Service[nginx]
  }
  service { 'nginx':
    ensure => running,
  }
}

define nginx::site( $ensure = 'present', $template = $name, $auth = false, $site_root = '/srv/www/app' ) {
  file { "/etc/nginx/sites-enabled/${name}":
    ensure  => $ensure,
    owner   => root,
    group   => root,
    mode    => '644',
    content => template("nginx/${template}.tpl"),
    require => Package[nginx],
    notify  => Service[nginx],
  }
  if ($auth) {
    file { "/etc/nginx/htpasswd-${name}":
      ensure  => $ensure,
      owner   => root,
      group   => root,
      mode    => '644',
      content => "${auth}\n",
      require => File["/etc/nginx/sites-enabled/${name}"],
    }
  }
}

define nginx::site::redirect( $ensure = 'present', $template = 'redirects', $redirects ) {
  file { "/etc/nginx/sites-enabled/${name}":
    ensure  => $ensure,
    owner   => root,
    group   => root,
    mode    => '644',
    content => template("nginx/${template}.tpl"),
    require => Package[nginx],
    notify  => Service[nginx],
  }
}

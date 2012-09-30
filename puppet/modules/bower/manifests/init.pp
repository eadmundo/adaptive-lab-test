class bower {
  exec { 'bower-install':
    command => '/usr/bin/npm install bower -g',
    creates => '/usr/local/bin/bower',
    require => Package[npm],
  }
}

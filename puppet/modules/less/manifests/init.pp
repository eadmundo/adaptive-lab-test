class less {
  exec { 'less-install':
    command => '/usr/bin/npm install less --global',
    creates => '/usr/local/bin/lessc',
    require => Package[npm],
  }
}

# Adaptive Lab Test Application #

## Set-up

### Dependencies

* [git](http://git-scm.com)
* [Virtualbox](https://www.virtualbox.org)
* [Vagrant](http://vagrantup.com)
* a working internet connection

Although Vagrant does work cross-platform, the Vagrantfile in this repo sets up an NFS share in a way which won't work on Windows, so it requires OS X or Linux/Unix variant as the host OS.

### Starting the application

	$ git clone git@github.com:eadmundo/adaptive-lab-test.git
	$ cd adaptive-lab-test
	$ vagrant up

`vagrant up` may take a while, especially the first time (as it needs to download and/or import the basebox). Administrator privileges will be required, because of the NFS share mentioned above.

	$ vagrant ssh

`vagrant ssh` will drop you into the `adaptive-lab-test` folder but in the guest VM. From there you can run:

	$ fab run

and the application will be available from the host OS at [http://0.0.0.0:5000/](http://0.0.0.0:5000/).

## Developing the application

The app is built with the [Flask](http://flask.pocoo.org) micro-framework, with [SQLAlchemy](http://www.sqlalchemy.org) for the ORM and [PostgreSQL](http://www.postgresql.org) for the database. [Alembic](http://alembic.readthedocs.org/en/latest/index.html) is used for database migrations. You can get to the database via the PostgreSQL CLI client in the guest VM with the command:

	$ psql app

[Fabric](http://docs.fabfile.org/en/1.4.3/index.html) is used for management commands (e.g. `fab run`, in "Starting the application" above), a full list of available tasks can be seen with:

	$ fab -l

from within the vagrant shell.

The app itself is primarily in a [Flask Blueprint](http://flask.pocoo.org/docs/blueprints/) in the folder `app/blueprints/adaptive/`, config values for the app are stored in `app/config/`.

The Vagrant VM is provisioned using [Puppet](http://puppetlabs.com).

## TODO

* I did notice that some of the messages contain one of the keywords in a way that a human immediately recognises but a straight string match doesn't (e.g. 'Coca cola' instead of 'coca-cola'), something that would be nice to think about and do better.

* The API request is made on the load of the main (only) page - that's not desirable or scalable, even with caching or the current "rate-limiting", so would need to fix that.
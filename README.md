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


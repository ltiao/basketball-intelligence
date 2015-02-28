Quick Reference
===============


Show list of packages not in ``base.txt``::

	$ pip freeze | diff requirements/base.txt - | grep '>' | cut -d " " -f 2

The Digital Ocean ``gunicorn`` log is located at::

	/var/log/upstart/gunicorn.log

The Digital Ocean ``gunicorn`` configuration is located at::

	/etc/init/gunicorn.conf

Force reload Upstart configuration file (remember to execute 
after modifying Gunicorn configuration)::

	$ initctl reload-configuration

Getting Started
===============

This page delineates how the project was originally setup and configured to 
ease deployment to platforms from various (PaaS) providers such as Heroku 
and  Digital Ocean.

Local development environment
-----------------------------

Prerequisites
*************

The local development environment is on a Macbook Pro running
Mac OS X 10.10.1 (Yosemite). Throughout the documentation, it is assumed 
that the local development environment has been set-up as below:

1. Install the latest version of Python (2.7) according to the 
   `official guide`_, whose most crucial steps are summarized below:

  * Install GCC, which can be obtained through XCode Command Line Tools.
  * Install Homebrew::

      $ ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
  * Insert the Homebrew directory at the top of your ``PATH`` environment,
    which can be done by adding::

      export PATH=/usr/local/bin:/usr/local/sbin:$PATH

    to the bottom of your shell startup file (`~/.bash_profile`). This step 
    may not always be required so make sure to check your ``PATH`` to see if 
    it was already added.
  * Install Python 2.7::

      $ brew install python

    .. note:: Homebrew also installs ``setuptools`` and ``pip`` for you, which
       which is fantastic.

2. Install Virtual Environments

  * Install ``virtualenv``::

      $ pip install virtualenv

  * Install ``virtualenvwrapper``::

      $ pip install virtualenvwrapper

    You will need to add a few lines to the shell startup file to install
    and configure ``virtualenvwrapper``. Follow the `virtualenvwrapper documentation`_
    for more information. The most crucial lines to add will be::
      
      export WORKON_HOME=$HOME/.virtualenvs
      source /usr/local/bin/virtualenvwrapper.sh

Django project
**************

1. Create a virtual environment for the project::

    $ mkvirtualenv <env_name>

  and activate it::

    $ workon <env_name>

2. Initialize a ``git`` repository. For automatically generated
   ``.gitigore``, ``LICENSE`` and ``README.md``, do this from the
   Github (https://github.com/new) and clone the directory::

    $ git clone <repo_url> <repo_root>
    $ cd <repo_root>

3. Append ``.DS_Store`` (and possibly other junk) to ``.gitignore``::

    $ cat >> .gitignore
    .DS_Store
4. Start the Django project::

    $ django-admin.py startproject <dj_project_name> <dj_project_root>
5. Create ``Procfile`` in ``<repo_root>`` (not the usual `dj_project_root`)::

    $ cat > Procfile
    web: gunicorn --pythonpath <dj_project_root> <dj_project_name>.wsgi --log-file -
6. Create a ``requirements`` directory::

    $ mkdir requirements
7. Install the Django Toolbelt, which is a collection of
   common Django tools and utilities, recommended for later 
   deployment to Heroku::

    $ pip install django-toolbelt

  .. note:: When installing ``psycopg``, it is not uncommon to get 
     the following error:: 

       Error: pg_config executable not found. 

       Please add the directory containing pg_config to the PATH 

       or specify the full executable path with the option: 

           python setup.py build_ext --pg-config /path/to/pg_config build ... 

       or with the pg_config option in 'setup.cfg'. 

     We just need to make sure ``postgresql`` is properly installed:: 

       $ brew install postgresql

8. *(Optional)* Install 3rd-party Django apps:
  
  The following usually come in handy or end up being used
  one way or another in any Django project:

  * ``django-extensions``
  * ``django-filter``
  * ``django-mptt``
  * ``djanorestframework``
  * ``South`` if using Django version < 7.0

9. Populate the base requirements file::

    $ pip freeze > requirements/base.txt

  and set this to be the default (for Heroku)::

    $ cat > requirements.txt
    -r base.txt

10. Restructure the ``settings`` module to enable inheritance, settings for
    different environments, etc.

  * Create the ``settings`` directory and set the auto-generated default 
    settings as the base setting::

      $ mkdir <dj_project_root>/<dj_project_name>/settings
      $ touch <dj_project_root>/<dj_project_name>/settings/__init__.py
      $ mv <dj_project_root>/<dj_project_name>/settings.py <dj_project_root>/<dj_project_name>/settings/base.py
  
      # (Optional)
      $ mkdir <dj_project_root>/<dj_project_name>/settings/dev
      $ touch <dj_project_root>/<dj_project_name>/settings/dev/__init__.py

  * Create the local development settings file 
    ``<dj_project_root>/<dj_project_name>/settings/dev/local.py``::

      from ..base import *

  * Modify ``<dj_project_root>/manage.py`` to::

      os.environ.setdefault("DJANGO_SETTINGS_MODULE", "<dj_project_name>.settings.base")

  * Modify ``<dj_project_root>/<dj_project_name>/wsgi.py``::

      import os
      os.environ.setdefault("DJANGO_SETTINGS_MODULE", "<dj_project_name>.settings.base")

      from django.core.wsgi import get_wsgi_application
      from dj_static import Cling
      application = Cling(get_wsgi_application())

11. *(Optional)* Install ``unipath``::

      $ pip install unipath

    and use its much cleaner syntax in the `base.py` settings file::

      from unipath import Path

      PROJECT_DIR = Path(__file__).ancestor(4)
      BASE_DIR = Path(__file__).ancestor(3)

12. *(Optional)* Take advantage of ``dj_database_url`` by specifying the
    database URL in the ``DATABASE_URL`` environment variable to configure 
    the database::

      import dj_database_url
      DATABASES = {
          'default': dj_database_url.config(default='sqlite:///{base}/db.sqlite3'.format(base=BASE_DIR))
      }

    Refer to https://crate.io/packages/dj-database-url/ for URL syntax for
    different databases.

13. Add settings for (Heroku) staging environment 
    (`<dj_project_root>/<dj_project>/settings/dev/heroku.py`)::

      from ..base import *

      # Honor the 'X-Forwarded-Proto' header for request.is_secure()
      SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

      # Allow all host headers
      ALLOWED_HOSTS = ['*']

      # Static asset configuration
      STATIC_ROOT = 'staticfiles'
      STATIC_URL = '/static/'

      STATICFILES_DIRS = (
          BASE_DIR.child('static'),
      )

14. *(Optional)* Create a Sublime Text project and modify the 
    ``<sublime_project_file>``::

      {
          "folders":
          [
              {
                  "path": "<repo_root>"
              },
              {
                  "path": "$WORKON_HOME/<env_name>/bin",
                  "file_include_patterns": ["*activate"],
                  "file_exclude_patterns": ["*.*"]
              }
          ]
      }

    This will show the ``virtualenvwrapper`` triggers in the file explorer
    for ease of editing.

15. *(Optional)* Set up the ``postactivate`` trigger and symmetrically, 
    the ``predeactivate`` trigger

  * ``$WORKON_HOME/<env_name>/bin/postactivate``::

      export PROJECT_ROOT=<repo_root>

      # (Optional) So that Scrapy or other scripts can use Django models
      export PYTHONPATH="$PROJECT_ROOT/nba_stats/:$PYTHONPATH"

      export DJANGO_SETTINGS_MODULE=<dj_project_name>.settings.<setting_file>
      export DATABASE_URL=<db_url>

      echo "Changing current working directory to [$PROJECT_ROOT]..."
      cd $PROJECT_ROOT

      # (Optional) Startup sublime project
      echo "Starting up Sublime Text project..."
      subl --project <sublime_project_file>

  * ``$WORKON_HOME/<env_name>/bin/predeactivate``::

      unset DJANGO_SETTINGS_MODULE
      unset DATABASE_URL

17. Commit

Staging on Heroku
*****************

1. Create a repository on Heroku::

    $ heroku create <subdomain_name>

  which automatically creates a ``git`` remote ``heroku``
  for us.

2. Now we simply need to ``git push``::

    $ git push heroku master

3. Configure the ``DJANGO_SETTINGS_MODULE`` environment variable
   either using the Heroku web interface or via the
   command line using the Heroku Toolbelt::

    $ heroku config:set DJANGO_SETTINGS_MODULE=<dj_project_name>.settings.development.heroku

4. Ensure we have one dyno running the ``web`` process type::

    $ heroku ps:scale web=1

5. Visit the app in the browser::

    $ heroku open

  which should show the "It worked" Django welcome page.

Refer to the Heroku `Getting Started with Django guide`_ for more information.

Staging on Digital Ocean
************************

The easiest way to go about this is to create a droplet with Django
and related libraries (virtualenv, gunicorn, etc) installed and ready 
to go. Note that this will come with an empty Django project already 
deployed for us, so the tricky part of deploying our project to this 
environment is updating the existing configurations to instead host
our Django application. The configuration details are provided in 
`How To Use the Django One-Click Install Image`_. We basically have
to reconcile the differences between this tutorial and 
`How To Install and Configure Django with Postgres, Nginx, and Gunicorn`_.

1. Create a Droplet (the most economic option will suffice.) 
   Select the Django on 14.04 application.
2. Login to the Droplet with root credentials, which should
   have been emailed to you. (You will be immediately prompted
   to change this password.)

A couple of things to note at this stage:

- The empty Django project is located at ``/home/django/``.
- Git is not installed
- Virtual Environments are not used by this project at all
- The latter tutorial suggests that the virtual environment
  and Django project be located at ``/opt/``. This is not 
  a bad idea since the ``opt`` directory is intended for 
  additional software we may wish to install.

So lets go ahead and get our files onto the Droplet:

1. Install ``git``::

    $ sudo apt-get install git

2. Clone our project. This can either be located in ``/opt``
   under a virtual environment directory, which some 
   people seem to prefer, or in ``/home``, with the existing
   Django project. I prefer the latter::

    $ cd /home
    $ git clone <repo_url> <repo_root>

3. Create a virtual environment::

    $ virtualenv /opt/<env_name>
    $ source /opt/<env_name>/bin/activate

4. Install packages::
    
    $ pip install -r requirements/dev_digital_ocean.txt

Configure nginx:

1. Create a configuration file ``<nginc_conf>`` in ``/etc/nginx/sites-available``::

    upstream app_server {
        server 127.0.0.1:9000 fail_timeout=0;
    }

    server {
        listen 80 default_server;
        listen [::]:80 default_server ipv6only=on;

        root /usr/share/nginx/html;
        index index.html index.htm;

        client_max_body_size 4G;
        server_name _;

        keepalive_timeout 5;

        # Your Django project's media files - amend as required
        location /media  {
            alias <repo_root>/<django_project_root>/media;
        }

        # your Django project's static files - amend as required
        location /static {
            alias <repo_root>/<django_project_root>/static; 
        }

        location / {
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header Host $http_host;
            proxy_redirect off;
            proxy_pass http://app_server;
        }
    }

2. Remove the existing symlink ``django`` to ``/etc/nginx/sites-available/django``
   from ``/etc/nginx/sites-enabled``::

    $ rm /etc/nginx/sites-enabled/django

3. Add the symlink to ``/etc/nginx/sites-available/<nginc_conf>`` in 
   ``/etc/nginx/sites-enabled``::

    $ ln -s /etc/nginx/sites-available/<nginc_conf>

4. Restart ``nginx``::

    $ sudo service nginx restart

Gunicorn

1. Modify the Gunicorn configuration file::

    description "Gunicorn daemon for Django project"

    start on (local-filesystems and net-device-up IFACE=eth0)
    stop on runlevel [!12345]

    # If the process quits unexpectadly trigger a respawn
    respawn

    setuid django
    setgid django
    chdir /home/<repo_root>

    env DJANGO_SETTINGS_MODULE=nba_stats.settings.<settings_file>

    exec /opt/<env_name>/bin/gunicorn \
        --name=<dj_project_name> \
        --pythonpath=<dj_project_name> \
        --bind=0.0.0.0:9000 \
        --config /etc/gunicorn.d/gunicorn.py \
        <dj_project_name>.wsgi:application

2. Force reload Upstart configuration file::

    $ initctl reload-configuration

3. Restart ``gunicorn``::

    $ service gunicorn restart

Resources:

- `How To Install and Configure Django with Postgres, Nginx, and Gunicorn`_
- `How To Use the Django One-Click Install Image`_
- `How To Deploy a Local Django App to a VPS`_

.. _official guide: http://docs.python-guide.org/en/latest/starting/install/osx/
.. _virtualenvwrapper documentation: http://virtualenvwrapper.readthedocs.org/
                                     en/latest/install.html#shell-startup-file 
.. _Getting Started with Django guide: https://devcenter.heroku.com/articles/
                                       getting-started-with-django
.. _`How To Use the Django One-Click Install Image`: https://www.digitalocean.com/community/tutorials/how-to-use-the-django-one-click-install-image
.. _`How To Install and Configure Django with Postgres, Nginx, and Gunicorn`: https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-django-with-postgres-nginx-and-gunicorn
.. _`How To Deploy a Local Django App to a VPS`: https://www.digitalocean.com/community/tutorials/how-to-deploy-a-local-django-app-to-a-vps
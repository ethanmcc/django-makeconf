# django-makeconf

Make config files from Django settings variables and templates.

## Installation

From your Django app, install the module from pip:

	pip install django-makeconf
	
Then make sure it's included in your `INSTALLED_APPS` section:

	INSTALLED_APPS = (
		...
	    'makeconf',
	)

## Templates

Create templates in the `templates/` directory of your app. For example, if you create `myapp/templates/makeconf/Dockerfile.tmpl`, you can generate `Dockerfile` in the root of your app by configuring `MAKECONF_MAP` in your settings file:

	MAKECONF_MAP = {
		'Dockerfile': 'makeconf/Dockerfile.tmpl',
	}
	
This relies on Django's template finder, which is pretty flexible. It will scan all your apps for a template with the same path name. The `Dockerfile` will be generated using the `Dockerfile.tmpl`, and it will have access to the `settings` variable. 

## Usage

Assuming you have a `TIER` variable defined as `'qa'` in your settings file and the following template,

	FROM amazon/aws-eb-python:3.4.2-onbuild-3.5.1
	
	ADD uwsgi-start.sh /
	
	ENV DJANGO_SETTINGS_MODULE config.settings.{{ settings.TIER }}
	
	EXPOSE 8080

you could run

	python manage.py makeconf
	
and `{{ settings.TIER }}` would be replaced with `qa` in the output file.

## Shared Templates

If people use this, I could see shareable formats published for different services and needs. I'm currently using it to build Elastic Beanstalk and Docker configurations based on my Django settings, so I may end up publishing Django apps with names like `django-makeconf-elasticbeanstalk-configure-proxy`, or `django-makeconf-eb-docker-settings-module`, which would simply contain templates in their `templates/` directories (plus a `setup.py` and a `MANIFEST.in` that included the template files). You'd be able to pip install those templates and use them directly in your `MAKECONF_MAP`.

Also, I'm totally open to contributions in that vein or pull requests / issues on this project.

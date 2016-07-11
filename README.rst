Custom Theme
============

.. image:: https://travis-ci.org/novapost/django-pimpmytheme.png?branch=master
    :target: https://travis-ci.org/novapost/django-pimpmytheme

Per client/user/whatever django template and statics theming.

WHY
===

When you need to use custom template and/or styling based on a model
in your app (Site, User, etc).

pimpmytheme will create a folder per "client" (a client can be a
User, a Site or everything that implement the get_current method (see
below). It also can be used for multiple projects at the same
time. The folders are under a project name folder located in the
pimpmytheme directory. Your designer can then pull/push this
repository to edit the whole look and feel of all your projects in the
same repository!

How
===

With the help of custom template loader ans static file loader,
pimpmytheme load the custom template and statics files if they exists
for the current object.

INSTALLATION
============

.. code:: sh

    $ pip install django-pimpmytheme

CONFIGURATION
=============

Add pimpmytheme in your ``INSTALLED_APPS``:

.. code:: python

    INSTALLED_APPS = (
        'pimpmytheme',
        ...
    )

Add the pimpmytheme staticfiles_finder to your ``STATICFILES_FINDERS``:

.. code:: python

    STATICFILES_FINDERS = (
        "pimpmytheme.static_finder.CustomFinder",
        "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    )

Add the custom template loader to your ``TEMPLATE_LOADERS``:

.. code:: python

    TEMPLATE_LOADERS = (
        'pimpmytheme.template_loader.Loader',
        'django.template.loaders.app_directories.Loader',
    )

Finaly, you need a model with the "get_current" method. get_current
will return the object responsible for customization. For example, you
can use the django.contrib.sites.Site model to customize your project
per a site basis:

.. code:: python

    CUSTOM_THEME_LOOKUP_OBJECT = "django.contrib.sites.models.Site"
    CUSTOM_THEME_LOOKUP_ATTR = "name"

Then select the directory path where your customizations will be stored.
It must be an absolute path.

.. code:: python

    PIMPMYTHEME_FOLDER = "/home/user/myproject/custom_statics"

You can stop configuration here, it will work and your static files will
be collected in STATIC_ROOT by the collectstatic command.

If you want to go further in your configuration, you can set the
directory name where your assets will be copied by the by the collectstatic
command. It will be a subfolder of django_settings.STATIC_ROOT:

.. code:: python

    PIMPMYTHEME_FOLDER_NAME = 'pimp_theme'

Then tell compressor to use pimpmytheme's filter to build link to your assets:

.. code:: python

    STATICFILES_FINDERS = (
        "yourapp.your_finder.PrefixedFinder",
        "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    )

    COMPRESS_CSS_FILTERS = ['pimpmytheme.filters.PrefixedCssAbsoluteFilter']

COMMANDS
========

To create the needed folders for customization, you can run the
management command provided by pimpmytheme:

.. code:: sh

    $ python manage.py create_folders

Inside custom_form you will get a folder named as your project
name. And inside this folder you wil get as many folders as you
customization model objects. If you use the Site, you will get a
example.com folder.

You will also find a static folder containing an empty custom.less file.
Here for your convenience. you can start editing this file to customize
your style.

You can also create a template folder next to the static one and put
some custom templates in it.

The pimpmytheme template loader will first look in this directory to
load templates files. If not found, it will fallback on the django
template loader

If your themes are in a git repo, add settings:

.. code:: python

    PIMPMYTHEME_GIT_REPOSITORY = 'git@github.com:foo/your_pimp_folders.git'

and run the useful command to pull them into PIMPMYTHEME_FOLDER:

.. code:: sh

    $ python manage.py update_themefolder_from_git


TEMPLATETAG SYSTEM
==================

With django-pimpmytheme you get a templatetag system to manage custom
media (css, js and images).

This template system ensure the custom media exist for the current
customization. You can so get a bunch of css/js/img for each of your
client and django-pimpmytheme will only load the media revelant for
the current customization.

You can then use an asset management, compressor and so on on those
files.

To use the templatetags first load it on the template:

.. code:: jinja

    {% load pimptheme %}

Then use pimp_css, pimp_js or pimp_img to load your assets:

.. code:: jinja

    <img src="{% pimp 'myimage.jpg'%}" alt="Hello" style="opacity:0.8;">
    {% pimp_css 'custom.css'%}
    {% pimp_js 'javascript.js'%}
    {% pimp_img 'myimage.jpg'%}

NOTE
====

Thanks to `@leotrouvtou`_ for helping finding the project name.


.. _`@leotrouvtou`: https://github.com/leotrouvtou

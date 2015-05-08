django-odesk-auth
=================

Simple oDesk login for your Django-based project.

At current version, it requires Django 1.6
and has inflexible and impossible to disable access control.

Note: oDesk rebranded as Upwork. They promised to continue supporting oDesk APIs until May 19.
A backwards-compatible release to this library will be made, after which it will talk directly to upwork.com.
After that, support will be continued only for the new ``django-upwork-auth``, which is in the works. (See #4.)


Creating oDesk OAuth API key
----------------------------

Go to https://www.odesk.com/services/api/apply.

* Authentication type should be set to "OAuth 1.0".
* Callback URL should be left blank.
* Permission "View the structure of your companies/teams" is currently
  required to be checked.


Quick start
-----------

Provided you have installed ``django-odesk-auth`` and ``python-odesk==0.5``.

1. Add ``django_odesk_auth`` to INSTALLED_APPS.
   Make sure you have ``django.contrib.sites`` app in INSTALLED_APPS as well.

2. Add ``django_odesk_auth.backends.ODeskOAuthBackend``
   to AUTHENTICATION_BACKENDS.

3. Specify ``ODESK_OAUTH_KEY`` and ``ODESK_OAUTH_SECRET`` settings
   with your key information.

4. Add your_username@odesk.com to ``ODESK_AUTH_ALLOWED_USERS``,
   and set ``ODESK_AUTH_CREATE_UNKNOWN_USER`` to True.

5. Include ``django_odesk_auth.urls`` in your URL patterns.

6. In your login page template, put a link "Log in via oDesk" and point it
   to ``{% url "odesk_oauth_login" %}``.

7. Open login page and click "Log in via oDesk" to verify everything works.

Important: keep ``ODESK_OAUTH_KEY`` and ``ODESK_OAUTH_SECRET`` settings in a file
that is not under version control.


Example project
--------------

Install ``django==1.6`` and ``python-odesk==0.5`` (better do this
in virtual Python environment created specifically for example project).

Fill in some critical settings in ``example_project/settings.py`` (see comments),
then run ``./manage.py syncdb``, then you can run development server and
open ``localhost:8000``.


Access control
--------------

App has basic access control facilities.

You can specify who is allowed to log in to your site and who upon login gets
staff and/or superuser statuses. This is configured through Django settings.

Currently access control cannot be turned off.
You **have** to explicitly specify at least who is allowed to log in to your site.
(Yes, this means you can't grant access to everyone yet, unless you hack the app.)

Users that aren't allowed to log in get ``User.is_active`` flag set to False.
See ``utils.update_user_permissions()`` definition if you're interested in other specifics,
and see available settings below.


Making authenticated oDesk API calls
------------------------------------

After user is successfully authenticated, you can call oDesk API on their behalf.

Here's a quick example::

    from django_odesk_auth import utils, O_ACCESS_TOKEN
    
    odesk_client = utils.get_client(request.session[O_ACCESS_TOKEN])
    print odesk_client.hr.get_teams()
    # Should output list of teams user has access to

Some notes:

* How you make API calls is up to you. Internally django-odesk-auth
  uses python-odesk library, and so does this example.

* ``utils.get_client()`` function returns an instance of ``odesk.Client``.
  Handy if you're using python-odesk library to make API calls.

* OAuth access token, obtained during authentication, is stored
  under ``request.session[O_ACCESS_TOKEN]``.


Checking OAuth access token
---------------------------

Sometimes there's a need to make sure that current user's authentication
is still valid—that they, for example, didn't revoke access to their account.

For that you can use ``utils.check_login()`` in Python, or make an AJAX request
to named URL ``'odesk_oauth_check_login'`` from client side
(see ``views.oauth_check_login``).


Available Django settings
-------------------------

ODESK_OAUTH_KEY, ODESK_OAUTH_SECRET  
  API key information.

ODESK_AUTH_CREATE_UNKNOWN_USER = False  
  Whether to create a new account in Django if given user logs in via oDesk
  for the first time.

ODESK_AUTH_ALLOWED_USERS = ()  
  oDesk emails of users who are allowed to log in via oDesk.

ODESK_AUTH_ADMINS = ()  
  oDesk emails of users who are marked as ``is_staff`` upon login.

ODESK_AUTH_SUPERUSERS = ()  
  oDesk emails of users who are marked as ``is_superuser`` upon login.

ODESK_AUTH_ALLOWED_TEAMS = ()  
  IDs of oDesk teams, members of which are allowed to log in via oDesk.

ODESK_AUTH_ADMIN_TEAMS = ()  
  IDs of oDesk teams, members of which are marked as ``is_staff`` upon login.

ODESK_AUTH_SUPERUSER_TEAMS = ()  
  IDs of oDesk teams, members of which are marked as ``is_superuser`` upon login.

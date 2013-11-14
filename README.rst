django-odesk-auth
=================

Django app for simple “Log in via oDesk” functionality.
Authentication backend and a couple of views.

DOESN'T WORK YET.


Creating oDesk OAuth API key
----------------------------

Go to https://www.odesk.com/services/api/apply.
Authentication type should be set to "OAuth 1.0".
Callback URL should be left blank.


Quick start
-----------

1. Add ``django_odesk_auth`` to INSTALLED_APPS.

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

See also example project in the repository.


Access control
--------------

Currently there's no way to turn off access control: you have to explicitly
specify which teams or particular users are allowed to log in to your site.
You can also specify which users are assigned staff and superuser status
upon login.

Users that aren't allowed to log in get ``User.is_active`` flag set to False.

See ``utils.update_user_permissions()`` definition and list of settings below.


Making API calls after authentication
-------------------------------------

After user is successfully authenticated, you can make API calls on their behalf.

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
is still valid. You can use ``utils.check_login()`` in Python,
or make an HTTP request to named URL ``'odesk_oauth_check_login'``
from client side (see ``views.oauth_check_login``).


Available settings
------------------

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
  IDs of oDesk teams, members of which are allowed to access FIVS backend.

ODESK_AUTH_ADMIN_TEAMS = ()
  IDs of oDesk teams, members of which are marked as ``is_staff`` upon login.

ODESK_AUTH_SUPERUSER_TEAMS = ()
  IDs of oDesk teams, members of which are marked as ``is_superuser`` upon login.

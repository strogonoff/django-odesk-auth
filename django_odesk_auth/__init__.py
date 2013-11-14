"""Offers "Log in via oDesk" functionality.

Relevant settings:

* :data:`settings.ODESK_OAUTH_KEY` and :data:`settings.ODESK_OAUTH_SECRET`
  are used to instantiate python-odesk's :class:`odesk.Client`.

* :data:`settings.ODESK_AUTH_ALLOWED_USERS`,
  :data:`settings.ODESK_AUTH_ALLOWED_TEAMS`
  define who's able to access the website.

  .. note:: User can log in if at least one of their teams are listed under
            ``ODESK_AUTH_ALLOWED_TEAMS`` *or* if their username is listed under
            ``ODESK_AUTH_ALLOWED_USERS``.

* :data:`settings.ODESK_AUTH_ADMINS`,
  :data:`settings.ODESK_AUTH_SUPERUSERS`,
  :data:`settings.ODESK_AUTH_ADMIN_TEAMS`,
  :data:`settings.ODESK_AUTH_SUPERUSER_TEAMS`
  define basic user access privileges
  (whether :attr:`User.is_staff <django.contrib.auth.models.User.is_staff>` or
  :attr:`~django.contrib.auth.models.User.is_superuser` flags are set
  during authentication. See :func:`django_odesk_auth.utils.update_user_permissions`).

* :data:`settings.ODESK_AUTH_CREATE_UNKNOWN_USER`
"""

O_REQUEST_TOKEN = '_ort'
O_ACCESS_TOKEN = '_oat'

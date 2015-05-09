#coding: utf-8

import logging
from upwork import exceptions as odesk_exceptions

from django.contrib.auth.models import User
from django.conf import settings

from . import utils


logger = logging.getLogger(__name__)


CREATE_UNKNOWN_USER = getattr(settings, 'ODESK_AUTH_CREATE_UNKNOWN_USER', False)
"""Whether to create a new Django account if user logs in via oDesk
the first time."""

ODESK_USERNAME_SUFFIX = "@odesk.com"
"""String appended to oDesk user ID to be used
as :attr:`User.username <django.contrib.auth.models.User.username>`
for newly created users."""


class ODeskOAuthBackend(object):
    """Backend for Django auth system."""

    def authenticate(self, access_token=None):
        """Verifies that given OAuth ``access_token`` is valid by making
        a request to oDesk API to get current user's information.

        If request is successful, creates/updates corresponding
        :class:`~django.contrib.auth.models.User` object.

        **When user logs in for the first time,**
        :attr:`~django.contrib.auth.models.User.username` is set in the form
        ``'<odesk_username>@odesk.com'``, same as ``email``.
        ``first_name`` and ``last_name`` are also set based on user's info
        returned by oDesk API.

        .. seealso:: :func:`django_odesk_auth.utils.set_user_info`

        **On each subsequent logins,** user's permissions
        (``is_staff``, ``is_superuser``, ``is_active`` flags)
        are updated based on oDesk teams user belongs to and teams
        in FIVS :mod:`settings`.

        .. seealso:: :func:`django_odesk_auth.utils.update_user_permissions`
        """

        odesk_client = utils.get_client()
        (
            odesk_client.oauth_access_token,
            odesk_client.oauth_access_token_secret,
        ) = access_token

        try:
            auth_user = odesk_client.hr.get_user('me')
        except odesk_exceptions.HTTP403ForbiddenError:
            logger.exception(
                "Invalid access token given to authenticate(): %s",
                access_token)
            return None
        else:
            if auth_user.get('status') != 'active':
                logger.warn(
                    "Inactive user authentication attempt: %s",
                    auth_user.get('id'))
                return None

        username = "{odesk_id}{username_suffix}".format(
            odesk_id=auth_user['id'],
            username_suffix=ODESK_USERNAME_SUFFIX)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            if CREATE_UNKNOWN_USER:
                logger.info("Creating new user: %s", username)
                user = User.objects.create(username=username)
                user = utils.set_user_info(user, auth_user)
            else:
                logger.info(
                    "Unknown user %s tried to log in, declining",
                    username)
                return None

        teams = set(team['id'] for team in odesk_client.hr.get_teams())
        user = utils.update_user_permissions(user, teams)

        return user

    def get_user(self, user_id):
        return User.objects.get(id=user_id)

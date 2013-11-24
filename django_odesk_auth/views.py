#coding: utf-8

from django.core.urlresolvers import reverse
from django import http
from django.contrib.auth import authenticate, login
from django.contrib.sites.models import Site

from . import utils
from . import O_REQUEST_TOKEN, O_ACCESS_TOKEN


def oauth_login(request):
    """Initiates OAuth login process."""

    odesk_client = utils.get_client()

    # After oDesk redirects user back, we can fetch request token from session
    # and use it to obtain access token and finish authentication
    request.session[O_REQUEST_TOKEN] = odesk_client.auth.get_request_token()

    # (OAuth.get_request_token() magically sets ``request_token[_secret]``
    # attributes on OAuth instance under c.auth, so we don't have to do that)

    site = Site.objects.get_current()

    return http.HttpResponseRedirect(odesk_client.auth.get_authorize_url(
        'http://{domain}{url}?next={redirect}'.format(
            domain=site.domain,
            url=reverse('odesk_oauth_login_callback'),
            redirect=request.GET.get('next'),
        )
    ))


def oauth_login_callback(request):
    """Handles redirect from oDesk side during OAuth login process."""

    odesk_client = utils.get_client()

    if O_REQUEST_TOKEN in request.session:
        (
            odesk_client.auth.request_token,
            odesk_client.auth.request_token_secret,
        ) = request.session.get(O_REQUEST_TOKEN, [None, None])
        del request.session[O_REQUEST_TOKEN]

    else:
        return http.HttpResponse("Request token is missing", status=401)

    try:
        access_token = \
            odesk_client.auth.get_access_token(
                request.GET.get('oauth_verifier'))
    except Exception, e:
        return http.HttpResponse(e, status=401)

    user = authenticate(access_token=access_token)
    # ODeskOAuthBackend will retrieve user details
    # and create new user if it's first-time login

    if user:
        # If we want to make a request to oDesk API on user's behalf later
        # after authentication, access token tuple can be obtained
        # from user's session (and applied to corresponding
        # Client.auth.oauth_ attributes)
        request.session[O_ACCESS_TOKEN] = access_token

        if user.is_active:
            login(request, user)
        else:
            return http.HttpResponse("User is not active", status=401)
    else:
        return http.HttpResponse("User not found", status=401)

    redirect_url = request.GET.get('next', '/')

    # oDesk apparently sets "next" in GET query to string None
    if redirect_url == 'None':
        redirect_url = '/'

    return http.HttpResponseRedirect(redirect_url)


def oauth_check_login(request):
    """Verifies that there's a valid OAuth access token stored in user's
    session, and that user is active. If there's a problem,
    returns HTTP 401 (Unauthorized). Otherwise returns HTTP 200 (OK).
    Additional information might be in response body text.
    """
    access_token = request.session.get(O_ACCESS_TOKEN, None)

    if access_token is None or len(access_token) != 2:
        return http.HttpResponse("Access token is missing", status=401)

    result, details = utils.check_login(access_token)

    if result is True:
        return http.HttpResponse(details, status=200)
    else:
        return http.HttpResponse(details, status=401)

from django import http
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse


class GuestView(TemplateView):
    template_name = 'guest.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return http.HttpResponseRedirect(reverse('member_page'))

        return super(GuestView, self).get(request, *args, **kwargs)


class MemberView(TemplateView):
    template_name = 'member.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return http.HttpResponseRedirect(reverse('guest_page'))

        return super(MemberView, self).get(request, *args, **kwargs)
